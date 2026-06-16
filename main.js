/* =====================================================================
   CJY · 陈俊烨 — interactions
   ===================================================================== */
(() => {
  "use strict";
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- footer year ---------- */
  $("#year").textContent = new Date().getFullYear();

  /* ===================================================================
     Project data → cards
     =================================================================== */
  const projects = [
    { emoji: "🛡️", cat: "系统平台", title: "研究生院督导管理系统",
      desc: "浙江工商大学研究生院的教学督导全流程数字化管理平台。",
      url: "http://121.196.217.243/login" },
    { emoji: "🦞", cat: "AI Agent", title: "会议室预约虾",
      desc: "会议室预约智能体：自然语言下单，自动排期与冲突检测。",
      url: "https://meetroomshrimp-gvfhrxz8.manus.space" },
    { emoji: "🚢", cat: "数字孪生", title: "智慧港口数字孪生",
      desc: "港口装卸与物流的三维孪生可视化，实时映射运营态势。",
      url: "https://cargo-claw.vercel.app" },
    { emoji: "✈️", cat: "数字孪生", title: "成都天府国际机场孪生",
      desc: "天府国际机场的数字孪生模拟，空地协同的可视化沙盘。",
      url: "http://aerotwin-tfu.vercel.app/" },
    { emoji: "🛢️", cat: "数字孪生", title: "海上油田视觉模拟",
      desc: "海上油田钻井平台的数字孪生与视觉仿真演示。",
      url: "https://deepblue-rig.vercel.app/" },
    { emoji: "🏠", cat: "VR / 3D", title: "虚拟看房 · 样板间漫游",
      desc: "沉浸式样板间漫游，第一视角自由穿行的虚拟看房体验。",
      url: "https://virtual-reality-mocha.vercel.app/" },
    { emoji: "🪐", cat: "3D 可视化", title: "太阳系模拟与漫游",
      desc: "可交互的太阳系三维模拟，自由漫游每一颗行星。",
      url: "https://virtual-universe-eight.vercel.app/" },
    { emoji: "🎨", cat: "作品展台", title: "首届 AI 黑客松作品展",
      desc: "信电学院 · 人工智能学院首届 AI 黑客松大赛学生作品展示。",
      url: "http://43.133.22.250:8089/" },
  ];

  const fmtHost = (u) => { try { return new URL(u).host; } catch { return u; } };

  const grid = $("#projectsGrid");
  if (grid) {
    grid.innerHTML = projects.map((p) => `
      <a class="pcard reveal" data-reveal href="${p.url}" target="_blank" rel="noopener">
        <div class="pcard__top">
          <span class="pcard__emoji">${p.emoji}</span>
          <span class="pcard__cat">${p.cat}</span>
        </div>
        <h3>${p.title}</h3>
        <p>${p.desc}</p>
        <div class="pcard__foot">
          <span class="pcard__url">${fmtHost(p.url)}</span>
          <span class="pcard__arrow">↗</span>
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
  ["about", "lobster", "projects", "journey", "campus", "volunteer"].forEach((id) => {
    const s = document.getElementById(id); if (s) secObserver.observe(s);
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

    const dots = [];
    for (let i = 0; i < N; i++) {
      const t = i / (N - 1);
      const d = document.createElement("span");
      d.className = "lobtrail__dot";
      const size = 11 - t * 8;                 // 11px → 3px
      d.style.width = d.style.height = `${size}px`;
      d.style.opacity = (0.8 * (1 - t)).toFixed(2);
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
      head.style.transform =
        `translate(${hp.x}px, ${hp.y}px) translate(-50%, -50%) rotate(${tilt + snap}rad) scale(${scale}) scaleX(${facing * squish})`;
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
        s.className = "lobtrail__pop" + (k % 3 === 0 ? " lobtrail__pop--lime" : "");
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
})();
