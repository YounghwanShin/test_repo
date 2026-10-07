"""고3 영어 29번 어법 인쇄물 PDF 생성

실행: python3 grammar29/print/build_pdf.py --fonts <글꼴 디렉터리> [--only exam|guide]
  글꼴 디렉터리에는 UnBatang.ttf, UnBatangBold.ttf, UnDotum.ttf, UnDotumBold.ttf,
  LiberationSerif-Regular.ttf, LiberationSerif-Bold.ttf, LiberationSerif-Italic.ttf가 있어야 함.
  교재 머리말(@page 여백 상자)은 시스템 글꼴을 쓰므로 같은 글꼴을 ~/.local/share/fonts에도 설치함.
입력:
  src/passages.json          시험지 지문 (밑줄형 {n|표현}, 네모형 {A|선택1|선택2})
  src/explanations.json      해설지 문장 (정답 선지 풀이, 나머지 선지 한 줄)
  src/총정리_빈칸.md         개념 정리 원고 (빈칸 {{답}})
  ../data/questions.json     정답, 고친 형태, 개념 분류
출력 (out/):
  영어29번_어법기출69제_문제지.pdf       학생용 시험지
  영어29번_어법기출69제_교사용.pdf       정답 표시 시험지
  영어29번_어법기출69제_정답과해설.pdf   빠른 정답표와 문항별 해설
  영어29번_어법개념정리_학생용.pdf       빈칸 학습지
  영어29번_어법개념정리_교사용.pdf       빈칸 답 표시본과 확인 문제 정답 부록
"""
import argparse
import html
import json
import re
import sys
from collections import Counter
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
EXAM_SUB = "2016년~2026년 고3 수능, 모의평가, 학력평가 69문항"
GUIDE_TITLE = "영어 29번 어법 개념 정리"
GUIDE_SUB = "2016년~2026년 고3 수능, 모의평가, 학력평가 기출"
NOTICE = ("※ 각 문항의 [ ] 안은 출제 시험입니다. 28번으로 출제된 문항은 원래 번호를 함께 적었습니다. "
          "남는 자리는 풀이 공간으로 쓰십시오.")


# ---------------------------------------------------------------- 데이터

def load_questions():
    qs = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
    return {q["exam"]["id"]: q for q in qs}


def load_json(name):
    data = json.loads((HERE / "src" / name).read_text(encoding="utf-8"))
    return {p["exam_id"]: p for p in (data["items"] if isinstance(data, dict) else data)}


def exam_order(questions, passages):
    """최근 시행 시험부터 시행 월 역순"""
    ids = [i for i in passages if questions.get(i) and questions[i]["record"]["found"]
           and questions[i]["record"]["format"] != "네모3지"]
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


def live_sections():
    """원고의 절 제목으로 category → (장 번호, 절 번호)"""
    md = (HERE / "src" / "총정리_빈칸.md").read_text(encoding="utf-8")
    by_title = {v: k for k, v in DISPLAY.items()}
    return {by_title[m.group(3).strip()]: (int(m.group(1)), int(m.group(2)))
            for m in re.finditer(r"(?m)^### (\d+)\.(\d+) (.+)$", md) if m.group(3).strip() in by_title}


def sec_label(n, k):
    return f"{style.ROMAN[n]}-{k:02d}"


# ---------------------------------------------------------------- 시험지

def dashes(s):
    s = s.replace("─", "―")
    return re.sub("([—―])", r'<span class="dash">\1</span>', s)


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


def render_passage(text, rec):
    choices = {c["label"]: c for c in rec["choices"]}
    out, pos = [], 0
    for m in re.finditer(r"\{([1-5A-C])\|([^{}]*)\}", text):
        out.append(dashes(html.escape(text[pos:m.start()])))
        key, body = m.group(1), m.group(2)
        if key.isdigit():
            label = CIRCLED[int(key) - 1]
            ans = choices.get(label, {}).get("is_answer") and rec["format"] == "밑줄5지"
            cls = "opt ans" if ans else "opt"
            out.append(f'<span class="{cls}"><span class="cn">{label}</span><u>{html.escape(body)}</u></span>')
        else:
            right = (choices.get(f"({key})") or {}).get("correct_form", "").strip()
            pick = ' class="pick"'
            cells = "".join(f'<span{pick if o.strip() == right else ""}>{html.escape(o.strip())}</span>'
                            for o in body.split("|"))
            out.append(f'<span class="nemo-label">({key})</span><span class="nemo">{cells}</span>')
        pos = m.end()
    out.append(dashes(html.escape(text[pos:])))
    return "".join(f"<p>{p.strip()}</p>" for p in "".join(out).split("\n\n") if p.strip())


def render_box_choices(rows, ans):
    if not rows:
        return ""
    trs = ['<tr><td></td><td>(A)</td><td></td><td>(B)</td><td></td><td>(C)</td></tr>']
    for r in rows:
        num = r[:1]
        parts = [p.strip() for p in re.split(r"…+|\.{3,}|‥+", r[1:]) if p.strip()]
        cells = '<td class="dots">……</td>'.join(f"<td>{html.escape(p)}</td>" for p in parts)
        cls = ' class="ans"' if num == ans else ""
        trs.append(f'<tr{cls}><td class="n"><span class="cn">{num}</span></td>{cells}</tr>')
    return f'<table class="box-choices">{"".join(trs)}</table>'


def question_html(no, q, p):
    rec = q["record"]
    ans = answer_number(q, p)
    inst = html.escape(p["instruction"])
    if rec["format"] == "밑줄5지":
        inst = inst.replace("틀린", "<u>틀린</u>", 1)
    inst = inst.replace("[3점]", '<span class="pt">[3점]</span>')
    parts = [f'<div class="q"><div class="stem"><span class="qno">{no}.</span>{inst}'
             f'<span class="src">[{source_tag(q)}]</span></div>',
             f'<div class="passage">{render_passage(p["passage"], rec)}</div>']
    if p.get("footnotes"):
        foot = "".join(f"<div>{html.escape(f.replace(chr(0xFF65), chr(0xB7)))}</div>" for f in p["footnotes"])
        parts.append(f'<div class="foot">{foot}</div>')
    if rec["format"] == "네모3지":
        parts.append(render_box_choices(p.get("box_choices") or [], ans))
        key = f"정답 {ans}"
    else:
        key = f"정답 {ans} {rec['answer_fix']}"
    parts.append(f'<div class="key">{html.escape(key)}</div></div>')
    return "".join(parts)


def explanation_html(no, q, p, ex, secs):
    rec = q["record"]
    ans = answer_number(q, p)
    nemo = rec["format"] == "네모3지"
    head = (f'<div class="ex-head"><b>{no}.</b> [출제 의도] 어법상 {"맞는 표현 고르기" if nemo else "틀린 것 찾기"} '
            f'<span class="src">[{source_tag(q)}]</span></div>')
    lines = [f'<div class="line">[정답] {ans}' + ("" if nemo else f' {html.escape(rec["answer_fix"])}') + "</div>",
             f'<div class="line sol">[풀이] {html.escape(ex["answer_text"])}</div>']
    under = {c["label"]: c["underlined"] for c in rec["choices"]}
    for o in ex.get("others", []):
        text = o["text"].strip()
        w = under.get(o["label"], "")
        if w and text.lower().startswith(w.lower()):
            w, text = text[:len(w)], text[len(w):]
        elif w:
            text = " " + text
        lead = f'<span class="w lead">{html.escape(w)}</span>' if w else ""
        lines.append(f'<div class="line"><span class="lbl">{o["label"]}</span> {lead}{html.escape(text)}</div>')
    cat = next((c["category"] for c in rec["choices"] if c["is_answer"]), rec["choices"][0]["category"])
    if cat in secs and not nemo:
        lines.append(f'<div class="line">[관련 개념] {DISPLAY.get(cat, cat)} (개념 정리 {sec_label(*secs[cat])})</div>')
    return f'<div class="ex">{head}{"".join(lines)}</div>'


# ---------------------------------------------------------------- 개념 정리 원고 변환

NOTE_FORMS = [
    "※ 기출 73문항 중 {n}문항에서 이 개념이 틀린 표현으로 출제",
    "※ 정답(틀린 표현)으로 {n}번 출제",
    "※ {n}문항의 정답이 이 개념",
]


def is_stat_bullet(line):
    return bool(re.match(r"^- .*(출제 선지|정답 선지|출제 \d+개|\d+개 개념|정답 \d+개|맞는 선지 \d+개)", line))


def transform_guide_md(md, wrong_counts, secs):
    md = re.sub(r"^# .*\n", "", md, count=1)
    md = re.sub(r" \(2026년 5월 학평 ④는 선택률 [\d.]+%로 가장 많이 고른 오답\)", "", md)
    md = re.sub(r"(?m)^(\s*- )예: (?=\d{4}(?:학년도|년))", r"\1", md)
    md = re.sub(r"(?m)^[^\n|#-][^\n]* / [^\n]*\n(?=\n?\|)", "", md)
    lines, out, i, note_i = md.split("\n"), [], 0, 0
    cat_by_title = {DISPLAY[c]: c for c in secs}
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m2 = re.match(r"^## \d+\. ", line)
        m3 = re.match(r"^### \d+\.\d+ (.+)$", line)
        if m2 or m3:
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or is_stat_bullet(lines[j])
                                      or (lines[j].startswith("    ") and is_stat_bullet(lines[j - 1]))):
                j += 1
            out.append("")
            if m3:
                n = wrong_counts.get(cat_by_title.get(m3.group(1).strip()), 0)
                if False:
                    out.append(f'<p class="note">{NOTE_FORMS[note_i % len(NOTE_FORMS)].format(n=n)}</p>')
                    out.append("")
                    note_i += 1
            i = j
            continue
        i += 1
    return "\n".join(out)


def norm_words(s):
    return re.findall(r"[a-z']+", re.sub(r"\*\*|\[[^\]]*/[^\]]*\]", " ", s.lower()))


def split_quizzes(md):
    """절마다 확인 문제와 같은 문장의 표 행을 지우고, 확인 문제 정답을 따로 모음"""
    answers = []
    parts = re.split(r"(?m)^(?=### )", md)
    for idx, part in enumerate(parts):
        title = part.split("\n", 1)[0]
        qm = re.search(r"(?ms)^#### 확인 문제\n(.*?)(?=^<details>|\Z)", part)
        if not qm:
            continue
        quiz_sets = [norm_words(l) for l in qm.group(1).split("\n") if re.match(r"^\d+\. ", l)]

        def dup(row):
            if not row.startswith("|") or "---" in row:
                return False
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) < 3:
                return False
            w = norm_words(cells[2])
            if len(w) < 6:
                return False
            grams = {" ".join(w[k:k + 6]) for k in range(len(w) - 5)}
            return any(" ".join(qs[k:k + 6]) in grams for qs in quiz_sets for k in range(len(qs) - 5))
        body = "\n".join(l for l in part.split("\n") if not dup(l))
        dm = re.search(r"(?s)<details>\s*<summary>.*?</summary>(.*?)</details>", body)
        if dm:
            answers.append((title.replace("### ", "").strip(), dm.group(1).strip()))
            body = body[:dm.start()] + body[dm.end():]
        body = re.sub(r"(?ms)^(#### 확인 문제\n.*?)(?=^#{2,4} |\Z)",
                      lambda m: f'<div class="quiz" markdown="1">\n\n{m.group(1).rstrip()}\n\n</div>\n\n', body)
        parts[idx] = body
    return "".join(parts), answers


def renumber(md, secs):
    valid = {f"{n}.{k}": sec_label(n, k) for n, k in secs.values()}
    md = re.sub(r"(?m)^### (\d+)\.(\d+) ", lambda m: f'### <span class="num">{int(m.group(2)):02d}</span> ', md)
    md = re.sub(r"(?m)^## (\d+)\. ", lambda m: f'## <span class="num">{style.ROMAN[int(m.group(1))]}</span> ', md)
    return re.sub(r"(?<![\d.A-Za-z])([1-6])\.([1-9])(?![\d.%A-Za-z]|배)",
                  lambda m: valid.get(f"{m.group(1)}.{m.group(2)}", m.group(0)), md)


EX_HEAD = ["시험", "선지", "원문 발췌", "판정", "포인트"]


def style_tables(body, state):
    def fix(m):
        t = m.group(0)
        heads = re.findall(r"<th[^>]*>(.*?)</th>", t)
        if heads == EX_HEAD:
            cols = ('<colgroup><col style="width:40mm"><col style="width:16mm"><col>'
                    '<col style="width:46mm"><col style="width:66mm"></colgroup>')
            t = t.replace("<table>", f'<table class="fixed">{cols}', 1)
            t = re.sub(r"<th[^>]*>포인트</th>", "<th>판단 근거</th>", t)

            def row(rm):
                cells = re.findall(r"<td[^>]*>(.*?)</td>", rm.group(0), flags=re.S)
                if len(cells) != 5:
                    return rm.group(0)
                ex = re.sub(r"^(\d{4}(?:학년도|년)) ", r"\1<br>", cells[0])
                return (f'<tr><td>{ex}</td><td class="c">{cells[1]}</td><td class="ex">{cells[2]}</td>'
                        f'<td class="v">{cells[3]}</td><td>{cells[4]}</td></tr>')
            t = re.sub(r"<tr>\s*<td.*?</tr>", row, t, flags=re.S)
            wrap = f'<div class="tw">{t}</div>'
            if not state.get("legend"):
                state["legend"] = True
                wrap = ('<p class="legend">※ 판정의 O는 맞는 표현, X는 틀린 표현이며 화살표 뒤가 고친 형태. '
                        '원문 발췌의 밑줄은 기출의 밑줄 선지.</p>') + wrap
            return wrap
        if heads and heads[0].startswith("밑줄에 나온 표현"):
            cols = '<colgroup><col style="width:68mm"><col><col style="width:48mm"></colgroup>'
            t = t.replace("<table>", f'<table class="fixed">{cols}', 1)
            t = re.sub(r"<tr>((?:\s*<td[^>]*>.*?</td>){2})\s*<td[^>]*>(.*?)</td>\s*</tr>",
                       lambda r: f'<tr>{r.group(1)}<td class="c">{r.group(2)}</td></tr>', t, flags=re.S)
        return f'<div class="tw">{t}</div>'
    return re.sub(r"<table>.*?</table>", fix, body, flags=re.S)


def guide_html(md_raw):
    """원고 → (본문 HTML, 확인 문제 정답 부록 HTML, 장 목록)"""
    questions = load_questions()
    secs = live_sections()
    wrong = Counter(c["category"] for q in questions.values()
                    if q["record"]["found"] and q["record"]["format"] == "밑줄5지"
                    for c in q["record"]["choices"] if c["is_answer"])
    md = re.sub(r"^((?:  )+)(?=(?:[-*]|\d+\.) )", lambda m: m.group(1) * 2, md_raw, flags=re.M)
    md = transform_guide_md(md, wrong, secs)
    md, answers = split_quizzes(md)
    md = re.sub(r"(?ms)^#### 판단 규칙\n(.*?)(?=^#{2,4} |^<div|\Z)",
                lambda m: f'<div class="rulebox" markdown="1">\n\n#### 판단 규칙\n\n{m.group(1).rstrip()}\n\n</div>\n\n', md)
    md = re.sub(r"\{\{(.*?)\}\}", lambda m: f'<span class="bl"><b>{html.escape(m.group(1))}</b></span>', md)
    md = renumber(md, secs)
    chapters, html_parts, state = [], [], {}
    for cm in re.split(r"(?m)^(?=## )", md):
        h = re.match(r'## <span class="num">(\S+)</span> (.+)', cm)
        if not h:
            continue
        n = style.ROMAN.index(h.group(1))
        chapters.append((n, h.group(2).strip()))
        body = markdown.markdown(cm, extensions=["tables", "sane_lists", "md_in_html"])
        html_parts.append(f'<section class="chap c{n}">{style_tables(body, state)}</section>')
    rows = []
    for title, ans in answers:
        t = renumber("### " + title, secs).replace("### ", "")
        rows.append(f"<h3>{t}</h3>" + markdown.markdown(ans, extensions=["sane_lists"]))
    app = ('<section class="chap appendix"><h2>확인 문제 정답</h2>' + "".join(rows) + "</section>") if rows else ""
    return "\n".join(html_parts), app, chapters


def toc_key(title):
    """PDF 개요 제목은 로마 숫자가 겹쳐 나오므로 앞 번호를 떼고 비교"""
    return re.sub(r"^[\sⅠ-Ⅻ0-9]+", "", title).strip()


def toc_html(entries, pages):
    rows = ['<div class="toc"><div class="head">차례</div>']
    for lvl, title in entries:
        cls = "ch" if lvl == 1 else "sec"
        rows.append(f'<div class="row {cls}"><span>{html.escape(title)}</span><span class="lead"></span>'
                    f'<span class="pg">{pages.get(title, 0)}</span></div>')
    rows.append("</div>")
    return "".join(rows)


# ---------------------------------------------------------------- PDF 출력

def chromium(pw):
    exe = "/opt/pw-browsers/chromium"
    return pw.chromium.launch(executable_path=exe if Path(exe).exists() else None)


def print_pdf(html_text, pdf_path, wait_js=None, outline=False):
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
        page.pdf(path=str(pdf_path), print_background=True, prefer_css_page_size=True, scale=style.SCALE,
                 outline=outline, tagged=outline)
        b.close()


def finish(pdf_path, out_path, title, keep_toc=False):
    """메타데이터 정리 (Creator, Producer 비움)"""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    toc = [[lvl, re.sub(r"^([Ⅰ-Ⅻ])\1", r"\1", t), pg] for lvl, t, pg in doc.get_toc() if lvl <= 3] if keep_toc else []
    out = pymupdf.open()
    out.insert_pdf(doc)
    if toc:
        out.set_toc(toc)
    out.set_metadata({"title": title, "author": "", "subject": "", "keywords": "", "creator": "", "producer": ""})
    out.save(out_path, garbage=3, deflate=True)
    print("wrote", out_path, out.page_count, "pages")
    return out.page_count


def build_exam(questions, fonts, tmpdir):
    passages = load_json("passages.json")
    expl = load_json("explanations.json")
    secs = live_sections()
    order = exam_order(questions, passages)
    qhtml = "\n".join(question_html(i + 1, questions[e], passages[e]) for i, e in enumerate(order))
    for teacher in (False, True):
        part = tmpdir / f"exam_{'t' if teacher else 's'}.pdf"
        print_pdf(style.exam_page(qhtml, teacher, fonts, EXAM_TITLE, EXAM_SUB, html.escape(NOTICE)), part,
                  wait_js="window.__done === true")
        name = "영어29번_어법기출69제_교사용.pdf" if teacher else "영어29번_어법기출69제_문제지.pdf"
        finish(part, OUT / name, EXAM_TITLE + (" 교사용" if teacher else " 문제지"))
    quick = "".join(f'<div>{i + 1:02d}. {answer_number(questions[e], passages[e])}</div>' for i, e in enumerate(order))
    items = "\n".join(explanation_html(i + 1, questions[e], passages[e], expl[e], secs) for i, e in enumerate(order))
    part = tmpdir / "answers.pdf"
    print_pdf(style.answers_page(quick, items, fonts, EXAM_TITLE, EXAM_SUB), part, wait_js="window.__done === true")
    finish(part, OUT / "영어29번_어법기출69제_정답과해설.pdf", EXAM_TITLE + " 정답과 해설")


def build_guide(fonts, tmpdir):
    md = (HERE / "src" / "총정리_빈칸.md").read_text(encoding="utf-8")
    body, appendix, chapters = guide_html(md)
    for teacher in (False, True):
        part = tmpdir / f"guide_{'t' if teacher else 's'}.pdf"
        print_pdf(style.guide_page(body + (appendix if teacher else ""), teacher, fonts, GUIDE_TITLE, GUIDE_SUB,
                                   chapters), part, outline=True)
        name = "영어29번_어법개념정리_교사용.pdf" if teacher else "영어29번_어법개념정리_학생용.pdf"
        finish(part, OUT / name, GUIDE_TITLE + (" 교사용" if teacher else " 학생용"), keep_toc=True)


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
        build_exam(questions, args.fonts, tmpdir)
    if args.only in (None, "guide"):
        build_guide(args.fonts, tmpdir)


if __name__ == "__main__":
    main()
