#!/usr/bin/env python3
"""Generate a brand "ecosystem-tank" QR card for the CJY site.

Pipeline:  segno (encode, ECC=H)  ->  writes a self-contained tools/qr.html
           ->  render to public/qr.png with Chromium (see make_qr.js)

ECC level H (~30% recovery) lets the centre 🦞 logo sit on the code without
breaking scannability. The code itself stays ink-on-cream (max contrast);
all the lobster/tank colour lives in the frame around it.
"""
import json, pathlib, segno

URL = "https://cjy77.zeabur.app"
qr = segno.make(URL, error="h")
rows = ["".join(str(m) for m in row) for row in qr.matrix_iter(border=0)]
print(f"encoded {URL!r}  version={qr.version}  ecc=H  modules={len(rows)}x{len(rows)}")

TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;600;700&family=Noto+Sans+SC:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
<style>
  * { margin: 0; box-sizing: border-box; }
  html, body { width: 920px; height: 1300px; }
  body {
    display: flex; align-items: center; justify-content: center;
    background: #F7F2E4;
    background-image:
      linear-gradient(rgba(20,17,11,.05) 1.5px, transparent 1.5px),
      linear-gradient(90deg, rgba(20,17,11,.05) 1.5px, transparent 1.5px);
    background-size: 34px 34px;
    font-family: "Noto Sans SC", "Space Grotesk", system-ui, sans-serif;
  }
  .card {
    position: relative; width: 820px; height: 1170px; overflow: hidden;
    display: flex; flex-direction: column; align-items: center; padding: 46px 50px 0;
    color: #F7F2E4; border: 8px solid #14110B; border-radius: 36px; box-shadow: 16px 16px 0 #14110B;
    background:
      radial-gradient(125% 80% at 50% -12%, rgba(255,255,255,.20), rgba(255,255,255,0) 58%),
      linear-gradient(180deg, #3a54f1 0%, #2a45ee 46%, #1f37c8 100%);
  }
  /* god-ray light shafts */
  .rays { position: absolute; left:0; top:0; right:0; bottom:0; z-index: 1; overflow: hidden; mix-blend-mode: screen; }
  .rays i { position: absolute; top: -12%; width: 95px; height: 150%;
    background: linear-gradient(#fff, rgba(255,255,255,0) 70%); filter: blur(11px); opacity: .15; transform: skewX(-17deg); }
  /* bubbles */
  .bub { position: absolute; z-index: 2; border-radius: 50%; border: 2px solid rgba(255,255,255,.55); background: rgba(255,255,255,.10); }
  /* header */
  .head { position: relative; z-index: 3; width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
  /* intro chips — what I do */
  .chips { position: relative; z-index: 3; display: flex; flex-wrap: wrap; justify-content: center; gap: 13px; max-width: 700px; margin-bottom: 28px; }
  .chip { font-weight: 700; font-size: 18px; color: #14110B; background: #FFFBF0; border: 3px solid #14110B;
    border-radius: 999px; padding: 9px 18px; box-shadow: 4px 4px 0 #14110B; }
  .chip--lime { background: #C8FF2D; }
  .brand { display: flex; align-items: center; gap: 15px; }
  .brand .logo { font-size: 56px; line-height: 1; filter: drop-shadow(3px 3px 0 rgba(20,17,11,.35)); }
  .name { font-weight: 900; font-size: 32px; color: #fff; letter-spacing: .5px; text-shadow: 2px 2px 0 rgba(20,17,11,.35); }
  .vibe { font: 700 15px/1 "Space Mono", monospace; color: #C8FF2D; letter-spacing: 2.5px; margin-top: 6px; }
  .badge { font-weight: 900; font-size: 19px; color: #14110B; background: #C8FF2D; border: 3px solid #14110B;
    border-radius: 999px; padding: 11px 20px; box-shadow: 4px 4px 0 #14110B; transform: rotate(3deg); }
  /* QR "glass" panel */
  .panel { position: relative; z-index: 3; background: #F7F2E4; border: 6px solid #14110B; border-radius: 26px;
    box-shadow: 11px 11px 0 #14110B; padding: 30px; }
  #qr { display: block; width: 520px; height: 520px; shape-rendering: crispEdges; }
  .center { position: absolute; left: 30px; top: 30px; right: 30px; bottom: 30px; display: flex; align-items: center; justify-content: center; pointer-events: none; }
  .plate { background: #F7F2E4; border: 4px solid #14110B; border-radius: 18px; box-shadow: 3px 3px 0 rgba(20,17,11,.55);
    display: flex; align-items: center; justify-content: center; }
  .plate span { line-height: 1; filter: drop-shadow(2px 2px 0 rgba(20,17,11,.25)); }
  /* caption */
  .foot { position: relative; z-index: 3; margin-top: 26px; text-align: center; }
  .cap { font-weight: 900; font-size: 27px; color: #fff; text-shadow: 2px 2px 0 rgba(20,17,11,.4); }
  .url { display: inline-block; margin-top: 15px; font: 700 21px/1 "Space Mono", monospace; color: #14110B;
    background: #C8FF2D; border: 3px solid #14110B; border-radius: 999px; padding: 10px 20px; box-shadow: 4px 4px 0 #14110B; }
  /* planted tank floor */
  .flora { position: absolute; left: 0; right: 0; bottom: 0; height: 150px; z-index: 2; pointer-events: none; }
  .weed { position: absolute; bottom: -4px; }
  .peb { position: absolute; bottom: -6px; border: 2px solid #14110B; border-radius: 50% 50% 46% 46% / 64% 64% 40% 40%; }
</style>
</head>
<body>
  <div class="card">
    <div class="rays"><i style="left:12%"></i><i style="left:46%;opacity:.10"></i><i style="left:78%;width:120px"></i></div>
    <span class="bub" style="width:18px;height:18px;left:8%;top:24%"></span>
    <span class="bub" style="width:11px;height:11px;left:88%;top:30%"></span>
    <span class="bub" style="width:26px;height:26px;left:84%;top:54%"></span>
    <span class="bub" style="width:9px;height:9px;left:14%;top:60%"></span>
    <span class="bub" style="width:15px;height:15px;left:6%;top:78%"></span>
    <span class="bub" style="width:13px;height:13px;left:92%;top:80%"></span>

    <div class="head">
      <div class="brand">
        <span class="logo">🦞</span>
        <div><div class="name">CJY · 陈俊烨</div><div class="vibe">VIBE CODER · 生态缸</div></div>
      </div>
      <div class="badge">扫码 ↓</div>
    </div>

    <div class="chips">
      <span class="chip">AI 教育系统数字化</span>
      <span class="chip">未来课堂探索</span>
      <span class="chip chip--lime">AI 多模态</span>
    </div>

    <div class="panel">
      <svg id="qr" xmlns="http://www.w3.org/2000/svg"></svg>
      <div class="center"><div class="plate"><span>🦞</span></div></div>
    </div>

    <div class="foot">
      <div class="cap">扫码游进我的生态缸 🦞</div>
      <div class="url">__DISPLAY__</div>
    </div>

    <div class="flora" id="flora"></div>
  </div>

<script>
  const QR_ROWS = __ROWS__;
  const M = QR_ROWS.map(s => Array.prototype.map.call(s, Number));
  const n = M.length, quiet = 4, size = n + quiet * 2;
  const svg = document.getElementById("qr");
  svg.setAttribute("viewBox", `0 0 ${size} ${size}`);
  // central knockout for the lobster logo (ECC-H tolerates it)
  const lw = Math.max(5, Math.round(n * 0.20));
  const lo = (n - lw) >> 1, lhi = lo + lw - 1;
  let rects = "";
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
    if (!M[r][c]) continue;
    if (r >= lo && r <= lhi && c >= lo && c <= lhi) continue;
    rects += `<rect x="${c + quiet}" y="${r + quiet}" width="1" height="1"/>`;
  }
  svg.innerHTML = `<rect width="${size}" height="${size}" fill="#F7F2E4"/><g fill="#14110B">${rects}</g>`;
  // size the lobster plate to the knockout
  const qpx = 520, ps = Math.round((lw / size) * qpx) - 2;
  const plate = document.querySelector(".plate");
  plate.style.width = plate.style.height = ps + "px";
  plate.querySelector("span").style.fontSize = Math.round(ps * 0.6) + "px";

  // a few seaweed blades + pebbles along the bottom
  const blade = (h, w, fill) =>
    `<svg class="weed" width="${w}" height="${h}" viewBox="0 0 40 160" preserveAspectRatio="none">` +
    `<path d="M20 160 C 6 122, 33 92, 16 62 C 5 38, 30 20, 20 0 C 24 28, 9 44, 22 70 C 34 100, 11 132, 20 160 Z" ` +
    `fill="${fill}" stroke="#14110B" stroke-width="3" stroke-linejoin="round"/></svg>`;
  const greens = ["#C8FF2D", "#3DDC97", "#1F9E6E"];
  const flora = document.getElementById("flora");
  const blades = [[6,118],[15,150],[26,96],[50,140],[70,108],[80,150],[91,124]];
  let fh = "";
  blades.forEach(([left, h], i) => {
    const w = h * 0.26;
    fh += `<span style="position:absolute;bottom:-4px;left:${left}%;transform:translateX(-50%) rotate(${(i%2?1:-1)*3}deg);opacity:${i%3?.95:.7}">${blade(h, w, greens[i%3])}</span>`;
  });
  const pebs = [[4,40],[12,30],[20,46],[33,34],[48,52],[63,30],[78,44],[90,36],[97,40]];
  pebs.forEach(([left, w]) => {
    const h = w * (0.55 + Math.random()*0.18), col = ["#CBB68A","#A7A290","#86A05A","#5E6B49"][(Math.random()*4)|0];
    fh += `<span class="peb" style="left:${left}%;width:${w|0}px;height:${h|0}px;background:${col};transform:translateX(-50%)"></span>`;
  });
  flora.innerHTML = fh;

  // a couple of little fish drifting in the side margins (clear of the code)
  const fish = (c) =>
    `<svg width="42" height="26" viewBox="0 0 36 22">` +
    `<path d="M3 11 C 6 3.5,21 3.5,26 11 C 21 18.5,6 18.5,3 11 Z" fill="${c}" stroke="#14110B" stroke-width="1.6"/>` +
    `<path d="M24.5 11 L34 5 L32 11 L34 17 Z" fill="${c}" stroke="#14110B" stroke-width="1.6" stroke-linejoin="round"/>` +
    `<circle cx="9" cy="9.4" r="1.5" fill="#14110B"/></svg>`;
  const fishes = [[6.5,40,1,"#FF5DA2"],[93.5,53,-1,"#3DDC97"],[8,72,1,"#C8FF2D"]];
  let fhtml = "";
  fishes.forEach(([l, t, dir, col]) => {
    fhtml += `<span style="position:absolute;z-index:2;left:${l}%;top:${t}%;` +
             `transform:translate(-50%,-50%) scaleX(${dir});opacity:.92;` +
             `filter:drop-shadow(2px 2px 0 rgba(20,17,11,.25))">${fish(col)}</span>`;
  });
  document.querySelector(".card").insertAdjacentHTML("beforeend", fhtml);
</script>
</body>
</html>"""

html = (TEMPLATE
        .replace("__ROWS__", json.dumps(rows))
        .replace("__DISPLAY__", "cjy77.zeabur.app"))
out = pathlib.Path(__file__).resolve().parent / "qr.html"
out.write_text(html, encoding="utf-8")
print("wrote", out)
