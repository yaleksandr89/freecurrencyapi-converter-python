# 安装与首次运行

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](getting-started.md) | [English](getting-started_en.md) | [Español](getting-started_es.md) | **当前语言** | [Français](getting-started_fr.md) | [Deutsch](getting-started_de.md) |

## 准备工作

- 用于克隆仓库的 Git、Python 3.12 或更高版本，以及带有 `pip` 的 `venv` 模块。
- 转换货币需要您自己的 FreecurrencyAPI 密钥。注册后可从账户中获取密钥；API 详情见 [FreecurrencyAPI 文档](https://freecurrencyapi.com/docs/)。

## 获取源代码

克隆仓库并进入包含 `index.py` 的根目录。以下命令均在该目录执行。

```bash
# 克隆仓库并进入项目目录。
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

## 安装依赖

### Linux 与 macOS

确认 `python3` 对应 Python 3.12 或更高版本，并已安装 `make`。`make setup` 会在 `.venv` 不存在时创建它，并安装项目和开发依赖。

```bash
# 检查 Python 版本。
python3 --version

# 创建 .venv 并安装开发依赖。
make setup

# 创建本地配置，不覆盖已有的密钥。
cp -n .env.example .env
```

如果合适的解释器使用其他命令名，可设置 `PYTHON`，例如 `make setup PYTHON=python3.12`。该变量只在创建环境时生效。

### Windows PowerShell

此处的 `python` 指已添加到 `PATH` 的 Python 3.12 或更高版本。命令直接调用 `.venv` 中的解释器，无需激活环境或安装 `make`。

```powershell
# 检查已安装的 Python 版本。
python --version

# 创建虚拟环境并安装开发依赖。
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# 仅在 .env 不存在时复制配置模板。
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

如果只安装程序及运行依赖，请把 `pip install` 命令中的 `requirements-dev.txt` 换成 `requirements.txt`。运行本地检查需要开发依赖。

## 配置密钥与 API 地址

用编辑器打开 `.env`。将 `API_TOKEN` 替换为您的密钥；`API_URL` 保留 API 基础地址，不要加具体端点路径。

```ini
API_TOKEN=your_api_token_here
API_URL=https://api.freecurrencyapi.com/v1
```

请仅在本地保存密钥，不要把 `.env` 提交到 Git 或附在问题报告中。进程环境中已设置的变量优先于 `.env` 的值。

## 启动与验证

在 Linux 和 macOS 上使用 `make` 启动：

```bash
# 俄语界面（默认）。
make run

# 英语界面。
make run CLI_LANG=en
```

在 Windows PowerShell 中，使用虚拟环境中的 Python 运行 `index.py`：

```powershell
# 俄语界面（默认）。
.\.venv\Scripts\python.exe index.py

# 英语界面。
.\.venv\Scripts\python.exe index.py --lang en
```

程序显示欢迎信息后会列出货币。如果列表包含 `USD`、`EUR` 和 `GBP`，依次输入 `USD`、`12.5`、`EUR,GBP`，每次按 Enter。成功后会为每种目标货币输出一行结果；数值取决于实际汇率。

如需验证 CLI 能在没有 API 密钥和请求的情况下启动，可查看帮助：Linux/macOS 执行 `.venv/bin/python index.py --help`，PowerShell 执行 `.\.venv\Scripts\python.exe index.py --help`。

## 启动失败时

| 现象 | 检查内容 |
| --- | --- |
| 缺少 `API_TOKEN` 或 `API_URL` | 检查 `.env` 文件名、变量名以及是否填写了非空值，同时检查 shell 中已有的环境变量。 |
| 显示 HTTP 状态错误 | 检查基础地址、密钥有效性和 FreecurrencyAPI 的剩余请求额度。 |
| 请求超时或失败 | 检查 `API_URL` 以及 FreecurrencyAPI 是否可用。 |
| CLI 拒绝输入 | 重新启动，选择列表中存在的货币代码，使用逗号分隔目标货币，并用小数点输入正数金额。 |

详细错误类型和退出码见 [CLI 与错误参考](../reference/cli-and-errors_zh.md)。

## 本地检查

安装开发依赖后，从仓库根目录运行检查。

Linux 与 macOS：

```bash
# 运行测试、Ruff 及依赖检查。
make check
```

Windows PowerShell：

```powershell
# 离线测试。
.\.venv\Scripts\python.exe -m pytest

# 代码风格和格式检查。
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .

# 检查已安装依赖。
.\.venv\Scripts\python.exe -m pip check
```

测试会模拟 FreecurrencyAPI 的响应及失败情况，并阻止真实 HTTP 请求，因此不需要有效密钥。服务可用性和密钥有效性只能通过实际的交互式转换验证。
