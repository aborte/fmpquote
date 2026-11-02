# FMP API 中文文档与Ultimate Key 免费使用指南（附开箱即用 SDK）

> 🌐 **FMP数据源中文站官网**：[https://fmpquote.com/](https://fmpquote.com/) ｜ 🚀 **5分钟快速接入与免费领专属Key**：[https://fmpquote.com/quick-start/](https://fmpquote.com/quick-start/) ｜ 📖 **283个中文API文档全集**：[https://fmpquote.com/apis/](https://fmpquote.com/apis/) ｜ 📐 **86条财务指标计算公式表**：[https://fmpquote.com/formulas/](https://fmpquote.com/formulas/) ｜ 💡 **实盘量化排雷博客**：[https://fmpquote.com/blog/](https://fmpquote.com/blog/)

本项目是面向中文美股投研、价值分析、量化回测与 AI Agent 开发者的 **Financial Modeling Prep（简称 FMP）中文文档速查手册与轻量级 Python SDK（`fmpquote`）**。

针对国内开发者使用 **Financial Modeling Prep (FMP API)** 最常见的三大痛点：
1. **官方免费版权限阉割严重**：官方 Free 档仅开放少量基础端点，无法调用 `13F` 机构持仓、财报电话会议纪要（`Earnings Transcript`）、港股/A股/欧股财报与分钟级 K 线；
2. **全英文接口字段口径复杂**：FMP 全站 **283 个 `/stable/` 接口、5,467 个返回字段** 缺乏系统的中文会计准则与量化防未来函数（Point-in-Time）说明；
3. **跨境网络不稳定与 `yfinance` 频繁 `429` 限流**：国内直连海外源站经常超时中断。

本项目直接内置了**免注册开箱即用的公用 FMP Ultimate 免费体验 Key** 与**国内高可用直连网关（`https://quote-fmp.com/stable`）**，让您复制代码第一秒即可跑通美股、港股、A 股、加密货币及宏观国债的真实 API 数据。

---

## 一、 内置 FMP Ultimate 免费试用 Key 与使用说明

为了方便开发者零门槛验证接口数据结构，本仓库在代码与文档中内置了 **2 把公用 FMP Ultimate 体验 Key**（底层具备完整的 Ultimate 旗舰级端点权限）：

| Key 角色 | 公用体验 Key 明文 | 获取与切换方式（人工替换，程序不自动切换） |
| :--- | :--- | :--- |
| **1. 代码默认内置 Key** | `Hqn1wUDEAFxfzkjo` | 已内置于 `fmpquote` SDK 与下方示例代码中，**安装后无需任何配置默认生效** |
| **2. 文档/注释备用 Key** | `rVJrTXQBRiyNyGqZ` | 明文保存在本表及 `fmpquote/client.py`、`examples/quickstart.py` 源码注释中。**注意：程序不会自动切换 Key**；若默认 Key 当日公共体验额度用完，请从代码注释或此处手动复制备用 Key 传入 `FMPClient(api_key="rVJrTXQBRiyNyGqZ")` |

### 📌 公用体验 Key 支持的跨市场示范标的与规则
- **支持的跨市场示范标的（覆盖 7 大资产类别，零配置直接返回 200 真实数据）**：
  - **美股核心科技与巨头**：`AAPL`（苹果）、`NVDA`（英伟达）、`TSLA`（特斯拉）、`MSFT`（微软）、`AMZN`（亚马逊）、`META`、`GOOGL`（谷歌）、`AMD`、`AVGO`（博通）
  - **港股与 A 股代表标的**：`00700.HK` / `0700.HK`（腾讯控股）、`600519.SS`（贵州茅台）、`300750.SZ`（宁德时代）
  - **ETF、指数、外汇、加密与商品**：`SPY`（标普500 ETF）、`^GSPC`（标普500指数）、`EURUSD`（欧元兑美元）、`BTCUSD`（比特币）、`GCUSD`（黄金）
  - **无代码限制的全局/宏观接口**：如 `/stable/treasury-rates`（美债收益率曲线）、`/stable/economic-calendar`（宏观经济日历）、`/stable/market-risk-premium`（国家股权风险溢价）等全部直接放行。
- **如何免费获取不限股票代码的个人独享 Key？**
  - 公用 Key 仅用于测试接口连通性与字段结构（不支持 `Bulk` 全市场打包下载与非示范标的查询）。
  - 如需查询**全美股 10,000+ 股票、历年退市股票池及全市场批量数据**，请直接访问 **[FMP数据源中文站（https://fmpquote.com/）](https://fmpquote.com/)** 或阅读 **[5分钟快速接入指南（https://fmpquote.com/quick-start/）](https://fmpquote.com/quick-start/)**，微信扫码即可**免费领取个人专属试用 Key**（个人独享额度，支持全市场标的）。

---

## 二、 30 秒安装与开箱即用 Python 示例

### 1. 安装 `fmpquote`

```bash
pip install fmpquote
# 如需直接将接口返回转为 pandas.DataFrame，建议一并安装 pandas：
pip install "fmpquote[pandas]"
```

### 2. Python 实盘调用示例（直接复制即可运行）

```python
from fmpquote import FMPClient

# 默认自动使用内置公用体验 Key ("Hqn1wUDEAFxfzkjo") 与国内直连网关 https://quote-fmp.com/stable
# 若默认体验 Key 当日公共额度耗尽，请手动从此处复制备用 Key 传入：
# client = FMPClient(api_key="rVJrTXQBRiyNyGqZ")
client = FMPClient()

# -------------------------------------------------------------------------
# 示例 1：获取美股、港股、A股与加密货币最新实时报价 (/stable/quote)
# 完整字段中文说明：https://fmpquote.com/apis/stock-quote/
# -------------------------------------------------------------------------
for symbol in ["AAPL", "NVDA", "00700.HK", "600519.SS", "BTCUSD"]:
    quote_data = client.quote(symbol)[0]
    print(f"{quote_data['symbol']:<10} 最新价: {quote_data['price']:<10} 涨跌幅: {quote_data['changePercentage']}%")

# -------------------------------------------------------------------------
# 示例 2：拉取英伟达 (NVDA) 历年 10-K 利润表，提取 SEC 精确披露时间防回测未来函数
# 完整字段中文说明：https://fmpquote.com/apis/income-statement/
# -------------------------------------------------------------------------
income_list = client.income_statement("NVDA", period="annual", limit=3)
for row in income_list:
    print(
        f"财年期末: {row['date']} | SEC接收时刻(acceptedDate): {row['acceptedDate']} | "
        f"营收: ${row['revenue']/1e9:.2f}B | 净利润: ${row['netIncome']/1e9:.2f}B"
    )

# -------------------------------------------------------------------------
# 示例 3：获取微软 (MSFT) TTM 关键财务比率与 DCF 现金流折现估值
# 财务比率接口文档：https://fmpquote.com/apis/financial-ratios-ttm/
# 86条财务公式速查：https://fmpquote.com/formulas/
# -------------------------------------------------------------------------
ratios = client.ratios_ttm("MSFT")[0]
dcf_val = client.dcf("AAPL")[0]
print("MSFT PE(TTM):", ratios.get("priceToEarningsRatioTTM"))
print("AAPL DCF估值:", dcf_val.get("dcf"), "当前股价:", dcf_val.get("Stock Price"))
```

### 3. 不装 SDK，直接用原生 `requests` 或 `cURL` 调通网关

如果您在现有量化回测框架（Backtrader / Qlib / VN.PY）或其它语言中使用，可以直接请求国内直连网关 `https://quote-fmp.com/stable`（支持 URL 参数 `?apikey=`、`apikey` 请求头、或 `Authorization: Bearer <key>` 三种标准鉴权方式）：

```python
import requests

# 默认体验 Key：Hqn1wUDEAFxfzkjo
# 备用体验 Key（手动替换用）：rVJrTXQBRiyNyGqZ
# 个人专属免费 Key 领取：https://fmpquote.com/quick-start/
API_KEY = "Hqn1wUDEAFxfzkjo"

resp = requests.get(
    "https://quote-fmp.com/stable/income-statement",
    params={"symbol": "AAPL", "period": "annual", "limit": 3, "apikey": API_KEY},
    timeout=15,
)
print(resp.json())
```

---

## 三、 Financial Modeling Prep (FMP) 33 大分类与核心接口中文文档速查表

**FMP数据源中文站（[https://fmpquote.com/apis/](https://fmpquote.com/apis/)）** 已完成 FMP 全站 **30 个顶层大类、3 个财务报表子专题、283 个接口详情页及 5,467 个返回字段** 的 100% 中文深度重写与实盘校验。您可以直接点击下方表格进入对应分类枢纽（Hub）与高频接口文档：

| 数据大类（点击进入分类中文目录） | 典型量化与投研应用场景 | 代表性高频接口（点击查看字段字典与代码示例） | 核心返回字段举例 |
| :--- | :--- | :--- | :--- |
| **[财务报表总览 (Statements)](https://fmpquote.com/apis/statements/)** | 美股/港股/A股 `10-K` 年报与 `10-Q` 季报三表拉取、Point-in-Time 历史基本面回测 | • [利润表 (Income Statement)](https://fmpquote.com/apis/income-statement/)<br>• [资产负债表 (Balance Sheet)](https://fmpquote.com/apis/balance-sheet-statement/)<br>• [现金流量表 (Cash Flow)](https://fmpquote.com/apis/cash-flow-statement/)<br>• [三大核心报表子专题](https://fmpquote.com/apis/statements/reports/) | `date`, `filingDate`, `acceptedDate`, `reportedCurrency`, `revenue`, `ebitda`, `netIncome`, `freeCashFlow` |
| **[财务比率与核心指标 (Metrics)](https://fmpquote.com/apis/statements/metrics/)** | 跨行业估值因子库构建、ROE/ROIC/毛利率/周转率横截面选股、Piotroski F-Score 与 Altman Z-Score | • [TTM 财务比率 (Ratios TTM)](https://fmpquote.com/apis/financial-ratios-ttm/)<br>• [历史财务比率 (Financial Ratios)](https://fmpquote.com/apis/financial-ratios/)<br>• [TTM 关键指标 (Key Metrics TTM)](https://fmpquote.com/apis/key-metrics-ttm/)<br>• [财务健康评分 (Financial Scores)](https://fmpquote.com/apis/financial-scores/) | `priceToEarningsRatioTTM`, `returnOnEquityTTM`, `roicTTM`, `daysOfInventoryOutstandingTTM`, `piotroskiScore` |
| **[原始申报财报与营收拆分](https://fmpquote.com/apis/statements/as-reported/)** | SEC XBRL 原始科目核对、按产品线（如 iPhone/Mac）与按地区营收拆分分析 | • [按产品营收细分 (Revenue Product)](https://fmpquote.com/apis/revenue-product-segmentation/)<br>• [按地区营收细分 (Revenue Geo)](https://fmpquote.com/apis/revenue-geographic-segments/)<br>• [原始申报利润表 (As Reported)](https://fmpquote.com/apis/as-reported-income-statements/) | `fiscalYear`, `period`, `data`, `segment` |
| **[股票实时报价 (Quote)](https://fmpquote.com/apis/quote/)** | 跨市场实时价格快照、自选股批量监控、盘前盘后异动扫描 | • [股票实时报价 (Stock Quote)](https://fmpquote.com/apis/stock-quote/)<br>• [批量股票报价 (Batch Quote)](https://fmpquote.com/apis/stock-batch-quote/)<br>• [盘后实时报价 (Aftermarket Quote)](https://fmpquote.com/apis/aftermarket-quote/) | `symbol`, `price`, `changePercentage`, `volume`, `marketCap`, `dayHigh`, `dayLow`, `timestamp` |
| **[历史行情与 K 线 (Chart)](https://fmpquote.com/apis/chart/)** | 日线 `OHLCV`、分红复权价格序列、`1min/5min/1hour` 分钟级高频回测 | • [完整日线行情 (EOD Full)](https://fmpquote.com/apis/stock-price-and-volume-data/)<br>• [分红复权日线 (Dividend Adjusted)](https://fmpquote.com/apis/dividend-adjusted-price-chart/)<br>• [1分钟K线 (1-Min Chart)](https://fmpquote.com/apis/1-min-interval-stock-chart/) | `date`, `open`, `high`, `low`, `close`, `adjClose`, `volume`, `vwap` |
| **[13F 机构持仓追踪 (Form 13F)](https://fmpquote.com/apis/form13f/)** | 追踪伯克希尔（巴菲特）、桥水、文艺复兴等顶级华尔街机构季度建仓、增减持与持仓成本 | • [机构持仓申报明细 (Filings Extract)](https://fmpquote.com/apis/filings-extract/)<br>• [持股机构申报分析 (Analytics)](https://fmpquote.com/apis/filings-extract-with-analytics-by-holder/)<br>• [13F 申报日期清单 (Filing Dates)](https://fmpquote.com/apis/form-13f-filings-dates/) | `cik`, `cusip`, `symbol`, `sharesNumber`, `marketValue`, `weight`, `changeInSharesNumberPercentage` |
| **[业绩电话会纪要 (Earnings Transcript)](https://fmpquote.com/apis/earningstranscript/)** | 管理层陈述与分析师问答（Q&A）逐字稿全文拉取、LLM / RAG 投研 Agent 业绩指引提取 | • [电话会纪要全文 (Transcript)](https://fmpquote.com/apis/earnings-transcript/)<br>• [按代码查电话会日期 (Dates)](https://fmpquote.com/apis/transcripts-dates-by-symbol/)<br>• [最新业绩电话会纪要](https://fmpquote.com/apis/latest-earning-transcripts/) | `symbol`, `period`, `year`, `date`, `content` |
| **[DCF 现金流折现估值](https://fmpquote.com/apis/discountedcashflow/)** | 企业自由现金流（UFCF）与股权自由现金流（LFCF）自动估值、WACC 敏感性测算 | • [DCF 估值 (DCF Valuation)](https://fmpquote.com/apis/dcf-valuation/)<br>• [自定义高级 DCF (Custom DCF)](https://fmpquote.com/apis/custom-dcf-advanced/)<br>• [自定义杠杆 DCF (Levered DCF)](https://fmpquote.com/apis/custom-dcf-levered/) | `dcf`, `Stock Price`, `wacc`, `ufcf`, `terminalValue`, `equityValuePerShare` |
| **[高管内幕交易 (Insider Trades)](https://fmpquote.com/apis/insidertrades/)** | SEC Form 4 公司高管与大股东真实二级市场买入（`P-Purchase`）/ 抛售（`S-Sale`）监控 | • [内幕交易检索 (Search Insider)](https://fmpquote.com/apis/search-insider-trades/)<br>• [内幕交易统计 (Statistics)](https://fmpquote.com/apis/insider-trade-statistics/)<br>• [最新内幕交易流 (Latest)](https://fmpquote.com/apis/latest-insider-trading/) | `reportingCik`, `transactionDate`, `transactionType`, `securitiesTransacted`, `price` |
| **[美国参众两院议员交易 (Senate & House)](https://fmpquote.com/apis/senate/)** | 国会参议员与众议员股票买卖披露追踪（聪明钱政治 Alpha 因子） | • [参议院交易动态 (Senate Trading)](https://fmpquote.com/apis/senate-trading-activity/)<br>• [众议院交易记录 (House Trades)](https://fmpquote.com/apis/u-s-house-trades/)<br>• [参议院最新财务披露](https://fmpquote.com/apis/latest-senate-financial-disclosures/) | `firstName`, `lastName`, `disclosureDate`, `transactionDate`, `ticker`, `type`, `amount` |
| **[公司概况与高管治理 (Company)](https://fmpquote.com/apis/company/)** | 公司基本面档案、市值历史、流通股本（Share Float）、高管薪酬与同行对比 | • [公司概况 (Company Profile)](https://fmpquote.com/apis/company-profile-data/)<br>• [历史市值序列 (Historical Market Cap)](https://fmpquote.com/apis/historical-market-cap/)<br>• [股票同业可比公司 (Stock Peers)](https://fmpquote.com/apis/stock-peer-comparison/) | `symbol`, `companyName`, `industry`, `sector`, `marketCap`, `beta`, `isin`, `cusip` |
| **[退市股票与指数历史成分股](https://fmpquote.com/apis/directory/)** / **[指数 (Indexes)](https://fmpquote.com/apis/indexes/)** | 消除量化回测“幸存者偏差（Survivorship Bias）”、还原历史任意时点标普500/纳指成分股 | • [退市公司清单 (Delisted Companies)](https://fmpquote.com/apis/delisted-companies/)<br>• [标普500成分历史变动](https://fmpquote.com/apis/historical-s-p-500/)<br>• [标普500当前成分股](https://fmpquote.com/apis/s-p-500-index/) | `symbol`, `companyName`, `exchange`, `ipoDate`, `delistedDate`, `dateAdded`, `removedTicker` |
| **[华尔街分析师预期与评级 (Analyst)](https://fmpquote.com/apis/analyst/)** | 一致预期 EPS/营收预测、目标价共识（Price Target）、大行评级上调/下调 | • [财务预测共识 (Financial Estimates)](https://fmpquote.com/apis/financial-estimates/)<br>• [目标价摘要 (Price Target Summary)](https://fmpquote.com/apis/price-target-summary/)<br>• [评级共识汇总 (Grades Summary)](https://fmpquote.com/apis/stock-grades-summary/) | `estimatedRevenueAvg`, `estimatedEpsAvg`, `lastMonthAvgPriceTarget`, `strongBuy`, `buy` |
| **[财报日历、分红与拆股 (Calendar)](https://fmpquote.com/apis/calendar/)** | 财报发布日历、业绩超预期（Earnings Surprises）、历史分红派息与股票拆分（Stock Splits） | • [财报日历 (Earnings Calendar)](https://fmpquote.com/apis/earnings-calendar/)<br>• [公司分红历史 (Dividends)](https://fmpquote.com/apis/dividends-company/)<br>• [公司拆股历史 (Stock Splits)](https://fmpquote.com/apis/stock-split-details/) | `epsActual`, `epsEstimated`, `adjDividend`, `recordDate`, `numerator`, `denominator` |
| **[宏观经济与美债收益率 (Economics)](https://fmpquote.com/apis/economics/)** | 美债收益率曲线、CPI/非农/GDP 经济指标序列、全球各国股权风险溢价（ERP） | • [美债收益率曲线 (Treasury Rates)](https://fmpquote.com/apis/treasury-rates/)<br>• [宏观经济指标 (Indicators)](https://fmpquote.com/apis/economics-indicators/)<br>• [市场风险溢价 (Market Risk Premium)](https://fmpquote.com/apis/market-risk-premium/) | `month3`, `year2`, `year10`, `year30`, `country`, `totalEquityRiskPremium` |
| **[更多专业分类导航](https://fmpquote.com/apis/)** | 涵盖技术指标、ETF、SEC 原始申报、外汇、加密、大宗商品、COT 持仓、实时流等 | • [技术指标 (SMA/EMA/RSI/ADX)](https://fmpquote.com/apis/technicalindicators/) · [ETF 与共同基金](https://fmpquote.com/apis/etfandmutualfunds/)<br>• [SEC 原始申报文件 (8-K/10-K)](https://fmpquote.com/apis/secfilings/) · [CFTC COT 期货持仓报告](https://fmpquote.com/apis/commitmentoftraders/)<br>• [外汇行情](https://fmpquote.com/apis/forex/) · [加密货币](https://fmpquote.com/apis/crypto/) · [大宗商品](https://fmpquote.com/apis/commodity/)<br>• [Bulk 全市场批量下载](https://fmpquote.com/apis/bulk/) · [WebSocket 实时流](https://fmpquote.com/apis/websockets/)<br>• [证券代码与 CIK 检索](https://fmpquote.com/apis/search/) · [涨跌幅与板块表现](https://fmpquote.com/apis/marketperformance/)<br>• [全球交易所交易时段](https://fmpquote.com/apis/markethours/) · [财经新闻与研报](https://fmpquote.com/apis/news/) · [ESG 评级](https://fmpquote.com/apis/esg/) | 详见各分类页完整中文参数表与 Python 代码示例 |

---

## 四、 量化回测三大实盘排雷与深度技术专题（延伸阅读）

基于对 Financial Modeling Prep 上游真实返回数据的逐字段实盘对账，我们在 **[FMP数据源中文站技术博客（https://fmpquote.com/blog/）](https://fmpquote.com/blog/)** 发布了多篇带真实 JSON 存证与复现脚本的深度研究文章：

1. **防回测“未来函数”与存货周期拐点**：
   - 财报的 `date`（如 `2025-09-30`）只是会计期末日，真正在二级市场公开的时间必须取 `acceptedDate`（SEC EDGAR 接收时间戳）。
   - 延伸阅读：
     - 📖 **[《AI 硬件周期到了哪一步？用 FMP 财报 API 拆解英伟达与美光的毛利率与存货周转天数 (DIO)》](https://fmpquote.com/blog/ai-hardware-cycle-nvda-mu-margin-dio/)**
     - 📖 **[《如何消除美股回测中的“幸存者偏差”？基于 FMP 退市股票与标普 500 历史成分股接口实战》](https://fmpquote.com/blog/survivorship-bias-sp500-delisted/)**
2. **日线 `vwap` 字段的真实计算口径**：
   - 经对 AAPL、SPY、BTCUSD 等 176 根历史日线实测核验，FMP 日线接口返回的 `vwap` 在已收盘结算日恒等于**四价均值 `(open + high + low + close) / 4`**（非成交量加权）；如需真实成交量加权 VWAP，请拉取 [1分钟分时 K 线接口](https://fmpquote.com/apis/1-min-interval-stock-chart/) 按 `sum(close * volume) / sum(volume)` 自行合成。
   - 延伸阅读：
     - 📖 **[《FMP API 深度评测：283 个接口全景、实盘延迟、字段口径排雷与平替对比》](https://fmpquote.com/blog/fmp-api-full-review/)**
     - 📖 **[《FMP (Financial Modeling Prep) 是什么？美股财报、13F 持仓与全球行情接口全景指南》](https://fmpquote.com/blog/what-is-fmp/)**
3. **追踪华尔街“聪明钱”与构建 AI 财报投研 Agent**：
   - 延伸阅读：
     - 📖 **[《如何用 Python 追踪华尔街“聪明钱”？13F 机构持仓、高管内幕交易与国会议员交易 API 实战》](https://fmpquote.com/blog/smart-money-13f-insider-senate/)**
     - 📖 **[《用 AI Agent 自动拆解美股财报电话会：基于 FMP 电话会议纪要 API 与业绩指引核验》](https://fmpquote.com/blog/ai-agent-earnings-transcripts-guidance/)**
     - 📖 **[《FMP vs Massive (原 Polygon.io)：做美股量化与投研到底该选哪家数据源？》](https://fmpquote.com/blog/20261020-4sxl/)**

---

## 五、 常见报错状态码说明与技术支持

当您使用内置公用体验 Key 或个人专属 Key 调用接口时，如遇 HTTP 非 200 响应，可参考以下说明或查阅 **[常见问题与实盘避坑 FAQ（https://fmpquote.com/faq/）](https://fmpquote.com/faq/)**：

- **`HTTP 403`（`Demo key only supports sample tickers...`）**：
  当前使用的是公用体验 Key 且查询了非示范股票代码（或调用了 `-bulk` 批量下载接口）。请前往 **[https://fmpquote.com/](https://fmpquote.com/)** 免费领取个人专属试用 Key 即可解锁全市场代码。
- **`HTTP 429`（`Demo key quota exceeded...`）**：
  当前公用体验 Key 的体验额度已用完。您可以：
  1. 手动将代码中的 `api_key` 替换为本仓库注释中的备用体验 Key **`rVJrTXQBRiyNyGqZ`**；
  2. 或直接访问 **[https://fmpquote.com/quick-start/](https://fmpquote.com/quick-start/)** 扫码免费领取个人独享 Key。
- **财务指标计算公式核对**：
  对 `ROE`、`ROIC`、`EV/EBITDA`、`FCF`、`Piotroski F-Score`、`Altman Z-Score` 等分子分母口径有疑问时，请直接查阅 **[FMP 财务指标计算公式中英对照词典（https://fmpquote.com/formulas/）](https://fmpquote.com/formulas/)**。

---

## License

MIT License · 由 **[FMP数据源中文站（https://fmpquote.com/）](https://fmpquote.com/)** 维护发布。
