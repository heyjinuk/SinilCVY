# -*- coding: utf-8 -*-
"""신일콘베어 홈페이지 생성 스크립트.

사이트 내용(제품 설명, 연락처 등)은 이 파일에서 고친 뒤
`python3 tools/build_site.py` 를 실행하면 모든 HTML 페이지가 다시 만들어집니다.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.sinilconveyor.com"
BRAND = "신일콘베어"

COMPANY = {
    "name": "신일콘베어㈜",
    "name_en": "Sinil Conveyor Inc.",
    "ceo": "김복선",
    "tel": "02-2679-3225",
    "fax": "02-2679-9635",
    "email": "sinil3359@daum.net",
    "hq": "경기도 김포시 하성면 원산로 9",
    "plant2": "경기도 김포시 통진읍 서암로 183번길 36-22",
}

# 제품 데이터 ---------------------------------------------------------------
CATS = [
    ("auto", "자동화 롤러", "물류·생산 자동화 컨베이어 라인에 들어가는 롤러"),
    ("industrial", "산업용 롤러", "벨트 컨베이어의 벨트를 받치고 충격을 흡수하는 롤러"),
    ("pulley", "풀리", "벨트 컨베이어의 구동과 장력을 담당하는 풀리"),
]

P = [
    dict(slug="mr", cat="auto", name="MR 롤러", en="MR Roller", thumb="mr롤러2.jpg",
         title="MR 롤러 제작 – 컨베이어 이송 롤러",
         desc="MR 롤러 제작 – 자동화 컨베이어와 단순 이송 컨베이어 라인의 핵심 롤러. 파이프 Ø38.1~Ø60.5, 축 Ø12 규격을 기본으로 길이·재질을 맞춤 제작합니다. 신일콘베어",
         short="자동화·이송 컨베이어 라인에 가장 많이 쓰이는 기본 롤러",
         lead="MR 롤러는 자동화 컨베이어와 단순 이송 컨베이어 라인에 가장 많이 쓰이는 롤러입니다. 파이프 외경과 축 지름을 기본 규격에서 고르고, 길이와 재질은 주문 사양에 맞춰 제작합니다.",
         points=["파이프 외경 Ø38.1 · Ø42.7 · Ø48.6 · Ø50.8 · Ø60.5", "축 지름 Ø12 (Ø60.5는 Ø14 선택 가능)", "파이프 재질: 스틸(아연도금), 스테인리스, 엔지니어링 플라스틱", "롤러 길이는 주문 사양에 맞춤"],
         spec=dict(caption="기술 데이터 (롤러 길이 500mm 기준)",
                   head=["파이프 외경", "축 지름", "허용 하중 (kgf)", "속도 (m/min)", "베어링"],
                   rows=[["Ø38.1", "Ø12", "100", "40", "6002ZZ"], ["Ø42.7", "Ø12", "100", "40", "6002ZZ"],
                         ["Ø48.6", "Ø12", "120", "40", "6002ZZ"], ["Ø50.8", "Ø12", "140", "70", "6002ZZ"],
                         ["Ø60.5", "Ø12 (14)", "140", "70", "6002ZZ"]]),
         imgs=[("mrproduct1.PNG", "MR 롤러 기술 데이터표와 모델 부여법"), ("mrproduct2.PNG", "MR 롤러 FR50·FR60 치수 도면과 모델 표"), ("mrproduct3.PNG", "MR 롤러 스프링 축 타입 치수 도면")]),
    dict(slug="br", cat="auto", name="BR 롤러", en="Ball Bearing Roller", thumb="BR롤러2.jpg",
         title="BR 롤러(베어링 롤러) 제작",
         desc="BR 롤러(볼 베어링 롤러) 제작 – 파이프 양단에 베어링을 삽입해 회전이 부드러우며, 베어링 규격에 맞춰 맞춤 제작합니다. 컨베이어 롤러 전문 신일콘베어",
         short="양 끝에 볼 베어링을 넣어 회전이 부드러운 롤러",
         lead="BR 롤러(볼 베어링 롤러)는 파이프 양 끝에 볼 베어링을 넣어 회전이 부드럽고 오래 쓰는 롤러입니다. 사용하실 베어링 규격에 맞춰 맞춤 제작합니다.",
         points=["파이프 양단 볼 베어링 삽입", "베어링 규격에 맞춘 맞춤 제작", "파이프 외경·길이·축 가공은 도면 기준"],
         imgs=[("brproduct1.PNG", "BR 롤러 치수 도면과 규격표"), ("mrproduct2.PNG", "롤러 FR50·FR60 치수 도면과 모델 표"), ("mrproduct3.PNG", "롤러 스프링 축 타입 치수 도면")]),
    dict(slug="chain", cat="auto", name="스프라켓 롤러", en="Sprocket Roller", thumb="sprocket2.jpg",
         title="스프라켓 롤러 제작 – 체인 컨베이어 구동",
         desc="스프라켓 롤러 제작 – 체인 컨베이어 구동에 필수적인 롤러로, 체인 규격과 라인 사양에 맞춰 싱글·더블 스프라켓 타입을 맞춤 제작합니다. 컨베이어 롤러 전문 신일콘베어",
         short="체인으로 동력을 전달하는 체인 컨베이어 구동 롤러",
         lead="스프라켓 롤러는 체인 컨베이어 라인에서 구동을 맡는 롤러입니다. 롤러 끝에 스프라켓을 달아 체인으로 동력을 이어 주며, 컨베이어를 움직이는 데 꼭 필요한 제품입니다.",
         points=["싱글 스프라켓 · 더블 스프라켓 타입", "체인 규격(RS#40, RS#50 등)과 잇수에 맞춰 제작", "파이프 외경 Ø50 · Ø60 계열 기본"],
         imgs=[(f"chain{i}.PNG", f"스프라켓 롤러 도면 및 규격 {i}") for i in range(1, 8)]),
    dict(slug="accum", cat="auto", name="어큐뮬레이션 롤러", en="Accum Roller", thumb="accum2.jpg",
         title="어큐뮬레이션(Accum) 롤러 제작",
         desc="어큐뮬레이션(Accum) 롤러 제작 – 체인기어와 함께 샤프트에 스프링이 장착되어 장력 전달에 적합한 컨베이어 롤러입니다. 컨베이어 롤러 전문 신일콘베어",
         short="스프링이 든 샤프트로 장력을 전달하는 체인 구동 롤러",
         lead="어큐뮬레이션 롤러는 체인기어와 함께 샤프트에 스프링이 들어간 롤러로, 장력 전달에 가장 알맞은 제품입니다. 물건을 잠시 모아 두는 구간이 있는 컨베이어 라인에 쓰입니다.",
         points=["체인기어 + 스프링 내장 샤프트 구조", "장력 전달용", "체인 규격과 길이는 주문 사양에 맞춤"],
         imgs=[(f"accum{i}.PNG", f"어큐뮬레이션 롤러 도면 및 규격 {i}") for i in range(1, 9)]),
    dict(slug="ringbelt", cat="auto", name="링벨트 롤러", en="Ring Belt Roller", thumb="ringbelt2.jpg",
         title="링벨트 롤러 제작",
         desc="링벨트 롤러(환롤러) 제작 – 벨트 컨베이어 구동용 기본 롤러로, 벨트 타입에 따라 1열·2열 환롤러를 맞춤 제작합니다. 컨베이어 롤러 전문 신일콘베어",
         short="링벨트로 롤러끼리 동력을 이어 주는 벨트 구동 롤러",
         lead="링벨트 롤러(환롤러)는 롤러 사이를 둥근 벨트로 연결해 컨베이어를 움직이는 기본 롤러입니다. 사용하는 벨트 타입에 따라 1열·2열 홈 롤러가 대표적입니다.",
         points=["1열 · 2열 링벨트 홈 타입", "벨트 규격에 맞춘 홈 가공", "파이프 외경·길이는 주문 사양에 맞춤"],
         imgs=[("ring1.PNG", "링벨트 롤러 치수 도면 1"), ("ring2.PNG", "링벨트 롤러 치수 도면 2")]),
    dict(slug="taper", cat="auto", name="테이퍼 롤러", en="Taper Roller", thumb="테이퍼2.jpg",
         title="테이퍼 롤러 제작 – 곡선 컨베이어용",
         desc="테이퍼 롤러 제작 – 경사(크라운)로 가공해 곡선 컨베이어에 쓰는 롤러로, 일반형과 체인형이 있습니다. 컨베이어 롤러 전문 신일콘베어",
         short="곡선 구간에 쓰는 경사형 롤러, 일반형·체인형",
         lead="테이퍼 롤러는 한쪽으로 갈수록 지름이 커지도록 경사(크라운)를 준 롤러입니다. 곡선 컨베이어 구간에서 물건이 일정하게 돌아가도록 쓰이며, 일반형과 체인형이 있습니다.",
         points=["일반형 · 체인형", "곡선 컨베이어 구간용", "경사 각도와 길이는 라인 사양에 맞춤"],
         imgs=[("taper.PNG", "테이퍼 롤러 치수 도면")]),
    dict(slug="return", cat="industrial", name="캐리어·리턴 롤러", en="Carrier / Return Roller", thumb="return.jpg",
         title="캐리어·리턴 롤러 제작",
         desc="캐리어·리턴 롤러 제작 – 벨트 컨베이어의 벨트를 지지하는 산업용 롤러로, 내부 베어링 밀봉 구조이며 벨트 폭에 맞춰 제작합니다. 컨베이어 롤러 전문 신일콘베어",
         short="벨트 컨베이어의 벨트를 받쳐 주는 산업용 롤러",
         lead="캐리어 롤러는 벨트 컨베이어에서 짐을 싣고 가는 쪽 벨트를 받치고, 리턴 롤러는 돌아오는 쪽 벨트를 받칩니다. 내부에 베어링을 넣고 밀봉한 구조이며, 축은 컨베이어 프레임에 고정됩니다.",
         points=["내부 베어링 밀봉 구조", "리턴 롤러는 벨트 폭과 같은 길이의 단일 롤러", "벨트 폭과 프레임 규격에 맞춰 제작"],
         imgs=[("returncarrier.PNG", "캐리어·리턴 롤러 도면 1"), ("returncarrier1.PNG", "캐리어·리턴 롤러 도면 2"), ("returncarrier2.PNG", "캐리어·리턴 롤러 도면 3")]),
    dict(slug="idler", cat="industrial", name="자동조심 롤러", en="Self-aligning Idler", thumb="idler.jpg",
         title="자동조심 롤러 제작",
         desc="자동조심 롤러(아이들러) 제작 – 산업용 벨트 컨베이어의 롤러를 받쳐 주는 제품으로, 롤러 규격에 맞춰 제작합니다. 컨베이어 롤러 전문 신일콘베어",
         short="벨트 컨베이어의 롤러를 받쳐 주는 아이들러",
         lead="자동조심 아이들러는 산업용 벨트 컨베이어에서 롤러를 받쳐 주는 제품입니다. 사용하는 롤러 규격에 맞춰 제작합니다.",
         points=["산업용 벨트 컨베이어용", "롤러 규격에 맞춘 프레임 제작"],
         imgs=[("idler1.PNG", "자동조심 롤러 도면 1"), ("idler2.PNG", "자동조심 롤러 도면 2"), ("idler3.PNG", "자동조심 롤러 도면 3")]),
    dict(slug="impact", cat="industrial", name="임팩트 롤러", en="Impact Roller", thumb="impact.jpg",
         title="임팩트 롤러 제작",
         desc="임팩트 롤러 제작 – 벨트 컨베이어의 충격을 완화·흡수하는 고무 코팅 산업용 롤러입니다. 컨베이어 롤러 전문 신일콘베어",
         short="고무 링으로 충격을 흡수하는 산업용 롤러",
         lead="임팩트 롤러는 벨트에 물건이 떨어지는 구간의 충격을 줄이고 흡수하는 산업용 롤러입니다. 보통 고무를 입혀 제작합니다.",
         points=["고무 코팅으로 충격 완화", "투입부·낙하 구간용", "벨트 폭과 하중에 맞춰 제작"],
         imgs=[("impact1.PNG", "임팩트 롤러 도면 1"), ("impact2.PNG", "임팩트 롤러 도면 2")]),
    dict(slug="pully", cat="pulley", name="헤드·테일 풀리", en="Head / Tail Pulley", thumb="head.jpg",
         title="헤드·테일 풀리 제작",
         desc="헤드·테일 풀리 제작 – 벨트 컨베이어의 구동력이 집중되는 부분으로, 고정도 가공과 작업 용량에 맞춘 규격 선정이 필요합니다. 컨베이어 풀리 전문 신일콘베어",
         short="벨트 컨베이어의 구동력이 모이는 양 끝 풀리",
         lead="헤드 풀리는 벨트 컨베이어의 구동력이 모이는 부분이라 정밀한 가공이 필요하고, 컨베이어 작업 용량에 맞춰 규격을 골라야 합니다.",
         points=["고정도 가공", "컨베이어 작업 용량에 맞춘 규격 선정", "축·키홈 가공은 도면 기준"],
         imgs=[("head1.PNG", "헤드·테일 풀리 도면")]),
    dict(slug="pully2", cat="pulley", name="스냅 풀리", en="Snap Pulley", thumb="pully.jpg",
         title="스냅 풀리 제작",
         desc="스냅 풀리 제작 – 벨트 컨베이어의 구동력이 집중되는 부분에서 벨트 장력을 높여 주는 풀리입니다. 컨베이어 풀리 전문 신일콘베어",
         short="벨트 장력을 높여 주는 풀리",
         lead="스냅 풀리는 헤드 풀리와 함께 벨트 컨베이어의 구동력이 모이는 곳에 쓰이며, 벨트 장력을 최대한 끌어올려 줍니다.",
         points=["벨트 장력 확보용", "헤드 풀리와 함께 사용", "규격은 벨트 폭과 구동 조건에 맞춤"],
         imgs=[("pully2.PNG", "스냅 풀리 도면")]),
    dict(slug="pully3", cat="pulley", name="특수처리 풀리", en="Rubber Lagged Pulley", thumb="pully.jpg",
         title="특수처리 롤러 제작",
         desc="특수처리 드럼 풀리·롤러 제작 – 표면을 경도 높은 고무로 코팅해 마찰 계수를 높입니다. 컨베이어 롤러 전문 신일콘베어",
         short="고무 코팅으로 마찰력을 높인 드럼 풀리",
         lead="드럼 풀리 표면을 경도 높은 고무로 코팅해 벨트와의 마찰 계수를 높인 제품입니다. 벨트 미끄러짐을 줄여야 하는 구동부에 쓰입니다.",
         points=["고경도 고무 코팅", "마찰 계수 향상", "헤드·스냅 풀리에 적용 가능"],
         imgs=[("rubber.PNG", "특수처리 고무 코팅 풀리 도면")]),
]
BY = {p["slug"]: p for p in P}

# 공통 조각 ---------------------------------------------------------------
e = html.escape


def head(title, desc, path, extra=""):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/main_slider01.jpg">
<meta property="og:locale" content="ko_KR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
"""


NAV = [("/about/overview", "회사소개"), ("/product/", "제품"), ("/#facilities", "가공 설비")]


def header(active=""):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/"><img src="/img/logo_top.gif" alt="{BRAND}" width="184" height="54"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav">메뉴</button>
    <nav class="nav" id="nav" aria-label="주 메뉴">{links}<a class="btn" href="/contact">견적 문의</a></nav>
  </div>
</header>
"""


FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <img src="/img/logo_top.gif" alt="" width="184" height="54">
    <div>
      <p>{COMPANY['name']} · 대표 {COMPANY['ceo']}</p>
      <p>본사(제1공장) {COMPANY['hq']} · 제2공장 {COMPANY['plant2']}</p>
      <p>전화 <a href="tel:{COMPANY['tel']}">{COMPANY['tel']}</a> · 팩스 {COMPANY['fax']} · <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
      <p>© {COMPANY['name_en']}</p>
    </div>
  </div>
</footer>
<script>
(function(){{var b=document.querySelector('.menu-toggle'),n=document.getElementById('nav');
if(!b||!n)return;b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}});}})();
</script>
</body>
</html>
"""


def contact_band():
    return f"""<section class="contact-band">
  <div class="wrap">
    <div>
      <h2>도면이나 사양만 보내 주세요</h2>
      <p>롤러 종류, 파이프 외경, 길이, 수량을 알려 주시면 확인 후 견적을 드립니다. 도면 파일이 있으면 함께 보내 주세요.</p>
      <a class="btn" href="/contact">견적 문의하기</a>
    </div>
    <dl>
      <dt>전화</dt><dd><a href="tel:{COMPANY['tel']}">{COMPANY['tel']}</a></dd>
      <dt>팩스</dt><dd>{COMPANY['fax']}</dd>
      <dt>이메일</dt><dd><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></dd>
      <dt>본사</dt><dd>{COMPANY['hq']}</dd>
    </dl>
  </div>
</section>
"""


def catalog(cats=CATS, head_level="h3"):
    out = []
    for key, label, _ in cats:
        items = "".join(
            f'<li><a href="/product/{p["slug"]}"><img src="/img/{p["thumb"]}" alt="{e(p["name"])} 단면 이미지" width="300" height="113" loading="lazy"><strong>{e(p["name"])}</strong><span>{e(p["short"])}</span></a></li>'
            for p in P if p["cat"] == key)
        out.append(f'<div class="cat"><{head_level}>{label}</{head_level}><ul class="cat-list">{items}</ul></div>')
    return "\n".join(out)


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# 페이지 ---------------------------------------------------------------
def page_index():
    org = {
        "@context": "https://schema.org", "@type": "Organization",
        "name": COMPANY["name"], "alternateName": [BRAND, COMPANY["name_en"]],
        "url": SITE + "/", "logo": SITE + "/img/logo_top.gif",
        "telephone": "+82-2-2679-3225", "faxNumber": "+82-2-2679-9635", "email": COMPANY["email"],
        "address": {"@type": "PostalAddress", "streetAddress": "하성면 원산로 9", "addressLocality": "김포시",
                    "addressRegion": "경기도", "addressCountry": "KR"},
    }
    ld = f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>\n'
    body = f"""{header()}
<main id="main">
<section class="hero">
  <div class="wrap">
    <div>
      <h1>컨베이어 롤러,<br>사양대로 맞춰 만듭니다</h1>
      <p class="lead">MR·BR·스프라켓 롤러부터 캐리어·리턴 롤러, 풀리까지. 원하시는 사양과 납기에 맞춰 주문 제작하고, 100% 검수를 마친 뒤 납품합니다. 30년 넘게 컨베이어 롤러를 만들어 왔고, 지금은 연간 수백 개 고객사에 납품하고 있습니다.</p>
      <div class="actions">
        <a class="btn" href="/contact">견적 문의하기</a>
        <a class="btn ghost" href="/product/">제품 보기</a>
      </div>
      <p class="tel">전화 문의 <a href="tel:{COMPANY['tel']}">{COMPANY['tel']}</a></p>
    </div>
    <figure class="hero-drawing"><img src="/assets/hero-roller.svg" alt="컨베이어 롤러 단면 도면 – 파이프 외경, 축 지름, 롤러 길이를 주문 사양에 맞춰 제작" width="720" height="460"></figure>
  </div>
</section>

<section class="section" id="products">
  <div class="wrap">
    <div class="section-head">
      <h2>제품</h2>
      <div class="dim" aria-hidden="true"></div>
      <p>규격품 외에도 도면이나 사양에 맞춰 길이, 축, 재질을 바꿔 제작합니다.</p>
    </div>
    {catalog()}
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head">
      <h2>주문은 이렇게 진행됩니다</h2>
      <div class="dim" aria-hidden="true"></div>
    </div>
    <ol class="steps">
      <li><strong>문의</strong><span>도면이나 롤러 종류, 외경, 길이, 수량을 보내 주세요.</span></li>
      <li><strong>사양 확인·견적</strong><span>필요한 부분을 확인하고 견적을 드립니다.</span></li>
      <li><strong>주문 제작</strong><span>확정된 사양과 납기에 맞춰 가공·조립합니다.</span></li>
      <li><strong>검수·납품</strong><span>모든 제품을 100% 검수한 뒤 약속한 날짜에 납품합니다.</span></li>
    </ol>
  </div>
</section>

<section class="section" id="facilities">
  <div class="wrap split">
    <div class="section-head">
      <h2>가공 설비</h2>
      <div class="dim" aria-hidden="true"></div>
      <p>롤러에 들어가는 축 가공, 스프라켓 치형, 용접까지 공장 안에서 직접 합니다. 그래서 규격에 없는 사양도 원하시는 납기에 맞출 수 있습니다.</p>
    </div>
    <ul class="facts">
      <li><strong>CNC·MCT 가공</strong><span>축, 하우징, 풀리 등 정밀 부품 가공</span></li>
      <li><strong>호빙 가공</strong><span>스프라켓 치형 가공</span></li>
      <li><strong>용접</strong><span>레이저 용접, CO2 용접, 알곤(TIG) 용접 – 파이프·하우징·축·브라켓 접합</span></li>
      <li><strong>롤러 조립</strong><span>베어링 압입, 파이프 가공, 최종 조립과 100% 검수</span></li>
    </ul>
  </div>
</section>
</main>
{contact_band()}{FOOTER}"""
    write("index.html", head(f"컨베이어 롤러 제작 전문 | {BRAND}",
                             "신일콘베어는 30년 넘게 컨베이어 롤러를 전문으로 제작해 온 제조업체로, 원하시는 사양과 납기에 맞춰 주문 제작하고 100% 검수 후 납품합니다. MR·BR·스프라켓·어큐뮬레이션·링벨트·테이퍼 롤러와 캐리어·리턴·임팩트 롤러, 풀리를 규격에 맞춰 맞춤 제작합니다.",
                             "/", ld) + body)


def page_products():
    body = f"""{header('/product/')}
<main id="main">
<div class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/">홈</a> / 제품</p>
  <h1>컨베이어 롤러 제품<small>Products</small></h1>
  <p class="lead">자동화 롤러, 산업용 롤러, 풀리를 만듭니다. 제품을 누르면 규격과 도면을 볼 수 있습니다.</p>
</div></div>
<section class="section"><div class="wrap">
{catalog(head_level="h2")}
</div></section>
</main>
{contact_band()}{FOOTER}"""
    write("product/index.html", head(f"컨베이어 롤러 제품 – 자동화·산업용 롤러, 풀리 | {BRAND}",
                                     "신일콘베어 컨베이어 롤러 제품 – 자동화 롤러(MR, BR, 스프라켓, 어큐뮬레이션, 링벨트, 테이퍼), 산업용 롤러(캐리어·리턴, 자동조심, 임팩트), 헤드·테일·스냅 풀리를 맞춤 제작합니다.",
                                     "/product/") + body)


def page_product(p):
    cat_label = dict((k, l) for k, l, _ in CATS)[p["cat"]]
    pts = "".join(f"<li>{e(x)}</li>" for x in p["points"])
    spec = ""
    if p.get("spec"):
        s = p["spec"]
        th = "".join(f'<th scope="col">{e(h)}</th>' for h in s["head"])
        rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in s["rows"])
        spec = f"""<h2>규격</h2>
<div class="table-wrap"><table><caption class="note" style="caption-side:bottom;text-align:left;padding-top:8px">{e(s['caption'])}</caption><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">표에 없는 규격도 주문 사양에 맞춰 제작합니다.</p>"""
    figs = "".join(f'<figure><img src="/img/{f}" alt="{e(a)}" loading="lazy"></figure>' for f, a in p["imgs"])
    rel = "".join(f'<li><a href="/product/{q["slug"]}">{e(q["name"])}</a></li>' for q in P if q["cat"] == p["cat"] and q is not p)
    product_ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"],
                  "description": p["lead"], "image": f"{SITE}/img/{p['thumb']}",
                  "brand": {"@type": "Brand", "name": BRAND}, "manufacturer": {"@type": "Organization", "name": COMPANY["name"]}}
    ld = f'<script type="application/ld+json">{json.dumps(product_ld, ensure_ascii=False)}</script>\n'
    body = f"""{header('/product/')}
<main id="main">
<div class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/">홈</a> / <a href="/product/">제품</a> / {cat_label}</p>
  <h1>{e(p['name'])}<small>{e(p['en'])}</small></h1>
</div></div>
<div class="wrap">
  <div class="product-top">
    <figure><img src="/img/{p['thumb']}" alt="{e(p['name'])} 단면 이미지" width="300" height="113"></figure>
    <div>
      <p>{e(p['lead'])}</p>
      <ul>{pts}</ul>
      <a class="btn" href="/contact?product={p['slug']}">{e(p['name'])} 견적 문의</a>
    </div>
  </div>
  <div class="prose">
    {spec}
    <h2>도면·규격 자료</h2>
    <div class="drawings">{figs}</div>
  </div>
  <div class="quote-box">
    <p>필요한 길이·축 사양이 표와 다르면 도면이나 메모로 보내 주세요. 확인 후 견적을 드립니다.</p>
    <a class="btn" href="/contact?product={p['slug']}">견적 문의하기</a>
  </div>
  <section class="section" style="padding-top:48px">
    <h2 style="font-size:18px;margin-bottom:12px">같은 분류의 제품</h2>
    <ul class="related">{rel}</ul>
  </section>
</div>
</main>
{FOOTER}"""
    write(f"product/{p['slug']}.html", head(f"{p['title']} | {BRAND}", p["desc"], f"/product/{p['slug']}", ld) + body)


def page_about():
    c = COMPANY
    body = f"""{header('/about/overview')}
<main id="main">
<div class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/">홈</a> / 회사소개</p>
  <h1>회사소개<small>About us</small></h1>
  <p class="lead">컨베이어 롤러가 필요할 때, 사양만 주시면 나머지는 신일콘베어가 책임집니다. 30년 넘게 컨베이어 롤러 한 길만 걸어온 전문 제조사로서, 원하시는 사양과 납기에 정확히 맞춰 만들고 100% 검수한 제품만 내보냅니다.</p>
</div></div>
<section class="section"><div class="wrap split">
  <div class="section-head">
    <h2>신일콘베어를 선택하는 이유</h2>
    <div class="dim" aria-hidden="true"></div>
    <p>연간 수백 개 컨베이어 제작업체가 신일콘베어 롤러로 라인을 완성합니다. 규격품이든 처음 보는 사양이든, 한 곳에서 빠르고 정확하게 해결하기 때문입니다.</p>
  </div>
  <ul class="facts">
    <li><strong>원하는 사양 그대로</strong><span>파이프 외경, 길이, 축, 재질, 스프라켓까지 도면 한 장이면 맞춤 제작합니다.</span></li>
    <li><strong>원하는 날짜에</strong><span>축 가공부터 스프라켓, 용접, 조립까지 공장 안에서 직접 하기 때문에 외주를 기다릴 일이 없습니다.</span></li>
    <li><strong>100% 검수 후 납품</strong><span>샘플 검사가 아니라 모든 제품을 하나하나 검수한 뒤 내보냅니다.</span></li>
    <li><strong>롤러부터 풀리까지</strong><span>자동화 롤러, 산업용 롤러, 풀리 12종을 한 곳에서 공급합니다.</span></li>
    <li><strong>직접 보유한 설비</strong><span>CNC·MCT 가공, 호빙, 레이저·CO2·알곤 용접</span></li>
  </ul>
</div></section>
<section class="section alt"><div class="wrap" style="max-width:820px">
  <div class="section-head"><h2>대표 인사말</h2><div class="dim" aria-hidden="true"></div></div>
  <p style="font-size:20px;font-weight:700;line-height:1.5;margin-bottom:24px">"좋은 컨베이어는 좋은 롤러에서 시작합니다. 그 롤러를 가장 잘 만드는 회사가 되겠습니다."</p>
  <p>신일콘베어㈜는 설립 이래 30년 넘게 컨베이어 롤러 하나에만 집중해 왔습니다. 그 시간 동안 쌓은 노하우로 지금은 연간 수백 개 고객사의 컨베이어 라인에 롤러를 납품하고 있습니다.</p>
  <p>저희가 고객사에 드리는 약속은 분명합니다. 원하시는 사양 그대로, 원하시는 날짜에, 100% 검수한 제품으로 납품하는 것입니다. 이 약속을 지키기 위해 CNC·MCT 가공, 호빙, 레이저·CO2·알곤 용접 설비를 직접 갖추고 모든 공정을 공장 안에서 책임지고 있습니다.</p>
  <p>규격품이 맞지 않아 고민이시거나, 납기가 급하시거나, 지금 쓰는 롤러의 품질이 아쉬우시다면 신일콘베어에 맡겨 주십시오. 도면 한 장, 전화 한 통이면 충분합니다. 고객사의 라인이 멈추지 않도록 끝까지 책임지겠습니다.</p>
  <p style="font-weight:700;margin-top:24px">{c['name']} 대표이사 {c['ceo']}</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>오시는 길</h2><div class="dim" aria-hidden="true"></div></div>
  <div class="sites">
    <div class="site-card">
      <h3>본사 · 제1공장</h3>
      <p>{c['hq']}</p>
      <p>전화 {c['tel']} · 팩스 {c['fax']}</p>
      <a href="https://map.naver.com/p/search/{c['hq']}" target="_blank" rel="noopener">네이버 지도에서 보기</a>
    </div>
    <div class="site-card">
      <h3>제2공장 · 창고</h3>
      <p>{c['plant2']}</p>
      <p>전화 {c['tel']}</p>
      <a href="https://map.naver.com/p/search/{c['plant2']}" target="_blank" rel="noopener">네이버 지도에서 보기</a>
    </div>
  </div>
</div></section>
</main>
{contact_band()}{FOOTER}"""
    write("about/overview.html", head(f"회사소개 – 김포 컨베이어 롤러 제조 | {BRAND}",
                                      "30년 넘게 컨베이어 롤러만 만들어 온 신일콘베어㈜. 원하시는 사양과 납기에 맞춰 주문 제작하고 100% 검수 후 연간 수백 개 고객사에 납품합니다. 회사소개와 오시는 길.",
                                      "/about/overview") + body)


def page_contact():
    c = COMPANY
    opts = "".join(f'<option value="{p["slug"]}">{e(p["name"])}</option>' for p in P)
    body = f"""{header('/contact')}
<main id="main">
<div class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/">홈</a> / 견적 문의</p>
  <h1>견적 문의<small>Request a quote</small></h1>
  <p class="lead">롤러 종류와 사양, 수량을 남겨 주시면 확인 후 연락드립니다. 도면 파일을 첨부하시면 더 정확한 견적을 드릴 수 있습니다.</p>
</div></div>
<div class="wrap contact-layout">
  <form name="quote" method="POST" action="/contact-thanks" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data">
    <input type="hidden" name="form-name" value="quote">
    <p class="hp"><label>입력하지 마세요 <input name="bot-field"></label></p>
    <div class="form-grid">
      <div class="field"><label for="company">회사명 <span class="req">*</span></label><input id="company" name="company" required autocomplete="organization"></div>
      <div class="field"><label for="person">담당자 <span class="req">*</span></label><input id="person" name="person" required autocomplete="name"></div>
      <div class="field"><label for="phone">연락처 <span class="req">*</span></label><input id="phone" name="phone" type="tel" required autocomplete="tel" inputmode="tel"></div>
      <div class="field"><label for="email">이메일</label><input id="email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="product">제품 종류</label><select id="product" name="product"><option value="">선택해 주세요</option>{opts}<option value="etc">기타 / 잘 모르겠음</option></select></div>
      <div class="field"><label for="qty">수량</label><input id="qty" name="qty" placeholder="예: 200개"></div>
      <div class="field full"><label for="message">요청 사양 <span class="req">*</span></label><textarea id="message" name="message" required placeholder="파이프 외경, 길이, 축 지름, 재질, 납기 등 아는 만큼 적어 주세요."></textarea></div>
      <div class="field full"><label for="file">도면·사양 파일</label><input id="file" name="file" type="file" accept=".pdf,.dwg,.dxf,.jpg,.jpeg,.png,.xlsx,.xls,.zip"><span class="hint">PDF, DWG, DXF, 이미지, 엑셀 파일 한 개 (8MB 이하). 여러 개면 압축해서 올려 주세요.</span></div>
      <div class="consent">
        <p style="margin:0">수집 항목: 회사명, 담당자, 연락처, 이메일 · 이용 목적: 견적 회신과 상담 · 보유 기간: 문의 처리 후 1년. 동의하지 않으면 견적 문의를 보낼 수 없습니다.</p>
        <label><input type="checkbox" name="consent" value="동의" required> 개인정보 수집·이용에 동의합니다</label>
      </div>
      <div class="field full"><button class="btn" type="submit">견적 문의 보내기</button></div>
    </div>
  </form>
  <aside class="contact-aside">
    <h2 style="font-size:20px;margin-bottom:12px">전화·메일로 문의</h2>
    <dl>
      <dt>전화</dt><dd><a href="tel:{c['tel']}">{c['tel']}</a></dd>
      <dt>팩스</dt><dd>{c['fax']}</dd>
      <dt>이메일</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd>
    </dl>
    <p class="note" style="margin-top:16px">{c['hq']}</p>
  </aside>
</div>
</main>
<script>
(function(){{var m=location.search.match(/product=([a-z0-9]+)/),s=document.getElementById('product');
if(m&&s){{for(var i=0;i<s.options.length;i++)if(s.options[i].value===m[1])s.selectedIndex=i;}}}})();
</script>
{FOOTER}"""
    write("contact.html", head(f"견적 문의 – 컨베이어 롤러 맞춤 제작 | {BRAND}",
                               "컨베이어 롤러·풀리 견적 문의. 롤러 종류와 사양, 수량, 도면 파일을 보내 주시면 신일콘베어가 확인 후 견적을 드립니다. 전화 02-2679-3225",
                               "/contact") + body)

    thanks = f"""{header()}
<main id="main">
<div class="page-head"><div class="wrap">
  <h1>견적 문의가 접수되었습니다</h1>
  <p class="lead">보내 주신 사양을 확인한 뒤 남겨 주신 연락처로 회신드리겠습니다. 급한 건은 {c['tel']}로 전화 주세요.</p>
  <p style="margin-top:24px"><a class="btn ghost" href="/product/">제품 더 보기</a></p>
</div></div>
</main>
{FOOTER}"""
    write("contact-thanks.html", head(f"견적 문의 접수 | {BRAND}", "견적 문의가 접수되었습니다.", "/contact-thanks",
                                      '<meta name="robots" content="noindex">\n') + thanks)


def extras():
    urls = ["/", "/product/", "/about/overview", "/contact"] + [f"/product/{p['slug']}" for p in P]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n")
    r = ["# 예전 주소 → 새 주소 (검색 순위 유지용 301 이동)",
         "/product/product.html  /product/  301", "/product/product  /product/  301",
         "/product.html  /product/  301", "/product  /product/  301",
         "/overview.html  /about/overview  301", "/overview  /about/overview  301",
         "/about/sub.html  /about/overview  301", "/about/sub  /about/overview  301",
         ]
    from urllib.parse import quote
    for k in ["테이퍼", quote("테이퍼")]:
        r += [f"/product/{k}.html  /product/taper  301", f"/product/{k}  /product/taper  301",
              f"/{k}.html  /product/taper  301", f"/{k}  /product/taper  301"]
    for s in ["MR", "BR", "chain", "accum", "idler", "impact", "pully", "pully2", "pully3", "return", "ringbelt"]:
        r += [f"/{s}.html  /product/{s.lower()}  301", f"/{s}  /product/{s.lower()}  301"]
        if s != s.lower():
            r += [f"/product/{s}.html  /product/{s.lower()}  301", f"/product/{s}  /product/{s.lower()}  301"]
    r += ["/tools/*  /404  404"]
    write("_redirects", "\n".join(r) + "\n")


if __name__ == "__main__":
    page_index(); page_products(); page_about(); page_contact()
    for p in P:
        page_product(p)
    extras()
    print("built", 4 + len(P), "pages")
