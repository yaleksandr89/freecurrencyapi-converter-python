# 参与开发

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../../.github/CONTRIBUTING.md) | [English](../en/CONTRIBUTING.md) | [Español](../es/CONTRIBUTING.md) | **当前语言** | [Français](../fr/CONTRIBUTING.md) | [Deutsch](../de/CONTRIBUTING.md) |

## 开始之前

先确认是否已有相关讨论。如需提交[新问题](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues/new/choose)，请选择错误报告或功能建议表单。

- 错误报告应包含运行环境、命令、输入、复现步骤、预期输出和实际输出。
- 功能建议应说明要解决的问题及期望的 CLI 行为。
- 安全漏洞请按照[安全政策](SECURITY.md)私下报告。

## 分支与提交

从 `master` 创建单独分支，例如 `fix/invalid-amount` 或 `docs/setup-guide`。提交信息和 Pull Request 标题采用 Conventional Commits：类型前缀为英文，**描述必须为俄语**。

```text
docs: уточнить запуск конвертера
fix: отклонять недопустимые суммы
test: проверить обработку некорректных ответов API
```

## 本地检查

在安装了 Python 3.12 或更高版本的 Linux/macOS 上，从仓库根目录运行以下命令。`make setup` 会在需要时创建 `.venv` 并安装开发依赖。创建环境时可通过 `PYTHON` 指定解释器。

```bash
make setup PYTHON=python3
make check
```

`make check` 执行 pytest、Ruff 代码风格和格式检查，以及 `pip check`。测试会模拟 FreecurrencyAPI 响应，无需真实密钥。PowerShell 命令见[入门指南](guides/getting-started.md#本地检查)。

不要将 `.env`、真实 API 密钥或包含机密信息的日志提交到 Git。

## Pull Request

向 `master` 提交 Pull Request，说明修改原因、实际运行的检查以及对 CLI、FreecurrencyAPI 请求或密钥处理的影响。必要时同步修改测试和文档。

保持六种文档语言版本和两种界面语言同步。
