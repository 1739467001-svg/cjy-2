# 作品预览图 / Project shots

把每个作品的截图放进**这个文件夹**，用下表的**固定文件名**，卡片就会自动用真图替换占位图。

- 推荐尺寸：**1280 × 800**（16:10），`.png` 或 `.jpg`
- 卡片以 `object-fit: cover` 铺满预览框，建议截**横版主界面**
- 放好后，把 `public/main.js` 里对应项目的 `shot: null` 改成 `shot: "shots/<文件名>"`
  （或交给我来接线）。路径错误 / 文件缺失会**自动回退**到占位图，不会破图。

| # | 作品 | 文件名 | 线上 |
|---|---|---|---|
| 01 | 研究生院督导管理系统 | `supervision.png` | 121.196.217.243/login |
| 02 | 会议室预约虾 | `meetshrimp.png` | meetroomshrimp-gvfhrxz8.manus.space |
| 03 | 会议室预约虾 · 3D 数字孪生 | `zjgsu.png` | zjgsu.vercel.app |
| 04 | CARGO CLAW · 智慧港口 | `cargo-claw.png` | cargo-claw.vercel.app |
| 05 | 天府TWIN · 成都天府机场 | `aerotwin.png` | aerotwin-tfu.vercel.app |
| 06 | 海上油田视觉模拟 | `deepblue-rig.png` | deepblue-rig.vercel.app |
| 07 | 虚拟看房 · 样板间漫游 | `virtual-house.png` | virtual-reality-mocha.vercel.app |
| 08 | 太阳系模拟与漫游 | `solar.png` | virtual-universe-eight.vercel.app |
| 09 | 首届 AI 黑客松作品展 | `hackathon.png` | 43.133.22.250:8089 |
