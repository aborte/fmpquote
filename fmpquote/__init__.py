"""
FMP Ultimate API 中文接口文档（附开箱即用 SDK）
Financial Modeling Prep (FMP) 国内直连 Python 轻量客户端

- 官方网站（FMP数据源中文站）：https://fmpquote.com/
- 5分钟快速接入与免费领取专属 Key：https://fmpquote.com/quick-start/
- 283 个中文 API 接口文档总览：https://fmpquote.com/apis/
"""

from .client import (
    DEFAULT_API_KEY,
    GATEWAY_BASE_URL,
    FMPAPIError,
    FMPClient,
    doc_url,
    format_cik,
    normalize_hk_symbol,
    quote,
    income_statement,
    balance_sheet,
    cash_flow,
    ratios_ttm,
    key_metrics_ttm,
    dcf,
    eod_chart,
    earnings_transcript,
    treasury_rates,
)

__version__ = "0.2.0"
__all__ = [
    "DEFAULT_API_KEY",
    "GATEWAY_BASE_URL",
    "FMPAPIError",
    "FMPClient",
    "doc_url",
    "format_cik",
    "normalize_hk_symbol",
    "quote",
    "income_statement",
    "balance_sheet",
    "cash_flow",
    "ratios_ttm",
    "key_metrics_ttm",
    "dcf",
    "eod_chart",
    "earnings_transcript",
    "treasury_rates",
]
