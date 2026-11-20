# CLI 命令、输入与错误

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](cli-and-errors.md) | [English](cli-and-errors_en.md) | [Español](cli-and-errors_es.md) | **当前语言** | [Français](cli-and-errors_fr.md) | [Deutsch](cli-and-errors_de.md) |

## 启动参数

在项目根目录使用安装时创建的 `.venv` 中的 Python 运行 `index.py`。以下示例适用于 Linux 和 macOS：

```bash
# 使用俄语界面进行交互式转换。
.venv/bin/python index.py

# 使用英语界面。
.venv/bin/python index.py --lang en

# 显示帮助，不读取 .env，也不请求 API。
.venv/bin/python index.py --help
```

Windows PowerShell 请将 `.venv/bin/python` 替换为 `.\.venv\Scripts\python.exe`。安装步骤见[入门指南](../guides/getting-started_zh.md)。

| 参数 | 行为 |
| --- | --- |
| `-h`, `--help` | 以所选语言显示帮助，不读取 `.env` 或调用 API。 |
| `--lang ru` | 使用俄语界面，为默认值。 |
| `--lang en` | 使用英语界面，可与 `--help` 一起使用。 |

## 输入与结果格式

CLI 首先获取并显示货币列表。代码放在方括号内；名称来自 FreecurrencyAPI。

1. 从列表中输入源货币代码，例如 `USD`。
2. 输入有限的正数，使用小数点，例如 `2.5`。`2,5`、`NaN`、`inf` 会被拒绝。
3. 输入一个或多个目标货币代码，例如 `EUR,GBP`。空项（包括末尾多余的逗号）属于错误输入。

货币代码不区分大小写，且会去除两端空格。输入错误时当前运行结束，需要重新启动命令。

金额转换为 `float`，再通过 `round` 保留三位小数后乘以汇率。如果舍入后为零或乘积不是有限数值，程序会报错。

结果写入标准输出，每种目标货币一行，顺序与 API 返回的顺序一致。源金额不强制固定小数位数，换算金额保留两位小数。下例使用测试中模拟的汇率，而非实时汇率。

```text
2.5 USD = 2.00 EUR
2.5 USD = 1.25 GBP
```

## FreecurrencyAPI 请求

两个请求均使用 `GET`，从 `API_URL` 获取基础地址，并通过查询参数 `apikey` 传递 `API_TOKEN`。

| 端点 | CLI 的使用方式 |
| --- | --- |
| [`/currencies`](https://freecurrencyapi.com/docs/currencies) | 在第一次输入提示前获取货币列表，并检查每个货币代码是否有非空名称。 |
| [`/latest`](https://freecurrencyapi.com/docs/latest) | 在输入合法后获取汇率。源货币通过 `base_currency` 传入，目标货币以逗号分隔并通过 `currencies` 传入。金额乘法在本地完成。 |

客户端仅接受 HTTP 200 且 JSON 中包含非空 `data` 对象的响应。连接超时为 4 秒，读取响应超时为 10 秒；不允许 HTTP 重定向。每种目标货币都必须有汇率，程序只使用请求的汇率。可用货币、汇率和请求额度由 FreecurrencyAPI 决定。

## 退出码

| 代码 | 含义 |
| --- | --- |
| `0` | 转换成功，或已显示帮助。 |
| `1` | 配置、请求、API 响应或输入错误，包括提前到达输入结尾（EOF）。 |
| `2` | 命令行参数错误，例如未知选项或不支持的 `--lang` 值。 |
| `130` | 用户使用 Ctrl+C 中断交互式运行。 |

## 错误信息

错误写入 `stderr`，语言由 `--lang` 决定。使用不支持的 `--lang` 时，会显示俄语错误。

| 类别 | 原因 |
| --- | --- |
| 配置 | `API_TOKEN` 或 `API_URL` 缺失，或仅包含空格。 |
| 网络请求 | 请求超时或其他请求错误，例如连接失败。 |
| HTTP | 服务器返回非 200 状态，CLI 会显示该状态码。 |
| API 响应 | JSON 错误；`data` 缺失、为空或格式不正确；货币信息无效；目标货币汇率缺失、非正数、非数字或非有限数。 |
| 输入 | 未知源/目标货币代码、空目标项、金额不合法、舍入为零或计算溢出。 |
| 会话结束 | 所有输入尚未完成时输入流就结束，或者用户按下 Ctrl+C。 |
