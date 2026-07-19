# Chrys Data Platform Demo

一个专门用于验证 Chrys 完整数据链路的公开 Demo 仓库：

```text
Chrys Session
  -> Git AI agent-v1 代码归因
  -> Chrys Data Uploader
  -> Chrys Data Server
  -> 管理与业务看板
```

项目本身是一个零第三方运行时依赖的 Python 任务看板，便于用 Chrys 持续完成小功能、运行测试并创建真实 Commit。

## 本地验证

```bash
python -m unittest discover -s tests -v
```

## 建议的 Chrys 实验任务

- 给任务增加优先级，并支持按优先级排序。
- 增加按标签筛选任务的能力。
- 增加任务删除与重新打开功能。
- 增加 JSON 导入和导出。
- 增加命令行入口，并补充测试。

每次实验建议只完成一个任务，检查测试后创建一个 Commit。这样可以清晰观察 Session、工具调用、Commit 和代码行归因之间的关系。

