"""인쇄물 CSS, 쪽 배치 스크립트, 머리말과 꼬리말 템플릿

치수 근거는 DESIGN.md (2025학년도 수능과 2025년 7월 학평 원본 실측, EBS 해설지와 HWP 기본값)
"""
from pathlib import Path

RED = "#e00000"      # 교사용 정답 (HWP 학습지의 빨간 정답 관례)
SPOT = "#1b4a8c"     # 교재 별색, 단원 번호와 절 번호에만


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
@font-face{{font-family:"ExamGraphic";src:url({d}/UnGraphic.ttf);font-weight:400}}
"""


# ====================================================================== 시험지

EXAM_CSS = """
@page { size: A4; margin: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; background: #fff; color: #000; }
#src { position: absolute; left: -9999px; top: 0; }
.page { width: 210mm; height: 296.5mm; box-sizing: border-box; padding: 10mm 13mm 8mm; position: relative;
        page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }

/* 머리말 */
.hd { display: grid; grid-template-columns: 34mm 1fr 34mm; align-items: end; padding-bottom: 1.6mm;
      border-bottom: 0.9pt solid #000; }
.hd .subj { justify-self: start; font: 700 10pt "ExamGothic"; border: 0.45pt solid #000; border-radius: 1.6mm;
            padding: 0.6mm 2.4mm 0.4mm; }
.hd .ttl { text-align: center; font: 700 15pt "ExamGothic"; letter-spacing: 0.02em; }
.hd .no { justify-self: end; font: 700 21pt/1 "ExamLatin"; }
.hd.even .subj { grid-column: 3; justify-self: end; }
.hd.even .ttl { grid-column: 2; grid-row: 1; }
.hd.even .no { grid-column: 1; grid-row: 1; justify-self: start; }
.hd .tch { font: 400 8pt "ExamGothic"; border: 0.45pt solid #000; padding: 0.2mm 1.4mm; margin-left: 2mm;
           vertical-align: 3pt; letter-spacing: 0; }
.first .hd { grid-template-columns: 34mm 1fr 34mm; padding-bottom: 2mm; }
.first .hd .ttl { font: 700 20pt "ExamGothic"; }
.first .hd .sub { display: block; font: 400 9pt "ExamMyeongjo"; letter-spacing: 0; margin-bottom: 1.2mm; }
.first .hd .no { font-size: 26pt; }
.namebar { text-align: right; font: 400 9pt "ExamMyeongjo"; padding: 1.6mm 0 0; }
.namebar span { display: inline-block; border-bottom: 0.35pt solid #000; height: 3.6mm; vertical-align: -0.6mm; }

/* 본문 2단 */
.cols { position: absolute; left: 13mm; right: 13mm; bottom: 15mm; display: flex; gap: 0; }
.col { width: 88.3mm; position: relative; overflow: hidden; }
.rule { width: 7.4mm; position: relative; }
.rule::after { content: ""; position: absolute; left: 50%; top: 0; bottom: 0; border-left: 0.7pt solid #000; }
.ft { position: absolute; left: 0; right: 0; bottom: 6mm; text-align: center; font: 400 8.5pt "ExamLatin"; }

/* 안내 상자 (첫 쪽 왼쪽 단 위) */
.notice { border: 0.3pt solid #000; padding: 1.8mm 2.4mm; font: 400 8.6pt/1.55 "ExamMyeongjo"; text-align: justify;
          margin-bottom: 5mm; word-break: keep-all; }

/* 문항 */
.q { font: 400 9.5pt/18px "ExamLatin", "ExamMyeongjo", serif; }
.stem { font-family: "ExamMyeongjo", "ExamLatin", serif; font-size: 9.6pt; line-height: 18px; padding-left: 8.8pt;
        text-indent: -8.8pt; word-break: normal; text-align: left; }
.qno { font: 400 10.3pt "ExamNumber"; margin-right: 0.25em; }
.stem u { text-decoration-thickness: 0.45pt; text-underline-offset: 2.2pt; }
.src { font-size: 7.9pt; white-space: nowrap; }
.pt { white-space: nowrap; }
.passage { margin-top: 4pt; padding-left: 8.8pt; text-align: justify; hyphens: none; }
.passage p { margin: 0; text-indent: 8.2pt; }
.cn { font-family: "ExamMyeongjo"; font-size: 9.6pt; margin-right: 0.18em; }
.opt u { text-decoration-thickness: 0.37pt; text-underline-offset: 2.3pt; }
.nemo-label { margin-right: 0.15em; }
.nemo { display: inline-flex; flex-direction: column; vertical-align: middle; border: 0.5pt solid #000;
        padding: 0 1.2mm; line-height: 12px; margin: 1px 0; text-align: center; }
.foot { text-align: right; font-size: 8.6pt; line-height: 13px; margin-top: 1.4mm; }
.foot div { font-family: "ExamLatin", "ExamMyeongjo"; }
.box-choices { margin: 2.4mm 0 0 8.8pt; border-collapse: collapse; font-size: 9.3pt; line-height: 16px; }
.box-choices td { padding: 0 2.2mm 0 0; }
.box-choices tr:first-child td { text-align: center; }
.box-choices td.n { font-family: "ExamMyeongjo"; padding-right: 1.5mm; }
.box-choices td.dots { padding: 0 2mm 0 0; }
.key { visibility: hidden; margin-top: 1.6mm; padding-left: 8.8pt; font: 400 8.6pt/13px "ExamMyeongjo", "ExamLatin"; color: """ + RED + """; }

/* 교사용 표시 */
.teacher .key { visibility: visible; }
.teacher .opt.ans .cn { outline: 0.6pt solid """ + RED + """; outline-offset: 0.3pt; border-radius: 50%; color: """ + RED + """; }
.teacher .opt.ans u { color: """ + RED + """; }
.teacher .nemo .pick { color: """ + RED + """; }
.teacher .box-choices tr.ans td.n { outline: 0.6pt solid """ + RED + """; outline-offset: 0.3pt; border-radius: 50%; color: """ + RED + """; }
"""

EXAM_JS = """
(function () {
  const MM = 96 / 25.4;
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
            <div class="namebar">3학년 <span style="width:9mm"></span>반 <span style="width:9mm"></span>번 이름 <span style="width:27mm"></span></div>`;
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
  let cols = newPage(), ci = 0, used = 0, count = 0;
  const notice = book.dataset.notice;
  if (notice) { const d = document.createElement('div'); d.className = 'notice'; d.innerHTML = notice; cols[0].appendChild(d); used = d.getBoundingClientRect().height + 5 * MM; }
  const GAP = 9 * MM;
  for (const q of qs) {
    while (true) {
      const col = cols[ci];
      const H = col.getBoundingClientRect().height;
      col.appendChild(q);
      q.style.marginTop = '0px';
      const qh = q.getBoundingClientRect().height;
      let start = used === 0 ? 0 : Math.max(used + GAP, count === 1 ? H * 0.5 : used + GAP);
      if (count < 2 && start + qh <= H) {
        q.style.marginTop = (start - used) + 'px';
        used = start + qh; count += 1;
        break;
      }
      col.removeChild(q);
      if (used === 0) { col.appendChild(q); used = H; count = 2; break; }  // 단보다 긴 문항은 그대로 둠
      ci += 1; used = 0; count = 0;
      if (ci > 1) { cols = newPage(); ci = 0; }
    }
  }
  document.body.dataset.pages = pages.length;
  window.__done = true;
})();
"""


def exam_page(questions_html, n, teacher, font_dir, title, sub, notice):
    cls = "teacher" if teacher else ""
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>{title}{' (교사용)' if teacher else ''}</title>
<style>{font_faces(font_dir)}{EXAM_CSS}</style></head>
<body class="{cls}"><div id="src">{questions_html}</div>
<div id="book" data-title="{title}" data-sub="{sub}" data-teacher="{1 if teacher else 0}" data-notice="{notice}"></div>
<script>document.fonts.ready.then(() => {{ {EXAM_JS} }});</script>
</body></html>"""


# ====================================================================== 정답과 해설

ANS_CSS = """
@page { size: A4; margin: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; background: #fff; color: #000; font: 400 9.3pt/1.55 "ExamMyeongjo", "ExamLatin", serif; }
#src { position: absolute; left: -9999px; top: 0; width: 84mm; }
.page { width: 210mm; height: 296.5mm; box-sizing: border-box; position: relative; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.ahd { position: absolute; left: 16mm; right: 16mm; top: 12mm; display: flex; justify-content: space-between;
       font: 400 8pt "ExamGothic"; border-bottom: 1.08pt solid #000; padding-bottom: 1mm; }
.aft { position: absolute; left: 16mm; right: 16mm; bottom: 9mm; text-align: center; font: 400 8.5pt "ExamLatin";
       border-top: 0.6pt solid #000; padding-top: 0.5mm; }
.aft div { border-top: 0.25pt solid #000; padding-top: 1.6mm; }
.top { position: absolute; left: 16mm; right: 16mm; top: 20mm; }
.title { border: 0.35pt solid #000; outline: 0.35pt solid #000; outline-offset: 0.6mm; padding: 2.4mm 3mm; text-align: center;
         font: 700 14pt "ExamGothic"; margin: 1mm 1mm 4mm; }
.title small { display: block; font: 400 8.8pt "ExamMyeongjo"; margin-top: 0.8mm; }
.quick { border-top: 1.08pt solid #000; border-bottom: 1.08pt solid #000; padding: 2mm 0; margin-bottom: 1mm;
         display: grid; grid-template-columns: repeat(10, 1fr); row-gap: 1.2mm; font: 700 9.4pt "ExamLatin", "ExamMyeongjo"; }
.cols { position: absolute; left: 16mm; right: 16mm; bottom: 20mm; display: flex; }
.col { width: 84mm; overflow: hidden; }
.rule { width: 10mm; position: relative; }
.rule::after { content: ""; position: absolute; left: 50%; top: 0; bottom: 0; border-left: 0.35pt solid #000; }
.ex { margin-bottom: 3.4mm; text-align: justify; word-break: normal; }
.ex-head { margin-bottom: 0.6mm; }
.ex-head b { font: 400 10.3pt "ExamNumber"; }
.ex-head .src { font-size: 8.4pt; }
.ex .line { padding-left: 12pt; text-indent: -12pt; }
.ex .lbl { white-space: nowrap; }
.ex i { font-family: "ExamLatin"; font-style: italic; }
"""

ANS_JS = """
(function () {
  const MM = 96 / 25.4;
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
      // 긴 해설은 줄 단위로 다음 단에 이어 씀 (머리와 최소 두 줄은 남김)
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
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title} 정답과 해설</title>
<style>{font_faces(font_dir)}{ANS_CSS}</style></head><body>
<div id="first" hidden><div class="title">{title} 정답과 해설<small>{sub}</small></div><div class="quick">{quick_html}</div></div>
<div id="src">{items_html}</div><div id="book" data-title="{title}"></div>
<script>document.fonts.ready.then(() => {{ {ANS_JS} }});</script>
</body></html>"""


# ====================================================================== 개념 정리 교재

GUIDE_CSS = """
@page { size: A4; margin: 24mm 20mm 20mm; }
@page :left { margin-left: 18mm; margin-right: 22mm; }
@page :right { margin-left: 22mm; margin-right: 18mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; background: #fff; color: #000; font: 400 10.4pt/1.62 "ExamMyeongjo", "ExamLatin", serif;
       text-align: justify; word-break: normal; }
h1, h2, h3, h4, th { word-break: keep-all; }
.cover { border-bottom: 0.9pt solid #000; padding-bottom: 2mm; display: grid; grid-template-columns: auto 1fr; align-items: end; gap: 4mm; }
.cover .subj { font: 700 10pt "ExamGothic"; border: 0.45pt solid #000; border-radius: 1.6mm; padding: 0.6mm 2.4mm 0.4mm; }
.cover h1 { margin: 0; font: 700 19pt "ExamGothic"; letter-spacing: 0.02em; }
.cover .sub { font: 400 9pt "ExamMyeongjo"; display: block; margin-bottom: 1mm; }
.namebar { text-align: right; font: 400 9pt "ExamMyeongjo"; padding: 1.6mm 0 3mm; }
.namebar span { display: inline-block; border-bottom: 0.35pt solid #000; height: 3.6mm; vertical-align: -0.6mm; }
h2 { break-before: page; font: 700 15.5pt "ExamGothic"; margin: 0 0 4mm; padding-bottom: 1.6mm;
     border-bottom: 1.1pt solid """ + SPOT + """; }
.cover + .namebar + h2, h2.first { break-before: auto; }
h2 .num { font: 700 22pt/1 "ExamLatin"; color: """ + SPOT + """; margin-right: 2.4mm; vertical-align: -1pt; }
h3 { font: 700 11.6pt "ExamGothic"; margin: 7mm 0 1.6mm; break-after: avoid; }
h3 .num { color: """ + SPOT + """; margin-right: 1.2mm; }
h4 { font: 700 9.8pt "ExamGothic"; margin: 3.2mm 0 1mm; break-after: avoid; }
h4::before { content: "■ "; font-size: 8pt; vertical-align: 0.6pt; }
p { margin: 0.8mm 0; }
ul, ol { margin: 0.6mm 0 1.4mm; padding-left: 5mm; }
li { margin: 0.3mm 0; }
ul { list-style: none; }
ul > li { position: relative; }
ul > li::before { content: "◦"; position: absolute; left: -4mm; }
ul ul > li::before { content: "-"; left: -3.4mm; }
ol { padding-left: 5.4mm; }
strong { font-weight: 400; text-decoration: underline; text-decoration-thickness: 0.37pt; text-underline-offset: 2.2pt; }
.rulebox { border: 0.35pt solid #000; padding: 1.6mm 3.2mm 1.8mm; margin: 2.6mm 0 2mm; break-inside: auto; }
.rulebox h4 { margin-top: 0.6mm; }
.tw { margin: 1.6mm 0 3mm; }
table { width: 100%; border-collapse: collapse; font-size: 8.7pt; line-height: 1.45; border-top: 0.71pt solid #000;
        border-bottom: 0.71pt solid #000; text-align: left; }
th { font: 700 8.4pt "ExamGothic"; background: #e6e6e6; padding: 1mm 1.4mm; border-bottom: 0.34pt solid #000; white-space: nowrap; }
td { padding: 0.9mm 1.4mm; border-bottom: 0.34pt solid #000; vertical-align: top; }
tr { break-inside: avoid; }
td.v { text-align: center; white-space: nowrap; }
.tnote { font-size: 8.6pt; margin: 2mm 0 0.6mm; }
.bl { display: inline-block; border-bottom: 0.42pt solid #000; text-align: center; text-indent: 0; line-height: 1.2;
      padding: 0 1em; margin: 0 0.1em; }
.bl b { font-weight: 400; visibility: hidden; }
.teacher .bl b { visibility: visible; color: """ + RED + """; }
.answers { visibility: hidden; border-top: 0.34pt solid #000; padding-top: 1mm; margin: 1.6mm 0 2mm; font-size: 9.6pt; }
.answers ol { margin: 0; }
.answers-head { font: 700 9pt "ExamGothic"; }
.teacher .answers { visibility: visible; color: """ + RED + """; border-color: """ + RED + """; }
"""


def guide_page(body_html, teacher, font_dir, title, sub):
    cls = "teacher" if teacher else ""
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}{' (교사용)' if teacher else ''}</title>
<style>{font_faces(font_dir)}{GUIDE_CSS}</style></head><body class="{cls}">
<div class="cover"><span class="subj">고3 영어</span><div><span class="sub">{sub}</span><h1>{title}</h1></div></div>
<div class="namebar">3학년 <span style="width:9mm"></span>반 <span style="width:9mm"></span>번 이름 <span style="width:27mm"></span></div>
{body_html}
</body></html>"""


def guide_header_footer(title, teacher):
    tag = ("<span style=\"border:0.45pt solid #000;padding:0 1.4mm;font-size:7.6pt\">교사용</span>" if teacher else "")
    header = f"""<div style="width:100%;margin:0 20mm;padding-top:10mm;font:400 7.8pt 'UnDotum';display:flex;justify-content:space-between;
      align-items:flex-end;border-bottom:0.35pt solid #000;padding-bottom:1mm"><span>{title}</span>{tag}</div>"""
    footer = """<div style="width:100%;text-align:center;font:400 8.5pt 'Liberation Serif';margin-bottom:8mm">- <span class="pageNumber"></span> -</div>"""
    return header, footer, None
