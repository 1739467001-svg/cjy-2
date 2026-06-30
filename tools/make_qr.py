#!/usr/bin/env python3
"""Generate the CJY brand "ecosystem-tank" QR poster -> public/qr.png.

Pure Python (Pillow + segno via tools/qrkit) — no browser. ECC level H lets the
centre 🦞 ride on the code. Re-run after changing URL:  python3 tools/make_qr.py
"""
import pathlib
from PIL import Image, ImageDraw
import qrkit as K
from qrkit import S, INK, PAPER, LIME, BLUE_HI, BLUE_LO

URL     = "https://cjy-webpage.zeabur.app"
DISPLAY = "cjy-webpage.zeabur.app"

W, H = 920 * S, 1300 * S
CARD_X, CARD_Y = 50 * S, 65 * S
CW, CH = 820 * S, 1170 * S


def caption(card, cx, y, text, emoji="🦞", fsize=27):
    """Centered bold caption with a trailing colour emoji. `y` is the text top;
    returns the height occupied (text/emoji, whichever is taller) for stacking."""
    f = K.font(fsize * S)
    d = ImageDraw.Draw(card)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    em = K.emoji_img(emoji, fsize * 1.15 * S)
    gap = 12 * S
    total = tw + gap + em.width
    x = cx - total / 2
    d.text((x + 2 * S, y + 2 * S), text, font=f, fill=(INK[0], INK[1], INK[2], 100))
    d.text((x, y), text, font=f, fill=(255, 255, 255, 255))
    em_top = y + th / 2 - em.height / 2 + bb[1]
    K.paste(card, em, (x + tw + gap, em_top), "lt")
    return int(max(bb[3], em_top + em.height - y))


def build():
    base = K.grid_bg(W, H)

    # ---- card layer (own image for clean rounded clip) ----
    card = K.vgrad(CW, CH, BLUE_HI, BLUE_LO)
    K.rays(card, [(0.12, 95, 0.16), (0.46, 95, 0.10), (0.78, 120, 0.15)])
    K.bubbles(card, [(0.08, 0.24, 18), (0.88, 0.30, 11), (0.84, 0.54, 26),
                     (0.14, 0.60, 9), (0.06, 0.78, 15), (0.92, 0.80, 13)])

    # header + chips
    K.brand_header(card, 50 * S, 46 * S)
    K.chips_row(card, CW / 2, 132 * S,
                [("AI 教育系统数字化", False), ("未来课堂探索", False), ("AI 多模态", True)])

    # QR glass panel
    rows, ver = K.qr_matrix(URL)
    box = K.qr_panel(card, (CW / 2, 506 * S), 520 * S, rows, pad=30, knockout=0.20)
    panel_bottom = box[3] + 11 * S          # include the panel's drop shadow

    # caption + url — stacked below the panel with guaranteed gaps (no overlap)
    cap_y = panel_bottom + 30 * S
    cap_h = caption(card, CW / 2, cap_y, "扫码游进我的生态缸")
    url = K.pill(DISPLAY, 20, INK, LIME, px=22, py=11, bw=3, mono=True, tracking=1.2)
    K.paste(card, url, (CW / 2, cap_y + cap_h + 26 * S), "ct")

    # planted floor
    K.seaweed(card, CH - 6 * S,
              [(0.06, 118), (0.15, 150), (0.26, 96), (0.50, 140),
               (0.70, 108), (0.80, 150), (0.91, 124)])
    K.pebbles(card, CH - 6 * S,
              [(0.04, 40), (0.12, 30), (0.20, 46), (0.33, 34), (0.48, 52),
               (0.63, 30), (0.78, 44), (0.90, 36), (0.97, 40)])
    # drifting fish in the side margins (clear of the code)
    K.fishes(card, [(0.075, 0.40, 1, K.PINK), (0.93, 0.53, -1, (61, 220, 151)),
                    (0.085, 0.72, 1, LIME)])

    # ---- composite card onto base: shadow + rounded clip + border ----
    rad = 36 * S
    d = ImageDraw.Draw(base)
    so = 16 * S
    K.rrect(d, (CARD_X + so, CARD_Y + so, CARD_X + CW + so, CARD_Y + CH + so), rad, fill=INK)
    mask = Image.new("L", (CW, CH), 0)
    K.rrect(ImageDraw.Draw(mask), (0, 0, CW - 1, CH - 1), rad, fill=255)
    base.paste(card, (CARD_X, CARD_Y), mask)
    K.rrect(d, (CARD_X, CARD_Y, CARD_X + CW, CARD_Y + CH), rad, outline=INK, width=8 * S)

    out = pathlib.Path(__file__).resolve().parent.parent / "public" / "qr.png"
    K.finish(base, out)
    print(f"wrote {out}  ({W//S}x{H//S})  url={URL}  qr v{ver} ecc=H")


if __name__ == "__main__":
    build()
