"""
FMP Ultimate API 中文接口文档（附开箱即用 SDK） — 快速演示脚本
在线文档：https://fmpquote.com/apis/
"""

from fmpquote import FMPClient

# 默认内置测试 Key（也可替换为个人专属 Key 或备用测试 Key: rVJrTXQBRiyNyGqZ）
client = FMPClient()

print("=== 1. 跨市场实时报价（美股 AAPL / 港股 00700.HK / A股 600519.SS / 加密 BTCUSD）===")
for ticker in ["AAPL", "00700.HK", "600519.SS", "BTCUSD"]:
    res = client.quote(ticker)
    if res:
        q = res[0]
        print(f"  {q.get('symbol'):<10} | 最新价: {q.get('price'):<10} | 涨跌幅: {q.get('changePercentage')}% | 名称: {q.get('name')}")

print("\n=== 2. 英伟达 (NVDA) 最新 10-K 年度利润表与 SEC 真实披露时刻 (acceptedDate) ===")
inc = client.income_statement("NVDA", period="annual", limit=2)
for row in inc:
    print(
        f"  财年期末(date): {row.get('date')} | SEC披露时刻(acceptedDate): {row.get('acceptedDate')} "
        f"| 营收: ${row.get('revenue', 0) / 1e9:.2f}B | 净利润: ${row.get('netIncome', 0) / 1e9:.2f}B"
    )

print("\n=== 3. 微软 (MSFT) 滚动十二个月 (TTM) 核心财务比率 ===")
ratios = client.ratios_ttm("MSFT")
if ratios:
    r = ratios[0]
    print(
        f"  PE(TTM): {r.get('priceToEarningsRatioTTM'):.2f} | "
        f"PB(TTM): {r.get('priceToBookRatioTTM'):.2f} | "
        f"净利率(TTM): {r.get('netProfitMarginTTM') * 100:.2f}%"
    )

print("\n=== 4. 宏观无风险利率：美国国债全期限收益率曲线 ===")
rates = client.treasury_rates()
if rates:
    latest = rates[0]
    print(
        f"  日期: {latest.get('date')} | 3月期: {latest.get('month3')}% | "
        f"2年期: {latest.get('year2')}% | 10年期: {latest.get('year10')}% | 30年期: {latest.get('year30')}%"
    )
