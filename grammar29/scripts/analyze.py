"""고3 영어 어법 기출 데이터(data/questions.json)를 집계해 문서와 CSV를 생성한다.

실행: python3 grammar29/scripts/analyze.py
출력:
  data/choices.csv            선지 단위 표
  docs/01_기출문항_목록.md    시험별 어법 문항과 선지별 문법 포인트
  docs/02_출제분석.md         문법 개념별 출제 빈도와 추세
  data/stats.json             총정리 집필에 쓰는 집계값
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

# 수집 단계 category 값 → 문서 표기
DISPLAY = {
    "수일치": "주어와 동사의 수일치",
    "동사vs준동사": "동사 자리와 준동사 자리",
    "능동vs수동": "능동태와 수동태",
    "분사(현재vs과거)": "현재분사와 과거분사",
    "분사구문": "분사구문",
    "시제": "시제",
    "조동사": "조동사",
    "가정법": "가정법",
    "to부정사": "to부정사",
    "동명사": "동명사",
    "관계대명사": "관계대명사",
    "관계대명사what": "what과 that의 구분",
    "관계부사/전치사+관계사": "관계부사와 전치사+관계대명사",
    "명사절접속사(that/whether/if/의문사)": "명사절 접속사 that, whether, if",
    "접속사vs전치사": "접속사와 전치사",
    "대명사(수·격)": "대명사의 수와 격",
    "재귀대명사": "재귀대명사",
    "지시대명사that/those": "지시대명사 that과 those",
    "형용사vs부사": "형용사와 부사",
    "보어(2형식/5형식목적격보어)": "보어와 목적격보어",
    "비교구문": "비교 구문",
    "병렬구조": "병렬 구조",
    "도치": "도치",
    "강조구문": "강조 구문",
    "대동사": "대동사",
    "가주어/가목적어it": "가주어와 가목적어 it",
    "한정사/수량사": "한정사와 수량사",
    "명사(가산/불가산)": "명사의 수",
    "자동사vs타동사": "자동사와 타동사",
    "기타": "기타",
}

# 총정리 단원 구성
CHAPTERS = [
    ("동사", ["수일치", "동사vs준동사", "능동vs수동", "시제", "조동사", "가정법", "대동사", "자동사vs타동사"]),
    ("준동사", ["분사(현재vs과거)", "분사구문", "to부정사", "동명사", "보어(2형식/5형식목적격보어)"]),
    ("연결어", ["관계대명사", "관계대명사what", "관계부사/전치사+관계사", "명사절접속사(that/whether/if/의문사)", "접속사vs전치사"]),
    ("품사와 대명사", ["대명사(수·격)", "재귀대명사", "지시대명사that/those", "형용사vs부사", "한정사/수량사", "명사(가산/불가산)"]),
    ("특수 구문", ["비교구문", "병렬구조", "도치", "강조구문", "가주어/가목적어it", "기타"]),
]
CHAPTER_OF = {c: ch for ch, cats in CHAPTERS for c in cats}

KIND_ORDER = {"수능": 0, "평가원": 1, "교육청": 2}
RECENT_FROM = 2022  # 시행 연도 기준 최근 5개년(2022~2026)


def disp(cat):
    return DISPLAY.get(cat, cat)


def exam_label(q):
    e = q["exam"]
    if e["kind"] == "수능":
        return f"{e['H']}학년도 수능"
    if e["kind"] == "평가원":
        return f"{e['H']}학년도 {e['M']}월 모평"
    return f"{e['Y']}년 {e['M']}월 학평"


def sort_key(q):
    e = q["exam"]
    return (e["Y"], e["M"])


def md_escape(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def load():
    qs = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    qs.sort(key=sort_key)
    return qs


def write_csv(qs):
    path = DATA / "choices.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["exam_id", "시험", "시행연도", "월", "구분", "문항번호", "선지", "밑줄", "정답여부",
                    "고친형태", "개념", "세부포인트", "설명", "원문발췌", "신뢰도"])
        for q in qs:
            r, e = q["record"], q["exam"]
            for c in r["choices"]:
                w.writerow([e["id"], exam_label(q), e["Y"], e["M"], e["kind"], r["question_number"], c["label"],
                            c["underlined"], "O" if c["is_answer"] else "", c["correct_form"], disp(c["category"]),
                            c["sub_point"], c["explanation"], c["context"], r["confidence"]])


def write_list(qs):
    out = ["# 고3 영어 어법 기출 문항 목록", ""]
    out.append("## 1. 수록 범위")
    out.append("")
    found = [q for q in qs if q["record"] and q["record"]["found"]]
    out.append(f"- 2016년 3월 학평부터 2027학년도 9월 모평까지 고3 시험 {len(qs)}회 중 어법 문항 확인 {len(found)}회")
    out.append("- 시험별 표의 굵은 행이 정답(어법상 틀린 표현) 선지이며, 네모형은 행마다 맞는 표현을 괄호에 표기")
    out.append("- 신뢰도 high는 서로 독립된 출처 2곳 이상에서 정답과 선지가 일치한 문항, medium과 low는 일부만 확인된 문항")
    out.append("")
    years = defaultdict(list)
    for q in qs:
        years[q["exam"]["Y"]].append(q)
    sec = 2
    for y in sorted(years):
        out.append(f"## {sec}. {y}년 시행 ({y + 1}학년도)")
        out.append("")
        sec += 1
        for q in years[y]:
            r = q["record"]
            out.append(f"### {exam_label(q)}")
            out.append("")
            if not r or not r["found"]:
                note = (r or {}).get("notes", "수집 실패")
                out.append(f"- 어법 문항 미확인. {md_escape(note)[:300]}")
                out.append("")
                continue
            out.append(f"- 문항 {r['question_number']}번, 형식 {r['format']}, 정답 {r['answer']} ({md_escape(r['answer_fix'])}), 신뢰도 {r['confidence']}")
            out.append(f"- 지문 소재는 {md_escape(r['passage_topic'])}")
            out.append("")
            out.append("선지 / 문법 개념 / 세부 포인트 / 원문 발췌")
            out.append("")
            out.append("| 선지 | 밑줄 | 개념 | 세부 포인트 | 원문 발췌 |")
            out.append("| --- | --- | --- | --- | --- |")
            for c in r["choices"]:
                row = [c["label"], md_escape(c["underlined"]), disp(c["category"]), md_escape(c["sub_point"]),
                       md_escape(c["context"]) or "-"]
                if is_wrong_choice(q, c):
                    row = [f"**{x}**" if x and x != "-" else x for x in row]
                elif r["format"] == "네모3지":
                    row[1] = f"{row[1]} (맞는 표현 {md_escape(c['correct_form'])})"
                out.append("| " + " | ".join(row) + " |")
            out.append("")
    (DOCS / "01_기출문항_목록.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def is_wrong_choice(q, c):
    """밑줄형에서 어법상 틀린 표현으로 출제된 선지. 네모형은 틀린 선지가 없어 제외"""
    return c["is_answer"] and q["record"]["format"] == "밑줄5지"


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "-"


def write_analysis(qs):
    found = [q for q in qs if q["record"] and q["record"]["found"]]
    n_q = len(found)
    choices = [(q, c) for q in found for c in q["record"]["choices"]]
    n_c = len(choices)
    tested = Counter(c["category"] for _, c in choices)
    answer = Counter(c["category"] for q, c in choices if is_wrong_choice(q, c))
    recent = [(q, c) for q, c in choices if q["exam"]["Y"] >= RECENT_FROM]
    tested_recent = Counter(c["category"] for _, c in recent)
    answer_recent = Counter(c["category"] for q, c in recent if is_wrong_choice(q, c))
    csat = [(q, c) for q, c in choices if q["exam"]["kind"] in ("수능", "평가원")]
    tested_csat = Counter(c["category"] for _, c in csat)
    answer_csat = Counter(c["category"] for q, c in csat if is_wrong_choice(q, c))
    n_recent_q = len({q["exam"]["id"] for q, _ in recent})
    n_csat_q = len({q["exam"]["id"] for q, _ in csat})

    cats = sorted(tested, key=lambda k: (-tested[k], -answer[k]))
    out = ["# 고3 영어 어법 기출 출제 분석", ""]
    out.append("## 1. 분석 대상")
    out.append("")
    out.append(f"- 어법 문항 {n_q}개, 밑줄 선지 {n_c}개")
    out.append(f"- 최근 5개년(2022~2026년 시행) 문항 {n_recent_q}개, 수능과 평가원 모의평가 문항 {n_csat_q}개")
    fmt = Counter(q["record"]["format"] for q in found)
    num = Counter(q["record"]["question_number"] for q in found)
    out.append("- 형식별 문항 수는 " + ", ".join(f"{k} {v}개" for k, v in fmt.most_common()))
    out.append("- 문항 번호별 문항 수는 " + ", ".join(f"{k}번 {v}개" for k, v in sorted(num.items())))
    conf = Counter(q["record"]["confidence"] for q in found)
    out.append("- 신뢰도별 문항 수는 " + ", ".join(f"{k} {v}개" for k, v in conf.most_common()))
    out.append("")

    out.append("## 2. 문법 개념별 출제 빈도")
    out.append("")
    out.append("출제 선지 수 (개) / 선지 하나가 밑줄로 나온 횟수 / 정답 선지 수는 그 개념이 어법상 틀린 표현으로 나온 횟수")
    out.append("")
    out.append("| 순위 | 개념 | 단원 | 출제 선지 | 문항당 출제율 | 정답 선지 | 출제 대비 정답 | 최근 5개년 출제 | 최근 5개년 정답 | 수능과 모평 출제 | 수능과 모평 정답 |")
    out.append("| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for i, k in enumerate(cats, 1):
        out.append(f"| {i} | {disp(k)} | {CHAPTER_OF.get(k, '-')} | {tested[k]} | {pct(tested[k], n_q)} | {answer[k]} | "
                   f"{pct(answer[k], tested[k])} | {tested_recent[k]} | {answer_recent[k]} | {tested_csat[k]} | {answer_csat[k]} |")
    out.append("")
    out.append("- 문항당 출제율은 해당 개념 선지 수를 문항 수로 나눈 값이며, 한 문항에 같은 개념이 두 번 나오면 100%를 넘을 수 있음")
    out.append("")

    out.append("## 3. 틀린 표현으로 출제된 개념 순위")
    out.append("")
    out.append("정답 선지 수 (개) / 밑줄형 문항에서 어법상 틀린 표현으로 출제된 횟수, 네모형 제외")
    out.append("")
    out.append("| 순위 | 개념 | 정답 선지 | 비중 | 최근 5개년 | 수능과 모평 |")
    out.append("| ---: | --- | ---: | ---: | ---: | ---: |")
    n_wrong = sum(answer.values())
    for i, (k, v) in enumerate(sorted(answer.items(), key=lambda kv: (-kv[1], -tested[kv[0]])), 1):
        out.append(f"| {i} | {disp(k)} | {v} | {pct(v, n_wrong)} | {answer_recent[k]} | {answer_csat[k]} |")
    out.append("")

    out.append("## 4. 단원별 출제 비중")
    out.append("")
    out.append("출제 선지 수 (개) / 단원 구성은 총정리 문서와 같음")
    out.append("")
    out.append("| 단원 | 출제 선지 | 비중 | 정답 선지 | 정답 비중 |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    n_ans = sum(answer.values())
    for ch, cs in CHAPTERS:
        t = sum(tested[c] for c in cs)
        a = sum(answer[c] for c in cs)
        out.append(f"| {ch} | {t} | {pct(t, n_c)} | {a} | {pct(a, n_ans)} |")
    out.append("")

    out.append("## 5. 시험별 정답 개념 흐름")
    out.append("")
    out.append("시험별 정답 선지의 개념 / 빈 칸은 미확인 시험")
    out.append("")
    out.append("| 시행 연도 | 3월 | 4월 또는 5월 | 6월 모평 | 7월 | 9월 모평 | 10월 | 수능 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    grid = defaultdict(dict)
    for q in qs:
        r = q["record"]
        m = q["exam"]["M"]
        col = {3: 0, 4: 1, 5: 1, 6: 2, 7: 3, 9: 4, 10: 5, 11: 6}[m]
        if r and r["found"]:
            ans = [c for c in r["choices"] if is_wrong_choice(q, c)]
            grid[q["exam"]["Y"]][col] = ", ".join(disp(c["category"]) for c in ans) or "네모형"
        else:
            grid[q["exam"]["Y"]][col] = "-"
    for y in sorted(grid):
        out.append(f"| {y} | " + " | ".join(grid[y].get(i, " ") for i in range(7)) + " |")
    out.append("")

    out.append("## 6. 개념별 세부 포인트")
    out.append("")
    out.append("- 개념마다 기출 선지의 세부 포인트를 시험 순서로 나열하며, 굵은 글씨는 정답 선지")
    out.append("")
    by_cat = defaultdict(list)
    for q, c in choices:
        by_cat[c["category"]].append((q, c))
    for i, k in enumerate(cats, 1):
        out.append(f"### 6.{i} {disp(k)}")
        out.append("")
        for q, c in by_cat[k]:
            s = f"{exam_label(q)} {c['label']} {md_escape(c['underlined'])}"
            if is_wrong_choice(q, c):
                s = f"**{s} → {md_escape(c['correct_form'])}**"
            elif q["record"]["format"] == "네모3지":
                s = f"{s} (맞는 표현 {md_escape(c['correct_form'])})"
            out.append(f"- {s}, {md_escape(c['sub_point'])}")
        out.append("")
    (DOCS / "02_출제분석.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    stats = {
        "n_questions": n_q, "n_choices": n_c,
        "tested": dict(tested), "answer": dict(answer),
        "tested_recent": dict(tested_recent), "answer_recent": dict(answer_recent),
        "tested_csat": dict(tested_csat), "answer_csat": dict(answer_csat),
        "rank": cats,
    }
    (DATA / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    qs = load()
    DOCS.mkdir(exist_ok=True)
    write_csv(qs)
    write_list(qs)
    write_analysis(qs)
    print(f"{len(qs)} exams processed")


if __name__ == "__main__":
    main()
