"""인쇄물 CSS, 쪽 배치 스크립트

치수 근거는 DESIGN.md (2025학년도 수능과 2025년 7월 학평 원본 실측, EBS 해설지와 HWP 기본값)

선 굵기: Chromium은 1px보다 가는 테두리와 밑줄을 1px(0.75pt)로 올림. 그래서 본문은 치수를 2배로 짜고
page.pdf(scale=0.5)로 인쇄함. CSS는 1배 치수로 적고 x2()가 mm, pt, px를 2배로 바꿈.
선 굵기는 'lw' 단위로 적으며 2배 조판의 정수 px로 그대로 옮김: 1lw = 0.375pt, 2lw = 0.75pt, 3lw = 1.125pt.
@page 규칙과 여백 상자는 축소되지 않으므로 x2()를 거치지 않음.
"""
import re
from pathlib import Path

RED = "#e00000"      # 교사용 정답 (HWP 학습지의 빨간 정답 관례)
SPOT = "#1b4a8c"     # 교재 별색, 장 번호와 절 번호, 장 제목 아래 줄에만
SCALE = 0.5
ROMAN = ["", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ"]


def x2(css):
    css = re.sub(r"(?<![\w#.])(-?\d*\.?\d+)(mm|pt|px)\b", lambda m: f"{float(m.group(1)) * 2:g}{m.group(2)}", css)
    return re.sub(r"(\d+)lw\b", r"\1px", css)


def font_faces(font_dir):
    d = Path(font_dir).resolve().as_uri()
    return f"""
@font-face{{font-family:"ExamLatin";src:url({d}/LiberationSerif-Regular.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:"ExamLatin";src:url({d}/LiberationSerif-Bold.ttf);font-weight:700;font-style:normal}}
@font-face{{font-family:"ExamLatin";src:url({d}/LiberationSerif-Italic.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:"ExamMyeongjo";src:url({d}/UnBatang.ttf);font-weight:400;size-adjust:92%}}
@font-face{{font-family:"ExamMyeongjo";src:url({d}/UnBatangBold.ttf);font-weight:700;size-adjust:92%}}
@font-face{{font-family:"ExamNumber";src:url({d}/UnBatangBold.ttf)}}
@font-face{{font-family:"ExamGothic";src:url({d}/UnDotum.ttf);font-weight:400}}
@font-face{{font-family:"ExamGothic";src:url({d}/UnDotumBold.ttf);font-weight:700}}
"""


PAGE0 = """@page { size: A4; margin: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
"""

# ====================================================================== 시험지

EXAM_CSS = """
body { margin: 0; background: #fff; color: #000; }
#src { position: absolute; left: -9999px; top: 0; }
.page { width: 210mm; height: 296.5mm; box-sizing: border-box; padding: 10mm 13mm 8mm; position: relative;
        page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }

/* 머리말 */
.hd { display: grid; grid-template-columns: 34mm 1fr 34mm; align-items: end; padding-bottom: 1.6mm;
      border-bottom: 3lw solid #000; position: relative; }
.hd .subj { justify-self: start; font: 700 10pt "ExamGothic"; border: 1lw solid #000; border-radius: 1.6mm;
            padding: 0.6mm 2.4mm 0.4mm; }
.hd .ttl { justify-self: center; text-align: center; font: 700 15pt "ExamGothic"; letter-spacing: 0.02em; position: relative; }
.hd .no { justify-self: end; font: 700 21pt/1 "ExamLatin"; }
.hd.even .subj { grid-column: 3; justify-self: end; }
.hd.even .ttl { grid-column: 2; grid-row: 1; }
.hd.even .no { grid-column: 1; grid-row: 1; justify-self: start; }
.hd .tch { position: absolute; left: 100%; bottom: 1.2mm; margin-left: 2.4mm; font: 400 8pt "ExamGothic";
           border: 1lw solid #000; padding: 0.2mm 1.4mm; letter-spacing: 0; white-space: nowrap; }
.first .hd .ttl { font: 700 20pt "ExamGothic"; }
.first .hd .sub { display: block; font: 400 9pt "ExamMyeongjo"; letter-spacing: -0.03em; margin-bottom: 1.2mm; }
.first .hd .no { font-size: 26pt; }
.namebar { text-align: right; font: 400 9pt "ExamMyeongjo"; padding: 1.4mm 0 1.4mm; border-bottom: 1lw solid #000; }
.namebar span { display: inline-block; border-bottom: 1lw solid #000; height: 3.6mm; vertical-align: -0.6mm; }

/* 본문 2단 */
.cols { position: absolute; left: 13mm; right: 13mm; bottom: 15mm; display: flex; }
.col { width: 88.3mm; position: relative; overflow: hidden; }
.rule { width: 7.4mm; position: relative; }
.rule::after { content: ""; position: absolute; left: 50%; top: -4.5mm; bottom: 0; border-left: 2lw solid #000; }
.ft { position: absolute; left: 0; right: 0; bottom: 6mm; text-align: center; font: 400 8.5pt "ExamLatin"; }

/* 안내 상자 (첫 쪽 왼쪽 단 위) */
.notice { border: 1lw solid #000; padding: 1.8mm 2.4mm; font: 400 8.6pt/13px "ExamMyeongjo"; text-align: left;
          word-break: keep-all; letter-spacing: -0.04em; }

/* 문항 */
.q { font: 400 9.5pt/18px "ExamLatin", "ExamMyeongjo", serif; }
.stem { font-family: "ExamMyeongjo", "ExamLatin", serif; font-size: 9.6pt; line-height: 18px; padding-left: 8.8pt;
        text-indent: -8.8pt; word-break: keep-all; overflow-wrap: anywhere; text-align: left; letter-spacing: -0.04em; }
.qno { font: 400 10.3pt "ExamNumber"; margin-right: 0.3em; letter-spacing: 0; }
.stem u { text-decoration-thickness: 1lw; text-underline-offset: 2.2pt; }
.src { display: block; text-align: right; font-size: 7.9pt; line-height: 12px; letter-spacing: 0; }
.pt { white-space: nowrap; }
.passage { margin-top: 2pt; padding-left: 8.8pt; text-align: justify; hyphens: none; }
.passage p { margin: 0; text-indent: 8.2pt; }
.cn { font-family: "ExamMyeongjo"; font-size: 9.6pt; margin-right: 0.3em; position: relative; }
.opt u { text-decoration-thickness: 1lw; text-underline-offset: 2.3pt; }
.dash { font-family: "ExamMyeongjo"; }
.nemo-label { margin-right: 0.15em; }
.nemo { display: inline-flex; flex-direction: column; vertical-align: middle; border: 1lw solid #000;
        padding: 0 1.2mm; line-height: 12px; margin: 1px 0; text-indent: 0; }
.nemo span { display: block; text-align: center; }
.foot { text-align: right; font-size: 8.6pt; line-height: 13px; margin-top: 1.4mm; }
.foot div { font-family: "ExamLatin", "ExamMyeongjo"; }
.box-choices { margin: 2.4mm 0 0 8.8pt; border-collapse: collapse; font-size: 9.3pt; line-height: 16px; }
.box-choices td { padding: 0 2.2mm 0 0; }
.box-choices tr:first-child td { text-align: center; }
.box-choices td.n { padding-right: 1.5mm; }
.key { visibility: hidden; margin-top: 1.6mm; padding-left: 8.8pt; font: 400 8.6pt/13px "ExamLatin", "ExamMyeongjo";
       color: RED; letter-spacing: -0.02em; }

/* 교사용 표시: 색과 위에 겹치는 원만 더해 학생용과 줄바꿈이 같게 둠 */
.teacher .key { visibility: visible; }
.teacher .ans .cn { color: RED; }
.teacher .ans .cn::after { content: ""; position: absolute; left: 50%; top: 52%; width: 1.32em; height: 1.32em;
                           transform: translate(-50%, -50%); border: 2lw solid RED; border-radius: 50%; }
.teacher .opt.ans u { color: RED; }
.teacher .nemo .pick { color: RED; }
""".replace("RED", RED)

EXAM_JS = """
(function () {
  const MM = 2 * 96 / 25.4;   /* 2배 조판 */
  const src = document.getElementById('src');
  const book = document.getElementById('book');
  const qs = Array.from(src.querySelectorAll('.q'));
  const TITLE = book.dataset.title, SUB = book.dataset.sub, TEACHER = book.dataset.teacher === '1';
  const tch = TEACHER ? '<span class="tch">교사용</span>' : '';
  let pages = [];
  function newPage() {
    const n = pages.length + 1;
    const p = document.createElement('div');
    p.className = 'page' + (n === 1 ? ' first' : '');
    let hd;
    if (n === 1) {
      hd = `<div class="hd"><span class="subj">고3 영어</span><div class="ttl"><span class="sub">${SUB}</span>${TITLE}${tch}</div><span class="no">${n}</span></div>
            <div class="namebar">3학년 <span style="width:18mm"></span>반 <span style="width:18mm"></span>번 이름 <span style="width:54mm"></span></div>`;
    } else {
      const even = n % 2 === 0;
      hd = `<div class="hd ${even ? 'even' : ''}"><span class="subj">고3 영어</span><div class="ttl">${TITLE}${tch}</div><span class="no">${n}</span></div>`;
    }
    p.innerHTML = hd + '<div class="cols"><div class="col"></div><div class="rule"></div><div class="col"></div></div><div class="ft">- ' + n + ' -</div>';
    book.appendChild(p);
    const cols = p.querySelector('.cols');
    const top = (n === 1 ? p.querySelector('.namebar') : p.querySelector('.hd')).getBoundingClientRect().bottom
                - p.getBoundingClientRect().top + 4.5 * MM;
    cols.style.top = top + 'px';
    const h = cols.getBoundingClientRect().height;
    p.querySelectorAll('.col').forEach(c => c.style.height = h + 'px');
    pages.push(p);
    return Array.from(p.querySelectorAll('.col'));
  }
  let cols = newPage(), ci = 0, used = 0, count = 0, afterNotice = false;
  const notice = book.dataset.notice;
  if (notice) {
    const d = document.createElement('div'); d.className = 'notice'; d.innerHTML = notice; cols[0].appendChild(d);
    used = d.getBoundingClientRect().height + 3.5 * MM; afterNotice = true;
  }
  const GAP = 9 * MM;
  for (const q of qs) {
    while (true) {
      const col = cols[ci];
      const H = col.getBoundingClientRect().height;
      col.appendChild(q);
      q.style.marginTop = '0px';
      const qh = q.getBoundingClientRect().height;
      let start;
      if (used === 0) start = 0;
      else if (afterNotice && count === 0) start = used;
      else start = count === 1 ? Math.max(used + GAP, H * 0.5) : used + GAP;
      if (count < 2 && start + qh <= H) {
        q.style.marginTop = (start - used) + 'px';
        used = start + qh; count += 1; afterNotice = false;
        break;
      }
      col.removeChild(q);
      if (used === 0) { col.appendChild(q); used = H; count = 2; break; }
      ci += 1; used = 0; count = 0; afterNotice = false;
      if (ci > 1) { cols = newPage(); ci = 0; }
    }
  }
  window.__done = true;
})();
"""


def exam_page(questions_html, teacher, font_dir, title, sub, notice):
    cls = "teacher" if teacher else ""
    css = PAGE0 + x2(font_faces(font_dir) + EXAM_CSS)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>{title}{' 교사용' if teacher else ' 문제지'}</title><style>{css}</style></head>
<body class="{cls}"><div id="src">{questions_html}</div>
<div id="book" data-title="{title}" data-sub="{sub}" data-teacher="{1 if teacher else 0}" data-notice="{notice}"></div>
<script>document.fonts.ready.then(() => {{ {EXAM_JS} }});</script>
</body></html>"""


# ====================================================================== 정답과 해설

ANS_CSS = """
body { margin: 0; background: #fff; color: #000; font: 400 9.3pt/19px "ExamLatin", "ExamMyeongjo", serif; }
#src { position: absolute; left: -9999px; top: 0; width: 84mm; }
.page { width: 210mm; height: 296.5mm; box-sizing: border-box; position: relative; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.ahd { position: absolute; left: 16mm; right: 16mm; top: 12mm; display: flex; justify-content: space-between;
       font: 400 8pt "ExamGothic"; border-bottom: 3lw solid #000; padding-bottom: 1mm; }
.aft { position: absolute; left: 16mm; right: 16mm; bottom: 9mm; text-align: center; font: 400 8.5pt "ExamLatin";
       border-top: 2lw solid #000; padding-top: 0.5mm; }
.aft div { border-top: 1lw solid #000; padding-top: 1.6mm; }
.top { position: absolute; left: 16mm; right: 16mm; top: 20mm; }
.title { border: 1lw solid #000; outline: 1lw solid #000; outline-offset: 0.6mm; padding: 2.4mm 3mm; text-align: center;
         font: 700 14pt "ExamGothic"; margin: 1mm 1mm 4mm; }
.title small { display: block; font: 400 8.8pt "ExamMyeongjo"; margin-top: 0.8mm; letter-spacing: -0.03em; }
.quick { border-top: 3lw solid #000; border-bottom: 3lw solid #000; padding: 2mm 0; margin-bottom: 1mm;
         display: grid; grid-template-columns: repeat(10, 1fr); row-gap: 1.2mm; font: 700 9.4pt "ExamLatin", "ExamMyeongjo"; }
.cols { position: absolute; left: 16mm; right: 16mm; bottom: 20mm; display: flex; }
.col { width: 84mm; overflow: hidden; }
.rule { width: 10mm; position: relative; }
.rule::after { content: ""; position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1lw solid #000; }
.ex { margin-bottom: 3.4mm; text-align: justify; word-break: normal; overflow-wrap: anywhere; letter-spacing: -0.03em; }
.ex-head { margin-bottom: 0.6mm; }
.ex-head b { font: 400 10.3pt "ExamNumber"; letter-spacing: 0; }
.ex-head .src { font-size: 8.4pt; }
.ex .line { padding-left: 1.2em; text-indent: -1.2em; }
.ex .sol { padding-left: 2.9em; text-indent: -2.9em; }
.ex .lbl { display: inline-block; text-indent: 0; }
.ex .w { font-family: "ExamLatin"; letter-spacing: 0; }
.ex .lead { font-weight: 700; }
"""

ANS_JS = """
(function () {
  const MM = 2 * 96 / 25.4;
  const src = document.getElementById('src'), book = document.getElementById('book');
  const items = Array.from(src.querySelectorAll('.ex'));
  const TITLE = book.dataset.title;
  let n = 0;
  function newPage() {
    n += 1;
    const p = document.createElement('div');
    p.className = 'page';
    p.innerHTML = `<div class="ahd"><span>${TITLE} 정답과 해설</span><span>교사용</span></div>` +
      (n === 1 ? `<div class="top">${document.getElementById('first').innerHTML}</div>` : '') +
      `<div class="cols"><div class="col"></div><div class="rule"></div><div class="col"></div></div>` +
      `<div class="aft"><div>- ${n} -</div></div>`;
    book.appendChild(p);
    const cols = p.querySelector('.cols');
    const anchor = n === 1 ? p.querySelector('.top') : p.querySelector('.ahd');
    cols.style.top = (anchor.getBoundingClientRect().bottom - p.getBoundingClientRect().top + 4 * MM) + 'px';
    const h = cols.getBoundingClientRect().height;
    p.querySelectorAll('.col').forEach(c => c.style.height = h + 'px');
    return Array.from(p.querySelectorAll('.col'));
  }
  let cols = newPage(), ci = 0;
  const fits = c => c.scrollHeight <= c.clientHeight + 1;
  function advance() { ci += 1; if (ci > 1) { cols = newPage(); ci = 0; } }
  for (let it of items) {
    while (true) {
      const col = cols[ci];
      col.appendChild(it);
      if (fits(col)) break;
      /* 긴 해설은 줄 단위로 다음 단에 이어 씀 (머리와 최소 두 줄은 남김) */
      if (it.children.length > 3) {
        const rest = document.createElement('div');
        rest.className = 'ex cont';
        while (!fits(col) && it.children.length > 3) rest.prepend(it.lastElementChild);
        if (fits(col)) { advance(); it = rest; continue; }
        while (rest.firstChild) it.appendChild(rest.firstChild);
      }
      col.removeChild(it);
      if (col.children.length === 0) { col.appendChild(it); break; }
      advance();
    }
  }
  window.__done = true;
})();
"""


def answers_page(quick_html, items_html, font_dir, title, sub):
    css = PAGE0 + x2(font_faces(font_dir) + ANS_CSS)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title} 정답과 해설</title>
<style>{css}</style></head><body>
<div id="first" hidden><div class="title">{title} 정답과 해설<small>{sub}</small></div><div class="quick">{quick_html}</div></div>
<div id="src">{items_html}</div><div id="book" data-title="{title}"></div>
<script>document.fonts.ready.then(() => {{ {ANS_JS} }});</script>
</body></html>"""


# ====================================================================== 개념 정리 교재

GUIDE_PAGE = """
@page { size: A4; margin: 24mm 20mm 21mm;
  @bottom-center { content: "- " counter(page) " -"; font: 400 8.5pt "Liberation Serif"; vertical-align: top; padding-top: 6mm; } }
@page :left { margin-left: 18mm; margin-right: 22mm;
  @top-left { content: "TITLE"; font: 400 7.8pt "UnDotum"; vertical-align: bottom; padding-bottom: 1.2mm;
              border-bottom: 0.4pt solid #000; width: 100%; } }
@page :right { margin-left: 22mm; margin-right: 18mm;
  @top-right { content: "TITLE"; font: 400 7.8pt "UnDotum"; vertical-align: bottom; padding-bottom: 1.2mm;
               border-bottom: 0.4pt solid #000; width: 100%; text-align: right; } }
@page :first { @top-left { content: none; border: 0; } @top-right { content: none; border: 0; } }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
"""

GUIDE_CSS = """
body { margin: 0; background: #fff; color: #000; font: 400 10.2pt/22px "ExamLatin", "ExamMyeongjo", serif;
       text-align: justify; word-break: keep-all; overflow-wrap: anywhere; letter-spacing: -0.03em; }
.cover { border-bottom: 3lw solid #000; padding-bottom: 2mm; display: grid; grid-template-columns: auto 1fr; align-items: end; gap: 4mm; }
.cover .subj { font: 700 10pt "ExamGothic"; border: 1lw solid #000; border-radius: 1.6mm; padding: 0.6mm 2.4mm 0.4mm; letter-spacing: 0; }
.cover h1 { margin: 0; font: 700 19pt "ExamGothic"; letter-spacing: 0.02em; }
.cover .sub { font: 400 9pt "ExamMyeongjo"; display: block; margin-bottom: 1mm; }
.namebar { text-align: right; font: 400 9pt "ExamMyeongjo"; padding: 1.6mm 0 2.4mm; }
.namebar span { display: inline-block; border-bottom: 1lw solid #000; height: 3.6mm; vertical-align: -0.6mm; }
.memo { text-align: left; font-size: 9pt; line-height: 16px; margin: 0 0 5mm; }
.toc { margin: 0 0 4mm; }
.toc .head { font: 700 12pt "ExamGothic"; margin: 0 0 2mm; letter-spacing: 0.3em; }
.toc .row { display: flex; align-items: baseline; gap: 2mm; line-height: 19px; font-size: 9.6pt; }
.toc .row.ch { font: 700 9.8pt/22px "ExamGothic"; margin-top: 2mm; letter-spacing: 0; }
.toc .row.sec { padding-left: 7mm; }
.toc .lead { flex: 1; border-bottom: 1lw dotted #000; transform: translateY(-1.2mm); }
.toc .pg { font-family: "ExamLatin"; min-width: 6mm; text-align: right; letter-spacing: 0; }
section.chap { break-before: page; }
section.chap.c1 { break-before: page; }
h2 { font: 700 15.5pt "ExamGothic"; margin: 0 0 4mm; padding-bottom: 1.6mm; border-bottom: 3lw solid SPOT; letter-spacing: 0; }
h2 .num { font: 700 21pt/1 "ExamLatin", "ExamMyeongjo"; color: SPOT; margin-right: 2.6mm; vertical-align: -1pt; }
h3 { font: 700 11.6pt "ExamGothic"; margin: 7mm 0 1.6mm; break-after: avoid; letter-spacing: 0; }
h3 .num { color: SPOT; margin-right: 1.6mm; font-family: "ExamLatin"; }
h4 { font: 700 9.8pt "ExamGothic"; margin: 3.2mm 0 1mm; break-after: avoid; letter-spacing: 0; }
h4::before { content: "■ "; font-size: 8pt; vertical-align: 0.6pt; }
p { margin: 1px 0; }
ul, ol { margin: 1px 0 4px; padding-left: 5mm; }
li { margin: 0; }
ul { list-style: none; }
ul > li { position: relative; }
ul > li::before { content: "◦"; position: absolute; left: -4mm; }
ul ul > li::before { content: "-"; left: -3.4mm; }
ol { padding-left: 5.4mm; }
strong { font-weight: 400; text-decoration: underline; text-decoration-thickness: 1lw; text-underline-offset: 2.2pt; }
.note { font-size: 9pt; line-height: 16px; margin: 0.4mm 0 1.2mm; }
.rulebox { border: 1lw solid #000; padding: 1.4mm 3.2mm 1.8mm; margin: 2.6mm 0 2mm;
           -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.rulebox h4 { margin-top: 0.6mm; }
.tw { margin: 1.2mm 0 3mm; break-before: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 8.7pt; line-height: 15px; border-top: 2lw solid #000;
        border-bottom: 2lw solid #000; text-align: left; letter-spacing: -0.02em; }
table.fixed { table-layout: fixed; }
th { font: 700 8.4pt "ExamGothic"; background: #e6e6e6; padding: 1mm 1.4mm; border-bottom: 1lw solid #000;
     white-space: nowrap; text-align: center; letter-spacing: 0; }
td { padding: 0.9mm 1.4mm; border-bottom: 1lw solid #000; vertical-align: top; }
tr { break-inside: avoid; }
td.v, td.c { text-align: center; }
td.v { white-space: nowrap; }
td.ex { font-family: "ExamLatin", "ExamMyeongjo"; letter-spacing: 0; text-align: left; }
.legend { font-size: 8.4pt; line-height: 14px; margin: 0.6mm 0 0; break-before: avoid; break-after: avoid; }
.quiz { break-inside: avoid; }
.bl { display: inline-block; border-bottom: 1lw solid #000; text-align: center; text-indent: 0; line-height: 1;
      padding: 0 1em 0.5pt; margin: 0 0.1em; }
.bl b { font-weight: 400; visibility: hidden; }
.teacher .bl b { visibility: visible; color: RED; }
.appendix h2 { color: RED; border-bottom-color: RED; }
.appendix h3 { font-size: 10.4pt; margin-top: 4mm; }
.appendix ol { color: RED; }
"""


def guide_page(body_html, teacher, font_dir, title, sub, chapters):
    """chapters: [(n, 이름)] 장마다 이름 붙은 쪽(page: chN)을 만들어 오른쪽 머리말에 장 이름을 둠"""
    named = "".join(
        f'section.c{n} {{ page: ch{n}; }}\n@page ch{n}:right {{ @top-right {{ content: "{ROMAN[n]} {name}"; }} }}\n'
        for n, name in chapters)
    page = GUIDE_PAGE.replace("TITLE", title) + named
    css = page + x2(font_faces(font_dir) + GUIDE_CSS.replace("SPOT", SPOT).replace("RED", RED))
    cls = "teacher" if teacher else ""
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}{' 교사용' if teacher else ' 학생용'}</title>
<style>{css}</style></head><body class="{cls}">
<div class="cover"><span class="subj">고3 영어</span><div><span class="sub">{sub}</span><h1>{title}</h1></div></div>
<div class="namebar">3학년 <span style="width:9mm"></span>반 <span style="width:9mm"></span>번 이름 <span style="width:27mm"></span></div>
{body_html}
</body></html>"""
