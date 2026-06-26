#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refined branded cover generator (1280x800) — no browser required.

Pure Pillow + numpy, rendered at 3x and downscaled (LANCZOS) for smooth,
anti-aliased edges. Re-creates the brand layout from tools/covers.html
(tag / big title / mono meter, scrim + vignette) but draws richer vector
scenes for the three covers that read flat as placeholders.

Outputs -> public/shots/{cargo-claw,aerotwin,solar}.png
Run:  python3 tools/covers.py
"""
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 3                      # supersample factor
W, H = 1280, 800
WS, HS = W * S, H * S
FP = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
OUT = "public/shots"

# ---------------------------------------------------------------- primitives
def F(size, mono=False):
    return ImageFont.truetype(FP, max(1, int(round(size * S))), index=1 if mono else 0)

def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def shade(c, f):
    return tuple(max(0, min(255, int(ch * f))) for ch in c[:3])

def layer():
    return Image.new("RGBA", (WS, HS), (0, 0, 0, 0))

def to_img(arr):
    return Image.fromarray(np.ascontiguousarray(arr.astype(np.uint8)), "RGBA")

def sx(v):
    return int(round(v * S))

def vgrad(stops):
    """Vertical gradient. stops = [(pos0..1, (r,g,b)), ...] sorted."""
    ys = np.linspace(0, 1, HS)
    pos = np.array([s[0] for s in stops])
    cols = np.array([s[1] for s in stops], dtype=float)
    col = np.stack([np.interp(ys, pos, cols[:, i]) for i in range(3)], 1)
    arr = np.repeat(col[:, None, :], WS, axis=1)
    a = np.full((HS, WS, 1), 255.0)
    return to_img(np.concatenate([arr, a], 2))

def radial_bg(inner, outer, cx=0.5, cy=0.5, rx=0.8, ry=0.8, power=1.0):
    yy, xx = np.mgrid[0:HS, 0:WS].astype(float)
    dx = (xx - cx * WS) / (rx * WS)
    dy = (yy - cy * HS) / (ry * HS)
    t = np.clip(np.sqrt(dx * dx + dy * dy), 0, 1) ** power
    inner = np.array(inner, float); outer = np.array(outer, float)
    col = inner[None, None, :] * (1 - t[..., None]) + outer[None, None, :] * t[..., None]
    a = np.full((HS, WS, 1), 255.0)
    return to_img(np.concatenate([col, a], 2))

def scrim(img, color=(6, 8, 12), start=0.46, strength=0.86, power=1.15):
    yy = np.mgrid[0:HS, 0:WS][0].astype(float)
    ramp = np.clip((yy / HS - start) / (1 - start), 0, 1) ** power
    s = np.zeros((HS, WS, 4))
    s[..., 0], s[..., 1], s[..., 2] = color
    s[..., 3] = ramp * strength * 255
    img.alpha_composite(to_img(s))

def vignette(img, strength=0.5, inner=0.6, power=1.4):
    yy, xx = np.mgrid[0:HS, 0:WS].astype(float)
    dx = (xx - 0.5 * WS) / (0.5 * WS)
    dy = (yy - 0.5 * HS) / (0.5 * HS)
    t = np.clip((np.sqrt(dx * dx + dy * dy) - inner) / (1.45 - inner), 0, 1) ** power
    v = np.zeros((HS, WS, 4))
    v[..., 3] = t * strength * 255
    img.alpha_composite(to_img(v))

def glow(img, draw_fn, blur, passes=1):
    g = layer()
    draw_fn(ImageDraw.Draw(g))
    g = g.filter(ImageFilter.GaussianBlur(blur * S))
    for _ in range(passes):
        img.alpha_composite(g)

# ---------------------------------------------------------------- text / meta
def text_track(d, x, y, s, fnt, fill, track=0):
    for ch in s:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + track * S
    return x

def meta(img, tag, tag_color, title, meter_segs, title_color=(247, 245, 240), title_shadow=(0, 0, 0, 165)):
    tagf, titf, mtrf = F(22, mono=True), F(58), F(25, mono=True)
    a1, d1 = titf.getmetrics(); tit_h = a1 + d1
    tag_h = sum(tagf.getmetrics())
    mtr_h = sum(mtrf.getmetrics())
    total = tag_h + 8 * S + tit_h + 16 * S + mtr_h
    x0 = 60 * S
    y0 = (H - 52) * S - total

    d = ImageDraw.Draw(img)
    text_track(d, x0, y0, tag, tagf, tag_color, track=4)

    ty = y0 + tag_h + 8 * S
    if title_shadow:
        sh = layer()
        ImageDraw.Draw(sh).text((x0 + 2 * S, ty + 4 * S), title, font=titf,
                                fill=title_shadow, stroke_width=int(1.1 * S),
                                stroke_fill=title_shadow)
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7 * S)))
    ImageDraw.Draw(img).text((x0, ty), title, font=titf, fill=title_color,
                             stroke_width=max(1, int(0.9 * S)), stroke_fill=title_color)

    my = ty + tit_h + 16 * S
    d = ImageDraw.Draw(img)
    mx = x0
    for seg, c in meter_segs:
        d.text((mx, my), seg, font=mtrf, fill=c)
        mx += d.textlength(seg, font=mtrf)

def finish(img, name):
    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    out.save(f"{OUT}/{name}.png")
    print("wrote", f"{OUT}/{name}.png", out.size)

# ================================================================ PORT
def build_port():
    acc = hx("46E6B0")
    grey = (214, 224, 235)
    img = vgrad([(0, (13, 41, 64)), (0.36, (15, 47, 71)), (0.50, (12, 34, 52)),
                 (0.535, (8, 23, 37)), (1, (5, 11, 19))])
    d = ImageDraw.Draw(img)
    hz = 430

    # faint twin scan band in the sky
    for y in range(70, 250, 16):
        d.line([(0, sx(y)), (WS, sx(y))], fill=(70, 160, 150, 12), width=S)

    # distant shore lights along the horizon
    rnd = random.Random(7)
    for _ in range(80):
        x = rnd.randint(0, WS)
        c = (255, 206, 140, rnd.randint(60, 150)) if rnd.random() < .55 else (150, 200, 255, rnd.randint(40, 120))
        r = rnd.choice([1, 1, 2]) * S
        d.ellipse([x - r, sx(hz - 3) - r, x + r, sx(hz - 3) + r], fill=c)

    # perspective twin-grid on the water (digital-twin motif)
    grid = layer(); dgd = ImageDraw.Draw(grid)
    vpx, vpy = sx(640), sx(hz)
    for gx in range(-7, 8):
        dgd.line([(sx(640 + gx * 150), HS), (vpx, vpy)], fill=(70, 200, 170, 24), width=S)
    for gy in range(1, 9):
        yy = sx(hz) + (HS - sx(hz)) * (gy / 9) ** 1.7
        dgd.line([(0, int(yy)), (WS, int(yy))], fill=(70, 200, 170, int(32 - gy * 2)), width=S)
    img.alpha_composite(grid)

    # --- 5-agent mesh HUD, upper-left, clear of the cranes ---
    nodes = [(118, 150), (192, 104), (296, 138), (342, 214), (228, 226)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4)]
    mesh = layer(); dm = ImageDraw.Draw(mesh)
    for a, b in edges:
        dm.line([(sx(nodes[a][0]), sx(nodes[a][1])), (sx(nodes[b][0]), sx(nodes[b][1]))], fill=(*acc, 90), width=max(1, S))
    img.alpha_composite(mesh)
    glow(img, lambda dd: [dd.ellipse([sx(x) - sx(6), sx(y) - sx(6), sx(x) + sx(6), sx(y) + sx(6)], fill=(*acc, 170)) for x, y in nodes], blur=7)
    for x, y in nodes:
        d.ellipse([sx(x) - sx(7), sx(y) - sx(7), sx(x) + sx(7), sx(y) + sx(7)], outline=(*acc, 220), width=max(1, S))
        d.ellipse([sx(x) - sx(3), sx(y) - sx(3), sx(x) + sx(3), sx(y) + sx(3)], fill=(220, 255, 245))
    d.text((sx(112), sx(80)), "5 AGENTS · 自治协同", font=F(13, mono=True), fill=(*acc, 210))

    # --- container ship on the water ---
    deck, wl = 420, 455
    glow(img, lambda dd: dd.rectangle([sx(556), sx(wl - 4), sx(1074), sx(wl + 4)], fill=(70, 150, 150, 90)), blur=6)  # waterline sheen
    hull = [(548, wl), (572, deck + 6), (1060, deck + 6), (1086, deck + 18), (1074, wl)]
    d.polygon([(sx(a), sx(b)) for a, b in hull], fill=(18, 28, 42))
    d.line([(sx(572), sx(deck + 6)), (sx(1060), sx(deck + 6))], fill=(64, 88, 112), width=sx(2))   # deck edge highlight
    d.line([(sx(556), sx(wl - 3)), (sx(1072), sx(wl - 3))], fill=(160, 66, 56), width=max(1, S))  # boot-topping
    pal = [(231, 72, 59), (47, 125, 224), (55, 184, 107), (232, 181, 58), (138, 77, 224)]
    cw = 28
    for row, ry in enumerate((deck - 2, deck - 18)):
        for i, bx in enumerate(range(596, 1040, cw + 3)):
            c = pal[(i + row) % len(pal)]
            d.rectangle([sx(bx), sx(ry - 15), sx(bx + cw), sx(ry)], fill=c)
            d.rectangle([sx(bx), sx(ry - 15), sx(bx + cw), sx(ry)], outline=(0, 0, 0, 70), width=max(1, S // 2))
    d.rectangle([sx(1042), sx(deck - 40), sx(1080), sx(deck + 4)], fill=(24, 34, 48))            # accommodation
    for wx in range(1048, 1078, 8):
        for wy in range(deck - 34, deck - 4, 8):
            d.rectangle([sx(wx), sx(wy), sx(wx + 3), sx(wy + 3)], fill=(255, 214, 120, 210))
    d.rectangle([sx(1056), sx(deck - 54), sx(1066), sx(deck - 40)], fill=(20, 28, 40))           # funnel
    ref = layer(); drf = ImageDraw.Draw(ref)                                                     # reflection
    drf.rectangle([sx(556), sx(wl), sx(1074), sx(wl + 36)], fill=(11, 18, 28, 120))
    for k in range(3):
        drf.line([(sx(560), sx(wl + 8 + k * 9)), (sx(1070), sx(wl + 8 + k * 9))], fill=(120, 150, 170, 40), width=max(1, S))
    img.alpha_composite(ref.filter(ImageFilter.GaussianBlur(2 * S)))

    # --- gantry (STS) cranes ---
    def crane(cxl, lifting=False):
        cx = sx(cxl); top = sx(165); base = sx(462); apex = sx(118)
        span, steel = sx(52), (64, 80, 94)
        l, r = cx - span, cx + span
        d.line([(l, top), (l, base)], fill=steel, width=sx(6))
        d.line([(r, top), (r, base)], fill=steel, width=sx(6))
        d.line([(l - sx(15), base), (l + sx(15), base)], fill=steel, width=sx(6))
        d.line([(r - sx(15), base), (r + sx(15), base)], fill=steel, width=sx(6))
        d.line([(l, sx(320)), (r, sx(430))], fill=shade(steel, .7), width=max(1, S))             # X brace
        d.line([(r, sx(320)), (l, sx(430))], fill=shade(steel, .7), width=max(1, S))
        by, boomL, boomR = sx(165), cx - sx(178), cx + sx(66)
        d.line([(boomL, by), (boomR, by)], fill=steel, width=sx(7))                              # boom
        d.line([(boomL, by + sx(8)), (boomR, by + sx(8))], fill=shade(steel, .6), width=max(1, S))
        d.line([(l, top), (cx, apex)], fill=steel, width=sx(5))
        d.line([(r, top), (cx, apex)], fill=steel, width=sx(5))
        d.line([(cx, apex), (boomL, by)], fill=steel, width=sx(4))                               # forestay
        d.ellipse([cx - sx(4), apex - sx(4), cx + sx(4), apex + sx(4)], fill=(255, 140, 90))
        if lifting:
            tx = cx - sx(120)
            d.line([(tx, by), (tx, sx(290))], fill=(150, 160, 170), width=max(1, S))
            d.rectangle([tx - sx(10), by - sx(4), tx + sx(10), by + sx(6)], fill=steel)
            d.rectangle([tx - sx(16), sx(290), tx + sx(16), sx(308)], fill=(231, 72, 59))

    for cxl in (620, 820, 1020):
        crane(cxl, lifting=(cxl == 820))
    glow(img, lambda dd: [dd.ellipse([sx(c) - sx(6), sx(118) - sx(6), sx(c) + sx(6), sx(118) + sx(6)], fill=(255, 130, 90, 200)) for c in (620, 820, 1020)], blur=8)

    # --- foreground container yard (isometric stacks) ---
    def box(x, y, w, h, c, dep):
        d.polygon([(sx(x), sx(y)), (sx(x + dep), sx(y - dep)), (sx(x + w + dep), sx(y - dep)), (sx(x + w), sx(y))], fill=shade(c, 1.18))
        d.polygon([(sx(x + w), sx(y)), (sx(x + w + dep), sx(y - dep)), (sx(x + w + dep), sx(y + h - dep)), (sx(x + w), sx(y + h))], fill=shade(c, .62))
        d.rectangle([sx(x), sx(y), sx(x + w), sx(y + h)], fill=c)
        d.rectangle([sx(x), sx(y), sx(x + w), sx(y + h)], outline=(0, 0, 0, 90), width=max(1, S // 2))

    ypal = [(231, 72, 59), (47, 125, 224), (55, 184, 107), (232, 181, 58), (138, 77, 224)]
    for ri, (yy, bw, bh, x0, gap, dep) in enumerate([(500, 40, 16, 470, 5, 7), (532, 48, 19, 452, 6, 9), (572, 60, 24, 430, 7, 11)]):
        for i, bx in enumerate(range(x0, 1200, bw + gap)):
            box(bx, yy - bh, bw, bh, ypal[(i + ri) % len(ypal)], dep)

    scrim(img, start=0.52, strength=0.9)
    vignette(img, strength=0.5)
    meta(img, "CARGO CLAW · DIGITAL TWIN v3.0", acc, "五个智能体 · 自治协同的港口",
         [("OC AGENT SOCIETY · TEU/日 ", grey), ("885", acc), (" · 安全 ", grey), ("99.2", acc)])
    finish(img, "cargo-claw")

# ================================================================ AIRPORT
def build_airport():
    acc = hx("FF8A3C")
    grey = (214, 222, 232)
    img = vgrad([(0, (18, 36, 30)), (0.32, (14, 30, 34)), (0.52, (11, 22, 32)), (1, (7, 12, 21))])
    d = ImageDraw.Draw(img)
    VPy = 202

    haze = layer(); dh = ImageDraw.Draw(haze)
    dh.ellipse([sx(300), sx(150), sx(980), sx(300)], fill=(120, 150, 170, 24))
    img.alpha_composite(haze.filter(ImageFilter.GaussianBlur(28 * S)))
    for tx0, tx1 in ((300, 470), (810, 980)):                      # distant terminals frame the gap
        d.rectangle([sx(tx0), sx(206), sx(tx1), sx(222)], fill=(19, 28, 38))
        for wx in range(tx0 + 6, tx1 - 4, 11):
            d.rectangle([sx(wx), sx(211), sx(wx + 6), sx(217)], fill=(255, 220, 140, 190))
    d.rectangle([sx(631), sx(176), sx(641), sx(214)], fill=(22, 32, 42))                          # control tower
    d.rectangle([sx(625), sx(168), sx(647), sx(182)], fill=(30, 44, 56))
    glow(img, lambda dd: dd.ellipse([sx(630), sx(160), sx(642), sx(172)], fill=(255, 170, 90, 220)), blur=7)
    d.ellipse([sx(633), sx(163), sx(639), sx(169)], fill=(255, 220, 160))

    def lerp(a, b, t):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    def runway(near_l, near_r, far_cx, far_half, label, sub, lit):
        fl, fr = (far_cx - far_half, VPy), (far_cx + far_half, VPy)
        quad = [near_l, near_r, fr, fl]
        d.polygon([(sx(a), sx(b)) for a, b in quad], fill=(32, 38, 45))
        d.polygon([(sx(a), sx(b)) for a, b in quad], outline=(72, 82, 94), width=max(1, S))
        nc, tg = lerp(near_l, near_r, .5), (far_cx, VPy)
        for k in range(0, 17):                                     # centreline dashes
            t0, t1 = (k / 17) ** 1.25, ((k + .5) / 17) ** 1.25
            p0, p1 = lerp(nc, tg, t0), lerp(nc, tg, t1)
            d.line([(sx(p0[0]), sx(p0[1])), (sx(p1[0]), sx(p1[1]))], fill=(236, 226, 200), width=max(1, int(S * (1.6 * (1 - t0) + .3))))
        for k in range(18):                                        # edge lights
            t = (k / 18) ** 1.3
            for edge, col in ((0.0, (255, 255, 235)), (1.0, (120, 200, 255))):
                pe = lerp(lerp(near_l, fl, t), lerp(near_r, fr, t), edge)
                rr = S * (2.4 * (1 - t) + .5)
                d.ellipse([sx(pe[0]) - rr, sx(pe[1]) - rr, sx(pe[0]) + rr, sx(pe[1]) + rr], fill=(*col, 235))
        for j in range(8):                                         # threshold piano keys
            t = j / 8
            a, b = lerp(near_l, near_r, t + .01), lerp(near_l, near_r, t + .055)
            d.line([(sx(a[0]), sx(a[1])), (sx(b[0]), sx(b[1]))], fill=(236, 232, 220), width=sx(6))
        chip = lerp(nc, tg, .72)                                   # A/B label up near the tower
        cw2 = sx(72)
        d.rounded_rectangle([sx(chip[0]) - cw2, sx(chip[1]) - sx(13), sx(chip[0]) + cw2, sx(chip[1]) + sx(13)], radius=sx(13), fill=(14, 16, 20, 235), outline=(*lit, 235), width=max(1, S))
        ft = F(14, mono=True)
        txt = f"{label} · {sub}"
        tw = ImageDraw.Draw(img).textlength(txt, font=ft)
        ImageDraw.Draw(img).text((sx(chip[0]) - tw / 2, sx(chip[1]) - sx(10)), txt, font=ft, fill=(*lit, 255))
        return nc, tg

    ncA, tgA = runway((150, 815), (430, 815), 606, 12, "A", "FCFS", (170, 186, 205))
    ncB, tgB = runway((850, 815), (1130, 815), 674, 12, "B", "智能调度", acc)

    for nc, col in ((ncA, (255, 70, 70)), (ncB, (90, 240, 140))):  # PAPI near thresholds
        for i in range(4):
            x = nc[0] - 70 + i * 16
            d.ellipse([sx(x) - sx(3), sx(772) - sx(3), sx(x) + sx(3), sx(772) + sx(3)], fill=(*col, 240))

    def plane_tile(length, accent=(255, 150, 80)):
        body = (222, 228, 236)
        L = sx(length); span = int(length * 1.06 * S); pad = sx(12)
        w, h = span + 2 * pad, L + 2 * pad
        t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dd = ImageDraw.Draw(t)
        cx = w // 2; topy = pad; boty = pad + L
        fw = max(2, int(length * .12 * S))
        wy = pad + int(L * .52)
        for s_ in (-1, 1):
            dd.polygon([(cx + s_ * fw, wy - int(L * .12)), (cx + s_ * (span // 2), wy + int(L * .10)), (cx + s_ * (span // 2), wy + int(L * .15)), (cx + s_ * fw, wy + int(L * .02))], fill=body)
        ty2 = pad + int(L * .88)
        for s_ in (-1, 1):
            dd.polygon([(cx + s_ * fw, ty2 - int(L * .05)), (cx + s_ * int(span * .22), ty2 + int(L * .05)), (cx + s_ * int(span * .22), ty2 + int(L * .08)), (cx + s_ * fw, ty2 + int(L * .02))], fill=body)
        dd.rounded_rectangle([cx - fw, topy + int(L * .06), cx + fw, boty], radius=fw, fill=body)
        dd.polygon([(cx - fw, topy + int(L * .10)), (cx + fw, topy + int(L * .10)), (cx, topy)], fill=body)
        dd.rounded_rectangle([cx - fw, boty - int(L * .12), cx + fw, boty], radius=fw, fill=accent)
        dd.ellipse([cx - fw * .6, topy + int(L * .11), cx + fw * .6, topy + int(L * .22)], fill=(120, 165, 205))
        return t

    def place_plane(cx, cy, length, target, accent=(255, 150, 80)):
        t = plane_tile(length, accent=accent)
        ang = math.degrees(math.atan2(target[1] - cy, target[0] - cx)) + 90
        rot = t.rotate(-ang, expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
        sh.paste((0, 0, 0, 120), (0, 0), rot.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(3 * S))
        img.alpha_composite(sh, (int(sx(cx) - rot.width / 2 + sx(5)), int(sx(cy) - rot.height / 2 + sx(7))))
        img.alpha_composite(rot, (int(sx(cx) - rot.width / 2), int(sx(cy) - rot.height / 2)))

    def along(nc, tg, t):
        return lerp(nc, tg, t)

    place_plane(*along(ncA, tgA, .44), 54, tgA)                    # A: rolling
    place_plane(*along(ncA, tgA, .62), 34, tgA)
    place_plane(*along(ncB, tgB, .22), 58, tgB, accent=acc)        # B: queued departures
    place_plane(*along(ncB, tgB, .46), 36, tgB, accent=acc)

    scrim(img, start=0.55, strength=0.82)
    vignette(img, strength=0.48)
    meta(img, "天府TWIN · 成都天府国际机场 TFU", acc, "调度算法 · A/B 影子仿真",
         [("FCFS ", grey), ("vs ", (150, 160, 175)), ("智能调度", acc), (" · 跑道实时对比", grey)])
    finish(img, "aerotwin")

# ================================================================ SOLAR
def sphere_tile(r, base, light, ambient=0.20, bands=False):
    r = sx(r); size = 2 * r + 2
    yy, xx = np.mgrid[0:size, 0:size].astype(float)
    nx = (xx - r) / r; ny = (yy - r) / r
    rr = nx * nx + ny * ny
    mask = rr <= 1.0
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    L = np.array(light, float); L = L / np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    inten = ambient + (1 - ambient) * diff
    base = np.array(base, float)
    col = np.repeat(base[None, None, :], size, 0).repeat(size, 1)
    if bands:
        lat = np.arcsin(np.clip(ny, -1, 1))
        band = 0.86 + 0.14 * np.sin(lat * 9.0)
        tint = 0.92 + 0.08 * np.sin(lat * 4.0 + 1)
        col = col * band[..., None] * tint[..., None]
    col = np.clip(col * inten[..., None], 0, 255)
    a = np.where(mask, 255.0, 0.0)
    a = a * np.clip((1 - rr) / (2.0 / r), 0, 1)        # feathered limb
    return to_img(np.dstack([col, a]))

def build_solar():
    acc = hx("9FB6FF")
    grey = (210, 218, 235)
    img = radial_bg((24, 21, 50), (4, 5, 11), cx=0.5, cy=0.5, rx=1.0, ry=0.95)

    neb = layer(); dn = ImageDraw.Draw(neb)
    for x, y, r, c in [(360, 250, 260, (70, 60, 150, 50)), (980, 540, 320, (140, 70, 120, 42)),
                       (820, 180, 220, (60, 110, 160, 40))]:
        dn.ellipse([sx(x - r), sx(y - r), sx(x + r), sx(y + r)], fill=c)
    img.alpha_composite(neb.filter(ImageFilter.GaussianBlur(140 * S)))

    d = ImageDraw.Draw(img); rnd = random.Random(42)
    for _ in range(300):
        x, y = rnd.randint(0, WS), rnd.randint(0, HS)
        b = rnd.random(); r = (0.5 + 1.7 * b) * S; a = int(60 + 180 * b)
        tint = (220, 228, 255) if rnd.random() < .8 else (255, 232, 210)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*tint, a))
    for _ in range(8):
        x, y = rnd.randint(80, WS - 80), rnd.randint(60, sx(560))
        glow(img, lambda dd, x=x, y=y: dd.ellipse([x - sx(4), y - sx(4), x + sx(4), y + sx(4)], fill=(230, 236, 255, 230)), blur=5)
        d.line([(x - sx(7), y), (x + sx(7), y)], fill=(235, 240, 255, 200), width=max(1, S // 2))
        d.line([(x, y - sx(7)), (x, y + sx(7))], fill=(235, 240, 255, 200), width=max(1, S // 2))

    cx, cy, ratio = 628, 404, 0.33
    orbits = [168, 232, 300, 372, 452, 540, 628]
    ol = layer(); do = ImageDraw.Draw(ol)
    for rx in orbits:
        do.ellipse([sx(cx - rx), sx(cy - rx * ratio), sx(cx + rx), sx(cy + rx * ratio)],
                   outline=(150, 170, 225, 64), width=max(1, int(1.3 * S)))
    img.alpha_composite(ol)

    ast = random.Random(11)
    for _ in range(220):
        rx = ast.uniform(404, 432); th = ast.uniform(0, 2 * math.pi)
        px, py = cx + rx * math.cos(th), cy + rx * ratio * math.sin(th)
        rr = ast.choice([1, 1, 2]) * S
        d.ellipse([sx(px) - rr, sx(py) - rr, sx(px) + rr, sx(py) + rr], fill=(180, 170, 150, ast.randint(70, 150)))

    def planet_pos(rx, deg):
        th = math.radians(deg)
        return cx + rx * math.cos(th), cy + rx * ratio * math.sin(th)

    def light_for(px, py):
        lx, ly = cx - px, cy - py
        n = math.hypot(lx, ly) or 1
        return (lx / n, ly / n, 0.72)

    JUP = (203, 168, 132)

    def draw_planet(rx, deg, pr, base, glowc=None, atmos=None):
        px, py = planet_pos(rx, deg)
        if glowc:
            glow(img, lambda dd: dd.ellipse([sx(px - pr * 1.5), sx(py - pr * 1.5), sx(px + pr * 1.5), sx(py + pr * 1.5)], fill=glowc), blur=int(pr * 0.7))
        t = sphere_tile(pr, base, light_for(px, py), bands=(base == JUP))
        if atmos:
            ImageDraw.Draw(t).ellipse([2, 2, t.width - 2, t.height - 2], outline=(*atmos, 90), width=max(1, S))
        img.alpha_composite(t, (sx(px) - t.width // 2, sx(py) - t.height // 2))
        return px, py

    draw_planet(168, 205, 9, (170, 150, 135))                              # Mercury
    draw_planet(232, 25, 14, (212, 175, 120), atmos=(255, 220, 160))       # Venus
    ex, ey = draw_planet(300, 142, 15, (70, 120, 195), glowc=(80, 150, 230, 70), atmos=(150, 200, 255))  # Earth
    mt = sphere_tile(4, (200, 200, 205), light_for(ex + 26, ey))           # Moon
    img.alpha_composite(mt, (sx(ex + 26) - mt.width // 2, sx(ey - 8) - mt.height // 2))
    draw_planet(372, 318, 12, (198, 92, 60), atmos=(230, 130, 90))         # Mars
    draw_planet(540, 8, 34, JUP)                                           # Jupiter
    jx, jy = planet_pos(540, 8)
    d.ellipse([sx(jx + 6) - sx(5), sx(jy + 4) - sx(3), sx(jx + 6) + sx(5), sx(jy + 4) + sx(3)], fill=(150, 90, 70, 200))

    # Saturn with ring (back arc -> planet -> front arc)
    spr = 26
    spx, spy = planet_pos(628, 200)
    ring_box = [sx(spx - spr * 2.05), sx(spy - spr * 0.78), sx(spx + spr * 2.05), sx(spy + spr * 0.78)]
    rl = layer(); dr = ImageDraw.Draw(rl)
    for off, col in ((0, (214, 198, 158, 200)), (sx(7), (180, 165, 130, 160)), (sx(13), (150, 140, 115, 120))):
        dr.arc([ring_box[0] + off, ring_box[1] + off * ratio, ring_box[2] - off, ring_box[3] - off * ratio], 180, 360, fill=col, width=max(1, int(2.2 * S)))
    img.alpha_composite(rl)
    t = sphere_tile(spr, (214, 192, 150), light_for(spx, spy), bands=True)
    img.alpha_composite(t, (sx(spx) - t.width // 2, sx(spy) - t.height // 2))
    rf = layer(); drf = ImageDraw.Draw(rf)
    for off, col in ((0, (214, 198, 158, 220)), (sx(7), (180, 165, 130, 175)), (sx(13), (150, 140, 115, 130))):
        drf.arc([ring_box[0] + off, ring_box[1] + off * ratio, ring_box[2] - off, ring_box[3] - off * ratio], 0, 180, fill=col, width=max(1, int(2.2 * S)))
    img.alpha_composite(rf)

    tr = layer(); dt = ImageDraw.Draw(tr)                                  # flight trail on Earth orbit
    dt.arc([sx(cx - 300), sx(cy - 300 * ratio), sx(cx + 300), sx(cy + 300 * ratio)], 96, 150, fill=(150, 200, 255, 150), width=max(1, int(2 * S)))
    img.alpha_composite(tr.filter(ImageFilter.GaussianBlur(1 * S)))

    glow(img, lambda dd: dd.ellipse([sx(cx - 150), sx(cy - 150), sx(cx + 150), sx(cy + 150)], fill=(255, 196, 92, 255)), blur=68)
    glow(img, lambda dd: dd.ellipse([sx(cx - 86), sx(cy - 86), sx(cx + 86), sx(cy + 86)], fill=(255, 222, 150, 255)), blur=24)
    glow(img, lambda dd: dd.ellipse([sx(cx - 60), sx(cy - 60), sx(cx + 60), sx(cy + 60)], fill=(255, 246, 214, 255)), blur=6)
    ImageDraw.Draw(img).ellipse([sx(cx - 52), sx(cy - 52), sx(cx + 52), sx(cy + 52)], fill=(255, 250, 232))

    scrim(img, color=(6, 6, 12), start=0.5, strength=0.82)
    vignette(img, strength=0.42, inner=0.66)
    meta(img, "SOLAR · 太阳系漫游", acc, "三维太阳系 · 自由飞行",
         [("行星漫游 · 真实星历 · 语音解说", grey)])
    finish(img, "solar")

# ================================================================ HACKATHON
def build_hackathon():
    ink = (20, 17, 11)
    red, blue, lime, yellow = (255, 77, 28), (43, 71, 240), (200, 255, 45), (245, 200, 30)
    paper = (244, 234, 210)
    img = vgrad([(0, (247, 238, 216)), (1, (235, 223, 197))])
    d = ImageDraw.Draw(img)

    # faint halftone dots
    for yy in range(40, 470, 34):
        for xx in range(30, 1260, 34):
            d.ellipse([sx(xx) - S, sx(yy) - S, sx(xx) + S, sx(yy) + S], fill=(20, 17, 11, 13))

    # bunting flags across the top
    flagcols = [red, blue, lime, yellow, red, blue, lime, yellow, red, blue]
    n = len(flagcols)
    pts = [(40 + i * (1200 / n), 44 + 24 * math.sin(i / n * math.pi)) for i in range(n + 1)]
    for i in range(n):
        d.line([(sx(pts[i][0]), sx(pts[i][1])), (sx(pts[i + 1][0]), sx(pts[i + 1][1]))], fill=ink, width=max(1, S))
    for i in range(n):
        (x0p, y0p), (x1p, y1p) = pts[i], pts[i + 1]
        mx, my = (x0p + x1p) / 2, (y0p + y1p) / 2
        tri = [(x0p, y0p), (x1p, y1p), (mx, my + 38)]
        d.polygon([(sx(a), sx(b)) for a, b in tri], fill=flagcols[i])
        d.polygon([(sx(a), sx(b)) for a, b in tri], outline=ink, width=max(1, S))

    # soft spotlight cone over the exhibits
    spot = layer()
    ImageDraw.Draw(spot).polygon([(sx(560), sx(60)), (sx(120), sx(360)), (sx(1080), sx(360))], fill=(255, 250, 230, 70))
    img.alpha_composite(spot.filter(ImageFilter.GaussianBlur(40 * S)))

    # scattered memphis confetti (behind the frames)
    cf = random.Random(5)
    for _ in range(30):
        x, y = cf.randint(60, 1200), cf.randint(95, 380)
        col = cf.choice([red, blue, lime, yellow])
        k = cf.choice(["dot", "ring", "plus", "tri", "diamond"])
        if k == "dot":
            d.ellipse([sx(x) - sx(7), sx(y) - sx(7), sx(x) + sx(7), sx(y) + sx(7)], fill=col, outline=ink, width=max(1, S // 2))
        elif k == "ring":
            d.ellipse([sx(x) - sx(8), sx(y) - sx(8), sx(x) + sx(8), sx(y) + sx(8)], outline=col, width=max(1, S))
        elif k == "plus":
            d.line([(sx(x - 8), sx(y)), (sx(x + 8), sx(y))], fill=col, width=max(1, 2 * S))
            d.line([(sx(x), sx(y - 8)), (sx(x), sx(y + 8))], fill=col, width=max(1, 2 * S))
        elif k == "tri":
            d.polygon([(sx(x), sx(y - 8)), (sx(x - 8), sx(y + 7)), (sx(x + 8), sx(y + 7))], outline=col, width=max(1, S))
        else:
            d.polygon([(sx(x), sx(y - 8)), (sx(x + 8), sx(y)), (sx(x), sx(y + 8)), (sx(x - 8), sx(y))], fill=col, outline=ink, width=max(1, S // 2))

    # framed AI exhibits — neo-brutalist hard border + offset shadow
    def frame(x, y, w, h, mat, icon):
        d.rectangle([sx(x + 12), sx(y + 14), sx(x + w + 12), sx(y + h + 14)], fill=ink)            # hard shadow
        d.rectangle([sx(x), sx(y), sx(x + w), sx(y + h)], fill=paper)
        d.rectangle([sx(x), sx(y), sx(x + w), sx(y + h)], outline=ink, width=sx(7))
        ins = 16
        d.rectangle([sx(x + ins), sx(y + ins), sx(x + w - ins), sx(y + h - ins)], fill=mat)
        icon(x + w / 2, y + h / 2)

    def ic_net(cx, cy):
        xs, ys3, ys2 = [cx - 44, cx, cx + 44], [cy - 34, cy, cy + 34], [cy]
        layers = [[(xs[0], v) for v in ys3], [(xs[1], v) for v in ys3], [(xs[2], v) for v in ys2]]
        for a in layers[0]:
            for b in layers[1]:
                d.line([(sx(a[0]), sx(a[1])), (sx(b[0]), sx(b[1]))], fill=ink, width=max(1, S // 2))
        for b in layers[1]:
            d.line([(sx(b[0]), sx(b[1])), (sx(layers[2][0][0]), sx(layers[2][0][1]))], fill=ink, width=max(1, S // 2))
        for col in layers:
            for (px, py) in col:
                d.ellipse([sx(px) - sx(6), sx(py) - sx(6), sx(px) + sx(6), sx(py) + sx(6)], fill=ink)

    def ic_chart(cx, cy):
        bx, by = cx - 50, cy + 40
        d.line([(sx(bx), sx(cy - 44)), (sx(bx), sx(by)), (sx(bx + 100), sx(by))], fill=ink, width=max(1, S))
        for i, hh in enumerate([28, 50, 38, 66]):
            x = bx + 16 + i * 22
            d.rectangle([sx(x), sx(by - hh), sx(x + 14), sx(by)], fill=ink)

    def ic_chat(cx, cy):
        d.rounded_rectangle([sx(cx - 52), sx(cy - 38), sx(cx + 52), sx(cy + 18)], radius=sx(14), outline=ink, width=max(1, 2 * S))
        d.polygon([(sx(cx - 24), sx(cy + 16)), (sx(cx - 6), sx(cy + 16)), (sx(cx - 22), sx(cy + 36))], fill=ink)
        d.text((sx(cx), sx(cy - 32)), "AI", font=F(30), fill=ink, anchor="ma")

    def ic_robot(cx, cy):
        d.line([(sx(cx), sx(cy - 54)), (sx(cx), sx(cy - 38))], fill=ink, width=max(1, 2 * S))
        d.ellipse([sx(cx) - sx(4), sx(cy - 58), sx(cx) + sx(4), sx(cy - 50)], fill=ink)
        d.rounded_rectangle([sx(cx - 42), sx(cy - 38), sx(cx + 42), sx(cy + 30)], radius=sx(12), outline=ink, width=max(1, 2 * S))
        for ex in (-18, 18):
            d.ellipse([sx(cx + ex) - sx(9), sx(cy - 12) - sx(9), sx(cx + ex) + sx(9), sx(cy - 12) + sx(9)], fill=ink)
        d.line([(sx(cx - 16), sx(cy + 12)), (sx(cx + 16), sx(cy + 12))], fill=ink, width=max(1, 2 * S))

    for fx in [(95, 118, 200, 210, lime, ic_net), (390, 104, 200, 210, blue, ic_chart),
               (685, 118, 200, 210, red, ic_chat), (980, 104, 200, 210, yellow, ic_robot)]:
        frame(*fx)

    # "首届" rosette medal
    mx, my = 590, 362
    glow(img, lambda dd: dd.ellipse([sx(mx) - sx(30), sx(my) - sx(30), sx(mx) + sx(30), sx(my) + sx(30)], fill=(255, 77, 28, 110)), blur=10)
    d.polygon([(sx(mx - 14), sx(my + 18)), (sx(mx - 4), sx(my + 60)), (sx(mx + 2), sx(my + 42))], fill=blue)
    d.polygon([(sx(mx + 14), sx(my + 18)), (sx(mx + 4), sx(my + 60)), (sx(mx - 2), sx(my + 42))], fill=red)
    for ang in range(0, 360, 30):
        rx, ry = mx + 30 * math.cos(math.radians(ang)), my + 30 * math.sin(math.radians(ang))
        d.line([(sx(mx), sx(my)), (sx(rx), sx(ry))], fill=yellow, width=max(1, 2 * S))
    d.ellipse([sx(mx) - sx(24), sx(my) - sx(24), sx(mx) + sx(24), sx(my) + sx(24)], fill=red, outline=ink, width=max(1, 2 * S))
    d.text((sx(mx), sx(my)), "首届", font=F(16), fill=paper, anchor="mm")

    scrim(img, color=paper, start=0.52, strength=0.96)
    meta(img, "HACKATHON · 首届 AI 黑客松", red, "学生作品 · 展台",
         [("信电学院 · 人工智能学院", (70, 60, 45))], title_color=ink, title_shadow=None)
    finish(img, "hackathon")

# ================================================================ VIRTUAL HOUSE
def build_virtual_house():
    img = vgrad([(0, (60, 46, 34)), (1, (32, 24, 18))])
    d = ImageDraw.Draw(img)
    VP = (560, 346)
    BL, BR, TL, TR = (358, 452), (812, 452), (358, 206), (812, 206)

    d.polygon([(sx(0), sx(800)), (sx(1280), sx(800)), (sx(BR[0]), sx(BR[1])), (sx(BL[0]), sx(BL[1]))], fill=(122, 88, 56))   # floor
    d.polygon([(sx(0), sx(0)), (sx(1280), sx(0)), (sx(TR[0]), sx(TR[1])), (sx(TL[0]), sx(TL[1]))], fill=(92, 75, 60))        # ceiling
    d.polygon([(sx(0), sx(0)), (sx(TL[0]), sx(TL[1])), (sx(BL[0]), sx(BL[1])), (sx(0), sx(800))], fill=(118, 93, 71))        # left wall
    d.polygon([(sx(1280), sx(0)), (sx(TR[0]), sx(TR[1])), (sx(BR[0]), sx(BR[1])), (sx(1280), sx(800))], fill=(168, 134, 100))  # right wall
    d.rectangle([sx(TL[0]), sx(TL[1]), sx(BR[0]), sx(BR[1])], fill=(150, 120, 92))                                          # back wall

    for fx in range(-7, 8):                                # floorboard seams converge to VP
        d.line([(sx(560 + fx * 95), sx(800)), (sx(VP[0]), sx(VP[1]))], fill=(86, 60, 38, 130), width=max(1, S))
    for i in range(1, 7):
        t = (i / 7) ** 1.7; y = 452 + (800 - 452) * t
        d.line([(0, sx(y)), (WS, sx(y))], fill=(86, 60, 38, int(95 * (1 - t) + 18)), width=max(1, S))

    # sunset window on the back wall
    wx0, wy0, wx1, wy1 = 600, 236, 792, 430
    win = Image.new("RGB", (sx(wx1 - wx0), sx(wy1 - wy0)))
    wd = ImageDraw.Draw(win)
    for yy in range(win.height):
        t = yy / win.height
        if t < 0.62:
            c = tuple(int(a + (b - a) * (t / 0.62)) for a, b in zip((255, 222, 150), (255, 168, 96)))
        else:
            c = tuple(int(a + (b - a) * ((t - 0.62) / 0.38)) for a, b in zip((255, 168, 96), (150, 92, 110)))
        wd.line([(0, yy), (win.width, yy)], fill=c)
    img.paste(win, (sx(wx0), sx(wy0)))
    glow(img, lambda dd: dd.ellipse([sx(696) - sx(30), sx(356) - sx(30), sx(696) + sx(30), sx(356) + sx(30)], fill=(255, 246, 214, 235)), blur=16)
    d.ellipse([sx(696) - sx(20), sx(356) - sx(20), sx(696) + sx(20), sx(356) + sx(20)], fill=(255, 250, 224))
    d.rectangle([sx(wx0), sx(wy0), sx(wx1), sx(wy1)], outline=(46, 34, 24), width=sx(8))
    d.line([(sx((wx0 + wx1) / 2), sx(wy0)), (sx((wx0 + wx1) / 2), sx(wy1))], fill=(46, 34, 24), width=sx(5))
    d.line([(sx(wx0), sx((wy0 + wy1) / 2)), (sx(wx1), sx((wy0 + wy1) / 2))], fill=(46, 34, 24), width=sx(5))
    shaft = layer()
    ImageDraw.Draw(shaft).polygon([(sx(wx0), sx(452)), (sx(wx1), sx(452)), (sx(wx1 - 150), sx(720)), (sx(wx0 - 360), sx(720))], fill=(255, 206, 124, 70))
    img.alpha_composite(shaft.filter(ImageFilter.GaussianBlur(16 * S)))

    def floor_shadow(cx, cy, rw, rh):
        sl = layer()
        ImageDraw.Draw(sl).ellipse([sx(cx - rw), sx(cy - rh), sx(cx + rw), sx(cy + rh)], fill=(0, 0, 0, 115))
        img.alpha_composite(sl.filter(ImageFilter.GaussianBlur(9 * S)))

    # wall art on the left wall (perspective)
    d.polygon([(sx(150), sx(298)), (sx(248), sx(284)), (sx(248), sx(398)), (sx(150), sx(420))], fill=(60, 46, 36))
    d.polygon([(sx(162), sx(308)), (sx(238), sx(296)), (sx(238), sx(388)), (sx(162), sx(406))], fill=(150, 170, 175))
    d.polygon([(sx(162), sx(372)), (sx(238), sx(360)), (sx(238), sx(388)), (sx(162), sx(406))], fill=(96, 126, 120))

    # pendant light
    d.line([(sx(470), sx(0)), (sx(470), sx(150))], fill=(40, 30, 22), width=max(1, S))
    d.polygon([(sx(452), sx(150)), (sx(488), sx(150)), (sx(480), sx(178)), (sx(460), sx(178))], fill=(54, 42, 32))
    glow(img, lambda dd: dd.ellipse([sx(470) - sx(20), sx(182) - sx(20), sx(470) + sx(20), sx(182) + sx(20)], fill=(255, 226, 150, 200)), blur=14)

    # rug
    rug = layer(); dru = ImageDraw.Draw(rug)
    dru.polygon([(sx(372), sx(636)), (sx(742), sx(636)), (sx(828), sx(764)), (sx(286), sx(764))], fill=(176, 120, 96, 225))
    dru.polygon([(sx(404), sx(652)), (sx(712), sx(652)), (sx(774), sx(748)), (sx(342), sx(748))], outline=(214, 166, 134, 230), width=max(1, 2 * S))
    img.alpha_composite(rug)

    # sofa (cool tone to pop against the warm room)
    floor_shadow(520, 612, 190, 30)
    sofa, sofa_d, sofa_l = (98, 122, 136), (74, 94, 106), (124, 148, 160)
    d.rectangle([sx(392), sx(498), sx(648), sx(548)], fill=sofa_d)                       # backrest
    d.rectangle([sx(392), sx(498), sx(648), sx(512)], fill=sofa_l)
    d.rectangle([sx(384), sx(508), sx(420), sx(602)], fill=sofa)                         # left arm
    d.rectangle([sx(620), sx(508), sx(656), sx(602)], fill=sofa)                         # right arm
    d.rectangle([sx(384), sx(508), sx(398), sx(602)], fill=sofa_l)
    d.rectangle([sx(414), sx(540), sx(626), sx(596)], fill=sofa)                         # seat
    for cxs in (446, 520, 594):                                                         # cushions
        d.line([(sx(cxs), sx(542)), (sx(cxs), sx(594))], fill=sofa_d, width=max(1, S))
        d.rectangle([sx(cxs - 34), sx(516), sx(cxs + 34), sx(548)], fill=sofa_l, outline=sofa_d, width=max(1, S))

    # coffee table on the rug
    floor_shadow(556, 712, 130, 24)
    d.polygon([(sx(486), sx(686)), (sx(636), sx(686)), (sx(668), sx(712)), (sx(454), sx(712))], fill=(150, 100, 64))
    d.polygon([(sx(454), sx(712)), (sx(668), sx(712)), (sx(668), sx(720)), (sx(454), sx(720))], fill=(108, 72, 46))
    for lx in (470, 652):
        d.rectangle([sx(lx), sx(712), sx(lx + 10), sx(744)], fill=(96, 64, 40))

    # floor lamp (right)
    glow(img, lambda dd: dd.ellipse([sx(892) - sx(40), sx(494) - sx(40), sx(892) + sx(40), sx(494) + sx(40)], fill=(255, 224, 150, 150)), blur=22)
    d.rectangle([sx(888), sx(500), sx(896), sx(706)], fill=(50, 38, 28))
    d.ellipse([sx(860), sx(700), sx(924), sx(716)], fill=(40, 30, 22))
    d.polygon([(sx(866), sx(500)), (sx(918), sx(500)), (sx(906), sx(456)), (sx(878), sx(456))], fill=(255, 226, 158))

    # potted plant (left foreground)
    floor_shadow(196, 742, 60, 18)
    d.polygon([(sx(168), sx(700)), (sx(224), sx(700)), (sx(214), sx(748)), (sx(178), sx(748))], fill=(170, 96, 64))
    d.polygon([(sx(168), sx(700)), (sx(224), sx(700)), (sx(220), sx(712)), (sx(172), sx(712))], fill=(196, 120, 84))
    for lx, ly, lw, lh, cc in [(196, 660, 16, 56, (70, 120, 70)), (174, 672, 14, 44, (88, 140, 84)),
                               (218, 672, 14, 44, (88, 140, 84)), (196, 642, 13, 40, (104, 158, 96))]:
        d.ellipse([sx(lx - lw), sx(ly - lh), sx(lx + lw), sx(ly + lh)], fill=cc)

    # warm ambience
    amb = layer()
    ImageDraw.Draw(amb).ellipse([sx(696 - 360), sx(356 - 280), sx(696 + 360), sx(356 + 280)], fill=(255, 190, 110, 46))
    img.alpha_composite(amb.filter(ImageFilter.GaussianBlur(90 * S)))

    scrim(img, color=(28, 18, 12), start=0.5, strength=0.9)
    vignette(img, strength=0.5, inner=0.62)
    meta(img, "VIRTUAL HOUSE · 虚拟看房", (255, 228, 184), "样板间 · 沉浸式漫游",
         [("两室一厅 · 灯光 / 家具 / 装修 ", (225, 214, 198)), ("自由调", (255, 210, 140))])
    finish(img, "virtual-house")

if __name__ == "__main__":
    build_port()
    build_airport()
    build_solar()
    build_hackathon()
    build_virtual_house()
