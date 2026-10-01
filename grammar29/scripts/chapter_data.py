"""총정리 집필용 단원별 기출 선지 묶음을 만든다.

실행: python3 grammar29/scripts/chapter_data.py <출력 디렉터리>
출력: 단원마다 JSON 파일 하나. 개념별 통계와 기출 선지(시험명, 밑줄, 정오, 고친 형태, 세부 포인트, 해설, 원문 발췌)
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze import CHAPTERS, DISPLAY, RECENT_FROM, exam_label, is_wrong_choice, load  # noqa: E402


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    qs = [q for q in load() if q["record"] and q["record"]["found"]]
    tested, wrong, wrong_recent, tested_recent = Counter(), Counter(), Counter(), Counter()
    for q in qs:
        for c in q["record"]["choices"]:
            tested[c["category"]] += 1
            recent = q["exam"]["Y"] >= RECENT_FROM
            tested_recent[c["category"]] += recent
            if is_wrong_choice(q, c):
                wrong[c["category"]] += 1
                wrong_recent[c["category"]] += recent
    for n, (chapter, cats) in enumerate(CHAPTERS, 1):
        concepts = []
        for cat in sorted(cats, key=lambda k: (-tested[k], -wrong[k])):
            items = []
            for q in qs:
                r = q["record"]
                for c in r["choices"]:
                    if c["category"] != cat:
                        continue
                    items.append({
                        "시험": exam_label(q),
                        "시행": f"{q['exam']['Y']}년 {q['exam']['M']}월",
                        "형식": r["format"],
                        "선지": c["label"],
                        "밑줄": c["underlined"],
                        "판정": "X(정답, 어법상 틀림)" if is_wrong_choice(q, c) else ("네모형 선택" if r["format"] == "네모3지" else "O(어법상 맞음)"),
                        "고친형태": c["correct_form"],
                        "세부포인트": c["sub_point"],
                        "해설": c["explanation"],
                        "원문발췌": c["context"],
                        "신뢰도": r["confidence"],
                    })
            concepts.append({
                "category": cat,
                "개념": DISPLAY[cat],
                "출제선지": tested[cat],
                "정답선지": wrong[cat],
                "최근5개년출제": tested_recent[cat],
                "최근5개년정답": wrong_recent[cat],
                "기출": items,
            })
        (out / f"chapter{n}.json").write_text(
            json.dumps({"단원번호": n, "단원": chapter, "개념": concepts}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(n, chapter, [(c["개념"], c["출제선지"], c["정답선지"]) for c in concepts])


if __name__ == "__main__":
    main(sys.argv[1])
