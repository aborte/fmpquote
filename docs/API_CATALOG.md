# Financial Modeling Prep (FMP Ultimate API) `/stable/` 核心接口路径速查表

> 完整 283 个接口的参数字典、返回字段类型与实盘 JSON 示例请参阅 **[FMP 中文接口文档中心](https://fmpquote.com/apis/)**。

| 分类模块 | 接口中文名称 | `/stable/` 端点路径 | 必选参数 | 典型返回字段 |
| :--- | :--- | :--- | :--- | :--- |
| **财务报表** | 利润表 (Income Statement) | `/stable/income-statement` | `symbol` | `date`, `acceptedDate`, `revenue`, `netIncome`, `eps` |
| **财务报表** | 资产负债表 (Balance Sheet) | `/stable/balance-sheet-statement` | `symbol` | `totalAssets`, `totalDebt`, `totalStockholdersEquity` |
| **财务报表** | 现金流量表 (Cash Flow) | `/stable/cash-flow-statement` | `symbol` | `operatingCashFlow`, `capitalExpenditure`, `freeCashFlow` |
| **财务报表** | 按产品营收细分 | `/stable/revenue-product-segmentation` | `symbol` | `fiscalYear`, `period`, `data` |
| **财务报表** | 按地区营收细分 | `/stable/revenue-geographic-segments` | `symbol` | `fiscalYear`, `period`, `data` |
| **财务比率** | TTM 财务比率 | `/stable/ratios-ttm` | `symbol` | `priceToEarningsRatioTTM`, `netProfitMarginTTM`, `returnOnEquityTTM` |
| **财务比率** | TTM 关键指标 | `/stable/key-metrics-ttm` | `symbol` | `evToEbitdaTTM`, `roicTTM`, `freeCashFlowYieldTTM` |
| **财务比率** | 财务健康评分 (F-Score / Z-Score) | `/stable/financial-scores` | `symbol` | `piotroskiScore`, `altmanZScore`, `workingCapital` |
| **估值模型** | DCF 自由现金流折现估值 | `/stable/discounted-cash-flow` | `symbol` | `dcf`, `Stock Price` |
| **估值模型** | 自定义高级 DCF | `/stable/custom-discounted-cash-flow` | `symbol` | `wacc`, `ufcf`, `terminalValue`, `equityValuePerShare` |
| **实时与历史行情** | 跨市场实时报价 | `/stable/quote` | `symbol` | `price`, `changePercentage`, `volume`, `marketCap` |
| **实时与历史行情** | 完整历史日线 (EOD Full) | `/stable/historical-price-eod/full` | `symbol` | `date`, `open`, `high`, `low`, `close`, `volume`, `vwap` |
| **实时与历史行情** | 分红复权日线序列 | `/stable/historical-price-eod/dividend-adjusted` | `symbol` | `date`, `adjOpen`, `adjHigh`, `adjLow`, `adjClose`, `volume` |
| **实时与历史行情** | 1分钟级分时 K 线 | `/stable/historical-chart/1min` | `symbol` | `date`, `open`, `high`, `low`, `close`, `volume` |
| **机构与聪明钱** | 13F 机构持仓申报明细 | `/stable/institutional-ownership/extract` | `cik`, `year`, `quarter` | `cusip`, `symbol`, `sharesNumber`, `marketValue`, `weight` |
| **机构与聪明钱** | 高管内幕交易检索 (Form 4) | `/stable/insider-trading/search` | — | `reportingCik`, `transactionDate`, `transactionType`, `price` |
| **机构与聪明钱** | 美国参议院议员交易披露 | `/stable/senate-trading` | `symbol` | `firstName`, `lastName`, `transactionDate`, `type`, `amount` |
| **机构与聪明钱** | 美国众议院议员交易披露 | `/stable/house-trading` | `symbol` | `firstName`, `lastName`, `transactionDate`, `type`, `amount` |
| **财报纪要与预期** | 财报电话会议纪要全文 | `/stable/earning-call-transcript` | `symbol`, `year`, `quarter` | `symbol`, `period`, `year`, `date`, `content` |
| **财报纪要与预期** | 华尔街分析师业绩预测共识 | `/stable/analyst-estimates` | `symbol`, `period` | `estimatedRevenueAvg`, `estimatedEpsAvg`, `numberAnalystsEstimatedEps` |
| **指数与退市池** | 标普 500 历史成分股变动 | `/stable/historical-sp500-constituent` | — | `dateAdded`, `addedSecurity`, `removedTicker`, `reason` |
| **指数与退市池** | 历年退市公司清单 | `/stable/delisted-companies` | — | `symbol`, `companyName`, `exchange`, `ipoDate`, `delistedDate` |
| **宏观与利率** | 美国国债全期限收益率曲线 | `/stable/treasury-rates` | — | `date`, `month3`, `year2`, `year10`, `year30` |
| **宏观与利率** | 宏观经济日历 | `/stable/economic-calendar` | — | `date`, `country`, `event`, `actual`, `estimate`, `previous` |
