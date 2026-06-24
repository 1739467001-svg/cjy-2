# CJY · 陈俊烨 — 个人介绍网页 🦞

> **Vibe Coder** ｜ AI 教育系统数字化 · 未来课堂探索 · AI 多模态
> 浙江工商大学 · 信电人工智能学院 · 研究生

一个**新潮野兽派（Neo-Brutalism）**风格的个人介绍单页：米色纸张底 ×
浓墨黑边框 × 硬投影，搭配龙虾红 / 电光蓝 / 酸性青柠的强烈撞色，超大海报字体、
跑马灯字幕与贴纸徽章。整体风格大胆、鲜明、具引领性，并以「小龙虾 🦞」个人 IP
作为贯穿全站的视觉符号。

## 🦞 项目作品 / Works

站点展示的作品（AI 智能体 + 数字孪生）逐个介绍与命名，见 **[项目介绍.md](项目介绍.md)**：
研究生院督导系统、会议室预约虾（及其 3D 数字孪生）、CARGO CLAW 智慧港口、天府TWIN 机场仿真等。
预览图放在 `public/shots/`（见该目录 [README](public/shots/README.md)）。

## ✨ 特性

- **纯静态、零依赖**：原生 HTML + CSS + JavaScript，任何静态托管即可部署。
- **数据驱动**：项目作品与黑客松时间轴由 `main.js` 中的数组生成，新增一条
  只需改数据，无需动结构。
- **强动效**：跑马灯、滚动揭示（健壮的滚动驱动 + IntersectionObserver 双保险）、
  打字机角色轮播、数字滚动计数、硬投影悬停交互。
- **三端适配**：桌面 / 平板 / 手机自适应协同，含移动端汉堡菜单；超宽屏才显示 hero 手绘装饰，避免小屏拥挤。
- **无障碍友好**：语义化标签、「跳到主要内容」跳转链接、`:focus-visible` 键盘焦点高亮、`prefers-reduced-motion` 全面降级。
- **分享 / SEO / PWA**：Open Graph + Twitter 大图分享卡（`og.png`）、JSON-LD `Person` 结构化数据、可「添加到主屏」的 `site.webmanifest` 与龙虾图标。

## 🥚 彩蛋

藏了几个小龙虾彩蛋，试着触发看看：

- **连点 5 下**（页面任意处）→ 一大群小龙虾横游过屏 🦞
- **键盘输入 `lobster` 或 `cjy`** → 同样的龙虾游行
- **Konami 秘籍** `↑ ↑ ↓ ↓ ← → ← → B A` → 龙虾雨 + 撞色彩纸 🎉
- **手机摇一摇** → 同样召唤出一群小龙虾（iOS 首次会请求体感权限）
- **滚动到页面最底**（完整看完）→ 底部龙虾礼炮上喷 + 一句感谢 🎉（每次访问一次）
- **打开浏览器控制台** → 一句隐藏的彩色问候

页脚有一枚不显眼的 🥚 按钮，点开会按当前设备给出对应的触发方式，并带一个「放一群虾出来」直接试玩按钮。彩蛋逻辑见 `main.js` 末尾的「Easter eggs」段；在「减少动态」模式下会自动降级数量与时长。

## 📁 结构

可部署的站点全部收在 `public/`（即 nginx / Zeabur 的 web 根目录），仓库元信息与生成源留在根目录：

```
public/                    可部署的静态站点（web 根目录）
  index.html               页面结构、内容与 <head> 元信息（OG / Twitter / JSON-LD）
  styles.css               野兽派设计系统（配色 / 边框 / 投影 / 排版 / 响应式）
  main.js                  交互逻辑、项目与时间轴数据、彩蛋
  og.png                   1200×630 社交分享大图
  icon-192/512.png         PWA 图标（apple-touch-icon.png 为 iOS 主屏图标）
  site.webmanifest         PWA 清单
  robots.txt · sitemap.xml 收录用
  404.html                 野兽派「迷路小龙虾」404 页
Dockerfile                 nginx 静态服务镜像（Zeabur 自动识别并构建）
default.conf.template      nginx 配置（404 / gzip / 缓存 / MIME / 监听 $PORT）
tools/                     分享图与图标的生成源（og.html / _icon.html，浏览器截图导出）
DEPLOY.md                  Zeabur 部署说明
```

## 🚀 本地预览

```bash
# 静态预览（任选其一）
cd public && python3 -m http.server 8000     # 或：npx serve public

# 或用与线上完全一致的 nginx 镜像
docker build -t cjy-site . && docker run --rm -p 8080:8080 cjy-site
```

## ☁️ 部署（Zeabur）

已整理成适合 Zeabur 的标准架构：站点在 `public/`，根目录的 `Dockerfile`
用 nginx 托管（处理 404、gzip、缓存、正确 MIME，并监听 Zeabur 注入的 `$PORT`）。
导入仓库后 Zeabur 会**自动识别 `Dockerfile`** 并构建部署。

完整步骤（含「纯静态」备选方案）见 **[DEPLOY.md](DEPLOY.md)**。
当前线上：<https://cjy-self-production.zeabur.app>

## 🎨 改配色 / 内容

- 配色与边框、投影统一在 `public/styles.css` 顶部的 `:root` 变量里调。
- 项目作品改 `public/main.js` 的 `projects` 数组；黑客松改 `journey` 数组；
  角色轮播改 `roles` 数组。

---

© 陈俊烨 CJY · 用 AI 把想法养成产品 · Made with vibe. 🦞
