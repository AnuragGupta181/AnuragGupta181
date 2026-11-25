#!/usr/bin/env python3
"""Generate neofetch-style profile cards (card-dark.svg / card-light.svg).

Usage: python3 scripts/make_card.py   (run from the repo root)
"""
from html import escape
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / "man.jpg"

COLS, ROWS = 66, 40
RAMP = " .:-=+*#%@"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"

# ---- ASCII portrait -------------------------------------------------------
def ascii_portrait(dark_bg: bool):
    im = Image.open(PHOTO).convert("L")
    w, h = im.size
    im = im.crop((int(w * 0.08), int(h * 0.05), int(w * 0.92), int(h * 0.62)))  # head + torso
    im = ImageOps.equalize(im)
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=3)
    px = im.load()
    lines = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            v = px[x, y] / 255
            v = min(1.0, max(0.0, (v - 0.12) / 0.88)) ** 0.8
            # on dark bg bright pixels -> dense chars; on light bg the reverse
            d = 1 - v  # subject (darker than backdrop) -> dense chars
            row += RAMP[min(int(d ** 1.1 * (len(RAMP) - 1)), len(RAMP) - 1)]
        lines.append(row.rstrip())
    return lines

# ---- Info panel -----------------------------------------------------------
W = 62  # panel width in chars

def kv(key, val):
    dots = max(2, W - len(key) - len(val) - 3)
    return ("kv", key, "." * dots, val)

def head(title):
    return ("head", title, "-" * max(2, W - len(title) - 2))

INFO = [
    head("anurag@gupta "),
    kv("Role:", "Software Engineer, DevOps"),
    kv("Uptime:", "1+ year hands-on"),
    kv("Host:", "LFX Mentee, The Linux Foundation"),
    kv("Project:", "GitMesh (open source)"),
    kv("Lead:", "ML & DevOps, Cloud Computing Cell"),
    kv("Campus:", "AKGEC, Ghaziabad, India"),
    ("blank",),
    kv("Lang.Programming:", "Python, TypeScript, JS, C++"),
    kv("Lang.Query:", "SQL, Bash"),
    kv("Focus.Backend:", "Node.js, FastAPI, Redis"),
    kv("Focus.Cloud:", "AWS, Docker, K8s, CI/CD"),
    kv("Focus.AI:", "MCP, RAG, LoRA, OCR"),
    kv("Focus.Robotics:", "ROS 2, PX4, ESP32"),
    ("blank",),
    kv("Hobbies.Software:", "Open source, Agentic AI"),
    kv("Hobbies.Hardware:", "Drones, LabVIEW, Edge AI"),
    ("blank",),
    head("- Contact "),
    kv("Email:", "job4anurag11@gmail.com"),
    kv("LinkedIn:", "anuragg1817"),
    kv("GitHub:", "AnuragGupta181"),
    kv("Website:", "anurag11.tech"),
    kv("X:", "@AnuragGupt1817"),
    kv("Linktree:", "linktr.ee/anuraggupta11"),
    kv("Book a call:", "cal.com/anurag-gupta-11"),
    ("blank",),
    head("- Stats "),
    kv("Merged PRs:", "25+"),
    kv("Users served at once:", "250+ (AWS, ~$50)"),
    kv("Resumes:", "5 role-specific"),
    kv("Education:", "B.Tech ECE, CGPA 7.2"),
]

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", art="#cfa355", key="#cfa355",
                 val="#e6edf3", dots="#484f58", head="#e6edf3", dim="#8b949e"),
    "light": dict(bg="#ffffff", border="#d0d7de", art="#8a5a00", key="#9a6700",
                  val="#1f2328", dots="#afb8c1", head="#1f2328", dim="#656d76"),
}

def build(name: str) -> str:
    t = THEMES[name]
    art = ascii_portrait(name == "dark")
    fs, lh = 8, 9.6            # art font size / line height
    ifs, ilh = 12, 17         # info font size / line height
    cw_art, cw_info = fs * 0.6, ifs * 0.6
    pad = 24
    art_w = COLS * cw_art
    info_x = pad + art_w + 28
    width = int(info_x + W * cw_info + pad)
    height = int(max(ROWS * lh, len(INFO) * ilh) + pad * 2 + 8)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="Anurag Gupta, neofetch-style profile card">',
         f'<style>text{{font-family:{FONT};white-space:pre}}'
         f'.a{{font-size:{fs}px;fill:{t["art"]}}}.i{{font-size:{ifs}px}}'
         f'.k{{fill:{t["key"]}}}.v{{fill:{t["val"]}}}.d{{fill:{t["dots"]}}}.h{{fill:{t["head"]};font-weight:700}}'
         f'.c{{animation:b 1.2s steps(1) infinite}}@keyframes b{{50%{{opacity:0}}}}</style>',
         f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}"/>']

    y0 = pad + (height - pad * 2 - ROWS * lh) / 2 + lh
    o.append(f'<g class="a" xml:space="preserve">')
    for i, line in enumerate(art):
        if line.strip():
            o.append(f'<text class="a" x="{pad}" y="{y0 + i*lh:.1f}">{escape(line)}</text>')
    o.append('</g>')

    y = pad + (height - pad * 2 - len(INFO) * ilh) / 2 + ilh - 3
    for row in INFO:
        if row[0] == "head":
            o.append(f'<text class="i h" x="{info_x}" y="{y}">{escape(row[1])}<tspan class="d" font-weight="400">{row[2]}</tspan></text>')
        elif row[0] == "kv":
            o.append(f'<text class="i" x="{info_x}" y="{y}"><tspan class="d">. </tspan>'
                     f'<tspan class="k">{escape(row[1])}</tspan> <tspan class="d">{row[2]}</tspan> '
                     f'<tspan class="v">{escape(row[3])}</tspan></text>')
        y += ilh
    o.append(f'<text class="i c" x="{info_x}" y="{y}" fill="{t["key"]}">&#9608;</text>')
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    for n in THEMES:
        (ROOT / f"card-{n}.svg").write_text(build(n), encoding="utf-8")
        print("wrote", f"card-{n}.svg")
