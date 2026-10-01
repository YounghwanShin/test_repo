# 영어 29번 어법 인쇄물 디자인 명세

- 대상 산출물은 A4 PDF 5종
  - 영어29번_어법기출73제_문제지.pdf, 학생용 기출 시험지
  - 영어29번_어법기출73제_교사용.pdf, 정답 표시 시험지
  - 영어29번_어법기출73제_정답과해설.pdf, EBS 해설지 형식의 정답과 해설
  - 영어29번_어법개념정리_학생용.pdf, 빈칸 교재
  - 영어29번_어법개념정리_교사용.pdf, 빈칸 답과 확인 문제 정답을 빨강으로 표시한 교재
- 조판 방식은 HTML과 CSS를 Chromium(playwright)으로 인쇄하는 방식
- 디자인 기준은 실제 수능 문제지, 교육청 학평 문제지, EBS 해설지, 교사 학습지에서 측정한 관례. 실물에서 관찰하지 못한 장식은 넣지 않음
- 기준일 2026년 10월 1일. 수치 단위는 pt(1pt = 0.3528mm)와 mm

## 1. 조사 요약

### 1.1 조사 범위

- 웹 자료는 AI 생성 디자인과 AI 문체의 특징을 다룬 글과 공개 저장소 20여 건, 평가원 양식과 HWP 기본값 자료
- 공개 저장소 분석(git clone)
  - anthropics/skills의 frontend-design, nexu-io/open-design의 anti-ai-slop.md, pbakaus/impeccable의 craft-floor.md
  - softaworks/agent-toolkit의 Wikipedia 'Signs of AI writing' 정리본, epoko77-ai/im-not-ai의 한국어 AI 티 85개 분류
  - handaram-dev/exam-hwpx-skill의 평가원 양식 hwpx
- 실물 측정(PyMuPDF로 글꼴, 크기, 좌표, 선 굵기 추출)
  - 2025학년도 수능 영어 원본 PDF 1, 4, 5, 8쪽. A3 2단, 생성 프로그램 Hancom PDF 2022
  - 2025년 7월 고3 학평 영어 1, 4, 5쪽. HWP 2022로 제작
  - EBS 2025년 6월 모평 영어 정답과 해설. A4, HWP 2022로 제작
  - 상용 학원 워크북 EXAM4YOU. A4, HWP로 제작
- 글꼴 확보와 Chromium PDF 임베드 시험(pdffonts 검사)
- 명세 작성 중 추가 검증(Chromium 141, playwright 번들)
  - @page 여백 상자의 웹 글꼴 임베드, 홀짝 쪽 머리말 반전, 머리말 아래 7mm 간격
  - visibility:hidden으로 숨긴 빈칸 답의 PDF 텍스트 추출 여부
  - 별도 family로 선언한 원문자용 글꼴(unicode-range)의 동작
  - string-set 지원 여부(미지원 확인)

### 1.2 AI 티 특징과 처리 방법

- AI 티는 개별 장식에서 생기지 않고 학습 데이터의 평균값(Tailwind indigo-500, Inter, shadcn 카드)이 여러 개 겹쳐서 생김. 여러 출처의 판단이 같음
  - Adrian Krebs의 Show HN 페이지 1,590개 채점에서 22%가 4개 이상 패턴에 걸림
- '종이 신문 느낌'도 요즘 AI가 자주 고르는 기본값. frontend-design 스킬은 크림 배경, 세리프, 테라코타, 헤어라인, radius 0, 빽빽한 단, 모노스페이스 라벨, 틴트 블랙을 AI가 몰리는 조합으로 지목함
  - 따라서 2단과 가는 괘선은 수능 실물 측정값으로만 쓰고, 그 위에 덧입히는 요소는 모두 뺌

| 특징 | 처리 방법 | 근거 |
| --- | --- | --- |
| 보라와 인디고 강조색(#6366f1, #4f46e5, #8b5cf6 등), 파랑에서 보라로 가는 그라데이션, 그라데이션 글자 | 먹 1도. 교재만 남색 별색 1도. 그라데이션 불허 | dev.to alanwest, impeccable.style/slop, 925studios |
| 모든 요소에 같은 radius와 회색 그림자 | box-shadow 0, radius 0. 예외는 과목 상자와 교사용 정답 원 | open-design anti-ai-slop.md, jkkms/ppt-deck |
| Inter, Roboto, system-ui, 한국어 Pretendard와 Noto Sans 단독 본문 | 본문은 명조(Batang), 영어는 Times 호환 글꼴(Liberation Serif). 고딕은 제목, 머리말, 표 머리칸에만 | uxskill.laithjunaidy.com, tali.kr |
| 같은 크기 둥근 카드의 3개 반복, 카드 안 카드, 상자 왼쪽 색 막대 | 상자는 교재의 판단 규칙 상자 1종. 테두리 없는 평망점 사각형 | adriankrebs.ch, 925studios |
| 이모지와 기호 아이콘(반짝이, 로켓, 전구, 체크, 경고 표시), 별점 | 0개. 화살표는 고쳐 쓰기 표기(틀린 형태 → 고친 형태)에만 허용 | open-design anti-ai-slop.md, im-not-ai |
| 알약 배지, 색 점, 제목 위 영문 대문자 eyebrow 라벨, 장식용 01/02/03 번호 | 불허. 번호는 실제 순서(문항 번호, 절 번호)에만 | impeccable craft-floor.md, adriankrebs.ch |
| 큰 숫자와 작은 라벨의 통계 띠, 근거 없는 수치(빈출도 별점, 지어낸 정답률) | 불허. 데이터에서 센 출제 횟수만 기재 | developersdigest.tech, 925studios |
| 전부 가운데 정렬, 큰 표지와 빈 여백 | 본문 양쪽 정렬, 제목 왼쪽 정렬. 가운데 정렬은 시험지 제목, 쪽 번호, 표 머리칸에만. 별도 표지 없음 | tali.kr, chatslide.ai |
| 크림 종이(#F4F1EA), 테라코타(#D97757), 틴트 블랙(#111), 모노스페이스 라벨, 가운뎃점으로 이은 메타 정보 | 종이 #fff, 먹 #000. 모노스페이스와 가운뎃점 불허 | anthropics/skills frontend-design |
| 문장마다 굵은 글씨, 굵은 라벨 뒤 콜론과 설명이 오는 불릿, 콜론 부제 제목 | 본문 볼드 0회, 강조는 밑줄. 볼드는 문항 번호와 제목에만. 제목은 명사구 | Wikipedia Signs of AI writing, pangram.com |
| em dash 남발(사람은 약 500단어에 1회, AI는 50~80단어에 1회), 무엇이든 셋씩 짝지은 나열 | 한국어 설명문 em dash 0회. 기출 원문의 줄표는 원문 표기 유지 | Wikipedia Signs of AI writing, im-not-ai C-2, C-5 |
| '핵심 요약', 'Key takeaway', '한눈에 보기', '완벽 정복', '꿀팁' 상자의 반복 | 불허. 단원 끝 요약 상자 없음 | im-not-ai J-1, J-3, brunch @webtutor |
| 마크다운 잔재(**, #) | PDF 텍스트에서 **와 # 0건 검사 | softaworks signs-of-ai-writing.md |
| 쪽마다 같은 제목 위치와 크기 | 시험지는 쪽 번호와 과목 상자를, 교재는 머리말을 홀짝 쪽에서 좌우 반전 | 2slides.com, 수능 원본 관찰 |
| PDF 메타데이터의 HeadlessChrome, Skia/PDF | creator와 producer를 빈 문자열로 설정. 다른 프로그램 이름 위조 불허 | 실물 PDF는 Hwp 2022와 Hancom PDF로 기록됨(측정) |

- 사람이 만든 한국 시험지와 학습지에서 관찰한 요소는 살림
  - 쪽 번호와 머리말의 바깥쪽 비대칭, 문항 길이에 따라 들쭉날쭉한 단 아래 빈 공간
  - 문항마다 출처 표기, 학년, 반, 번호, 이름 칸, '- 3 -' 쪽 번호
  - 원문자, 대괄호 라벨, ※와 ◦ 같은 HWP식 기호
  - 기출 원문의 따옴표와 줄표 보존, 양쪽 정렬로 벌어진 단어 간격

### 1.3 수능 문제지 측정값

- 대상은 2025학년도 수능 영어 29번(5쪽). PDF 판형 A3(842×1191pt), 실제 문제지 판형은 사륙판 8절(272×394mm)
- A4 적용 배율은 0.78(영어 9.5pt ÷ 12.18pt). A3에서 A4로 줄이는 0.707배를 쓰면 영어가 8.6pt로 작아짐

| 요소 | 원본 측정값 | A4 적용값 |
| --- | --- | --- |
| 영어 지문 | Times New Roman 12.18pt | 9.5pt |
| 발문 | 신명 중명조 11.21pt | 8.7pt(영어의 0.92배) |
| 문항 번호 | 한양견명조 13.16pt | 10.3pt |
| 원문자 ①~⑤ | 한양신명조 11.21pt | 8.7pt |
| 각주 | 영어 11.0pt, 한글 10.1pt | 8.6pt, 7.9pt |
| 줄 간격(기준선 사이) | 영어 17.25pt, 발문 17.8pt | 13.5pt(18px) |
| 단 폭, 단 사이 | 321.7pt, 27pt | 88.4mm, 7.4mm |
| 지문 왼쪽 들여쓰기, 첫 줄 추가 들여쓰기 | 11.3pt, 10.5pt | 8.8pt, 8.2pt |
| 발문 마지막 줄과 지문 첫 줄의 기준선 사이 | 22.6pt | 17.6pt |
| 원문자와 밑줄 낱말 사이 | 약 2.4pt | 0.2em |
| 밑줄 | 0.48pt, 기준선 아래 2.9pt | 0.4pt, offset 2.2pt |
| 머리 가로줄 | 1.14pt | 0.85pt |
| 단 구분선 | 0.9pt | 0.71pt |
| 상자 테두리 | 0.36pt | 0.34pt |
| 표 위아래 줄, 안쪽 줄 | 0.72pt, 0.36pt | 0.71pt, 0.34pt |

- 관찰 관례
  - 2단. 단마다 독해 문항 2개이고 둘째 문항은 단 높이 약 50% 지점에서 시작함. 남는 자리는 풀이 여백
  - 지문은 양쪽 정렬이라 단어 간격이 벌어진 줄이 있음
  - 원문자는 한글 글꼴로 조판되고 밑줄은 원문자 뒤 낱말에만 그어짐
  - 발문 강조는 굵기 대신 밑줄('틀린')
  - 각주는 지문 아래 오른쪽 정렬. 여러 개면 '* taint: 더럽히다  ** altruistic: 이타주의의'처럼 같은 줄에 이어 쓰고 넘치면 다음 줄로 넘김. 별표 뒤 공백 1칸
  - 줄표 ―는 한글 명조로 조판되고 앞뒤에 공백이 있음
  - 큰 쪽 번호는 바깥 위 모서리(홀수 쪽 오른쪽, 짝수 쪽 왼쪽)
  - 색은 먹 1도

### 1.4 학평, 해설지, 학습지 관례

- 2025년 7월 학평(HWP 2022)
  - 모든 글자가 한컴바탕. 문항 번호 13.4pt, 발문 11.2pt, 지문 11.3pt, 줄 간격 약 153%
  - 단 구분선 0.36pt, 머리 괘선 1.44pt
  - 각주는 '* ubiquity: 도처에 있음  ** supersede: 대체하다'처럼 공백 2칸으로 이어 씀
- EBS 정답과 해설(HWP 2022, A4)
  - 함초롬바탕 11pt, 줄 간격 160%(기준선 사이 17.6pt), 머리 괘선 1.08pt, 꼬리 0.6pt와 0.24pt 이중선, 가운데 쪽 번호
  - 첫 쪽 제목 상자 아래 두 괘선 사이에 빠른 정답표. '01. ③' 형식으로 줄마다 10개
  - 문항마다 '29. [출제 의도] 문법성 판단', [해석], [풀이], [Words and Phrases] 순서. 라벨은 대괄호에 보통 굵기, 볼드는 문항 번호뿐
  - [풀이]는 정답 선지를 먼저 쓰고 나머지 선지를 짧게 설명함
  - 색은 제목의 '영어' 두 글자 파랑뿐
- 학원 워크북 EXAM4YOU
  - 맑은고딕 10pt, 줄 간격 160%, 고르기형은 [A / B], 고쳐 쓰기는 '(1) ____ → ____'
  - 정답은 책 뒤에 2단으로 모음
- 교사 학습지(sciencelove.com/2469)
  - 같은 파일에 정답을 빨간 글씨로 넣고 학생용 인쇄 때 흰색으로 바꿈. 학생용에는 정답 자리가 빈칸과 빈 공간으로 남음
- HWP 기본값
  - A4, 여백 위 20, 아래 15, 좌우 30mm, 머리말과 꼬리말 각 15mm
  - 함초롬바탕 10pt, 줄 간격 160%, 표 테두리 0.12mm(0.34pt)
  - 선 굵기 단계 0.12, 0.25, 0.3, 0.4, 0.5mm

### 1.5 조사 결과 사이의 차이와 결정

| 항목 | 조사별 제안 | 결정과 이유 |
| --- | --- | --- |
| 한글 본문 글꼴 | Noto Serif KR, 은바탕(GPL-2), Batang(HanYang I&C, OFL) | Batang. 수능 발문 글꼴(한양신명조, 신명조)과 같은 한양 계열이고 OFL이라 임베드와 재배포 조건이 명확함. 은바탕에 없는 ◦도 들어 있음 |
| 영어 글꼴 | 세 조사 모두 Liberation Serif | Liberation Serif. Times New Roman과 글자 폭이 같아 줄바꿈이 원본과 같음 |
| 시험지 영어 크기 | 9.6pt, 9.5pt, 10.5pt | 9.5pt. 단 폭 88.4mm에서 지문 폭 25.45em으로 수능(25.48em)과 같고, 2025 수능 29번 15줄 중 14줄의 줄바꿈이 원본과 같음(조사 단계 검증). 10.5pt는 A4 2단에 들어가지 않음 |
| 단 구분선 | 0.5pt, 0.7pt | 0.71pt. HWP 0.25mm이고 수능 0.9pt의 0.78배 |
| 시험지 여백 | 13~20mm, 위 10mm와 좌우 13mm | 좌우 12.9mm(단 폭에서 역산), 위 10mm, 단 아래 15mm |
| 정답 숨김 | display:none 또는 DOM 제거, visibility:hidden | visibility:hidden. 학생용과 교사용의 줄바꿈과 쪽 배치가 자동으로 같아짐. 숨긴 글자가 PDF 텍스트로 추출되지 않음을 pdftotext로 확인(조사 단계, 명세 작성 중 각 1회). color:transparent와 흰 글자는 불허 |
| 교재 번호 체계 | Ⅰ. 다음 01, HWP 개요 Ⅰ. 다음 1. 다음 가. | 원고 번호(2, 2.1) 유지. 원고 본문에 '2.3 수동태 불가', '1.3 3단계' 같은 절 번호 참조가 있어 번호를 바꾸면 참조가 어긋남 |
| 교재 색 | 먹과 별색 #0a5aa8, 먹 1도에 필요하면 남색 | 먹과 남색 별색 #1b4a8c. 학교 흑백 복사에서 진회색으로 남는 명도 |
| 교재 머리말 | 바깥쪽 단원명, HWP식 아래 가운데 쪽 번호 | 바깥쪽 위 자료 이름, 아래 가운데 '- 6 -'. 단원명을 쪽마다 바꾸는 string-set은 Chromium 141에서 미지원(명세 작성 중 확인) |
| 해설의 [해석], [Words and Phrases] | EBS 형식대로 포함 | 제외. questions.json에 검증된 번역과 어휘 데이터가 없고 지어낸 번역은 오역 위험이 있음. 대신 [관련 개념]으로 교재 절 번호 연결 |
| 교사용 시험지 | 해설지만, 정답 표시 시험지 추가 | 둘 다. 정답 표시 시험지와 정답과 해설을 별도 PDF로 나눔 |
| 머리말 글꼴 공급 | 머리말 템플릿과 시스템 글꼴 | @page 여백 상자와 document.fonts.load 선로딩. 시스템 글꼴 의존 제거(명세 작성 중 확인, Noto Sans KR이 CID TrueType으로 임베드됨) |
| 각주 배치 | 줄마다 1개(현행 출력) | 같은 줄에 이어 쓰기. 수능과 학평 원본 모두 이어 씀 |

## 2. 공통 규칙

### 2.1 판형

- A4 세로 210×297mm. 단면 인쇄와 양면 인쇄 모두 허용
- 학교 흑백 복사기 출력을 전제로 함. 색은 회색으로 바뀌어도 읽히는 명도로 설정
- 별도 표지와 목차 쪽 없음. 첫 쪽 위 머리말에 제목, 부제, 이름 칸 배치

### 2.2 여백

| 산출물 | 위 | 아래 | 왼쪽 | 오른쪽 |
| --- | --- | --- | --- | --- |
| 시험지 | 10mm(머리말 위 끝) | 15mm(단 아래 끝), 쪽 번호는 쪽 아래 7mm | 12.9mm | 12.9mm |
| 정답과 해설 | 24mm | 20mm | 16mm | 16mm |
| 교재 홀수 쪽 | 22mm | 18mm | 22mm(제본 쪽) | 18mm |
| 교재 짝수 쪽 | 22mm | 18mm | 18mm | 22mm(제본 쪽) |

### 2.3 글꼴 파일과 용도

- 파일 위치는 grammar29/print/fonts/. 원본은 작업 스크래치패드의 fonts/ 폴더이고 각 글꼴의 OFL.txt를 함께 복사함
- fonts/는 용량이 약 34MB라 .gitignore에 추가하고, 출처와 커밋은 print/README.md에 기록

| CSS family | 파일 | weight | 용도 | 라이선스 |
| --- | --- | --- | --- | --- |
| Latin Serif | LiberationSerif-Regular.ttf | 400 | 영어 지문, 영어 예문, 숫자, 쪽 번호, 한국어 문장 속 라틴 문자 | OFL 1.1 |
| Latin Serif | LiberationSerif-Bold.ttf | 700 | 문항 번호, 빠른 정답표 번호, 대단원 번호, 큰 쪽 번호 | OFL 1.1 |
| Latin Serif | LiberationSerif-Italic.ttf | 400 italic | 기출 원문의 이탤릭 | OFL 1.1 |
| KR Serif | Batang-Regular.ttf(HanYang I&C, google/fonts ofl/batang) | 400 | 한글 본문, 발문, 해설, 빈칸 답 | OFL 1.1 |
| KR Serif | NotoSerifKR-Bold.ttf(정적 TTF) | 700 | 굵은 한글 명조 예비. 기본 조판에서는 쓰지 않음 | OFL 1.1 |
| KR Mark | Batang-Regular.ttf, unicode-range 제한 | 400 | ①~⑤, ㉠~㉢, ※, ○, ×, ■, ◦, ― | OFL 1.1 |
| KR Gothic | NotoSansKR-Medium.ttf(정적 TTF) | 500 | 머리말, 표 머리칸, 교사용 표시 | OFL 1.1 |
| KR Gothic | NotoSansKR-Bold.ttf(정적 TTF) | 700 | 제목, 소제목, 과목 상자 | OFL 1.1 |

- 시험지 전용 family
  - KR Serif Exam과 KR Mark Exam은 같은 Batang 파일에 size-adjust 92%를 준 선언
  - 같은 pt로 선언한 영어와 한글의 크기 비율이 수능(11.21 ÷ 12.18 = 0.92)과 같아짐
- 글꼴 스택
  - 교재와 해설 본문은 "KR Mark", "Latin Serif", "KR Serif"
  - 시험지는 "KR Mark Exam", "Latin Serif", "KR Serif Exam"
  - 제목, 머리말, 표 머리칸은 "KR Gothic"
- 규칙
  - 영문과 한글을 같은 family 이름에 unicode-range로 나눠 선언하지 않음. 나중에 선언한 한글 글꼴이 영문까지 가져감(조사 단계 확인)
  - KR Mark는 이름이 다른 별도 family라 위 문제가 생기지 않음(명세 작성 중 확인)
  - body에 `font-synthesis: none` 필수. 선언하지 않은 굵기는 가짜 볼드가 되고 Type 3로 임베드됨
  - Batang은 Regular만 있으므로 KR Serif 글자에 굵기 700 지정 불허. 빨간 답, 밑줄 강조 모두 400
  - CFF 기반 .otf(Noto CJK SubsetOTF, KoPubWorld, TeX Gyre)와 가변 글꼴 [wght].ttf 불허. Chromium PDF에서 Type 3로 임베드됨
  - 나눔명조와 나눔고딕 불허(①~⑤ 없음), KoPub Batang 불허(em dash와 en dash 글리프 없음)
  - 함초롬바탕 불사용. 수정 금지와 상업적 배포 금지 조건이 있어 OFL 글꼴로 대체

### 2.4 크기 체계

- 단위 pt. 시험지의 '선언'은 CSS font-size 값이고 한글은 size-adjust 92%로 0.92배 크기로 렌더링됨

| 요소 | 시험지 | 정답과 해설 | 교재 |
| --- | --- | --- | --- |
| 첫 쪽 제목 | 고딕 700, 20 | 고딕 700, 14(제목 상자) | 고딕 700, 19 |
| 부제 | 명조 9 | 명조 8.8 | 명조 9 |
| 이어지는 쪽 머리 제목 | 고딕 700, 15 | 고딕 500, 8 | 고딕 500, 7.8 |
| 큰 쪽 번호 | Latin 700, 21(첫 쪽 26) | 없음 | 없음 |
| 아래 쪽 번호 '- n -' | Latin 8.5 | Latin 8.5 | Latin 8.5 |
| 과목 상자 '고3 영어' | 고딕 700, 10 | 없음 | 고딕 700, 10 |
| 이름 칸 | 명조 9 | 없음 | 명조 9 |
| 안내 상자 | 선언 9.4(한글 8.6) | 없음 | 없음 |
| 문항 번호 | Latin 700, 10.3 | Latin 700, 10.3 | 없음 |
| 발문 | 선언 9.5(한글 8.7) | 없음 | 없음 |
| 영어 지문, 예문 | 9.5 | 9.5(인용 낱말) | 10 |
| 원문자 | 선언 9.5(8.7) | 9.5 | 10 |
| 출처 표기 | 선언 8.6(한글 7.9) | 8.4 | 8.5(확인 문제) |
| 각주 | 선언 8.6(한글 7.9) | 없음 | 없음 |
| 본문 | 없음 | 9.5 | 10 |
| 대단원 번호와 제목 | 없음 | 없음 | Latin 700 22, 고딕 700 15.5 |
| 단원 제목 | 없음 | 없음 | 고딕 700, 11.5 |
| 소제목 | 없음 | 없음 | 고딕 700, 9.8 |
| 표 본문, 머리칸 | 없음 | 없음 | 8.7, 고딕 500 8.4 |
| 표 주석 | 없음 | 없음 | 8.6 |

### 2.5 줄 간격

- line-height는 px 정수로 지정
  - 소수 pt(예 13.6pt)는 7줄마다 0.75pt씩 줄 간격이 튐. 18px로 지정하면 33줄 모두 13.5pt(조사 단계 검증)

| 자리 | line-height | pt 환산 | 글자 크기 대비 |
| --- | --- | --- | --- |
| 시험지 지문, 발문, 네모형 선택지 | 18px | 13.5pt | 영어 9.5pt의 1.42배(수능 1.414배) |
| 시험지 안내 상자 | 17px | 12.75pt | 한글 8.6pt의 148% |
| 시험지 각주, 교사용 정답 줄 | 14px | 10.5pt | 8.6pt의 122% |
| 해설 본문 | 20px | 15pt | 9.5pt의 158%(EBS 160%) |
| 교재 본문 | 21px | 15.75pt | 10pt의 158%(HWP 기본 160%) |
| 교재 표 | 17px | 12.75pt | 8.7pt의 147% |

- 자간은 0. 예외는 시험지와 교재 첫 쪽 제목 0.02em
- 장평 조정 없음. 평가원 문서 설정(장평 95%, 자간 -5%)은 CSS에서 글자 모양을 바꾸는 변형이 필요해 적용하지 않음

### 2.6 선 굵기

- HWP 선 굵기 단계만 사용. 0.5px, 1px 같은 화면 단위 불허

| HWP | pt | 쓰는 자리 |
| --- | --- | --- |
| 0.12mm | 0.34pt | 상자 테두리, 표 안쪽 가로줄, 교재 머리말 밑줄, 해설 단 구분선, 이름 칸 밑줄 |
| 글자 밑줄 | 0.4pt | 지문 밑줄, 발문 '틀린' 밑줄, 빈칸 밑줄, 교재 강조 밑줄. 수능 0.48pt의 0.78배 |
| 0.25mm | 0.71pt | 시험지 단 구분선, 표 위아래 줄 |
| 0.3mm | 0.85pt | 시험지 머리 가로줄 |
| 0.4mm | 1.13pt | 해설 머리줄, 빠른 정답표 위아래 줄, 교재 대단원 제목 밑줄(별색) |
| 이중선 | 0.6pt와 0.25pt, 간격 약 0.5mm | 해설 꼬리줄(EBS 측정) |
| 정답 원 | 0.6pt 빨강 | 교사용 시험지 정답 원문자 |

### 2.7 색

| 이름 | 값 | 쓰는 자리 | 산출물 |
| --- | --- | --- | --- |
| 먹 | #000 | 글자와 선 전부 | 5종 |
| 종이 | #fff | body 배경 | 5종 |
| 먹 10% | #e6e6e6 | 표 머리칸 바탕 | 교재 |
| 별색 | #1b4a8c | 대단원 번호, 대단원 제목 밑줄, 단원 번호, 판단 규칙 상자 제목 | 교재 2종 |
| 별색 12% 망점 | #e4e9f1 | 판단 규칙 상자 바탕 | 교재 2종 |
| 정답 빨강 | #e00000 | 빈칸 답, 확인 문제 정답, 시험지 정답 표시 | 교사용 2종 |

- 학생용 시험지와 정답과 해설은 먹 1도. 교사용 시험지는 먹과 빨강
- 학생용 교재는 먹과 별색. 빨강 0회
- 흑백 변환 명도는 #1b4a8c 약 26%(진회색), #e4e9f1 약 91%(옅은 회색). 흑백 복사에서 상자 바탕과 글자가 모두 남음
- 그라데이션, 그림자, 투명도 불허

### 2.8 쪽 번호와 머리말

- 시험지
  - 쪽 바깥 위 모서리에 큰 쪽 번호, 쪽 아래 가운데에 '- 3 -'
  - 홀수 쪽과 짝수 쪽에서 쪽 번호와 과목 상자 좌우 반전
- 정답과 해설
  - 머리 왼쪽에 자료 이름, 오른쪽에 '교사용', 아래 1.13pt 줄
  - 꼬리 이중선 아래 가운데 '- 1 -'. 해설 부분은 쪽 번호를 1부터 다시 매김(별책 관례)
- 교재
  - 바깥쪽 위에 자료 이름, 안쪽 위에 '교사용'(교사용만), 아래 0.34pt 줄
  - 아래 가운데 '- 6 -'. 첫 쪽은 머리말 없음

### 2.9 기호와 표기

- 문장 앞 기호는 ◦(1단계 불릿), -(2단계 불릿), ■(소제목), ※(안내)만 사용
- 화살표는 고쳐 쓰기 표기에만 허용. 예 'knows → know'
- 판정 기호는 ○와 ×(KR Mark). 영문자 O와 X로 쓰지 않음
- 원문자 ①~⑤는 선지 번호 전용. 풀이 순서는 1. 2. 3.
- 출처는 시험지와 해설에서 대괄호 [2026학년도 수능], 교재 본문에서 원고 표기(괄호)
- 기출 원문의 따옴표, 줄표, 하이픈, 이탤릭은 원문 표기 유지
- 한국어 설명문(안내문, 해설, 교재 본문)에는 em dash와 가운뎃점 0회
  - questions.json 해설 8곳에 가운뎃점으로 이은 표기('수동'과 '완료', '주어'와 '목적어' 등)가 있어 빌드 전에 '와', '과'나 쉼표로 고침
- 해설 문체는 '-다'로 통일. '-입니다'로 끝난 해설 문장은 빌드 전 데이터에서 고침

### 2.10 금지 목록

- 색
  - 보라와 인디고 계열, 그라데이션, 크림 종이, 테라코타, 틴트 블랙
  - 교사용 빨강을 뺀 셋째 색
- 상자
  - box-shadow, border-radius(과목 상자 1.6mm와 교사용 정답 원 제외)
  - 카드 안 카드, 2px 이상 색 막대, 같은 크기 상자의 격자 반복
- 장식
  - 이모지, 아이콘, 별점, 알약 배지, 색 점, 물결과 도형 배경, 장식용 01/02/03
- 제목과 라벨
  - 콜론 부제, 영문 대문자 eyebrow, Step, Point, Tip, Key Point 같은 영어 템플릿 라벨
  - 모노스페이스 글꼴, 가운뎃점 메타
- 글
  - 본문 볼드, 굵은 라벨 뒤 콜론과 설명이 오는 불릿, em dash
  - '핵심 요약', '한눈에 보기', '완벽 정복', '꿀팁', 홍보 문구, 근거 없는 수치
- 정렬과 여백
  - 전부 가운데 정렬, 큰 빈 표지, hero 영역
- 글꼴
  - Inter, Roboto, Pretendard, system-ui, Noto Sans 본문, 가짜 볼드, Type 3 임베드
- 시험 기관 형식 복제
  - 평가원 저작권 문구, '대학수학능력시험 문제지', '영어 영역', '홀수형', '제3교시'
  - 사선 쪽 번호 상자, '확인 사항' 상자
  - 형식(2단, 번호, 밑줄, 원문자)만 빌리고 기관 명의는 쓰지 않음
- 정답 숨김 방식
  - color:transparent, 흰 글자, 글자 위 흰 상자 덮기
- 메타데이터 위조
  - Creator나 Producer에 Hwp, Hancom 등 다른 프로그램 이름 기입

### 2.11 파일 이름과 메타데이터

| 파일 | HTML title과 PDF Title | 예상 쪽수 |
| --- | --- | --- |
| 영어29번_어법기출73제_문제지.pdf | 영어 29번 어법 기출 문제지 | 19 |
| 영어29번_어법기출73제_교사용.pdf | 영어 29번 어법 기출 교사용 | 약 37(시험지 19, 해설 약 18) |
| 영어29번_어법개념정리_학생용.pdf | 영어 29번 어법 개념 정리 학생용 | 약 58 |
| 영어29번_어법개념정리_교사용.pdf | 영어 29번 어법 개념 정리 교사용 | 학생용과 같음 |

- 출력 위치 grammar29/print/out/
- 시험지 제목 '영어 29번 어법 기출', 부제 '2016년~2026년 고3 수능, 모의평가, 학력평가 73문항'
- 교재 제목 '영어 29번 어법 개념 정리', 부제 '2016년~2026년 고3 기출 73문항 분석'
- pymupdf set_metadata로 title만 기입. author, subject, keywords, creator, producer는 빈 문자열

## 3. 시험지 명세

### 3.1 구성

- 문제지(학생용)
  - 73문항. 최근 시행 시험부터 역순, 같은 해는 시행 월 역순
  - 문항 번호는 1~73으로 다시 매김. 원래 시험과 문항 번호는 출처 표기로 보존
  - 지문을 확보하지 못한 2020년 4월 학평과 2026년 7월 학평은 수록하지 않음
- 교사용
  - 문제지와 같은 쪽 배치에 정답 표시를 더한 시험지 19쪽
  - 이어서 정답과 해설(쪽 번호 1부터)

### 3.2 판면과 2단

- 쪽 상자 210×296mm. 297mm보다 1mm 작게 설정해 빈 쪽 생성을 막음
- 2단. 단 폭 88.4mm, 단 사이 7.4mm, 좌우 여백 12.9mm
- 단 구분선은 단 사이 가운데 0.71pt 먹 실선. 머리 가로줄 아래 4.5mm에서 단 아래 끝까지
- 단 아래 끝은 쪽 아래에서 15mm
- 단 높이는 첫 쪽 약 245mm, 이어지는 쪽 약 258mm. 정확한 값은 렌더링에서 측정

### 3.3 첫 쪽 머리말

- 3칸 격자 34mm, 1fr, 34mm. 아래 정렬
  - 왼쪽 칸에 과목 상자 '고3 영어'. 고딕 700 10pt, 테두리 0.34pt, radius 1.6mm, 안쪽 여백 위 0.6mm 좌우 2.4mm 아래 0.4mm
  - 가운데 칸에 부제(명조 9pt)와 그 아래 제목(고딕 700 20pt, 자간 0.02em). 부제와 제목 사이 1.2mm
  - 오른쪽 칸에 쪽 번호 '1'(Latin 700 26pt)
- 격자 아래 2mm 띄우고 전폭 0.85pt 가로줄
- 가로줄 아래 1.6mm에 이름 칸, 오른쪽 정렬
  - '3학년 ____반 ____번 이름 ________'. 명조 9pt, 밑줄 0.34pt, 칸 폭 9mm, 9mm, 27mm
- 교사용은 제목 뒤 2mm에 '교사용' 상자. 고딕 500 8pt, 테두리 0.34pt, radius 0, 기준선 위 3pt

### 3.4 이어지는 쪽 머리말과 꼬리말

- 3칸 격자 34mm, 1fr, 34mm, 아래 정렬, 격자 아래 1.6mm 띄우고 0.85pt 가로줄
- 홀수 쪽은 왼쪽 과목 상자, 가운데 제목(고딕 700 15pt, 자간 0.02em), 오른쪽 쪽 번호(Latin 700 21pt)
- 짝수 쪽은 쪽 번호를 왼쪽, 과목 상자를 오른쪽에 두어 좌우 반전
- 부제와 이름 칸은 첫 쪽에만
- 꼬리말은 쪽 아래 7mm 가운데 '- 3 -'(Latin 8.5pt)

### 3.5 안내 상자

- 첫 쪽 왼쪽 단 맨 위. 테두리 0.34pt, 안쪽 여백 1.8mm 2.4mm, 아래 간격 5mm
- 선언 9.4pt(한글 8.6pt), 17px, 양쪽 정렬, word-break keep-all
- 문안 '※ 각 문항의 [ ] 안은 출제 시험입니다. 28번으로 출제된 문항은 원래 번호를 함께 적었습니다. 남는 자리는 풀이 공간으로 쓰십시오.'

### 3.6 문항 번호와 발문

- 번호 'N.'은 Latin 700 10.3pt, 뒤 간격 0.25em
- 발문은 선언 9.5pt(한글 8.7pt), 18px, 왼쪽 정렬
- 둘째 줄부터 내어쓰기 8.8pt(padding-left 8.8pt, text-indent -8.8pt)
- 밑줄형 발문 '다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?'
  - '틀린'에만 밑줄. 0.4pt, offset 2.2pt, skip-ink none
- 네모형 발문 '(A), (B), (C)의 각 네모 안에서 어법에 맞는 표현으로 가장 적절한 것은?'. 밑줄 없음
- [3점]은 원문항 표기를 따름(73문항 중 36개). 발문 끝, 발문과 같은 크기, 줄바꿈 금지

### 3.7 출처 표기

- 형식
  - 수능 [2026학년도 수능]
  - 모평 [2027학년도 9월 모평]
  - 학평 [2026년 5월 학평]
  - 원래 28번 문항 [2018학년도 수능 28번]
- 수능과 모평은 학년도, 학평은 시행 연월로 표기. 2026학년도 수능은 2025년 11월 시행
- 발문 끝([3점] 뒤)에 공백 1칸 두고 `float: right`로 배치. 마지막 줄에 자리가 없으면 다음 줄 오른쪽 끝으로 내려감
- 선언 8.6pt(한글 7.9pt), 줄바꿈 금지

### 3.8 지문, 밑줄, 원문자

- Latin 9.5pt, 18px, text-align justify, hyphens none, word-break normal
- 지문 블록 왼쪽 들여쓰기 8.8pt, 문단 첫 줄 들여쓰기 8.2pt
- 발문과 지문 사이 margin-top 4pt. 기준선 사이 17.5pt로 수능 환산값 17.6pt와 같음
- 양쪽 정렬로 단어 간격이 벌어진 줄은 고치지 않음
- 밑줄 선지 구조는 공백, 원문자(span.cn), 밑줄 낱말(u) 순서
  - 원문자는 KR Mark Exam(8.7pt 렌더링), 밑줄 없음, 뒤 간격 margin-right 0.2em(공백 문자 없음)
  - 밑줄은 0.4pt, text-underline-offset 2.2pt, text-decoration-skip-ink none(HWP처럼 하강부에서 끊기지 않음)
  - span.opt에 white-space nowrap. 밑줄 구간은 최장 14자('differentiates')라 단 폭 안에 들어감
- 줄표(U+2015)와 em dash(U+2014)는 원문 표기 유지. U+2015 줄표는 KR Mark Exam으로 조판되어 수능처럼 한글 명조 줄표가 됨
- 원문 이탤릭은 Latin Serif Italic

### 3.9 네모형 표기

- 대상 4문항. 2016년 3월 학평, 2017학년도 9월 모평, 2016년 10월 학평, 2018년 3월 학평
- 지문 안 표기는 '(A)'와 네모 상자
  - 상자는 inline-block, 테두리 0.34pt, 안쪽 여백 좌우 1.2mm, 선택어를 ' / '로 이어 같은 줄에 배치
  - 세로로 쌓지 않음. 줄 간격 18px 유지
- 선택지 표
  - 지문 아래 2.4mm, 왼쪽 8.8pt 들여 시작, 테두리 없음, 줄 높이 18px, 열 사이 2.2mm
  - 첫 줄은 (A), (B), (C) 열 머리, 가운데 정렬
  - 줄마다 원문자와 선택어 세 개, 선택어 사이 '……'(Latin)
  - 예 '① Adopt …… them …… where'

### 3.10 각주

- 지문 아래 1.2mm, 오른쪽 정렬, 선언 8.6pt(한글 7.9pt), 14px
- 각주가 여러 개면 같은 줄에 이어 쓰고 사이 간격 0.9em. 넘치면 다음 줄도 오른쪽 정렬
- 별표 뒤 공백 1칸. 데이터의 '*offspring: 자손'은 빌드에서 '* offspring: 자손'으로 바꿈
- 별표는 Latin Serif(수능 원본 TNR)
- 각주 항목마다 white-space nowrap. 항목 안에서는 줄을 나누지 않음
- 47문항에 각주가 있음

### 3.11 문항 간격과 단 나눔

- 단마다 최대 2문항, 쪽마다 최대 4문항
- 첫 문항은 단 맨 위. 첫 쪽 왼쪽 단은 안내 상자 아래
- 둘째 문항 시작 위치는 '단 높이의 50%'와 '첫 문항 끝 + 9mm' 중 큰 값
- 둘째 문항이 단 아래 끝을 넘으면 다음 단 맨 위로 넘김
- 문항은 단이나 쪽을 넘겨 나누지 않음(JS 배치로 보장)
- 단 아래 남는 공간은 풀이 여백. 단 높이를 맞추려고 글자 크기나 간격을 바꾸지 않음
- 높이 계산에 교사용 정답 줄을 포함함. 학생용에서는 같은 높이의 숨긴 줄이라 두 판의 쪽 배치가 같음
- 예상 쪽수 19쪽(쪽마다 4문항, 마지막 쪽 1문항)
- 높이 근거
  - 지문 길이 123~189단어, 평균 160단어
  - 최장 지문 약 17줄(81mm)에 발문, 각주, 정답 줄을 더하면 약 100mm. 단 높이 50%(약 122~129mm) 안에 들어감

### 3.12 교사용 정답 표시

- 밑줄형 정답 원문자는 글자 빨강에 0.6pt 빨간 원(outline, offset 0.3pt, radius 50%)
- 밑줄 낱말 색은 먹 유지
- 네모형은 지문 네모 안 맞는 선택어 빨강, 선택지 표 정답 줄 원문자에 빨간 원
- 정답 줄
  - 지문과 각주 아래 1.6mm, 왼쪽 8.8pt, 선언 8.6pt, 14px, 빨강
  - 밑줄형 '정답 ③ enable → enables', 네모형 '정답 ④'
  - 학생용은 같은 줄을 visibility:hidden으로 남겨 높이 유지
- 머리말 제목 뒤 '교사용' 상자(첫 쪽과 이어지는 쪽 모두)

### 3.13 정답표와 해설지 구성

- 판면은 @page A4, 여백 24mm 16mm 20mm
- 머리말과 꼬리말은 @page 여백 상자
  - 위 왼쪽 '영어 29번 어법 기출 정답과 해설', 위 오른쪽 '교사용'. 고딕 500 8pt, 아래 1.13pt 줄
  - 아래 가운데 이중선(0.6pt와 0.25pt)과 '- n -'(Latin 8.5pt)
- 제목 상자
  - 첫 쪽 맨 위, 0.34pt 이중 테두리(선 사이 0.6mm), 안쪽 여백 2.4mm 3mm, 가운데 정렬
  - 제목 '영어 29번 어법 기출 정답과 해설'(고딕 700 14pt), 아래 부제(명조 8.8pt)
- 빠른 정답표
  - 제목 상자 아래 4mm. 위아래 1.13pt 줄 사이, 안쪽 여백 위아래 2mm, 아래 간격 5mm
  - 10열 격자, 줄 사이 1.2mm, 73문항이라 8줄
  - '01. ③' 형식. 번호는 두 자리 Latin 700 9.5pt, 원문자는 KR Mark 9.5pt(Batang에 Bold가 없어 보통 굵기)
- 본문
  - 2단. column-count 2, column-gap 8mm, column-rule 0.34pt, column-fill auto(마지막 쪽 단 높이 맞추기 없음)
  - KR Serif 9.5pt, 20px, 양쪽 정렬, word-break keep-all, 먹 1도
- 문항 해설 구성
  - 첫 줄 '1. [출제 의도] 문법성 판단 [2027학년도 9월 모평]'. 번호만 Latin 700 10.3pt, 출처 8.4pt. 네모형은 '[출제 의도] 어법에 맞는 표현 고르기'
  - 둘째 줄 '[정답] ③ enable → enables'. 네모형 '[정답] ④ (A) Adopting (B) themselves (C) which'
  - '[풀이]' 뒤에 정답 선지를 먼저 쓰고('③ enable 동명사구 주어 ...'), 나머지 선지는 원문자 순서로 줄마다 1개, 내어쓰기 12pt
  - '[관련 개념] 주어와 동사의 수일치(2.1), 동사 자리와 준동사 자리(2.2)'. 괄호 안은 교재 절 번호
  - 라벨은 대괄호에 보통 굵기. 볼드는 문항 번호뿐
  - 인용한 밑줄 낱말은 정체(roman). 이탤릭 불허
  - [해석]과 [Words and Phrases]는 넣지 않음
- 문항 사이 3.4mm. 문항 해설은 단 경계에서 나눔 허용. 첫 줄과 [정답] 줄에 break-after avoid
- 예상 분량 약 18쪽

## 4. 교재 명세

### 4.1 구성

- 원고는 grammar29/print/src/총정리_빈칸.md. docs/03_어법총정리.md에 빈칸 표시 {{답}} 143곳을 더한 원고
- 대단원 6개
  - 1 출제 경향과 학습 순서, 2 동사, 3 준동사, 4 연결어, 5 품사와 대명사, 6 특수 구문
- 대단원 2~6의 단원 26개. 단원마다 판단 규칙, 풀이 순서, 기출 함정 유형, 기출 예문, 확인 문제(21개 단원)
- 학생용은 빈칸 답과 확인 문제 정답을 숨김. 교사용은 같은 자리에 빨강으로 표시
- 학생용과 교사용의 쪽수와 줄바꿈은 같아야 함

### 4.2 판면, 머리말, 쪽 번호

- @page A4. 위 22mm, 아래 18mm, 제본 쪽 22mm, 바깥쪽 18mm
  - 홀수 쪽(:right)은 왼쪽 22mm, 짝수 쪽(:left)은 오른쪽 22mm
- 본문 폭 170mm. 10pt 한글 기준 줄마다 약 48자
- 머리말은 @page 여백 상자
  - 바깥쪽 위에 '영어 29번 어법 개념 정리', 고딕 500 7.8pt
  - 안쪽 위에 교사용은 '교사용'(고딕 700 7.8pt, 상자 없음), 학생용은 빈칸(\00a0)
  - 바깥쪽과 안쪽 여백 상자 모두 아래 0.34pt 줄. 두 상자가 이어져 본문 폭 전체에 줄이 생김
  - 글자와 줄 사이 1mm, 줄과 본문 사이 7mm(margin-bottom 7mm)
- 쪽 번호는 아래 가운데 '- 6 -', Latin 8.5pt
- 첫 쪽(:first)은 머리말 없음, 쪽 번호 유지

### 4.3 첫 쪽

- 시험지 첫 쪽 머리말과 같은 구성
  - 왼쪽 과목 상자 '고3 영어', 가운데 부제(명조 9pt)와 제목(고딕 700 19pt), 오른쪽 칸 비움
  - 아래 0.85pt 가로줄, 오른쪽 이름 칸
- 이름 칸 아래 3mm에서 대단원 1 시작. 별도 표지와 목차 쪽 없음. 원고 1.5 문서 구성이 목차 구실을 함

### 4.4 단원과 절 제목 체계

- 번호는 원고 번호 유지. 대단원 2, 단원 2.1
- 대단원(## 2. 동사)
  - 새 쪽에서 시작(break-before page). 대단원 1은 첫 쪽에서 이어서 시작
  - 번호 '2'는 Latin 700 22pt 별색, 번호 뒤 마침표 삭제, 2.4mm 띄우고 제목 '동사'(고딕 700 15.5pt 먹)
  - 아래 1.13pt 별색 줄. 글자와 줄 사이 1.6mm, 줄 아래 4mm
- 단원(### 2.1 주어와 동사의 수일치)
  - 위 7mm, 아래 1.6mm, 고딕 700 11.5pt
  - 번호 '2.1'은 별색, 1.2mm 띄우고 제목(먹)
  - 줄 없음, break-after avoid
- 소제목(#### 판단 규칙)
  - '■ 판단 규칙'. 고딕 700 9.8pt, ■는 KR Mark 8pt 먹
  - 위 3.2mm, 아래 1mm, break-after avoid
- 소제목 이름은 원고의 판단 규칙, 풀이 순서, 기출 함정 유형, 기출 예문, 확인 문제 5종. Step, Point, Unit 같은 템플릿 라벨 불허

### 4.5 본문과 목록

- KR Serif 10pt, 21px, 양쪽 정렬, word-break keep-all. 영어 낱말이 섞인 문장도 같은 스택
- 문단 간격 위아래 0.8mm
- 1단계 불릿 기호 ◦(KR Mark). 텍스트 왼쪽 들여쓰기 5mm, 기호 위치 -4mm
- 2단계 불릿 기호 -(Latin). 1단계 텍스트에서 4mm 더 들임
- 원고의 '따라서'로 시작하는 결론 불릿도 같은 기호
- 원고의 굵게 표시(** **, 459곳)는 밑줄로 조판
  - 0.4pt, offset 2pt, skip-ink none, 굵기 400

### 4.6 개념 박스

- 대상은 단원마다 '판단 규칙' 소제목부터 다음 소제목 전까지 전체
- 별색 12% 망점 바탕(#e4e9f1), 테두리 없음, radius 0, 그림자 없음
- 안쪽 여백 2.4mm 3.2mm, 위 2.6mm, 아래 2mm
- 상자 제목 '■ 판단 규칙'은 ■를 포함해 별색
- 상자는 쪽 경계에서 나눔 허용(box-decoration-break slice, 기본값)
- 그 밖의 소제목은 상자 없이 본문으로 조판
- 단원 끝 요약 상자 없음

### 4.7 판단 규칙과 풀이 순서 표기

- 판단 규칙은 개념 박스 안 불릿 목록. 예외 규칙은 원고 문구('예외로')로 시작하는 불릿 유지
- 풀이 순서는 원고 번호 목록 1. 2. 3.
  - 번호는 Latin 10pt, 내어쓰기 5.4mm
  - 원문자로 바꾸지 않음. 선지 번호 ①~⑤와 겹침

### 4.8 기출 함정 유형

- 1단계 불릿은 함정 유형 이름, 2단계 불릿은 기출 사례
- 사례 형식은 원고 유지. 예 '2017년 4월 학평 ⑤ the traditional link ... were broken → was'
  - 판단 대상 낱말(원고 굵게)은 밑줄
  - 맞는 선지 표시 '(O)'는 '(○)'로 조판

### 4.9 기출 예문 표

- 원고 표 5열. 시험, 선지, 원문 발췌, 판정, 포인트
- 표 위 주석 줄 8.6pt. 원고 '선지 판정 (...) / ...' 줄이고 ' / ' 구분 허용
  - 원고 주석의 '밑줄 부분 굵게', '맞는 표현 굵게'는 조판에 맞게 '밑줄'로 고침
- 폭 100%, border-collapse collapse
- 위아래 0.71pt, 행 사이 0.34pt, 세로줄 없음
- 머리칸은 먹 10% 바탕, 고딕 500 8.4pt, 가운데 정렬, 아래 0.34pt
- 칸 안 여백 위아래 0.9mm 좌우 1.4mm, 세로 정렬 위
- 열 폭은 시험 22mm, 선지 9mm(가운데), 판정 15mm(가운데), 포인트 40mm, 원문 발췌는 나머지
- 글자 8.7pt, 17px. 원문 발췌의 판단 대상 낱말은 0.4pt 밑줄
- 행 단위로 쪽을 나눔(tr break-inside avoid). 쪽을 넘기면 머리 행 반복(thead table-header-group)
- 줄무늬 바탕 불허

### 4.10 O와 X 표기

- 원고 'O'는 ○, 'X'는 ×, 'X → were'는 '× → were', '네모형'은 원고 유지
- 기호는 KR Mark, 판정 열 가운데 정렬, 줄바꿈 금지
- 적용 범위는 기출 예문 표 판정 열 232칸(네모형 칸 포함)과 기출 함정 유형의 '(O)'
- 학생용과 교사용 표기가 같음. 판정은 원고 단계에서 공개한 정보

### 4.11 확인 문제

- 원고 번호 목록. 문항마다 고르기형 문장 1개와 출처
  - 예 'Listening to the needs of employees [enable / enables] leaders ... (2027학년도 9월 모평)'
- 문장 Latin 10pt, 고르기 괄호 [ / ]는 원고 표기 유지, 출처 8.5pt
- 정답 블록(원고 details)
  - 위 0.34pt 줄, 머리 '정답과 해설'(고딕 700 9pt), 번호 목록 9.6pt
  - 학생용은 블록 전체 visibility:hidden. 자리는 풀이 공간으로 남음(HWP 학습지에서 빨간 정답을 흰색으로 바꾼 결과와 같은 모양)
  - 교사용은 글자와 줄 모두 빨강
- 21개 단원에 수록

### 4.12 빈칸 모양과 교사용 답

- 원고 {{답}}은 span.bl 안의 b 요소로 변환
- 빈칸 모양
  - inline-block, 아래 0.4pt 먹 밑줄, 안쪽 여백 좌우 1em, 바깥 여백 좌우 0.15em
  - 가운데 정렬, line-height 1.2, text-indent 0
  - 폭은 정답 글자 폭과 2em의 합. 학생용과 교사용이 같음
  - inline-block이라 빈칸이 줄 끝에서 갈라지지 않음
- 학생용은 b 요소에 visibility:hidden
- 교사용은 b 요소를 빨강 #e00000, 굵기 400으로 표시. 밑줄은 먹 유지
- 빈칸은 판단 규칙과 풀이 순서에 143곳

## 5. CSS 구현 메모

### 5.1 @font-face

- 경로는 build_pdf.py의 --fonts 디렉터리(기본 grammar29/print/fonts)를 file URI로 변환해 삽입

```css
@font-face { font-family: "Latin Serif"; src: url(FONTS/LiberationSerif-Regular.ttf); font-weight: 400; font-style: normal; }
@font-face { font-family: "Latin Serif"; src: url(FONTS/LiberationSerif-Bold.ttf); font-weight: 700; font-style: normal; }
@font-face { font-family: "Latin Serif"; src: url(FONTS/LiberationSerif-Italic.ttf); font-weight: 400; font-style: italic; }
@font-face { font-family: "KR Serif"; src: url(FONTS/Batang-Regular.ttf); font-weight: 400; }
@font-face { font-family: "KR Serif"; src: url(FONTS/NotoSerifKR-Bold.ttf); font-weight: 700; }
@font-face { font-family: "KR Mark"; src: url(FONTS/Batang-Regular.ttf); font-weight: 400;
             unicode-range: U+00D7, U+2015, U+203B, U+2460-2473, U+25A0-25FF, U+3260-327F; }
@font-face { font-family: "KR Gothic"; src: url(FONTS/NotoSansKR-Medium.ttf); font-weight: 500; }
@font-face { font-family: "KR Gothic"; src: url(FONTS/NotoSansKR-Bold.ttf); font-weight: 700; }
/* 시험지 전용 */
@font-face { font-family: "KR Serif Exam"; src: url(FONTS/Batang-Regular.ttf); font-weight: 400; size-adjust: 92%; }
@font-face { font-family: "KR Mark Exam"; src: url(FONTS/Batang-Regular.ttf); font-weight: 400; size-adjust: 92%;
             unicode-range: U+00D7, U+2015, U+203B, U+2460-2473, U+25A0-25FF, U+3260-327F; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; background: #fff; color: #000; font-synthesis: none; }
```

### 5.2 @page 크기와 여백

```css
/* 시험지: 여백 0, 쪽 상자를 HTML로 직접 그림 */
@page { size: A4; margin: 0; }
.page { width: 210mm; height: 296mm; box-sizing: border-box; padding: 10mm 12.9mm 0;
        position: relative; overflow: hidden; break-after: page; }
.page:last-child { break-after: auto; }

/* 정답과 해설 */
@page { size: A4; margin: 24mm 16mm 20mm;
  @top-left  { content: "영어 29번 어법 기출 정답과 해설"; font: 500 8pt "KR Gothic";
               vertical-align: bottom; padding-bottom: 1mm; border-bottom: 1.13pt solid #000; margin-bottom: 5mm; }
  @top-right { content: "교사용"; font: 500 8pt "KR Gothic";
               vertical-align: bottom; padding-bottom: 1mm; border-bottom: 1.13pt solid #000; margin-bottom: 5mm; }
  @bottom-center { content: "- " counter(page) " -"; font: 400 8.5pt "Latin Serif";
                   vertical-align: top; padding-top: 2.4mm;
                   background: url("data:image/svg+xml,...이중선 SVG...") top left / 100% 1.5mm no-repeat; }
}

/* 교재 */
@page { size: A4; margin: 22mm 18mm 18mm 22mm;
  @bottom-center { content: "- " counter(page) " -"; font: 400 8.5pt "Latin Serif"; } }
@page :right { margin-left: 22mm; margin-right: 18mm;
  @top-right { content: "영어 29번 어법 개념 정리"; font: 500 7.8pt "KR Gothic"; vertical-align: bottom;
               padding-bottom: 1mm; border-bottom: 0.34pt solid #000; margin-bottom: 7mm; }
  @top-left  { content: "\00a0"; /* 교사용은 "교사용", font 700 */ font: 700 7.8pt "KR Gothic";
               vertical-align: bottom; padding-bottom: 1mm; border-bottom: 0.34pt solid #000; margin-bottom: 7mm; } }
@page :left { margin-left: 18mm; margin-right: 22mm;
  /* :right의 top-left와 top-right 내용을 서로 바꿈 */ }
@page :first { @top-left { content: none; border: 0; } @top-right { content: none; border: 0; } }
```

- 이중선 SVG는 폭 100 높이 4 viewBox에 높이 0.8 사각형(y 0)과 높이 0.33 사각형(y 2) 2개. 여백 상자 background로 그림(명세 작성 중 Chromium 141에서 확인)
- displayHeaderFooter와 머리말 템플릿은 쓰지 않음. 템플릿은 문서의 @font-face를 쓰지 못해 시스템 글꼴로 대체됨

### 5.3 시험지 쪽 배치와 columns

- 시험지는 CSS columns 대신 고정 쪽 상자와 JS 배치
  - 둘째 문항 50% 시작 규칙과 홀짝 쪽 머리말 반전은 CSS columns로 표현하지 못함
- 쪽 상자 안 구조
  - .hd(머리말), 첫 쪽만 .namebar, .cols(왼쪽 .col, 가운데 .rule, 오른쪽 .col), .ft(꼬리말)
  - .cols는 position absolute, left 12.9mm, right 12.9mm, bottom 15mm, top은 머리말(첫 쪽은 이름 칸) 아래 끝 + 4.5mm
  - .col 폭 88.4mm, .rule 폭 7.4mm. .rule::after에 border-left 0.71pt solid #000, left 50%
  - .ft는 bottom 7mm, 가운데 정렬
- 배치 절차
  1. document.fonts.ready 이후 실행
  2. 원본 문항(.q)을 화면 밖 컨테이너에 모두 생성
  3. 쪽 상자를 만들고 단 높이 H를 측정
  4. 문항을 순서대로 단에 넣고 높이 h를 측정
  5. 단의 첫 문항이면 top 0, 둘째 문항이면 top = max(0.5H, 첫 문항 끝 + 9mm)
  6. top + h > H이거나 단에 이미 2문항이면 다음 단으로, 오른쪽 단 다음은 새 쪽
  7. 끝나면 window.__done = true
- 학생용과 교사용에 같은 절차를 실행. .key(정답 줄)가 두 판에서 같은 높이를 차지하므로 결과가 같음
- JS를 쓰지 못하는 환경의 대체안. 50% 규칙은 포기함

```css
.cols { column-count: 2; column-gap: 7.4mm; column-rule: 0.71pt solid #000; column-fill: auto; height: 258mm; }
.q { break-inside: avoid; margin-bottom: 11mm; }
```

### 5.4 break-inside 규칙

| 대상 | 규칙 |
| --- | --- |
| 시험지 문항 .q | 나누지 않음(JS 배치, 대체안은 break-inside avoid) |
| 해설 문항 .ex | 나눔 허용. 첫 줄과 [정답] 줄은 break-after avoid |
| 교재 대단원 h2 | break-before page(첫 대단원 제외) |
| 교재 h3, h4 | break-after avoid |
| 교재 표 행 tr | break-inside avoid, thead 반복 |
| 교재 개념 박스 | 나눔 허용 |
| 교재 확인 문제 정답 블록 | break-inside avoid |
| 빈칸 .bl | inline-block이라 줄 단위로 나뉘지 않음 |

### 5.5 주요 선택자 수치

```css
/* 시험지 */
.q        { font: 400 9.5pt/18px "KR Mark Exam", "Latin Serif", "KR Serif Exam"; }
.stem     { padding-left: 8.8pt; text-indent: -8.8pt; text-align: left; }
.qno      { font: 700 10.3pt "Latin Serif"; margin-right: 0.25em; }
.stem u, .opt u { text-decoration: underline 0.4pt; text-underline-offset: 2.2pt; text-decoration-skip-ink: none; }
.src      { float: right; margin-left: 1em; font-size: 8.6pt; white-space: nowrap; }
.passage  { margin-top: 4pt; padding-left: 8.8pt; text-align: justify; hyphens: none; word-break: normal; }
.passage p { margin: 0; text-indent: 8.2pt; }
.opt      { white-space: nowrap; }
.cn       { margin-right: 0.2em; }
.nemo     { display: inline-block; border: 0.34pt solid #000; padding: 0 1.2mm; line-height: 1.25; }
.foot     { margin-top: 1.2mm; text-align: right; font-size: 8.6pt; line-height: 14px; }
.foot span { white-space: nowrap; margin-left: 0.9em; }
.key      { margin-top: 1.6mm; padding-left: 8.8pt; font-size: 8.6pt; line-height: 14px; color: #e00000; visibility: hidden; }
.teacher .key { visibility: visible; }
.teacher .opt.ans .cn { color: #e00000; outline: 0.6pt solid #e00000; outline-offset: 0.3pt; border-radius: 50%; }

/* 정답과 해설 */
body.ans  { font: 400 9.5pt/20px "KR Mark", "Latin Serif", "KR Serif"; text-align: justify; word-break: keep-all; }
.quick    { display: grid; grid-template-columns: repeat(10, 1fr); row-gap: 1.2mm;
            border-top: 1.13pt solid #000; border-bottom: 1.13pt solid #000; padding: 2mm 0; margin-bottom: 5mm; }
.body     { column-count: 2; column-gap: 8mm; column-rule: 0.34pt solid #000; column-fill: auto; }
.ex       { margin-bottom: 3.4mm; }
.ex .line { padding-left: 12pt; text-indent: -12pt; }

/* 교재 */
body.guide { font: 400 10pt/21px "KR Mark", "Latin Serif", "KR Serif"; text-align: justify; word-break: keep-all; }
h2        { break-before: page; font: 700 15.5pt "KR Gothic"; padding-bottom: 1.6mm; margin: 0 0 4mm;
            border-bottom: 1.13pt solid #1b4a8c; }
h2 .num   { font: 700 22pt/1 "Latin Serif"; color: #1b4a8c; margin-right: 2.4mm; }
h3        { font: 700 11.5pt "KR Gothic"; margin: 7mm 0 1.6mm; break-after: avoid; }
h3 .num   { color: #1b4a8c; margin-right: 1.2mm; }
h4        { font: 700 9.8pt "KR Gothic"; margin: 3.2mm 0 1mm; break-after: avoid; }
.rulebox  { background: #e4e9f1; padding: 2.4mm 3.2mm; margin: 2.6mm 0 2mm; }
.rulebox h4 { color: #1b4a8c; }
u, .ul    { text-decoration: underline 0.4pt; text-underline-offset: 2pt; text-decoration-skip-ink: none; }
table     { width: 100%; border-collapse: collapse; font-size: 8.7pt; line-height: 17px;
            border-top: 0.71pt solid #000; border-bottom: 0.71pt solid #000; }
th        { font: 500 8.4pt "KR Gothic"; background: #e6e6e6; text-align: center; border-bottom: 0.34pt solid #000; padding: 0.9mm 1.4mm; }
td        { border-bottom: 0.34pt solid #000; padding: 0.9mm 1.4mm; vertical-align: top; }
.bl       { display: inline-block; border-bottom: 0.4pt solid #000; padding: 0 1em; margin: 0 0.15em;
            text-align: center; text-indent: 0; line-height: 1.2; }
.bl b     { font-weight: 400; visibility: hidden; }
.teacher .bl b { visibility: visible; color: #e00000; }
.answers  { visibility: hidden; border-top: 0.34pt solid #000; padding-top: 1mm; margin: 1.6mm 0 2mm; font-size: 9.6pt; }
.teacher .answers { visibility: visible; color: #e00000; border-color: #e00000; }
```

### 5.6 렌더링 순서

1. Chromium 실행 경로 /opt/pw-browsers/chromium-1194/chrome-linux/chrome(playwright executable_path)
2. page.goto(HTML file URI)
3. 여백 상자에 쓰는 글꼴을 선로딩
   - document.fonts.load('500 8pt "KR Gothic"', 자료 이름과 '교사용'), document.fonts.load('700 7.8pt "KR Gothic"', '교사용'), document.fonts.load('400 8.5pt "Latin Serif"', '- 0123456789')
   - 선로딩이 없으면 여백 상자 글자가 빠진 채 인쇄됨(명세 작성 중 확인)
4. await document.fonts.ready
5. 시험지는 window.__done === true 대기
6. page.pdf(prefer_css_page_size=True, print_background=True). display_header_footer 미사용
7. pymupdf로 병합(교사용 시험지와 해설), set_metadata, save(garbage=3, deflate=True)

### 5.7 검수

- 글꼴
  - 4종 모두 pdffonts 결과가 CID TrueType, emb yes, sub yes만
  - Type 3, DejaVu, WenQuanYi, UnDotum 등 시스템 글꼴 0건
- 정답 누출
  - 교사용 PDF에서 색이 #e00000인 글자 span마다 학생용 같은 쪽 같은 bbox의 텍스트(page.get_textbox)가 빈 문자열인지 pymupdf로 확인
  - 학생용 HTML에 color transparent, color #fff 규칙 0건
- 쪽 일치
  - 학생용과 교사용 쪽수가 같음
  - 쪽마다 빨강을 뺀 첫 줄과 마지막 줄 텍스트가 같음
- 시험지 배치
  - 문항마다 아래 끝이 단 아래 끝 이하, 단마다 문항 2개 이하
- 색
  - 학생용 시험지 글자 색 집합 {#000000}, 학생용 교재 {#000000, #1b4a8c}. pymupdf span color로 확인
- 금지 문자
  - PDF 텍스트에서 '**', '##', 이모지 0건
  - em dash와 가운뎃점은 한국어 설명문 범위에서 0건. 기출 원문 발췌는 예외
- 메타데이터
  - pdfinfo의 Creator와 Producer가 빈 값, Title이 파일 이름 표의 값
- 눈 확인
  - 110dpi PNG로 시험지 1, 2, 3쪽과 마지막 쪽, 해설 1쪽, 교재 1쪽, 대단원 첫 쪽, 표가 있는 쪽
  - 홀짝 쪽 머리말 반전, 각주 이어 쓰기, 빈칸 밑줄 높이, 별색 상자 흑백 출력 명도 확인

## 6. 출처

- AI 티 조사
  - https://tali.kr/ai-slop-design-patterns
  - https://uxskill.laithjunaidy.com/blog/ko/ai-coding-design-korean.html
  - https://www.925studios.co/blog/ai-slop-design-tells
  - https://www.925studios.co/blog/ai-slop-web-design-guide
  - https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it
  - https://www.adriankrebs.ch/blog/design-slop/
  - https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p
  - https://impeccable.style/slop/
  - https://github.com/nexu-io/open-design/blob/main/craft/anti-ai-slop.md
  - https://github.com/anthropics/skills (skills/frontend-design/SKILL.md)
  - https://github.com/pbakaus/impeccable (skill/reference/craft-floor.md)
  - https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
  - https://github.com/softaworks/agent-toolkit/blob/main/skills/writing-clearly-and-concisely/signs-of-ai-writing.md
  - https://www.pangram.com/signs-of-ai-writing
  - https://github.com/epoko77-ai/im-not-ai (skills/humanize-korean/references/ai-tell-taxonomy.md)
  - https://brunch.co.kr/@webtutor/1155
  - https://www.chatslide.ai/guides/how-to-make-ai-slides-not-look-ai-generated
  - https://2slides.com/blog/can-ai-make-slides-that-dont-look-ai-generated
  - https://github.com/jkkms/ppt-deck
- 시험지와 교재 관례
  - 2025학년도 수능 영어 원본 PDF(2025_suneung_english.pdf), 2025년 7월 고3 학평 영어 PDF(2025_07_english.pdf)
  - EBS 2025년 6월 모평 영어 정답과 해설(msc_2025-6-eng_sol.pdf), EXAM4YOU 워크북(merged-2025-09mo.pdf)
  - https://github.com/handaram-dev/exam-hwpx-skill
  - https://orbi.kr/0004730915 (평가원 시험지 판형 272×394mm)
  - https://orbi.kr/00073267528 (평가원 글꼴 신명 중명조, 장평 95%, 자간 -5%)
  - https://orbi.kr/0009902939 (수능 영어 TNR과 신명조 혼용)
  - https://namu.wiki/w/시험지
  - https://help.hancom.com/hoffice/multi/ko_kr/hwp/format/paragraph/paragraph(line_spacing).htm
  - https://help.hancom.com/hoffice/multi/ko_kr/hwp/format/columns/columns.htm
  - https://sciencelove.com/2469, https://sciencelove.com/572 (빨간 정답 학습지)
  - https://brunch.co.kr/@sweetannie/127 (먹과 별색 2도 인쇄)
- 글꼴
  - https://github.com/google/fonts/tree/main/ofl/batang
  - https://github.com/google/fonts/tree/main/ofl/notoserifkr, https://github.com/google/fonts/tree/main/ofl/notosanskr
  - https://github.com/notofonts/noto-cjk
  - fonts-liberation 2.1.5(/usr/share/doc/fonts-liberation/copyright)
  - https://ko.wikipedia.org/wiki/함초롬체, https://github.com/itext/i7js-highlevel (hancom.txt)
  - https://wiki.archlinux.org/title/Metric-compatible_fonts
