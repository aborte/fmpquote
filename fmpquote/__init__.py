"""
FMP Ultimate API 中文接口文档（附开箱即用 SDK）
Financial Modeling Prep (FMP) Python 轻量客户端

- 在线文档首页：https://fmpquote.com/
- 快速接入指南：https://fmpquote.com/quick-start/
- 283 个中文 API 接口目录：https://fmpquote.com/apis/
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

__version__ = "0.2.2"
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
