"""고3 영어 29번 어법 인쇄물 PDF 생성

실행: python3 grammar29/print/build_pdf.py --fonts <글꼴 디렉터리>
  글꼴 디렉터리에는 UnBatang.ttf, UnBatangBold.ttf, UnDotum.ttf, UnDotumBold.ttf, UnGraphic.ttf,
  LiberationSerif-Regular.ttf, LiberationSerif-Bold.ttf, LiberationSerif-Italic.ttf가 있어야 함.
  머리말과 꼬리말 템플릿은 시스템 글꼴을 쓰므로 같은 글꼴을 ~/.local/share/fonts에도 설치함.
입력:
  src/passages.json          시험지 지문 (밑줄형 {n|표현}, 네모형 {A|선택1|선택2})
  src/총정리_빈칸.md         개념 정리 원고 (빈칸 {{답}})
  ../data/questions.json     정답, 고친 형태, 선지별 해설, 개념 분류
출력 (out/):
  영어29번_어법기출73제_문제지.pdf      학생용 시험지
  영어29번_어법기출73제_교사용.pdf      정답 표시 시험지 + 정답과 해설
  영어29번_어법개념정리_학생용.pdf      빈칸 학습지
  영어29번_어법개념정리_교사용.pdf      빈칸 답과 확인 문제 정답 표시본
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
import style  # noqa: E402
from analyze import CHAPTERS, DISPLAY  # noqa: E402

CIRCLED = "①②③④⑤"
OUT = HERE / "out"
EXAM_TITLE = "영어 29번 어법 기출"
EXAM_SUB = "2016년~2026년 고3 수능, 모의평가, 학력평가 73문항"
GUIDE_TITLE = "영어 29번 어법 개념 정리"
GUIDE_SUB = "2016년~2026년 고3 기출 73문항 분석"
NOTICE = ("※ 각 문항의 [ ] 안은 출제 시험입니다. 28번으로 출제된 문항은 원래 번호를 함께 적었습니다. "
          "남는 자리는 풀이 공간으로 쓰십시오.")


# ---------------------------------------------------------------- 데이터

def load_questions():
    qs = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
    return {q["exam"]["id"]: q for q in qs}


def load_passages():
    items = json.loads((HERE / "src" / "passages.json").read_text(encoding="utf-8"))
    return {p["exam_id"]: p for p in items}


def exam_order(questions, passages):
    """최근 시행 시험부터 시행 월 역순"""
    ids = [i for i in passages if questions.get(i) and questions[i]["record"]["found"]]
    return sorted(ids, key=lambda i: (-questions[i]["exam"]["Y"], -questions[i]["exam"]["M"]))


def source_tag(q):
    e, r = q["exam"], q["record"]
    if e["kind"] == "수능":
        s = f"{e['H']}학년도 수능"
    elif e["kind"] == "평가원":
        s = f"{e['H']}학년도 {e['M']}월 모평"
    else:
        s = f"{e['Y']}년 {e['M']}월 학평"
    if r["question_number"] != 29:
        s += f" {r['question_number']}번"
    return s


def section_of(category):
    """개념 분류 → 개념 정리 교재의 절 번호"""
    counts = json.loads((ROOT / "data" / "stats.json").read_text(encoding="utf-8"))["tested"]
    for n, (_, cats) in enumerate(CHAPTERS, 2):
        live = [c for c in sorted(cats, key=lambda k: -counts.get(k, 0)) if counts.get(c, 0) > 0]
        if category in live:
            return f"{n}.{live.index(category) + 1}"
    return ""


# ---------------------------------------------------------------- 시험지

def render_passage(text, rec):
    choices = {c["label"]: c for c in rec["choices"]}
    out, pos = [], 0
    for m in re.finditer(r"\{([1-5A-C])\|([^{}]*)\}", text):
        out.append(html.escape(text[pos:m.start()]))
        key, body = m.group(1), m.group(2)
        if key.isdigit():
            label = CIRCLED[int(key) - 1]
            ans = choices.get(label, {}).get("is_answer") and rec["format"] == "밑줄5지"
            out.append(f'<span class="opt{" ans" if ans else ""}"><span class="cn">{label}</span>'
                       f'<u>{html.escape(body)}</u></span>')
        else:
            right = (choices.get(f"({key})") or {}).get("correct_form", "").strip()
            pick = ' class="pick"'
            cells = "".join(f'<span{pick if o.strip() == right else ""}>{html.escape(o.strip())}</span>'
                            for o in body.split("|"))
            out.append(f'<span class="nemo-label">({key})</span><span class="nemo">{cells}</span>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(f"<p>{p.strip()}</p>" for p in "".join(out).split("\n\n") if p.strip())


def render_box_choices(rows, answer):
    if not rows:
        return ""
    trs = ['<tr><td></td><td>(A)</td><td></td><td>(B)</td><td></td><td>(C)</td></tr>']
    for r in rows:
        num = r[:1]
        parts = [p.strip() for p in re.split(r"…+|\.{3,}|‥+", r[1:]) if p.strip()]
        cells = '<td class="dots">……</td>'.join(f"<td>{html.escape(p)}</td>" for p in parts)
        cls = ' class="ans"' if num == answer[:1] else ""
        trs.append(f'<tr{cls}><td class="n">{num}</td>{cells}</tr>')
    return f'<table class="box-choices">{"".join(trs)}</table>'


def answer_number(q, p):
    """정답 원문자. 네모형은 맞는 표현 조합과 같은 선택지 줄에서 찾음"""
    rec = q["record"]
    if rec["format"] != "네모3지":
        return rec["answer"][:1]
    right = [c["correct_form"].strip().lower() for c in rec["choices"]]
    for row in p.get("box_choices") or []:
        parts = [x.strip().lower() for x in re.split(r"…+|\.{3,}|‥+", row[1:]) if x.strip()]
        if parts == right:
            return row[:1]
    raise ValueError(f"네모형 정답을 찾지 못함: {q['exam']['id']}")


def question_html(no, q, p):
    rec = q["record"]
    inst = html.escape(p["instruction"])
    if rec["format"] == "밑줄5지":
        inst = inst.replace("틀린", "<u>틀린</u>", 1)
    inst = inst.replace("[3점]", '<span class="pt">[3점]</span>')
    parts = [f'<div class="q"><div class="stem"><span class="qno">{no}.</span>{inst} '
             f'<span class="src">[{source_tag(q)}]</span></div>',
             f'<div class="passage">{render_passage(p["passage"], rec)}</div>']
    if p.get("footnotes"):
        foot = "".join(f"<div>{html.escape(f.replace(chr(0xFF65), chr(0xB7)))}</div>" for f in p["footnotes"])
        parts.append(f'<div class="foot">{foot}</div>')
    if rec["format"] == "네모3지":
        parts.append(render_box_choices(p.get("box_choices") or [], answer_number(q, p)))
        key = f'정답 {answer_number(q, p)}'
    else:
        key = f'정답 {rec["answer"][:1]} ({rec["answer_fix"]})'
    parts.append(f'<div class="key">{html.escape(key)}</div></div>')
    return "".join(parts)


def explanation_html(no, q, p):
    rec = q["record"]
    ans = answer_number(q, p)
    head = (f'<div class="ex-head"><b>{no}.</b> [출제 의도] 어법상 '
            f'{"틀린 것 찾기" if rec["format"] == "밑줄5지" else "맞는 표현 고르기"} '
            f'<span class="src">[{source_tag(q)}]</span></div>')
    lines = [f'<div class="line">[정답] {ans}' +
             (f' {html.escape(rec["answer_fix"])}' if rec["format"] == "밑줄5지" else "") + "</div>"]
    first = [c for c in rec["choices"] if c["is_answer"] and rec["format"] == "밑줄5지"]
    rest = [c for c in rec["choices"] if c not in first]
    for i, c in enumerate(first + rest):
        lab = "[풀이] " if i == 0 else ""
        lines.append(f'<div class="line">{lab}<span class="lbl">{c["label"]} <i>{html.escape(c["underlined"])}</i></span> '
                     f'{html.escape(c["explanation"])}</div>')
    secs = []
    for c in rec["choices"]:
        s = section_of(c["category"])
        name = f'{DISPLAY.get(c["category"], c["category"])}({s})' if s else DISPLAY.get(c["category"], "")
        if name not in secs:
            secs.append(name)
    lines.append(f'<div class="line">[관련 개념] {html.escape(", ".join(secs))}</div>')
    return f'<div class="ex">{head}{"".join(lines)}</div>'


# ---------------------------------------------------------------- 개념 정리

def guide_body():
    md = (HERE / "src" / "총정리_빈칸.md").read_text(encoding="utf-8")
    md = re.sub(r"^# .*\n", "", md, count=1)
    md = re.sub(r"^((?:  )+)(?=(?:[-*]|\d+\.) )", lambda m: m.group(1) * 2, md, flags=re.M)
    md = re.sub(r"\{\{(.*?)\}\}", lambda m: f'<span class="bl"><b>{html.escape(m.group(1))}</b></span>', md)

    def details(m):
        inner = markdown.markdown(m.group(2), extensions=["tables"])
        return f'<div class="answers"><div class="answers-head">정답과 해설</div>{inner}</div>'
    md = re.sub(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", details, md, flags=re.S)
    # 판단 규칙 절을 상자로 묶음
    md = re.sub(r"(?ms)^#### 판단 규칙\n(.*?)(?=^#{2,4} |\Z)",
                lambda m: f'<div class="rulebox" markdown="1">\n\n#### 판단 규칙\n\n{m.group(1).rstrip()}\n\n</div>\n\n', md)
    # 표 위 주석 줄
    md = re.sub(r"(?m)^(선지 판정[^\n]*|[^\n|#-][^\n]*/[^\n]*)\n(?=\n?\|)", r'<p class="tnote">\1</p>\n\n', md)
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "md_in_html"])
    body = re.sub(r"<h2>(\d+)\. ", r'<h2><span class="num">\1</span>', body)
    body = re.sub(r"<h3>(\d+\.\d+) ", r'<h3><span class="num">\1</span> ', body)
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    body = re.sub(r"<td>X(\s*→[^<]*)?</td>", lambda m: f'<td class="v">X{m.group(1) or ""}</td>', body)
    body = re.sub(r"<td>O</td>", '<td class="v">O</td>', body)
    body = re.sub(r"<td>네모형", '<td class="v">네모형', body)
    return body


# ---------------------------------------------------------------- PDF 출력

def chromium(pw):
    exe = "/opt/pw-browsers/chromium"
    return pw.chromium.launch(executable_path=exe if Path(exe).exists() else None)


def print_pdf(html_text, pdf_path, wait_js=None, templates=None):
    from playwright.sync_api import sync_playwright
    tmp = OUT / "html" / (pdf_path.stem + ".html")
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(html_text, encoding="utf-8")
    with sync_playwright() as pw:
        b = chromium(pw)
        page = b.new_page()
        page.goto(tmp.as_uri())
        page.evaluate("document.fonts.ready")
        if wait_js:
            page.wait_for_function(wait_js, timeout=120000)
            over = page.evaluate("Array.from(document.querySelectorAll('.col'))"
                                 ".filter(c => c.scrollHeight > c.clientHeight + 1).length")
            if over:
                print(f"경고: {pdf_path.name}에서 단 넘침 {over}곳")
        kw = dict(path=str(pdf_path), print_background=True, prefer_css_page_size=True)
        if templates:
            header, footer, margin = templates
            kw.update(display_header_footer=True, header_template=header, footer_template=footer)
            if margin:
                kw["margin"] = margin
        page.pdf(**kw)
        b.close()


def finish(pdf_paths, out_path, title):
    """여러 PDF를 합치고 메타데이터를 정리함 (Creator, Producer 비움)"""
    import pymupdf
    doc = pymupdf.open()
    for p in pdf_paths:
        doc.insert_pdf(pymupdf.open(p))
    doc.set_metadata({"title": title, "author": "", "subject": "", "keywords": "", "creator": "", "producer": ""})
    doc.save(out_path, garbage=3, deflate=True)
    print("wrote", out_path, doc.page_count, "pages")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default=str(HERE / "fonts"))
    ap.add_argument("--only", choices=["exam", "guide"], default=None)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    tmpdir = OUT / "tmp"
    tmpdir.mkdir(exist_ok=True)
    questions = load_questions()

    if args.only in (None, "exam"):
        passages = load_passages()
        order = exam_order(questions, passages)
        qhtml = "\n".join(question_html(i + 1, questions[e], passages[e]) for i, e in enumerate(order))
        for teacher in (False, True):
            doc = style.exam_page(qhtml, len(order), teacher, args.fonts, EXAM_TITLE, EXAM_SUB, html.escape(NOTICE))
            part = tmpdir / f"exam_{'t' if teacher else 's'}.pdf"
            print_pdf(doc, part, wait_js="window.__done === true")
            parts = [part]
            if teacher:
                quick = "".join(f'<div>{i + 1:02d}. {answer_number(questions[e], passages[e])}</div>'
                                for i, e in enumerate(order))
                items = "\n".join(explanation_html(i + 1, questions[e], passages[e]) for i, e in enumerate(order))
                ans = tmpdir / "answers.pdf"
                print_pdf(style.answers_page(quick, items, args.fonts, EXAM_TITLE, EXAM_SUB), ans,
                          wait_js="window.__done === true")
                parts.append(ans)
            name = "영어29번_어법기출73제_교사용.pdf" if teacher else "영어29번_어법기출73제_문제지.pdf"
            finish(parts, OUT / name, EXAM_TITLE + (" 교사용" if teacher else " 문제지"))

    if args.only in (None, "guide"):
        body = guide_body()
        for teacher in (False, True):
            doc = style.guide_page(body, teacher, args.fonts, GUIDE_TITLE, GUIDE_SUB)
            part = tmpdir / f"guide_{'t' if teacher else 's'}.pdf"
            print_pdf(doc, part, templates=style.guide_header_footer(GUIDE_TITLE, teacher))
            name = "영어29번_어법개념정리_교사용.pdf" if teacher else "영어29번_어법개념정리_학생용.pdf"
            finish([part], OUT / name, GUIDE_TITLE + (" 교사용" if teacher else " 학생용"))


if __name__ == "__main__":
    main()
