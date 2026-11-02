# FMP Ultimate API 中文接口文档（附开箱即用 SDK）

[![CI](https://github.com/aborte/fmpquote/actions/workflows/ci.yml/badge.svg)](https://github.com/aborte/fmpquote/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/fmpquote.svg)](https://pypi.org/project/fmpquote/)
[![Python Versions](https://img.shields.io/pypi/pyversions/fmpquote.svg)](https://pypi.org/project/fmpquote/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

面向中文量化投研与金融开发者的 **Financial Modeling Prep（简称 FMP）中文接口速查文档与零依赖 Python 客户端（`fmpquote`）**。

在美股、港股与全球跨市场量化开发中，直接对接海外源站常遇到三类工程阻碍：
1. **官方 Free 档权限受限**：无法直接验证 `13F` 机构持仓、财报电话会议纪要（`Earnings Transcript`）、港股/A股财报与分钟级行情的数据结构；
2. **字段口径缺少 Point-in-Time 说明**：全站 283 个 `/stable/` 接口、5,467 个返回字段缺乏中文会计口径与防回测未来函数校对；
3. **跨境连接易超时**：国内环境直连海外源站延迟高、易触发网络抖动。

本仓库内置了 **2 把开箱即用的公用 FMP Ultimate 体验 Key** 与国内直连网关（`https://quote-fmp.com/stable`），安装后零配置即可调通跨市场示范标的真实数据。

---

## 一、 内置公用 FMP Ultimate 体验 Key 与切换说明

本仓库在代码与文档中提供 2 把具备 **Ultimate 旗舰级端点权限** 的公共体验 Key：

| Key 类型 | Key 明文 | 生效与切换方式（人工复制，程序不自动切换） |
| :--- | :--- | :--- |
| **代码默认 Key** | `Hqn1wUDEAFxfzkjo` | 已内置于 `fmpquote/client.py` 的 `DEFAULT_API_KEY`，不传参时默认使用 |
| **文档/注释备用 Key** | `rVJrTXQBRiyNyGqZ` | 记录在本表与源码注释中。**程序不会自动切换 Key**；若默认 Key 当日公共额度耗尽，请手动复制传入 `FMPClient(api_key="rVJrTXQBRiyNyGqZ")` |

- **公用体验 Key 适用范围**：
  - 支持跨市场核心示范标的：美股 `AAPL`、`NVDA`、`TSLA`、`MSFT`、`AMZN`、`META`、`GOOGL`、`AMD`、`AVGO`；港股 `00700.HK` / `0700.HK`；A 股 `600519.SS`、`300750.SZ`；以及 `SPY`、`^GSPC`、`EURUSD`、`BTCUSD`、`GCUSD` 和无代码限制的宏观国债接口（`/stable/treasury-rates`）。
  - 如需解锁全美股 10,000+ 标的与退市股票池，可前往 [FMP数据源中文站](https://fmpquote.com/) 或查看 [5分钟快速接入指南](https://fmpquote.com/quick-start/) 免费领取个人独享试用 Key。

---

## 二、 快速安装与 Point-in-Time 量化实战

### 1. 安装

```bash
pip install fmpquote
# 可选：支持 as_df=True 直接返回 pandas.DataFrame
pip install "fmpquote[pandas]"
```

### 2. 多市场报价与防回测“未来函数”示例

```python
from fmpquote import FMPClient

# 默认使用内置体验 Key (Hqn1wUDEAFxfzkjo)；若公共额度用尽可手动替换为备用 Key：
# client = FMPClient(api_key="rVJrTXQBRiyNyGqZ")
client = FMPClient()

# 1) 跨市场实时报价（港股 5 位代码 00700.HK 会自动归一化为 FMP 标准 4 位 0700.HK）
for ticker in ["AAPL", "NVDA", "00700.HK", "600519.SS", "BTCUSD"]:
    q = client.quote(ticker)[0]
    print(f"{q['symbol']:<10} 最新价: {q['price']:<10} 涨跌幅: {q['changePercentage']}%")

# 2) 提取 10-K 利润表的 SEC EDGAR 真实披露时刻 (acceptedDate)，杜绝回测未来函数
for row in client.income_statement("NVDA", period="annual", limit=2):
    print(
        f"会计期末(date): {row['date']} | SEC披露时刻(acceptedDate): {row['acceptedDate']} "
        f"| 营收: ${row['revenue']/1e9:.2f}B | 净利润: ${row['netIncome']/1e9:.2f}B"
    )

# 3) TTM 关键财务比率与美国国债收益率曲线
ratios = client.ratios_ttm("MSFT")[0]
rates = client.treasury_rates()[0]
print("MSFT ROE(TTM):", ratios.get("returnOnEquityTTM"), "| 10Y美债收益率:", rates.get("year10"))
```

---

## 三、 核心分类导航与接口速查

全站 283 个接口已整理为结构化中文手册，详细端点路径表可查阅仓库内的 [`docs/API_CATALOG.md`](docs/API_CATALOG.md)，或直接访问在线分类目录：

| 数据域分类 | 核心 `/stable/` 端点路径 | 量化与投研典型用途 |
| :--- | :--- | :--- |
| [财务报表 (Statements)](https://fmpquote.com/apis/statements/) | `income-statement`, `balance-sheet-statement`, `cash-flow-statement` | 美股/港股/A股三表拉取、产品与地区营收拆分、Point-in-Time 基本面因子 |
| [财务比率与指标 (Metrics)](https://fmpquote.com/apis/statements/metrics/) | `ratios-ttm`, `key-metrics-ttm`, `financial-scores` | ROE/ROIC/EV-EBITDA 横截面选股、Piotroski F-Score 与 Altman Z-Score |
| [实时与历史行情 (Quote & Chart)](https://fmpquote.com/apis/quote/) | `quote`, `historical-price-eod/full`, `historical-chart/1min` | 跨市场实时快照、分红复权日线序列、1min/5min/1hour 高频回测 |
| [13F 机构持仓 (Form 13F)](https://fmpquote.com/apis/form13f/) | `institutional-ownership/extract`, `form-13f-filings-dates` | 伯克希尔、桥水、文艺复兴等顶级机构季度建仓与持仓权重追踪 |
| [财报电话会纪要 (Transcript)](https://fmpquote.com/apis/earningstranscript/) | `earning-call-transcript`, `earning-call-transcript-dates` | 管理层陈述与分析师 Q&A 逐字稿全文、LLM 投研 Agent 业绩指引提取 |
| [高管内幕与国会交易 (Insider)](https://fmpquote.com/apis/insidertrades/) | `insider-trading/search`, `senate-trading`, `house-trading` | SEC Form 4 高管增减持与美国参众两院议员股票交易披露监控 |
| [宏观经济与利率 (Economics)](https://fmpquote.com/apis/economics/) | `treasury-rates`, `economic-calendar`, `discounted-cash-flow` | 美债收益率曲线、CPI/非农日历、WACC 与自由现金流折现测算 |

- 更多分类与完整参数字典：[283 个中文 API 接口总览](https://fmpquote.com/apis/)
- 财务比率分子分母定义：[86 条财务指标计算公式词典](https://fmpquote.com/formulas/)
- 实盘数据对账与排雷研究：[量化技术专栏博客](https://fmpquote.com/blog/) ｜ [常见状态码 FAQ](https://fmpquote.com/faq/)

---

## 四、 仓库目录结构与本地测试

```text
fmpquote/
├── fmpquote/
│   ├── __init__.py          # 顶层快捷函数导出与版本定义
│   └── client.py            # 零依赖 HTTP 客户端、港股代码归一化与错误处理
├── docs/
│   └── API_CATALOG.md       # 24 个高频 /stable/ 端点路径与字段速查表
├── examples/
│   └── quickstart.py        # 跨市场报价、10-K 财报、TTM 比率与美债实盘演示
├── tests/
│   └── test_client.py       # 单元测试套件（Key 优先级、代码归一化、CIK 格式化）
├── CHANGELOG.md             # 版本迭代记录
└── pyproject.toml           # PEP 621 打包配置
```

在本地运行单元测试：

```bash
python -m unittest discover -s tests -v
```

## License

MIT License · 详见 [LICENSE](LICENSE)。
