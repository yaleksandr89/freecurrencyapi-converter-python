# 货币转换器

### 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
|---------|------------|------------|-----------|-------------|----------|
| [Русский](../../README.md) | [English](README_en.md) | [Español](README_es.md) | **已选** | [Français](README_fr.md) | [Deutsch](README_de.md) |

---

**货币转换器**是一个使用货币兑换API的项目。 您可以通过现成的测试请求汇率，执行转换和测试功能。

---

## 项目结构

```plain text
currency-converter/
├── docs/...              # 用于README.md
├── src/
│   ├── main.py           # 启动应用程序的主文件
│   ├── api_service.py    # 使用API（请求和处理）
├── tests/
│   ├── test.py           # 检查功能的测试
├── index.py              # 启动应用程序的入口点
├── .env                  # 配置文件（令牌和URL）。 它是独立创建的！
├── .env.example          # 配置文件示例
├── .gitignore            # 忽略Git文件
├── requirements.txt      # 依赖列表
├── README.md             # 项目文档
```

---

## 安装

### 1. 克隆存储库

将项目克隆到本地计算机:

```bash
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

### 2. 创建虚拟环境

建议使用虚拟环境隔离依赖关系:

```bash
#创建虚拟环境
python3 -m venv venv

# 虚拟环境激活
source venv/bin/activate  # 适用于 Bash/Zsh/Linux/macOS
venv\Scripts\activate     # 适用于 Windows
```

### 3. 安装依赖项

从 `requirements.txt` 安装依赖项:

```bash
pip install -r requirements.txt
```

---

## 配置

1. 将文件 `.env.example` 重命名为 `.env`:

```bash
mv .env.example .env
```

2. 在 `.env` 中指定令牌和基本API URL:

```plaintext
API_TOKEN='ВАШ_API_ТОКЕН'
API_URL='https://api.freecurrencyapi.com/v1'
```

---

## 启动

### 1. 启动应用程序

通过文件运行项目 `index.py`:

```bash
python3 index.py
```

---

## 测试

### 运行测试

要运行测试，请使用文件 `tests/test.py`:

```bash
python3 tests/test.py
```

此文件检查API连接的正确性并显示可用货币列表.

---

## 作品示范

成功转换

![currency-convert-result-work-success.png](/docs/img/currency-convert-result-work-success.png)

<details>
<summary>转换过程(成功转换(GIF))</summary>

![currency-convert-result-work-success.gif](/docs/img/currency-convert-result-work-success.gif)

</details>

转换错误

![currency-convert-result-work-error.png](/docs/img/currency-convert-result-work-error.png)

<details>
<summary>转换过程(转换过程中的错误(GIF))</summary>

![currency-convert-result-work-error.gif](/docs/img/currency-convert-result-work-error.gif)

</details>

---

## PHP 中的货币转换器

创建一个具有类似功能的PHP项目，但有许多不同之处:

- 实现了web界面
- 描述了所有可用端点的服务。

代码示例: [freecurrencyapi-converter-php](https://github.com/yaleksandr89/freecurrencyapi-converter-php) — 大家都在那里，进来！ 😄

---

## 注意事项

1. **保安令牌:**
-确保您的API令牌在 `.env` 中正确指定.
   -永远不要将文件 `.env` 添加到存储库。

2. **建议:**
-使用虚拟环境隔离依赖关系。
   -必要时通过 `pip install --upgrade` 更新依赖项。
