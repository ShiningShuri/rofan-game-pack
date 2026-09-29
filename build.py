"""게임팩 빌드: pack_core.md → dist/ 에 HTML·TXT 생성.

사용법:
  python build.py                      # 이미지 없는 버전 (삽화는 이름만 표시)
  python build.py https://주소/         # 이미지 주소를 넣은 배포 버전 (img/ 가 그 주소에 올라가 있어야 함)
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

IMAGES = [
    ("opening", "몰락한 저택 전경, 에스텔라와 루시안", "공녀 게임 시작·영지·귀환"),
    ("cast", "주요 인물 단체", "인물 소개·전원 집합"),
    ("debt", "집무실 빚 장부 폭탄", "재정 보고·빚·회계"),
    ("chicken", "닭아빠 심문 스포트라이트", "닭아빠·선대 공작"),
    ("inlaw", "황궁 상견례, 카엘란과 닭 장인어른", "황실·카엘란·협상"),
    ("farm", "황금 양계장", "사업·생산·납품"),
    ("wedding", "황실 결혼식·대관식", "로맨스·경사"),
    ("bitnyang", "빛냥이 신수 강림과 굿즈 상상", "빛냥이·굿즈·신수"),
    ("nursery", "전황제 카샤카샤 육아, 삼냥이", "육아·전황제·삼냥이"),
    ("dragon", "삐진 수호룡과 굿즈, 닭아빠 절친", "수호룡·계약"),
    ("catcity", "냥천시티 노동묘 노조 시위", "냥천시티·고양이 노동·온천"),
    ("golem", "고대 온천 골렘 수건 감사", "유적·조사·감사·골렘"),
    ("crisis", "밤의 채권단 습격", "위기·사기·재난·압류"),
    ("gold", "금화 비 대성공", "대박·결산·축하"),
    ("demon", "편의점 카운터의 혼란스러운 마왕", "마왕 편의점 게임 전반"),
    ("cathusband", "한밤중 침실, 계약서와 치즈냥이 남편", "고양이 남편 게임 전반"),
    ("idol", "반지하 연습실의 한별과 멤버들", "소속사 게임 전반"),
    ("custom", "펼쳐진 마법의 책", "내맘대로 세계관 시작"),
]

OFFLINE_MODE = """이 버전은 이미지 파일이 없다. 삽화를 표시할 때는 본문 위에 다음 한 줄만 쓴다.
`🖼️ 삽화: (장면 이름)` — 예: `🖼️ 삽화: 닭아빠 심문 스포트라이트`
이미지를 생성하거나 검색하지 않는다."""

ONLINE_MODE = """삽화는 반드시 **클릭 가능한 링크** 한 줄로 넣는다(마크다운 이미지 `![]()` 문법은 쓰지 않는다 — 대부분의 AI 화면에서 빈칸이 된다).
형식: `🖼️ [삽화 보기: 장면 이름](주소)`
예: `🖼️ [삽화 보기: 닭아빠 심문 스포트라이트](BASEimg/chicken.webp)`
주소는 [삽화 목록]에 적힌 것을 글자 하나 바꾸지 말고 그대로 쓴다. 이미지를 새로 생성하거나 검색하지 않는다."""


def build(base: str | None):
    core = open(os.path.join(HERE, "pack_core.md"), encoding="utf-8").read()
    if base:
        base = base.rstrip("/") + "/"
        mode = ONLINE_MODE.replace("BASE", base)
        rows = "\n".join(f"| {k} | {d} | {w} · 주소: {base}img/{k}.webp |" for k, d, w in IMAGES)
        suffix = ""
    else:
        mode = OFFLINE_MODE
        rows = "\n".join(f"| {k} | {d} | {w} |" for k, d, w in IMAGES)
        suffix = "_이미지없음"
    text = core.replace("{{IMAGE_MODE}}", mode).replace("{{IMAGE_TABLE}}", rows)

    out = os.path.join(HERE, "dist")
    os.makedirs(out, exist_ok=True)
    name = f"막장로판_게임팩{suffix}"
    with open(os.path.join(out, name + ".txt"), "w", encoding="utf-8") as f:
        f.write(text)
    gallery = ""
    if base:
        gallery = '<div class="gal">' + "".join(
            f'<a href="{base}img/{k}.webp" target="_blank"><img src="{base}img/{k}.webp" alt="{html.escape(d)}" loading="lazy"></a>'
            for k, d, _ in IMAGES) + "</div>"
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>막장 로판 게임팩</title>
<style>
body{{margin:0;background:#1a1222;color:#f5ecdc;font:15px/1.7 "Malgun Gothic","Apple SD Gothic Neo",sans-serif;word-break:keep-all}}
.w{{max-width:860px;margin:0 auto;padding:24px 16px 60px}}
.how{{background:#261a31;border:1px solid #8a6d3b;border-radius:14px;padding:14px 18px;margin-bottom:18px}}
.how b{{color:#e0bd72}}
.gal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-bottom:18px}}
.gal img{{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:10px;display:block}}
pre{{white-space:pre-wrap;background:#221729;border:1px solid #4a3760;border-radius:14px;padding:18px;font:14px/1.7 inherit}}
</style></head><body><div class="w">
<div class="how"><b>사용법</b> — 이 파일을 ChatGPT·Gemini·Claude 대화창에 첨부하고 <b>「게임 실행해줘」</b>라고 보내세요. 첨부가 안 되면 아래 내용을 전부 복사해서 붙여넣고 보내면 됩니다.</div>
{gallery}
<pre>
{html.escape(text)}
</pre>
</div></body></html>"""
    with open(os.path.join(out, name + ".html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("built", name, len(text), "chars")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
