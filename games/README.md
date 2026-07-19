# 小游戏合集

基于 Vue 3 + Vite 的练习用 Web 小游戏集合,与仓库根目录的 Python 任务看板(`src/`)完全独立。

## 环境要求

- Node.js 18+(推荐 20 或更高)

## 本地启动

```bash
cd games
npm install
npm run dev
```

浏览器打开 Vite 提示的本地地址(默认 http://localhost:5173)。

## 可用脚本

| 命令 | 作用 |
|---|---|
| `npm run dev` | 启动开发服务器(热更新) |
| `npm run build` | 构建生产产物到 `dist/` |
| `npm run preview` | 本地预览构建产物 |
| `npm run test` | 运行 Vitest 单元测试(一次) |
| `npm run test:watch` | 监听模式运行测试 |

## 目录约定

每个游戏独立放在 `src/games/<name>/` 下,遵循同一结构:

- `engine.js` — 框架无关的纯函数游戏规则(可单元测试)
- `engine.test.js` — Vitest 测试
- `index.vue` — 渲染层(只负责绘制与事件转发)

新增游戏时:在 `src/games/` 下建子目录 → 在 `src/router.js` 加一条路由 → 在 `src/views/Home.vue` 加一张入口卡片。

## 已有游戏

- 贪吃蛇(`/snake`)— 方向键 / WASD 控制,吃食物长大,撞墙或掉头判负。
