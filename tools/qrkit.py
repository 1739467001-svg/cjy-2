#!/usr/bin/env python3
"""qrkit — pure-Python (Pillow + segno) toolkit for CJY brand QR posters.

No browser needed. Renders at 3× and downsamples (LANCZOS) for clean edges,
mirroring tools/covers.py. Encodes with ECC level H so a centre 🦞 logo can
sit on the code (knockout ≈4% area, well inside H's ~30% budget). The code
stays ink-on-cream for max scan contrast; brand colour lives in the frame.

Primitives here are deliberately high-level so layout variants stay short:
    panel()  pill()  qr_panel()  bubbles()  rays()  seaweed()  pebbles()
    fish()   emoji_img()  brand_header()  grid_bg()  finish()

Shared palette + fonts match public/styles.css.
"""
import os, math, pathlib
import numpy as np
import segno
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- brand palette (== styles.css :root) --------------------------------
PAPER   = (247, 242, 228)   # #F7F2E4 warm cream
PAPER2  = (255, 251, 240)   # #FFFBF0
INK     = (20, 17, 11)      # #14110B near-black
RED     = (255, 77, 28)     # #FF4D1C lobster red
BLUE    = (43, 71, 240)     # #2B47F0 electric blue
BLUE_HI = (58, 84, 241)     # #3a54f1 card top
BLUE_LO = (31, 55, 200)     # #1f37c8 card bottom
LIME    = (200, 255, 45)    # #C8FF2D acid lime
PINK    = (255, 93, 162)    # #FF5DA2
GREENS  = [(200, 255, 45), (61, 220, 151), (31, 158, 110)]
PEBBLES = [(203, 182, 138), (167, 162, 144), (134, 160, 90), (94, 107, 73)]

S = 3  # supersample factor
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
WQY   = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
LAT   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"       # Latin display
MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"   # mono labels / URL

_fc = {}
def font(size, mono=False):
    """CJK-capable sans (wqy-zenhei). index 0 = proportional, 2 = mono."""
    key = (round(size), mono)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(WQY, int(round(size)), index=(2 if mono else 0))
    return _fc[key]

def font_lat(size):
    key = ("lat", round(size))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(LAT, int(round(size)))
    return _fc[key]

def font_mono(size):
    key = ("mono", round(size))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(MONO, int(round(size)))
    return _fc[key]

def _is_cjk(ch):
    o = ord(ch)
    return (0x3000 <= o <= 0x9FFF) or (0xF900 <= o <= 0xFAFF) or (0xFF00 <= o <= 0xFFEF)

def _runs(text):
    """Split a mixed CN/EN string into (substr, is_latin) runs."""
    out, cur, cur_lat = [], "", None
    for ch in text:
        lat = not _is_cjk(ch)
        if cur_lat is None or lat == cur_lat:
            cur += ch; cur_lat = lat
        else:
            out.append((cur, cur_lat)); cur, cur_lat = ch, lat
    if cur:
        out.append((cur, cur_lat))
    return out

def text_tile(text, size, fill, mono=False, tracking=0):
    """Render mixed CN/EN text to a tight RGBA tile, routing Latin runs to a
    proper Latin/mono face and CJK runs to wqy — glyphs share one baseline.
    `size` and `tracking` are in device px (already ×S by the caller)."""
    size = int(round(size))
    cjk = font(size)
    lat = font_mono(size) if mono else font_lat(size)
    big = Image.new("RGBA", (int(len(text) * size * 1.4 + size * 4), int(size * 2.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    baseline = int(size * 1.7)
    x = size * 0.3
    for run, is_lat in _runs(text):
        f = lat if is_lat else cjk
        for ch in run:
            d.text((x, baseline), ch, font=f, fill=fill, anchor="ls")
            x += d.textlength(ch, font=f) + tracking
    bb = big.getbbox()
    return big.crop(bb) if bb else big

_ec = {}
def emoji_img(ch, target_h):
    """RGBA image of a colour emoji scaled to ~target_h px tall (LANCZOS)."""
    target_h = int(round(target_h))
    key = (ch, target_h)
    if key in _ec:
        return _ec[key]
    f = ImageFont.truetype(EMOJI, 109)
    base = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(base).text((12, 6), ch, font=f, embedded_color=True)
    bb = base.getbbox()
    glyph = base.crop(bb)
    scale = target_h / glyph.height
    out = glyph.resize((max(1, round(glyph.width * scale)), target_h), Image.LANCZOS)
    _ec[key] = out
    return out


# ---- low-level shapes ----------------------------------------------------
def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle([box[0], box[1], box[2], box[3]], radius=radius,
                           fill=fill, outline=outline, width=int(round(width)))

def panel(img, box, radius, fill, border=INK, bw=6, shadow=INK, shoff=(11, 11),
          grad=None):
    """Neo-brutalist panel: hard offset shadow + thick border + fill/gradient.
    `grad`=(top_rgb, bottom_rgb) fills with a vertical gradient (clipped)."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    bw = bw * S
    radius = radius * S
    if shadow and shoff:
        ox, oy = shoff[0] * S, shoff[1] * S
        rrect(d, (x0 + ox, y0 + oy, x1 + ox, y1 + oy), radius, fill=shadow)
    if grad is not None:
        w, h = int(x1 - x0), int(y1 - y0)
        g = vgrad(w, h, grad[0], grad[1])
        mask = Image.new("L", (w, h), 0)
        rrect(ImageDraw.Draw(mask), (0, 0, w - 1, h - 1), radius, fill=255)
        img.paste(g, (int(x0), int(y0)), mask)
        rrect(d, box, radius, outline=border, width=bw)
    else:
        rrect(d, box, radius, fill=fill, outline=border, width=bw)

def vgrad(w, h, top, bottom):
    """Vertical gradient RGBA image."""
    t = np.linspace(0, 1, h)[:, None]
    arr = np.zeros((h, w, 4), np.uint8)
    for i in range(3):
        arr[..., i] = (top[i] * (1 - t) + bottom[i] * t).astype(np.uint8)
    arr[..., 3] = 255
    return Image.fromarray(arr, "RGBA")

def pill(text, fsize, fg, bg, px=18, py=9, bw=3, radius=999, shoff=(4, 4),
         rotate=0, mono=False, tracking=0):
    """A rounded brutalist pill (chip / badge / url) with mixed CN/EN type.
    Returns an RGBA tile auto-sized to its content."""
    content = text_tile(text, fsize * S, fg, mono=mono, tracking=tracking * S)
    cw, ch = content.size
    px, py, bw = px * S, py * S, bw * S
    W = int(cw + px * 2 + bw * 2)
    H = int(ch + py * 2 + bw * 2)
    pad = max(shoff) * S + 4
    tile = Image.new("RGBA", (W + pad, H + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    r = min(radius * S, H / 2)
    if shoff:
        ox, oy = shoff[0] * S, shoff[1] * S
        rrect(d, (ox, oy, W - 1 + ox, H - 1 + oy), r, fill=INK)
    rrect(d, (0, 0, W - 1, H - 1), r, fill=bg, outline=INK, width=int(bw))
    tile.alpha_composite(content, (int(bw + px), int(bw + py)))
    if rotate:
        tile = tile.rotate(rotate, expand=True, resample=Image.BICUBIC)
    return tile

def paste(base, tile, xy, anchor="lt"):
    """Alpha-paste a tile; anchor picks the reference point (l/c/r × t/m/b)."""
    w, h = tile.size
    x, y = xy
    if "c" in anchor: x -= w / 2
    elif "r" in anchor: x -= w
    if "m" in anchor: y -= h / 2
    elif "b" in anchor: y -= h
    base.alpha_composite(tile, (int(round(x)), int(round(y))))


# ---- QR -----------------------------------------------------------------
def qr_matrix(url):
    qr = segno.make(url, error="h")
    rows = ["".join(str(m) for m in r) for r in qr.matrix_iter(border=0)]
    return rows, qr.version

def qr_image(rows, px, quiet=4, knockout=0.20, fg=INK, bg=PAPER,
             plate_emoji="🦞", plate_bg=PAPER):
    """Render the QR matrix to an `px`×`px` RGBA tile (already supersampled
    if you pass px*S). Center knockout hosts the lobster on a brutalist plate."""
    M = [[int(c) for c in row] for row in rows]
    n = len(M)
    size = n + quiet * 2
    cell = px / size
    img = Image.new("RGBA", (int(px), int(px)), bg + (255,))
    d = ImageDraw.Draw(img)
    lw = max(5, round(n * knockout)); lw += (lw % 2 == 0)  # odd → centered
    lo = (n - lw) // 2; lhi = lo + lw - 1
    for r in range(n):
        for c in range(n):
            if not M[r][c]:
                continue
            if lo <= r <= lhi and lo <= c <= lhi:
                continue
            x = (c + quiet) * cell; y = (r + quiet) * cell
            d.rectangle([x, y, x + cell + 0.6, y + cell + 0.6], fill=fg)
    if plate_emoji:
        ps = lw * cell
        cx = cy = px / 2
        pb = (cx - ps / 2, cy - ps / 2, cx + ps / 2, cy + ps / 2)
        rad = ps * 0.16
        rrect(d, (pb[0] + 3 * S, pb[1] + 3 * S, pb[2] + 3 * S, pb[3] + 3 * S),
              rad, fill=(INK[0], INK[1], INK[2], 140))
        rrect(d, pb, rad, fill=plate_bg, outline=INK, width=int(4 * S))
        lob = emoji_img(plate_emoji, ps * 0.62)
        paste(img, lob, (cx, cy), "cm")
    return img

def qr_panel(base, center_xy, qr_px, rows, pad=30, **qr_kw):
    """Cream glass panel + QR, centered at center_xy. Returns the panel box."""
    qp = pad * S
    side = qr_px + qp * 2
    cx, cy = center_xy
    box = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
    panel(base, box, radius=26, fill=PAPER, bw=6, shoff=(11, 11))
    qr = qr_image(rows, qr_px, **qr_kw)
    paste(base, qr, (cx, cy), "cm")
    return box


# ---- aquarium ornaments --------------------------------------------------
def grid_bg(w, h):
    """Cream canvas with faint ink grid (matches site bg-grid)."""
    img = Image.new("RGBA", (w, h), PAPER + (255,))
    d = ImageDraw.Draw(img)
    step = 34 * S
    line = (INK[0], INK[1], INK[2], 13)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=line, width=max(1, S))
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=line, width=max(1, S))
    return img

def rays(card, specs):
    """God-ray light shafts (screen-ish): translucent white skewed bars."""
    w, h = card.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    skew = 0.30
    for left, bw, op in specs:
        x = left * w; bw = bw * S
        dx = skew * h
        d.polygon([(x, -0.1 * h), (x + bw, -0.1 * h),
                   (x + bw - dx, 1.1 * h), (x - dx, 1.1 * h)],
                  fill=(255, 255, 255, int(255 * op)))
    layer = layer.filter(ImageFilter.GaussianBlur(9 * S))
    card.alpha_composite(layer)

def bubbles(card, specs):
    d = ImageDraw.Draw(card)
    w, h = card.size
    for left, top, r in specs:
        x, y, r = left * w, top * h, r * S
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=(255, 255, 255, 26), outline=(255, 255, 255, 150),
                  width=max(1, 2 * S))

def blade_poly(x, base_y, h, w, lean):
    """Wavy seaweed blade as a closed polygon (two S-curve edges)."""
    n = 22
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        y = base_y - t * h
        wob = math.sin(t * math.pi * 2.1) * (w * 0.5)
        cx = x + lean * h * t + wob
        ww = w * (1 - t) * 0.5 + w * 0.12
        left.append((cx - ww, y))
        right.append((cx + ww, y))
    return left + right[::-1]

def seaweed(card, base_y, blades):
    d = ImageDraw.Draw(card)
    for i, (left, h) in enumerate(blades):
        x = left * card.size[0]
        col = GREENS[i % 3]
        lean = (1 if i % 2 else -1) * 0.12
        poly = blade_poly(x, base_y, h * S, (h * 0.26) * S, lean)
        d.polygon(poly, fill=col + (235,), outline=INK, width=int(2.4 * S))

def pebbles(card, base_y, pebs):
    d = ImageDraw.Draw(card)
    for left, w in pebs:
        x = left * card.size[0]; w = w * S
        ph = w * 0.62
        d.ellipse([x - w / 2, base_y - ph, x + w / 2, base_y],
                  fill=PEBBLES[(int(left * 13)) % 4] + (255,),
                  outline=INK, width=int(2 * S))

def fish_tile(color, L=42):
    """Little brutalist fish (body ellipse + tail + eye). RGBA, faces right."""
    L = int(L * S)
    H = int(L * 0.62)
    t = Image.new("RGBA", (L, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    bx0, bx1 = L * 0.06, L * 0.72
    d.ellipse([bx0, H * 0.16, bx1, H * 0.84], fill=color + (255,),
              outline=INK, width=int(1.8 * S))
    d.polygon([(L * 0.66, H * 0.5), (L * 0.99, H * 0.18),
               (L * 0.9, H * 0.5), (L * 0.99, H * 0.82)],
              fill=color + (255,), outline=INK, width=int(1.8 * S))
    er = max(2, int(1.7 * S))
    ex, ey = L * 0.26, H * 0.42
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=INK)
    return t

def fishes(card, specs):
    for left, top, dir_, color in specs:
        t = fish_tile(color)
        if dir_ < 0:
            t = t.transpose(Image.FLIP_LEFT_RIGHT)
        # drop shadow
        sh = Image.new("RGBA", t.size, (0, 0, 0, 0))
        sh.paste((INK[0], INK[1], INK[2], 70), (0, 0), t.split()[3])
        paste(card, sh, (left * card.size[0] + 2 * S, top * card.size[1] + 2 * S), "cm")
        paste(card, t, (left * card.size[0], top * card.size[1]), "cm")


# ---- composite header ----------------------------------------------------
def brand_header(card, x, y, name="CJY · 陈俊烨", vibe="VIBE CODER · 生态缸",
                 badge="扫码 ↓"):
    lob = emoji_img("🦞", 56 * S)
    paste(card, lob, (x, y), "lt")
    tx = x + lob.width + 16 * S
    # name: Latin (DejaVu Bold) + CJK (wqy), white with hard ink shadow
    nm = text_tile(name, 32 * S, (255, 255, 255, 255))
    sh = text_tile(name, 32 * S, (INK[0], INK[1], INK[2], 110))
    paste(card, sh, (tx + 2 * S, y + 2 * S), "lt")
    paste(card, nm, (tx, y), "lt")
    # vibe: mono Latin + CJK, lime, tracked
    vb = text_tile(vibe, 15 * S, LIME, mono=True, tracking=2.2 * S)
    paste(card, vb, (tx, y + 46 * S), "lt")
    if badge:
        b = pill(badge, 19, INK, LIME, px=20, py=11, bw=3, rotate=3)
        paste(card, b, (card.size[0] - 50 * S, y + 6 * S), "rt")

def chips_row(card, cx, y, chips):
    tiles = [pill(t, 18, INK, (LIME if lime else PAPER2), px=18, py=9, bw=3)
             for t, lime in chips]
    gap = 13 * S
    total = sum(t.width for t in tiles) + gap * (len(tiles) - 1)
    x = cx - total / 2
    for t in tiles:
        paste(card, t, (x, y), "lt")
        x += t.width + gap


# ---- output --------------------------------------------------------------
def finish(img, out_path, down=S):
    """Downsample by `down` (LANCZOS) and save RGB PNG."""
    w, h = img.size
    out = img.convert("RGB").resize((w // down, h // down), Image.LANCZOS)
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path)
    return out_path
