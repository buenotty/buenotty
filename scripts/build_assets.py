"""Builds assets/hero.svg and assets/skills.svg (self-hosted, animated, no third-party service).

Icons come from simple-icons (CC0): put them in scripts/icons/<slug>.svg first.
Run: python3 scripts/build_assets.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = Path(__file__).resolve().parent / "icons"
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

FONT = "'JetBrains Mono','SF Mono',Menlo,Consolas,monospace"


# ---------------------------------------------------------------- hero
def hero() -> str:
    lines = [
        ("Olá, bem-vindo(a) ao meu perfil!", 30, "#9ecbff", 0.4),
        ("Meu nome é Samuel Bueno", 44, "#ffffff", 3.0),
        ("Engenheiro de Dados e IA aplicada", 26, "#7ee787", 5.6),
        ("Construo agentes, automações e dados que funcionam.", 19, "#c9d1d9", 7.8),
    ]
    y, body, clips = 72, [], []
    for i, (text, size, color, begin) in enumerate(lines):
        width = len(text) * size * 0.62
        dur = max(1.2, len(text) * 0.055)
        steps = len(text)
        vals = ";".join(f"{width * k / steps:.1f}" for k in range(steps + 1))
        clips.append(
            f'<clipPath id="c{i}"><rect x="40" y="{y - size}" height="{size * 1.5:.0f}" width="0">'
            f'<animate attributeName="width" values="{vals}" begin="{begin}s" dur="{dur:.2f}s" fill="freeze"/>'
            f"</rect></clipPath>"
        )
        body.append(
            f'<text x="40" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="700" fill="{color}" '
            f'clip-path="url(#c{i})">{text}</text>'
        )
        y += size + 24
    body.append(
        f'<rect x="40" y="{y - 20}" width="12" height="24" fill="#58a6ff">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'
    )
    particles = "".join(
        f'<circle cx="{(37 * k) % 860}" cy="{(53 * k) % 300}" r="{1 + k % 3}" fill="#58a6ff" opacity=".35">'
        f'<animate attributeName="cy" values="{(53 * k) % 300};{((53 * k) % 300) - 40};{(53 * k) % 300}" '
        f'dur="{6 + k % 5}s" repeatCount="indefinite"/></circle>'
        for k in range(1, 28)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="900" height="320" role="img" aria-label="Olá, bem-vindo ao meu perfil. Meu nome é Samuel Bueno, engenheiro de dados e IA aplicada.">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0d1117"/><stop offset=".55" stop-color="#161b22"/><stop offset="1" stop-color="#0b2545"/>
</linearGradient>
{''.join(clips)}
</defs>
<rect width="900" height="320" rx="18" fill="url(#bg)"/>
{particles}
<rect x="1" y="1" width="898" height="318" rx="17" fill="none" stroke="#30363d"/>
{''.join(body)}
</svg>
"""


# ---------------------------------------------------------------- skills
def path_of(slug: str) -> str:
    text = (ICONS / f"{slug}.svg").read_text(encoding="utf-8")
    return re.search(r'<path d="([^"]+)"', text).group(1)


def simple(slug, color):
    return f'<path transform="translate(-12 -12)" d="{path_of(slug)}" fill="{color}"/>'


CUSTOM = {
    # Hermes Agent has no public icon: a neutral winged monogram
    "hermes-agent": (
        '<g fill="none" stroke="#e3b341" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M-6 -9v18M6 -9v18M-6 0h12"/><path d="M-11 -5l-6 3 6 1M11 -5l6 3-6 1"/></g>'
    ),
    "mcp": (
        '<g fill="none" stroke="#a5d6ff" stroke-width="2" stroke-linecap="round">'
        '<circle cx="-8" cy="6" r="3.4"/><circle cx="8" cy="6" r="3.4"/><circle cx="0" cy="-8" r="3.4"/>'
        '<path d="M-5.6 3.6L-2.4 -5M5.6 3.6L2.4 -5M-4.6 6h9.2"/></g>'
    ),
    "sql": (
        '<g fill="none" stroke="#79c0ff" stroke-width="2"><ellipse cx="0" cy="-8" rx="9" ry="3.5"/>'
        '<path d="M-9 -8v16c0 2 4 3.5 9 3.5s9-1.5 9-3.5V-8M-9 0c0 2 4 3.5 9 3.5s9-1.5 9-3.5"/></g>'
    ),
}

GROUPS = [
    ("IA e agentes", [("Claude", "claude", "#D97757"), ("Codex", "openai", "#ffffff"),
                      ("Gemini", "googlegemini", "#8AB4F8"), ("Hermes Agent", None, "hermes-agent"),
                      ("MCP", None, "mcp")]),
    ("Programação", [("Python", "python", "#4B8BBE"), ("JavaScript", "javascript", "#F7DF1E"),
                     ("HTML", "html5", "#E34F26"), ("CSS", "css3", "#1572B6"),
                     ("Kotlin", "kotlin", "#A97BFF"), ("Rust", "rust", "#DEA584")]),
    ("Dados", [("SQL", None, "sql"), ("Power BI", "powerbi", "#F2C811"),
               ("Looker Studio", "looker", "#6C9EF8"), ("Excel", "microsoftexcel", "#33C481")]),
    ("Ferramentas", [("Docker", "docker", "#2496ED"), ("Git", "git", "#F05032"), ("GitHub", "github", "#ffffff")]),
]


def skills() -> str:
    tile_w, tile_h, gap, per_row, left, top = 120, 104, 16, 6, 30, 20
    parts, y, n = [], top, 0
    for title, items in GROUPS:
        parts.append(
            f'<text x="{left}" y="{y + 14}" font-family="{FONT}" font-size="15" font-weight="700" fill="#8b949e">{title}</text>'
        )
        y += 28
        for i, (label, slug, color) in enumerate(items):
            x = left + (i % per_row) * (tile_w + gap)
            cy = y + (i // per_row) * (tile_h + gap)
            icon = simple(slug, color) if slug else CUSTOM[color]
            delay = n * 0.12
            parts.append(
                f'<g class="t" style="animation-delay:{delay:.2f}s" transform="translate({x} {cy})">'
                f'<g class="f" style="animation-delay:{delay + 1:.2f}s">'
                f'<rect width="{tile_w}" height="{tile_h}" rx="14" fill="#161b22" stroke="#30363d"/>'
                f'<g transform="translate({tile_w / 2} 42) scale(1.6)">{icon}</g>'
                f'<text x="{tile_w / 2}" y="88" text-anchor="middle" font-family="{FONT}" font-size="12.5" '
                f'font-weight="600" fill="#c9d1d9">{label}</text></g></g>'
            )
            n += 1
        rows = (len(items) + per_row - 1) // per_row
        y += rows * (tile_h + gap) + 6
    height = y + 6
    width = left * 2 + per_row * tile_w + (per_row - 1) * gap
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Tecnologias que uso: Claude, Codex, Gemini, Hermes Agent, MCP, Python, JavaScript, HTML, CSS, Kotlin, Rust, SQL, Power BI, Looker Studio, Excel, Docker, Git e GitHub">
<style>
.t{{opacity:0;animation:in .6s ease-out forwards}}
.f{{animation:float 4.5s ease-in-out infinite}}
@keyframes in{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
</style>
<rect width="{width}" height="{height}" rx="18" fill="#0d1117"/>
{''.join(parts)}
</svg>
"""


(OUT / "hero.svg").write_text(hero(), encoding="utf-8")
(OUT / "skills.svg").write_text(skills(), encoding="utf-8")
print("ok", (OUT / "hero.svg").stat().st_size, (OUT / "skills.svg").stat().st_size)
