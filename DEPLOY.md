# 部署到 Zeabur 🦞

本项目是**纯静态站点**，已整理成适合 Zeabur 部署的标准架构：

- 可部署的站点全部在 `public/`
- 根目录的 `Dockerfile` + `default.conf.template` 用 **nginx** 提供服务：处理
  `404`、`gzip`、缓存、正确的 `MIME` 类型，并监听 Zeabur 注入的 `$PORT`

---

## 方式一：Dockerfile（推荐，控制力最强）

Zeabur 会自动识别根目录的 `Dockerfile` 并构建，无需任何额外配置。

1. 登录 [Zeabur](https://zeabur.com) → 新建 **Project** → **Add Service** → **Deploy from GitHub**
2. 选择本仓库与分支
3. Zeabur 检测到 `Dockerfile`，自动构建 nginx 镜像并部署
4. 在服务的 **Networking / Domains** 绑定域名（如现有的 `cjy-self-production.zeabur.app`）

> **端口**：容器监听 `$PORT`（Zeabur 注入；本地默认 `8080`），Zeabur 自动探测，无需手动设置。

### 本地预览（与线上完全一致）

```bash
docker build -t cjy-site .
docker run --rm -p 8080:8080 cjy-site
# 打开 http://localhost:8080
# 自定义端口： docker run --rm -e PORT=9000 -p 9000:9000 cjy-site
```

---

## 方式二：纯静态（更快，无需容器）

如果想用 Zeabur 的原生静态托管（秒级部署、无构建）：

1. 删除根目录的 `Dockerfile` 与 `default.conf.template`
2. 新建 `zbpack.json`：
   ```json
   { "output_dir": "public" }
   ```
3. 推送后，Zeabur 以静态站点形式直接托管 `public/`

> 注意：纯静态模式下，自定义 `404.html` 是否返回 404 状态取决于平台默认行为；
> **Dockerfile 方式**通过 `error_page 404 /404.html;` 可确保正确返回。

---

## 部署后自检清单

- [ ] 首页打开正常：开场龙虾闪屏 / 龙虾光标拖尾 / 各版块排版
- [ ] 把链接发到微信 / X，能看到 `og.png` 龙虾大图预览
- [ ] 手机「添加到主屏」，图标是红底龙虾
- [ ] 访问一个不存在的路径（如 `/abc`），看到「迷路小龙虾」404 页
- [ ] `https://你的域名/robots.txt` 与 `/sitemap.xml` 可访问

---

## 重新生成分享图 / 图标

源文件在 `tools/`（`og.html` / `_icon.html`）。用浏览器把它们截图导出，覆盖：

- `public/og.png`（1200×630）
- `public/icon-192.png` · `public/icon-512.png` · `public/apple-touch-icon.png`
