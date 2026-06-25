/* =====================================================================
   CJY · 陈俊烨 — interactions
   ===================================================================== */
(() => {
  "use strict";
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Web Animations API — present on evergreen browsers; guard so older ones degrade quietly
  const HAS_WAAPI = typeof Element !== "undefined" && typeof Element.prototype.animate === "function";

  /* ---------- footer year ---------- */
  $("#year").textContent = new Date().getFullYear();

  /* ---------- intro splash (once per session, skippable) ---------- */
  const intro = $("#intro");
  if (intro) {
    let introed = false;
    try { introed = sessionStorage.getItem("cjy-introed") === "1"; } catch (_) {}
    if (reduceMotion || introed) {
      intro.remove();
    } else {
      try { sessionStorage.setItem("cjy-introed", "1"); } catch (_) {}
      document.body.style.overflow = "hidden";
      const fill = $("#introFill"), pct = $("#introPct");
      const DUR = 1300, t0 = performance.now();
      let raf = 0, closed = false;
      const draw = (now) => {
        const t = Math.min(1, (now - t0) / DUR);
        const v = Math.round((1 - Math.pow(1 - t, 2)) * 100); // ease-out toward 100%
        if (fill) fill.style.width = v + "%";
        if (pct) pct.textContent = v + "%";
        if (t < 1) raf = requestAnimationFrame(draw);
      };
      raf = requestAnimationFrame(draw);
      const finish = () => {
        if (closed) return; closed = true;
        cancelAnimationFrame(raf);
        if (fill) fill.style.width = "100%";
        if (pct) pct.textContent = "100%";
        intro.classList.add("is-done");
        document.body.style.overflow = "";
        setTimeout(() => intro.remove(), 820);
        ["pointerdown", "keydown", "wheel", "touchstart"].forEach((e) => window.removeEventListener(e, onSkip));
      };
      const onSkip = () => { clearTimeout(timer); finish(); };
      const timer = setTimeout(finish, 1750);
      ["pointerdown", "keydown", "wheel", "touchstart"].forEach((e) =>
        window.addEventListener(e, onSkip, { passive: true }));
    }
  }

  /* ---------- site-wide ambient bubbles ---------- */
  const ambient = $("#ambient");
  if (ambient && !reduceMotion) {
    let html = "";
    for (let i = 0; i < 14; i++) {
      const size = 10 + Math.random() * 42;
      const left = Math.random() * 100;
      const dur = 14 + Math.random() * 16;
      const delay = -Math.random() * dur;
      html += `<span style="left:${left.toFixed(1)}%;width:${size | 0}px;height:${size | 0}px;` +
              `animation-duration:${dur.toFixed(1)}s;animation-delay:${delay.toFixed(1)}s"></span>`;
    }
    ambient.innerHTML = html;
  }

  /* ---------- water-current dividers between sections (one descending tank) ---------- */
  ["lobster", "projects", "journey", "campus", "volunteer", "contact"].forEach((id) => {
    const sec = document.getElementById(id);
    if (!sec || !sec.parentNode) return;
    const cur = document.createElement("div");
    cur.className = "current";
    cur.setAttribute("aria-hidden", "true");
    sec.parentNode.insertBefore(cur, sec);
  });

  /* ===================================================================
     Project data → cards
     =================================================================== */
  // shot: drop a screenshot path (e.g. "shots/cargo.jpg") to replace the placeholder.
  // featured: renders as a larger "代表作" card. tint: placeholder accent colour.
  const projects = [
    { emoji: "🛡️", cat: "系统平台", title: "研究生院督导管理系统",
      desc: "浙江工商大学研究生院的教学督导全流程数字化管理平台。",
      url: "http://121.196.217.243/login", tint: "#FF4D1C", shot: "shots/supervision.png" },
    { emoji: "🦞", cat: "AI Agent", title: "会议室预约虾",
      desc: "会议室预约智能体：自然语言下单，自动排期与冲突检测。",
      url: "https://meetroomshrimp-gvfhrxz8.manus.space", tint: "#FF5DA2", shot: "shots/meetshrimp.png" },
    { emoji: "🏢", cat: "数字孪生", title: "会议室预约虾 · 3D 数字孪生",
      desc: "会议室预约的三维现实镜像：6 间会议室实时占用、全天时段回放、3D 预约。",
      url: "https://zjgsu.vercel.app/", tint: "#2B47F0", shot: "shots/zjgsu.png" },
    { emoji: "🚢", cat: "数字孪生", title: "智慧港口数字孪生",
      desc: "港口装卸与物流的三维孪生可视化，实时映射运营态势。",
      url: "https://cargo-claw.vercel.app", tint: "#2B47F0", shot: "shots/cargo-claw.png" },
    { emoji: "✈️", cat: "数字孪生", title: "成都天府国际机场孪生",
      desc: "天府国际机场的数字孪生模拟，空地协同的可视化沙盘。",
      url: "http://aerotwin-tfu.vercel.app/", tint: "#2B47F0", shot: "shots/aerotwin.png" },
    { emoji: "🛢️", cat: "数字孪生", title: "海上油田视觉模拟",
      desc: "海上油田钻井平台的数字孪生与视觉仿真演示。",
      url: "https://deepblue-rig.vercel.app/", tint: "#2B47F0", shot: "shots/deepblue-rig.png" },
    { emoji: "🏠", cat: "VR / 3D", title: "虚拟看房 · 样板间漫游",
      desc: "沉浸式样板间漫游，第一视角自由穿行的虚拟看房体验。",
      url: "https://virtual-reality-mocha.vercel.app/", tint: "#C8FF2D", shot: "shots/virtual-house.png" },
    { emoji: "🪐", cat: "3D 可视化", title: "太阳系模拟与漫游",
      desc: "可交互的太阳系三维模拟，自由漫游每一颗行星。",
      url: "https://virtual-universe-eight.vercel.app/", tint: "#7A5CFF", shot: "shots/solar.png" },
    { emoji: "🎨", cat: "作品展台", title: "首届 AI 黑客松作品展",
      desc: "信电学院 · 人工智能学院首届 AI 黑客松大赛学生作品展示。",
      url: "http://43.133.22.250:8089/", tint: "#FF4D1C", shot: "shots/hackathon.png" },
  ];

  const fmtHost = (u) => { try { return new URL(u).host; } catch { return u; } };

  const grid = $("#projectsGrid");
  if (grid) {
    grid.innerHTML = projects.map((p) => `
      <a class="pcard reveal${p.featured ? " pcard--feat" : ""}" data-reveal href="${p.url}" target="_blank" rel="noopener">
        <div class="pcard__thumb" style="--tint:${p.tint || "var(--blue)"}">
          <span class="pcard__ghost">${p.emoji}</span>
          ${p.shot
            ? `<img class="pcard__shot" src="${p.shot}" alt="${p.title} 预览" loading="lazy" onerror="this.remove()">`
            : `<span class="pcard__soon">预览即将上线</span>`}
          <span class="pcard__cat">${p.cat}</span>
        </div>
        <div class="pcard__body">
          <h3>${p.title}</h3>
          <p>${p.desc}</p>
          <div class="pcard__foot">
            <span class="pcard__url">${fmtHost(p.url)}</span>
            <span class="pcard__arrow">↗</span>
          </div>
        </div>
      </a>`).join("");
  }

  /* ===================================================================
     Hackathon timeline data → items
     =================================================================== */
  const T = (label, type = "") => ({ label, type });
  const journey = [
    { date: "2025.11.22", title: "魔搭社区开发者嘉年华 · 支付宝 MCP 开发黑客松",
      tags: [T("🦞 第一次黑客松", "first"), T("参赛者")], star: true },
    { date: "2025.11.30", title: "way to AGI 上海站 · 全球 30+ 城市 / 泰国清迈联动",
      tags: [T("第二次黑客松"), T("参赛者")] },
    { date: "2026.01.08", title: "信电学院 · 人工智能学院 AI 应用创新大赛",
      tags: [T("🏆 一等奖", "award")] },
    { date: "2026.01.16–18", title: "环球黑客松 · 杭州站",
      tags: [T("志愿者"), T("参赛者")] },
    { date: "2026.01.22", title: "百度千帆 Agent 训练营",
      tags: [T("🏆 最佳技术奖", "award")] },
    { date: "2026.01.23–25", title: "上海黑客松 · less is more",
      tags: [T("志愿者"), T("参赛者")] },
    { date: "2026.01.31–02.02", title: "南京模法学院 S2 赛季 ·「以赛促产」黑客松",
      tags: [T("志愿者")] },
    { date: "2026.02.07–08", title: "全国 10 城联动汤泉黑客松 · 太原站",
      tags: [T("⭐ 主办方负责人", "lead"), T("首次转向管理视角")], star: true },
    { date: "2026.03.07–08", title: "中国高校联盟 AI Hackathon Tour · 浙大线下复赛",
      tags: [T("协办方"), T("物资 / 复赛保障")] },
    { date: "2026.03.14–15", title: "中国高校联盟 AI Hackathon Tour · 西安交大站",
      tags: [T("协办方")] },
    { date: "2026.03.28", title: "GDPS Astron 产业智变黑客松",
      tags: [T("🏆 一等奖", "award")] },
    { date: "2026.03.27–29", title: "GDPS 上海全球开发者先锋大会",
      tags: [T("志愿者服务")] },
    { date: "2026.03.29", title: "商汤龙虾节 · SenseAudio & AudioClaw 多场景 Skills 创新赛",
      tags: [T("🥈 二等奖", "award")] },
    { date: "2026.03.29", title: "上海徐汇 · Agent 进化酒馆黑客松",
      tags: [T("🏆 最佳人气奖", "award")] },
    { date: "2026.04.09", title: "小红书黑客松巅峰赛",
      tags: [T("志愿者 / 工作人员"), T("参赛者")] },
    { date: "2026.04.23", title: "春潮 Spring｜深圳 OpenClaw 黑客松",
      tags: [T("参赛者")] },
    { date: "2026.05.01", title: "南京 Flux 南客松 S2 ·「Life's Short, Play More」赛道",
      tags: [T("🥈 银奖", "award")] },
    { date: "2026.05.31", title: "上海外滩 FTC！繁星计划 · FunSkills 初赛 + 决赛",
      tags: [T("工作人员")] },
    { date: "2026.06.12", title: "信电学院 · 人工智能学院首届 AI 黑客松大赛",
      tags: [T("宣传落地设计")] },
  ];

  const tagClass = (t) => t === "award" ? "tl-tag tl-tag--award"
    : t === "lead" ? "tl-tag tl-tag--lead"
    : t === "first" ? "tl-tag tl-tag--first" : "tl-tag";

  const tl = $("#timeline");
  if (tl) {
    tl.innerHTML = journey.map((e) => `
      <div class="tl-item${e.star ? " tl-item--star" : ""} reveal" data-reveal>
        <div class="tl-date">${e.date}</div>
        <div class="tl-body">
          <p class="tl-title">${e.title}</p>
          <div class="tl-role">
            ${e.tags.map((t) => `<span class="${tagClass(t.type)}">${t.label}</span>`).join("")}
          </div>
        </div>
      </div>`).join("");
  }

  /* ===================================================================
     Underwater bubbles inside the lobster ecosystem panel
     =================================================================== */
  const bubbleHost = $("#lobBubbles");
  if (bubbleHost && !reduceMotion) {
    const panelH = Math.max((bubbleHost.parentElement?.offsetHeight || 0), 360);
    let html = "";
    for (let i = 0; i < 11; i++) {
      const size = 8 + Math.random() * 26;
      const left = Math.random() * 100;
      const dur = 7 + Math.random() * 8;
      const delay = -Math.random() * dur;     // negative → already distributed on load
      html += `<span style="left:${left.toFixed(1)}%;width:${size | 0}px;height:${size | 0}px;` +
              `--rise:${(panelH + 80) | 0}px;animation-duration:${dur.toFixed(1)}s;animation-delay:${delay.toFixed(1)}s"></span>`;
    }
    bubbleHost.innerHTML = html;
  }

  /* ===================================================================
     Swaying seaweed — makes the whole page feel like an ecosystem tank 🌿
     =================================================================== */
  // one tapering, gently-curved seaweed blade as an inline <svg>
  const bladeSVG = (h, w, fill, stroke, waves, phase) => {
    const steps = 14, L = [], R = [];
    let minX = Infinity, maxX = -Infinity;
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const y = +(h - t * h).toFixed(1);
      const halfW = (w * 0.5) * (1 - t * 0.9) + 0.6;        // taper to a soft point
      const cx = w * 0.5 + Math.sin(phase + t * waves * Math.PI) * (w * 0.7) * t; // bends more toward the tip
      const lx = cx - halfW, rx = cx + halfW;
      if (lx < minX) minX = lx; if (rx > maxX) maxX = rx;
      L.push([lx, y]); R.push([rx, y]);
    }
    const pts = L.concat(R.reverse());
    const d = "M" + pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" L") + "Z";
    const pad = 2, vbX = (minX - pad).toFixed(1), vbW = (maxX - minX + pad * 2).toFixed(1);
    const st = stroke ? `stroke="${stroke}" stroke-width="2.2" stroke-linejoin="round"` : "";
    return `<svg width="${vbW}" height="${h | 0}" viewBox="${vbX} 0 ${vbW} ${h | 0}">` +
           `<path d="${d}" fill="${fill}" ${st}/></svg>`;
  };
  const edgeLeft = (edge) => {                              // cluster a position into the two bottom corners
    const r = Math.random() * edge;
    return Math.random() < 0.5 ? r : 100 - r;
  };
  // a field of blades → HTML string (outer .weed = cursor push, inner <i> = idle sway)
  const weedField = (n, o) => {
    let html = "";
    for (let i = 0; i < n; i++) {
      const left = o.edge ? edgeLeft(o.edge) : Math.random() * 100;
      const h = o.hMin + Math.random() * (o.hMax - o.hMin);
      const w = h * (0.12 + Math.random() * 0.07);
      const fill = o.palette[(Math.random() * o.palette.length) | 0];
      const stroke = o.outline && Math.random() < o.outline ? "var(--ink)" : "";
      const svg = bladeSVG(h, w, fill, stroke, 0.7 + Math.random() * 0.8, Math.random() * Math.PI * 2);
      const dur = (4.5 + Math.random() * 3.8).toFixed(2);
      const delay = (-Math.random() * dur).toFixed(2);
      const amp = (2.4 + Math.random() * 3.6).toFixed(1);
      const op = (o.opMin + Math.random() * (o.opMax - o.opMin)).toFixed(2);
      html += `<span class="weed" data-weed style="left:${left.toFixed(1)}%;opacity:${op};z-index:${h | 0}">` +
              `<i style="--sd:${dur}s;--sdl:${delay}s;--amp:${amp}deg">${svg}</i></span>`;
    }
    return html;
  };
  // substrate pebbles → HTML string
  const PEBBLES = ["#CBB68A", "#A7A290", "#86A05A", "#5E6B49"];
  const pebbleRow = (n, o) => {
    let html = "";
    for (let i = 0; i < n; i++) {
      const left = o.edge ? edgeLeft(o.edge) : Math.random() * 100;
      const w = o.wMin + Math.random() * (o.wMax - o.wMin);
      const h = w * (0.5 + Math.random() * 0.22);
      const fill = PEBBLES[(Math.random() * PEBBLES.length) | 0];
      const op = (o.opMin + Math.random() * (o.opMax - o.opMin)).toFixed(2);
      const rot = (Math.random() * 16 - 8).toFixed(1);
      html += `<span class="pebble" style="left:${left.toFixed(1)}%;width:${w | 0}px;height:${h | 0}px;` +
              `background:${fill};opacity:${op};transform:rotate(${rot}deg);z-index:${(w | 0) + 200}"></span>`;
    }
    return html;
  };

  const GREENS = ["#C8FF2D", "#3DDC97", "#1F9E6E"];
  const lobFlora = $("#lobFlora");
  if (lobFlora) {
    const small = window.innerWidth < 640;
    // back blades (faint, depth) → front blades (bold, outlined) → a band of pebbles to root them
    lobFlora.innerHTML =
      weedField(small ? 7 : 12, { hMin: 60, hMax: 150, palette: ["#3DDC97", "#1F9E6E"], outline: 0, opMin: 0.16, opMax: 0.3 }) +
      weedField(small ? 5 : 9, { hMin: 70, hMax: 175, palette: GREENS, outline: 0.7, opMin: 0.7, opMax: 0.95, edge: 30 }) +
      pebbleRow(small ? 9 : 16, { wMin: 16, wMax: 46, opMin: 0.55, opMax: 0.9 });
  }
  const seabed = $("#seabed");
  if (seabed && window.innerWidth >= 720) {                  // skip the tank floor on small screens
    seabed.innerHTML =
      weedField(10, { hMin: 46, hMax: 104, palette: GREENS, outline: 0.5, opMin: 0.14, opMax: 0.26, edge: 17 }) +
      pebbleRow(10, { wMin: 14, wMax: 40, opMin: 0.12, opMax: 0.24, edge: 17 });
  }

  /* ===================================================================
     Aquarium life — click ripples · cursor-parted seaweed · drifting fish
     =================================================================== */
  const pointer = { x: -1, y: -1 };
  const panelEl = $(".lobster__panel");

  // click anywhere → a few bubbles rise from the spot (the water is disturbed)
  const fxLayer = document.createElement("div");
  fxLayer.style.cssText = "position:fixed;inset:0;z-index:9989;pointer-events:none;overflow:hidden";
  fxLayer.setAttribute("aria-hidden", "true");
  document.body.appendChild(fxLayer);
  const disturb = (x, y) => {
    if (reduceMotion || !HAS_WAAPI) return;
    const n = 3 + (Math.random() * 2 | 0);
    for (let i = 0; i < n; i++) {
      const b = document.createElement("span"); b.className = "egg-rise";
      const sz = 5 + Math.random() * 7; b.style.width = b.style.height = `${sz | 0}px`;
      fxLayer.appendChild(b);
      const x0 = x + (Math.random() * 18 - 9), y0 = y + (Math.random() * 8 - 4);
      const rise = 42 + Math.random() * 58, drift = Math.random() * 22 - 11;
      b.animate([
        { transform: `translate(${x0.toFixed(1)}px, ${y0.toFixed(1)}px) scale(.5)`, opacity: 0 },
        { opacity: .85, offset: .15 },
        { transform: `translate(${(x0 + drift).toFixed(1)}px, ${(y0 - rise).toFixed(1)}px) scale(1)`, opacity: 0 },
      ], { duration: 700 + Math.random() * 500, delay: i * 40, easing: "cubic-bezier(.4,0,.5,1)", fill: "forwards" })
        .onfinish = () => b.remove();
    }
  };
  window.addEventListener("pointerdown", (e) => disturb(e.clientX, e.clientY), { passive: true });

  // cursor "parts" the ecosystem seaweed as it sweeps near the tank floor
  const floraWeeds = lobFlora ? [...lobFlora.querySelectorAll("[data-weed]")] : [];
  let pmRaf = 0;
  if (floraWeeds.length && panelEl) {
    let weedMeta = [], lastBand = false;
    const measureWeeds = () => { weedMeta = floraWeeds.map((el) => ({ el, cx: el.offsetLeft + el.offsetWidth / 2 })); };
    measureWeeds();
    window.addEventListener("resize", measureWeeds, { passive: true });
    const updateBend = () => {
      pmRaf = 0;
      const r = panelEl.getBoundingClientRect();
      const band = pointer.x >= 0 && pointer.y > r.bottom - 175 && pointer.y < r.bottom + 55 &&
                   pointer.x > r.left - 70 && pointer.x < r.right + 70;
      if (!band) { if (lastBand) weedMeta.forEach((m) => m.el.style.setProperty("--push", "0deg")); lastBand = false; return; }
      lastBand = true;
      const R = 80, MAX = 17;
      for (const m of weedMeta) {
        const d = pointer.x - (r.left + m.cx);
        const push = Math.abs(d) < R ? -Math.sign(d) * (1 - Math.abs(d) / R) * MAX : 0;
        m.el.style.setProperty("--push", push.toFixed(1) + "deg");
      }
    };
    window.addEventListener("pointermove", (e) => {
      pointer.x = e.clientX; pointer.y = e.clientY;
      if (!pmRaf) pmRaf = requestAnimationFrame(updateBend);
    }, { passive: true });
    document.addEventListener("mouseleave", () => { pointer.x = pointer.y = -1; if (!pmRaf) pmRaf = requestAnimationFrame(updateBend); });
  } else {
    window.addEventListener("pointermove", (e) => { pointer.x = e.clientX; pointer.y = e.clientY; }, { passive: true });
    document.addEventListener("mouseleave", () => { pointer.x = pointer.y = -1; });
  }

  // drifting fish that dart away from the cursor
  const crittersHost = $("#critters");
  if (crittersHost && !reduceMotion) {
    const FISHCOL = ["#3D6E8E", "#4FA3A0", "#7C6B8A", "#C56A3D", "#557A8E"];
    const fishSVG = (c) =>
      `<svg width="36" height="22" viewBox="0 0 36 22">` +
      `<path d="M3 11 C 6 3.5, 21 3.5, 26 11 C 21 18.5, 6 18.5, 3 11 Z" fill="${c}" stroke="#14110B" stroke-width="1.6"/>` +
      `<path d="M24.5 11 L 34 5 L 32 11 L 34 17 Z" fill="${c}" stroke="#14110B" stroke-width="1.6" stroke-linejoin="round"/>` +
      `<circle cx="9" cy="9.4" r="1.5" fill="#14110B"/></svg>`;
    let W = innerWidth, H = innerHeight;
    const N = W < 720 ? 2 : 3;
    const fishes = [];
    const reset = (f, now, spread) => {
      f.dir = Math.random() < 0.5 ? 1 : -1;
      f.scale = 0.55 + Math.random() * 0.6;
      f.baseY = (0.14 + Math.random() * 0.74) * H;
      f.bobA = 6 + Math.random() * 14; f.bobW = 0.8 + Math.random() * 0.9; f.phase = Math.random() * 6.28;
      f.speed = 32 + Math.random() * 36;
      f.x = spread ? Math.random() * W : (f.dir > 0 ? -60 : W + 60);
      f.waitUntil = spread ? 0 : now + (1500 + Math.random() * 5500);
      f.el.style.opacity = (0.18 + Math.random() * 0.16).toFixed(2);
    };
    for (let i = 0; i < N; i++) {
      const el = document.createElement("span");
      el.className = "fish"; el.innerHTML = fishSVG(FISHCOL[(Math.random() * FISHCOL.length) | 0]);
      crittersHost.appendChild(el);
      const f = { el }; reset(f, 0, true); fishes.push(f);
    }
    let last = performance.now(), raf = 0;
    const tick = (now) => {
      const dt = Math.min(0.05, (now - last) / 1000); last = now; const t = now / 1000;
      for (const f of fishes) {
        if (now < f.waitUntil) continue;                  // resting off-screen between crossings
        let sp = f.speed, veer = 0;
        if (pointer.x >= 0) {
          const dx = f.x - pointer.x, dy = f.y - pointer.y, dist = Math.hypot(dx, dy);
          if (dist < 135) { const k = 1 - dist / 135; sp = f.speed * (1 + k * 2.4); veer = Math.sign(dy || 1) * k * 50; }
        }
        f.x += f.dir * sp * dt;
        f.y = f.baseY + Math.sin(t * f.bobW + f.phase) * f.bobA + veer;
        if ((f.dir > 0 && f.x > W + 70) || (f.dir < 0 && f.x < -70)) reset(f, now, false);
        f.el.style.transform = `translate(${f.x.toFixed(1)}px, ${f.y.toFixed(1)}px) scale(${f.scale.toFixed(2)}) scaleX(${f.dir})`;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    window.addEventListener("resize", () => { W = innerWidth; H = innerHeight; }, { passive: true });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) cancelAnimationFrame(raf);
      else { last = performance.now(); cancelAnimationFrame(raf); raf = requestAnimationFrame(tick); }
    });
  }

  /* ===================================================================
     Reveal on scroll — scroll-driven (robust against anchor jumps /
     instant scrollIntoView, where IntersectionObserver can miss firing)
     =================================================================== */
  const revealEls = $$("[data-reveal]");
  // stagger siblings inside grids for a nicer cascade
  $$(".projects__grid [data-reveal], .lobster__grid [data-reveal], .vsteps [data-reveal], .about__cards [data-reveal]")
    .forEach((el, i) => { el.style.transitionDelay = `${(i % 6) * 60}ms`; });

  const reveal = (el) => el.classList.add("is-in");
  let pending = reduceMotion ? [] : revealEls.slice();
  if (reduceMotion) revealEls.forEach(reveal);

  // primary: scroll-driven position check (reliable for wheel / touch /
  // smooth-anchor scrolling and for pages loaded directly at an #anchor)
  const runReveal = () => {
    if (!pending.length) return;
    const vh = window.innerHeight;
    pending = pending.filter((el) => {
      const r = el.getBoundingClientRect();
      if (r.top < vh * 0.92 && r.bottom > -60) { reveal(el); return false; }
      return true;
    });
  };

  // complement: IntersectionObserver catches anything entering the viewport
  // immediately (e.g. very fast flicks the scroll sampler could skip)
  if (!reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          reveal(en.target); io.unobserve(en.target);
          pending = pending.filter((x) => x !== en.target);
        }
      });
    }, { threshold: 0, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach((el) => io.observe(el));
  }

  /* ===================================================================
     Counters
     =================================================================== */
  const animateCount = (el) => {
    const target = +el.dataset.target;
    const suffix = el.dataset.suffix || "";
    if (reduceMotion) { el.textContent = target + suffix; return; }
    const dur = 1400; const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const counters = $$(".counter");
  if (counters.length) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { animateCount(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach((c) => cio.observe(c));
  }

  /* ===================================================================
     Hero rotating role (typewriter)
     =================================================================== */
  const roles = ["Vibe Coder", "AI 教育探索者", "未来课堂建造者", "多模态玩家", "黑客松常旅客 🦞", "全栈开发者"];
  const rotateEl = $("#roleRotate");
  if (rotateEl) {
    if (reduceMotion) {
      rotateEl.textContent = roles[0];
    } else {
      let ri = 0, ci = 0, deleting = false;
      const type = () => {
        const word = roles[ri];
        rotateEl.textContent = word.slice(0, ci);
        if (!deleting && ci < word.length) { ci++; setTimeout(type, 95); }
        else if (!deleting && ci === word.length) { deleting = true; setTimeout(type, 1500); }
        else if (deleting && ci > 0) { ci--; setTimeout(type, 45); }
        else { deleting = false; ri = (ri + 1) % roles.length; setTimeout(type, 320); }
      };
      type();
    }
  }

  /* ===================================================================
     Nav: stuck state, active link, scroll progress, mobile menu
     =================================================================== */
  const nav = $("#nav");
  const progress = $("#scrollProgress");
  const scrollLob = $("#scrollLob");
  let scrollRaf = 0;
  const update = () => {
    scrollRaf = 0;
    const y = window.scrollY;
    nav.classList.toggle("is-stuck", y > 24);
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const pct = (y / (h || 1)) * 100;
    progress.style.width = `${pct}%`;
    if (scrollLob) scrollLob.style.left = `${pct}%`;
    runReveal();
  };
  const onScroll = () => { if (!scrollRaf) scrollRaf = requestAnimationFrame(update); };
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  // initial pass — reveals everything already in view, even if loaded at an anchor
  update();
  // safety re-checks after fonts/layout settle
  window.addEventListener("load", () => requestAnimationFrame(update));
  setTimeout(update, 400);

  // active link via section observer
  const links = $$("#navLinks a");
  const linkMap = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
  const secObserver = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        links.forEach((l) => l.classList.remove("is-active"));
        linkMap.get(en.target.id)?.classList.add("is-active");
      }
    });
  }, { threshold: 0.3, rootMargin: "-30% 0px -55% 0px" });
  ["about", "lobster", "projects", "journey", "campus", "volunteer", "contact"].forEach((id) => {
    const s = document.getElementById(id); if (s) secObserver.observe(s);
  });

  /* ===================================================================
     Contact — copy-to-clipboard buttons
     =================================================================== */
  const copyText = async (t) => {
    try { await navigator.clipboard.writeText(t); return true; }
    catch {
      try {
        const ta = document.createElement("textarea");
        ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.focus(); ta.select();
        const ok = document.execCommand("copy"); ta.remove(); return ok;
      } catch { return false; }
    }
  };
  $$("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const ok = await copyText(btn.getAttribute("data-copy"));
      const original = btn.dataset.label || btn.textContent;
      btn.dataset.label = original;
      btn.textContent = ok ? "已复制 ✓" : "复制失败，请手动复制";
      btn.classList.toggle("is-copied", ok);
      clearTimeout(btn._restore);
      btn._restore = setTimeout(() => { btn.textContent = original; btn.classList.remove("is-copied"); }, 1700);
    });
  });

  // mobile menu
  const burger = $("#navBurger");
  const navLinks = $("#navLinks");
  burger?.addEventListener("click", () => {
    const open = navLinks.classList.toggle("is-open");
    burger.setAttribute("aria-expanded", String(open));
  });
  navLinks?.addEventListener("click", (e) => {
    if (e.target.tagName === "A") { navLinks.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); }
  });

  /* ===================================================================
     Lobster cursor trail 🦞 — the signature touch
     A little lobster swims just behind the pointer, dragging a tail of
     lobster-red bubbles that whips around as you move. Native cursor is
     kept (so links/clicks behave); this is a pointer-events-none overlay.
     Desktop fine-pointer only; skipped under reduced-motion.
     =================================================================== */
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (finePointer && !reduceMotion) {
    const N = 15;
    const layer = document.createElement("div");
    layer.className = "lobtrail";
    layer.setAttribute("aria-hidden", "true");

    const TRAIL = ["#FF4D1C", "#C8FF2D", "#2B47F0"];   // lobster red · lime · electric blue
    const dots = [];
    for (let i = 0; i < N; i++) {
      const t = i / (N - 1);
      const d = document.createElement("span");
      d.className = i % 2 ? "lobtrail__star" : "lobtrail__dot";   // alternate bubble / sparkle
      const size = (i % 2 ? 13 : 11) - t * (i % 2 ? 9 : 8);
      d.style.width = d.style.height = `${size}px`;
      d.style.background = TRAIL[i % 3];
      d.style.opacity = (0.85 * (1 - t)).toFixed(2);
      layer.appendChild(d);
      dots.push(d);
    }
    const head = document.createElement("div");
    head.className = "lobtrail__head";
    head.textContent = "🦞";
    layer.appendChild(head);
    document.body.appendChild(layer);

    // chain: pts[0] chases the cursor; each following point chases the prior
    const pts = Array.from({ length: N }, () => ({ x: innerWidth / 2, y: innerHeight / 2 }));
    const mouse = { x: innerWidth / 2, y: innerHeight / 2 };
    let active = false, raf = 0, pinchAt = -1e9;
    const PINCH_MS = 320;

    const loop = () => {
      pts[0].x += (mouse.x - pts[0].x) * 0.34;
      pts[0].y += (mouse.y - pts[0].y) * 0.34;
      for (let i = 1; i < N; i++) {
        pts[i].x += (pts[i - 1].x - pts[i].x) * 0.42;
        pts[i].y += (pts[i - 1].y - pts[i].y) * 0.42;
      }
      for (let i = 0; i < N; i++) {
        dots[i].style.transform = `translate(${pts[i].x}px, ${pts[i].y}px) translate(-50%, -50%)`;
      }
      // lobster rides a few segments back and banks toward its heading
      const hp = pts[3], ref = pts[7];
      const vx = hp.x - ref.x, vy = hp.y - ref.y;
      const facing = vx >= 0 ? -1 : 1;          // 🦞 faces left by default; flip to face travel
      const tilt = Math.max(-0.4, Math.min(0.4, vy * 0.012));
      // click "pinch": a quick claw snap — pop up, sideways squish (open→close), wiggle
      const pe = (performance.now() - pinchAt) / PINCH_MS;
      let scale = 1, squish = 1, snap = 0;
      if (pe >= 0 && pe < 1) {
        scale  = 1 + Math.sin(pe * Math.PI) * 0.45;
        squish = 1 + Math.sin(pe * Math.PI * 2) * 0.28;
        snap   = Math.sin(pe * Math.PI * 2) * 0.22;
      }
      const wob = Math.sin(performance.now() / 130) * 0.13;   // constant swim wiggle
      head.style.transform =
        `translate(${hp.x}px, ${hp.y}px) translate(-50%, -50%) rotate(${tilt + snap + wob}rad) scale(${scale}) scaleX(${facing * squish})`;
      raf = requestAnimationFrame(loop);
    };

    const start = () => {
      if (!active) { active = true; pts.forEach((p) => { p.x = mouse.x; p.y = mouse.y; }); }
      layer.classList.add("is-on");
      cancelAnimationFrame(raf); loop();
    };

    const onMove = (e) => { mouse.x = e.clientX; mouse.y = e.clientY; if (!active) start(); };

    // a little bubble burst when the claw snaps
    const burst = (x, y) => {
      for (let k = 0; k < 7; k++) {
        const s = document.createElement("span");
        s.className = "lobtrail__pop" + ["", " lobtrail__pop--lime", " lobtrail__pop--blue"][k % 3];
        s.style.transform = `translate(${x}px, ${y}px)`;
        layer.appendChild(s);
        const ang = (Math.PI * 2 * k) / 7 + Math.random() * 0.6;
        const dist = 20 + Math.random() * 18;
        requestAnimationFrame(() => {
          s.style.transform = `translate(${x + Math.cos(ang) * dist}px, ${y + Math.sin(ang) * dist}px) scale(.4)`;
          s.style.opacity = "0";
        });
        setTimeout(() => s.remove(), 480);
      }
    };

    const onDown = (e) => {
      mouse.x = e.clientX; mouse.y = e.clientY;
      if (!active) start();
      pinchAt = performance.now();
      burst(e.clientX, e.clientY);
    };

    window.addEventListener("pointermove", onMove, { passive: true });
    window.addEventListener("pointerdown", onDown, { passive: true });
    document.addEventListener("mouseleave", () => layer.classList.remove("is-on"));
    document.addEventListener("mouseenter", () => active && layer.classList.add("is-on"));
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) cancelAnimationFrame(raf);
      else if (active) { cancelAnimationFrame(raf); loop(); }
    });
  }

  /* ===================================================================
     Easter eggs 🦞
     · 5 rapid clicks            → a parade of lobsters swims across screen
     · type "lobster" / "cjy"    → same parade
     · Konami ↑↑↓↓←→←→ B A        → lobster rain + brand confetti
     · open the console          → a hidden hello
     =================================================================== */
  (() => {
    const eggLayer = document.createElement("div");
    eggLayer.className = "egg-layer";
    eggLayer.setAttribute("aria-hidden", "true");
    document.body.appendChild(eggLayer);

    const rand = (a, b) => a + Math.random() * (b - a);
    const PALETTE = ["#FF4D1C", "#2B47F0", "#C8FF2D", "#FF5DA2", "#14110B"];

    let toastTimer;
    const toast = (msg, hold = 2600) => {
      let el = eggLayer.querySelector(".egg-toast");
      if (!el) { el = document.createElement("div"); el.className = "egg-toast"; eggLayer.appendChild(el); }
      el.textContent = msg; el.classList.add("is-show");
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => el.classList.remove("is-show"), hold);
    };

    // lobster parade — swim across horizontally with a gentle bob
    let paradeBusy = false;
    const parade = () => {
      if (paradeBusy) return; paradeBusy = true;
      toast("🦞 一大群小龙虾游过！");
      const N = reduceMotion ? 6 : 16;
      for (let i = 0; i < N; i++) {
        const lob = document.createElement("span");
        lob.className = "egg-lob"; lob.textContent = "🦞";
        lob.style.fontSize = `${rand(22, 48) | 0}px`;
        lob.style.top = `${rand(5, 90).toFixed(1)}vh`;
        eggLayer.appendChild(lob);
        const bob = rand(10, 26);
        const anim = lob.animate([
          { transform: "translateX(-20vw) translateY(0px) rotate(-8deg) scaleX(-1)", opacity: 0 },
          { opacity: 1, offset: 0.06 },
          { transform: `translateX(16vw) translateY(${-bob}px) rotate(7deg) scaleX(-1)`, offset: 0.25 },
          { transform: `translateX(50vw) translateY(${(bob * 0.5).toFixed(0)}px) rotate(-6deg) scaleX(-1)`, offset: 0.5 },
          { transform: `translateX(84vw) translateY(${-bob}px) rotate(7deg) scaleX(-1)`, offset: 0.75 },
          { opacity: 1, offset: 0.94 },
          { transform: "translateX(122vw) translateY(0px) rotate(-8deg) scaleX(-1)", opacity: 0 },
        ], { duration: reduceMotion ? 1000 : rand(2400, 4200), delay: reduceMotion ? i * 40 : rand(0, 800), easing: "linear", fill: "forwards" });
        anim.onfinish = () => lob.remove();
      }
      setTimeout(() => { paradeBusy = false; }, 7000);
    };

    // lobster rain + confetti — the "ultimate": more, bigger, and longer
    const rain = () => {
      const N = reduceMotion ? 16 : 110;
      const maxDelay = reduceMotion ? 400 : 5200;   // spread the downpour out over time
      toast("🦞 KONAMI! 龙虾雨 · 大招！🎉", reduceMotion ? 2600 : 8500);
      for (let i = 0; i < N; i++) {
        const isLob = Math.random() < 0.6;
        const p = document.createElement("span");
        if (isLob) { p.className = "egg-lob"; p.textContent = "🦞"; p.style.fontSize = `${rand(18, 56) | 0}px`; }
        else { p.className = "egg-confetti"; p.style.background = PALETTE[(Math.random() * PALETTE.length) | 0]; }
        p.style.left = `${rand(0, 100).toFixed(1)}vw`;
        eggLayer.appendChild(p);
        const anim = p.animate([
          { transform: "translateY(-14vh) translateX(0) rotate(0deg)", opacity: 1 },
          { transform: `translateY(114vh) translateX(${rand(-14, 14).toFixed(1)}vw) rotate(${rand(-900, 900) | 0}deg)`, opacity: 1 },
        ], { duration: reduceMotion ? 1300 : rand(2600, 5200), delay: reduceMotion ? (i / N) * maxDelay : rand(0, maxDelay), easing: "cubic-bezier(.35,.1,.5,1)", fill: "forwards" });
        anim.onfinish = () => p.remove();
      }
    };

    // celebration poppers — launch UP, then bounce on the "floor" with
    // damped (ever-lower) hops, finally resting at the bottom for a beat
    const burstFrom = (originVw) => {
      const N = reduceMotion ? 6 : (window.innerWidth < 640 ? 7 : 11);
      const UP = "cubic-bezier(.3,.72,.4,1)";    // decelerate (rising)
      const DN = "cubic-bezier(.55,0,.78,.46)";  // accelerate (falling)
      for (let i = 0; i < N; i++) {
        const isLob = Math.random() < 0.66;
        const p = document.createElement("span");
        if (isLob) { p.className = "egg-lob"; p.textContent = "🦞"; p.style.fontSize = `${rand(20, 48) | 0}px`; }
        else { p.className = "egg-confetti"; p.style.background = PALETTE[(Math.random() * PALETTE.length) | 0]; }
        p.style.left = `${originVw}vw`; p.style.top = "100vh";
        eggLayer.appendChild(p);

        const dx = rand(-24, 24), g = +(rand(2, 7)).toFixed(1), tilt = rand(-22, 22) | 0;
        const spin = (rand(220, 520) | 0) * (Math.random() < 0.5 ? -1 : 1);
        const sw = rand(0.3, 0.6), sr = rand(2, 5) | 0, ph = Math.random() < 0.5 ? 1 : -1;

        if (reduceMotion) {
          const a = p.animate([
            { transform: "translate(0,0)", opacity: 0 },
            { transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, opacity: 1, offset: 0.3 },
            { transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, opacity: 1, offset: 0.85 },
            { transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, opacity: 0 },
          ], { duration: 3000, fill: "forwards" });
          a.onfinish = () => p.remove();
          continue;
        }

        const L = rand(48, 80), b1 = g + L * 0.26, b2 = g + L * 0.11, b3 = g + L * 0.045;  // hops get lower
        const a = p.animate([
          { offset: 0,    transform: "translate(0vw, 0vh) rotate(0deg)", opacity: 0, easing: UP },
          { offset: 0.02, transform: `translate(${(dx * .2) | 0}vw, -${(L * .26) | 0}vh) rotate(${(spin * .12) | 0}deg)`, opacity: 1, easing: UP },
          { offset: 0.12, transform: `translate(${(dx * .5) | 0}vw, -${L | 0}vh) rotate(${(spin * .42) | 0}deg)`, easing: DN },   // launch peak
          { offset: 0.23, transform: `translate(${(dx * .72) | 0}vw, -${g}vh) rotate(${(spin * .6) | 0}deg)`, easing: UP },        // floor
          { offset: 0.30, transform: `translate(${(dx * .82) | 0}vw, -${b1 | 0}vh) rotate(${(spin * .72) | 0}deg)`, easing: DN },  // hop 1
          { offset: 0.37, transform: `translate(${(dx * .9) | 0}vw, -${g}vh) rotate(${(spin * .82) | 0}deg)`, easing: UP },        // floor
          { offset: 0.42, transform: `translate(${(dx * .95) | 0}vw, -${b2 | 0}vh) rotate(${(spin * .9) | 0}deg)`, easing: DN },   // hop 2
          { offset: 0.46, transform: `translate(${dx | 0}vw, -${g}vh) rotate(${(spin * .96) | 0}deg)`, easing: UP },               // floor
          { offset: 0.49, transform: `translate(${dx | 0}vw, -${b3 | 0}vh) rotate(${tilt}deg)`, easing: DN },                      // hop 3 (settling)
          { offset: 0.52, transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, easing: "ease-in-out" },               // settle on floor
          { offset: 0.60, transform: `translate(${+(dx + sw * ph).toFixed(2)}vw, -${g}vh) rotate(${tilt + sr * ph}deg)`, easing: "ease-in-out" },   // sway
          { offset: 0.68, transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, easing: "ease-in-out" },               // center
          { offset: 0.76, transform: `translate(${+(dx - sw * ph).toFixed(2)}vw, -${g}vh) rotate(${tilt - sr * ph}deg)`, easing: "ease-in-out" },   // sway other way
          { offset: 0.84, transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, easing: "ease-in-out" },               // center
          { offset: 0.92, transform: `translate(${+(dx + sw * ph * 0.4).toFixed(2)}vw, -${g}vh) rotate(${tilt + ((sr * ph * 0.4) | 0)}deg)`, opacity: 1, easing: "linear" }, // mid-sway fade
          { offset: 1,    transform: `translate(${dx | 0}vw, -${g}vh) rotate(${tilt}deg)`, opacity: 0 },                           // fade
        ], { duration: rand(8500, 11000) | 0, delay: rand(0, 350) | 0, fill: "forwards" });
        a.onfinish = () => p.remove();
      }
    };

    // surprise: fully scrolled to the bottom → "thanks for reading it all"
    let celebrated = false;
    const celebrate = () => {
      if (celebrated) return; celebrated = true;
      toast("🦞 恭喜你看完整了！谢谢你读到这里 ❤️", 9500);
      const small = window.innerWidth < 640;
      const waves = reduceMotion ? [[50, 0]]
        : small ? [[18, 0], [82, 650], [50, 1500], [40, 2400]]
                : [[12, 0], [88, 500], [50, 1100], [30, 1900], [70, 2600], [50, 3300]];
      waves.forEach(([vw, t]) => setTimeout(() => burstFrom(vw), t));
    };
    const atBottom = () => (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 4);
    const watchBottom = () => { if (atBottom()) { celebrate(); window.removeEventListener("scroll", watchBottom); } };
    window.addEventListener("scroll", watchBottom, { passive: true });

    // 🍤 feeding — drop food into the tank, lobsters scuttle over and gobble it up
    let feedBusy = false;
    const feed = () => {
      if (feedBusy) return; feedBusy = true;
      const small = window.innerWidth < 640;
      const W = window.innerWidth, H = window.innerHeight;
      const ground = H - (small ? 54 : 66);                 // floor line — lobsters sit clear of the edge
      toast("🍤 投喂时间！小龙虾们冲过来啦～");

      if (!HAS_WAAPI) { setTimeout(() => { feedBusy = false; }, 1500); return; }  // old browsers: toast only

      if (reduceMotion) {                                   // calm version: pellets fade, no chase
        for (let i = 0; i < 5; i++) {
          const fd = document.createElement("span"); fd.className = "egg-food";
          fd.style.transform = `translate(${(rand(0.2, 0.8) * W) | 0}px, ${(rand(0.25, 0.6) * H) | 0}px)`;
          eggLayer.appendChild(fd);
          fd.animate([{ opacity: 0 }, { opacity: 1, offset: .2 }, { opacity: 1, offset: .8 }, { opacity: 0 }],
            { duration: 2600, fill: "forwards" }).onfinish = () => fd.remove();
        }
        setTimeout(() => { feedBusy = false; }, 2800);
        return;
      }

      // food pellets sinking from the top with a little wobble
      const foods = [];
      const nFood = small ? 6 : 9;
      for (let i = 0; i < nFood; i++) {
        const el = document.createElement("span"); el.className = "egg-food";
        el.style.background = ["#FF4D1C", "#FF5DA2", "#C8FF2D"][i % 3];
        eggLayer.appendChild(el);
        foods.push({ el, x: rand(0.12, 0.88) * W, y: rand(-60, -10), vy: 120 + Math.random() * 70,
          swA: 8 + Math.random() * 14, swW: 1 + Math.random() * 1.4, ph: Math.random() * 6.28, eaten: false });
      }
      // hungry lobsters waiting on the floor — spread evenly and kept fully on-screen
      const lobs = [];
      const nLob = small ? 2 : 3;
      const pad = 12;                                        // keep clear of the screen edges
      for (let i = 0; i < nLob; i++) {
        const el = document.createElement("span"); el.className = "egg-feedlob"; el.textContent = "🦞";
        el.style.fontSize = `${((small ? 30 : 36) + Math.random() * 12) | 0}px`;
        eggLayer.appendChild(el);
        const w = el.offsetWidth || 40;                      // real emoji width, for even spacing + clamping
        const usable = Math.max(1, W - 2 * pad - w);
        const x = pad + (nLob === 1 ? usable / 2 : (i / (nLob - 1)) * usable) + rand(-8, 8);
        lobs.push({ el, w, x, y: ground, speed: 230 + Math.random() * 90, chomp: 0 });
      }

      let last = performance.now(), t0 = last, raf = 0, ended = false;
      const finish = () => {
        if (ended) return; ended = true; cancelAnimationFrame(raf);
        lobs.forEach((l, i) => {                           // satisfied → scuttle off the nearest side
          const dir = l.x < W / 2 ? -1 : 1;
          l.el.animate([
            { transform: l.el.style.transform, opacity: 1 },
            { transform: `translate(${(l.x + dir * W * 0.34) | 0}px, ${l.y | 0}px) scaleX(${dir < 0 ? 1 : -1})`, opacity: 0 },
          ], { duration: 1100, delay: i * 90, easing: "ease-in", fill: "forwards" }).onfinish = () => l.el.remove();
        });
        foods.forEach((f) => { if (!f.eaten) f.el.remove(); });
        toast("🦞 喂饱啦！谢谢投喂 ❤️", 3200);
        setTimeout(() => { feedBusy = false; }, 1500);
      };

      const tick = (now) => {
        const dt = Math.min(0.05, (now - last) / 1000); last = now; const t = (now - t0) / 1000;
        for (const f of foods) {                           // sink + settle on the floor
          if (f.eaten) continue;
          f.y = Math.min(ground + 6, f.y + f.vy * dt);
          const drawX = f.x + Math.sin(t * f.swW + f.ph) * f.swA;
          f.el.style.transform = `translate(${drawX.toFixed(1)}px, ${f.y.toFixed(1)}px)`;
        }
        for (const l of lobs) {                            // chase nearest uneaten pellet (by center)
          const lc = l.x + l.w / 2;
          let target = null, td = 1e9;
          for (const f of foods) { if (f.eaten) continue; const d = Math.abs((f.x + 6) - lc); if (d < td) { td = d; target = f; } }
          let dir = 0;
          if (target) {
            const fc = target.x + 6;                        // food centre
            dir = Math.sign(fc - lc);
            if (Math.abs(fc - lc) > 6) l.x += dir * l.speed * dt;
            const ty = target.y > ground - 230 ? Math.max(target.y - 16, ground - 150) : ground;
            l.y += (ty - l.y) * Math.min(1, dt * 6);
            if (Math.abs(fc - (l.x + l.w / 2)) < 24 && Math.abs(target.y - l.y) < 38) {
              target.eaten = true; l.chomp = 1; const fx = target.x, fy = target.y; target.el.remove(); disturb(fx, fy);
            }
          } else { l.y += (ground - l.y) * Math.min(1, dt * 6); }
          l.x = Math.max(pad, Math.min(W - l.w - pad, l.x));  // never scuttle off the screen
          l.chomp = Math.max(0, l.chomp - dt * 3);
          const face = dir < 0 ? 1 : -1;                   // 🦞 faces left by default
          const bob = Math.sin(t * 12 + l.x * 0.05) * (dir !== 0 ? 3 : 1);
          l.el.style.transform = `translate(${l.x.toFixed(1)}px, ${(l.y + bob).toFixed(1)}px) scale(${(1 + l.chomp * 0.25).toFixed(2)}) scaleX(${face})`;
        }
        if (foods.every((f) => f.eaten) || t > (small ? 9 : 11)) { finish(); return; }
        raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
    };

    // trigger: 5 rapid clicks
    let clicks = 0, clickTimer;
    window.addEventListener("pointerdown", () => {
      clicks++;
      clearTimeout(clickTimer);
      clickTimer = setTimeout(() => { clicks = 0; }, 1200);
      if (clicks >= 5) { clicks = 0; parade(); }
    }, { passive: true });

    // trigger: Konami code + secret words
    const KON = ["arrowup","arrowup","arrowdown","arrowdown","arrowleft","arrowright","arrowleft","arrowright","b","a"];
    let kIdx = 0, typed = "";
    window.addEventListener("keydown", (e) => {
      const k = (e.key || "").toLowerCase();
      kIdx = (k === KON[kIdx]) ? kIdx + 1 : (k === KON[0] ? 1 : 0);
      if (kIdx === KON.length) { kIdx = 0; rain(); }
      if (k.length === 1) {
        typed = (typed + k).slice(-8);
        if (/lobster$|cjy$/.test(typed)) { typed = ""; parade(); }
        else if (/feed$/.test(typed)) { typed = ""; feed(); }
      }
    });

    // trigger: shake the phone (iOS asks permission on first tap)
    if (window.matchMedia("(pointer: coarse)").matches && typeof DeviceMotionEvent !== "undefined") {
      const listen = () => {
        let last = null, hits = 0, hitAt = 0, lastT = 0;
        window.addEventListener("devicemotion", (e) => {
          const a = e.accelerationIncludingGravity || e.acceleration; if (!a) return;
          const now = Date.now(); if (now - lastT < 90) return; lastT = now;
          const cur = { x: a.x || 0, y: a.y || 0, z: a.z || 0 };
          if (last) {
            const d = Math.abs(cur.x - last.x) + Math.abs(cur.y - last.y) + Math.abs(cur.z - last.z);
            if (d > 30) { hits = (now - hitAt < 800) ? hits + 1 : 1; hitAt = now; if (hits >= 3) { hits = 0; parade(); } }
          }
          last = cur;
        });
      };
      if (typeof DeviceMotionEvent.requestPermission === "function") {
        window.addEventListener("pointerup", function ask() {
          DeviceMotionEvent.requestPermission().then((s) => { if (s === "granted") listen(); }).catch(() => {});
        }, { once: true });
      } else { listen(); }
    }

    // subtle footer hint → device-aware popover + a guaranteed "try it" button
    const hintWrap = document.getElementById("eggHint");
    if (hintWrap) {
      const btn = hintWrap.querySelector(".egg-hint__btn");
      const coarse = window.matchMedia("(pointer: coarse)").matches;
      const lines = ["任意处连续点 5 下"];
      if (coarse) { lines.push("摇一摇你的手机 📱"); lines.push("点下面的 🍤 投喂小龙虾"); }
      else { lines.push("输入 lobster 或 cjy"); lines.push("输入 feed 投喂小龙虾 🍤"); lines.push("Konami：↑↑↓↓←→←→ B A"); }
      const pop = document.createElement("div");
      pop.className = "egg-hint__pop";
      pop.innerHTML = `<h4>🦞 藏了几只小龙虾彩蛋</h4><ul>${lines.map((l) => `<li>· ${l}</li>`).join("")}</ul>` +
        `<button class="egg-hint__try" type="button">放一群虾出来 🦞</button>` +
        `<button class="egg-hint__try egg-hint__try--feed" type="button">投喂小龙虾 🍤</button>`;
      hintWrap.appendChild(pop);
      const setOpen = (o) => { pop.classList.toggle("is-open", o); btn.setAttribute("aria-expanded", String(o)); };
      btn.addEventListener("click", (e) => { e.stopPropagation(); setOpen(!pop.classList.contains("is-open")); });
      pop.querySelector(".egg-hint__try").addEventListener("click", (e) => { e.stopPropagation(); parade(); });
      pop.querySelector(".egg-hint__try--feed").addEventListener("click", (e) => { e.stopPropagation(); feed(); });
      document.addEventListener("click", () => setOpen(false));
      document.addEventListener("keydown", (e) => { if (e.key === "Escape") setOpen(false); });
    }

    // feed the tank: the wiggling hero "bait" (the obvious one) + poking the big lobster
    const bigLob = document.querySelector(".hero__biglob");
    if (bigLob) { bigLob.title = "戳我喂虾 🍤"; bigLob.addEventListener("click", () => feed()); }
    const bait = document.querySelector(".hero__bait");
    if (bait) bait.addEventListener("click", () => feed());

    // console hello
    try {
      console.log("%c🦞 CJY · 陈俊烨 — Vibe Coder",
        "font:700 20px 'Space Grotesk',sans-serif;color:#FF4D1C;text-shadow:1px 1px 0 #14110B");
      console.log("%c你发现了控制台 :) 连点 5 下、输入 lobster，或试试 Konami 秘籍 ↑↑↓↓←→←→ B A 🦞",
        "font:13px monospace;color:#2B47F0");
    } catch (_) {}
  })();
})();
