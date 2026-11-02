"""
Financial Modeling Prep (FMP Ultimate API) Python 客户端核心实现
接口参数与返回字段字典：https://fmpquote.com/apis/
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional, Union

# FMP API `/stable/` 接入端点
GATEWAY_BASE_URL = "https://quote-fmp.com/stable"

# 默认内置公共测试 Key（支持跨市场示范标的直接调用）
DEFAULT_API_KEY = "Hqn1wUDEAFxfzkjo"
# 备用公共测试 Key: rVJrTXQBRiyNyGqZ


class FMPAPIError(RuntimeError):
    """FMP API 请求异常"""

    def __init__(self, status_code: int, message: str, endpoint: str = ""):
        self.status_code = status_code
        self.message = message
        self.endpoint = endpoint
        super().__init__(f"[HTTP {status_code}] {message}")


def doc_url(slug: str) -> str:
    """
    返回指定接口的中文文档地址。
    示例：doc_url("income-statement") -> "https://fmpquote.com/apis/income-statement/"
    """
    clean = slug.strip().strip("/")
    return f"https://fmpquote.com/apis/{clean}/"


def format_cik(cik: Union[str, int]) -> str:
    """
    将 SEC CIK 编号统一补齐为标准 10 位前导零字符串（如 1067983 -> '0001067983'）。
    """
    digits = "".join(ch for ch in str(cik).strip() if ch.isdigit())
    return digits.zfill(10)


def normalize_hk_symbol(symbol: str) -> str:
    """
    港股代码归一化：FMP 上游采用 4 位数字港股代码（如 0700.HK），
    当传入 5 位代码（如 00700.HK）时自动转为 0700.HK。
    """
    s = str(symbol).strip()
    if s.upper().endswith(".HK"):
        code_part = s[:-3]
        if len(code_part) == 5 and code_part.isdigit() and code_part.startswith("0"):
            return f"{code_part[1:]}.HK"
    return s


class FMPClient:
    """
    Financial Modeling Prep (FMP Ultimate API) 轻量 Python 客户端

    参数说明：
    - api_key: FMP API Key。若不传，优先读取环境变量 `FMP_API_KEY`；
               未设置环境变量时使用内置默认测试 Key `DEFAULT_API_KEY`。
               个人专属 Key 可在 https://fmpquote.com/quick-start/ 免费获取。
    - base_url: 默认端点 `https://quote-fmp.com/stable`。
    - timeout: 单次 HTTP 请求超时秒数（默认 15 秒）。
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = GATEWAY_BASE_URL,
        timeout: int = 15,
    ):
        self.api_key = (api_key or os.environ.get("FMP_API_KEY") or DEFAULT_API_KEY).strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._headers = {
            "User-Agent": "fmpquote-python-sdk/0.2.1",
            "Accept": "application/json",
        }

    def build_query_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """构建请求查询参数字典"""
        query: Dict[str, Any] = {}
        if params:
            for k, v in params.items():
                if v is not None:
                    if k == "symbol" and isinstance(v, str):
                        v = normalize_hk_symbol(v)
                    query[k] = v
        query["apikey"] = self.api_key
        return query

    def _http_get(self, url: str, query: Dict[str, Any]) -> tuple[int, Dict[str, str], str]:
        qs = urllib.parse.urlencode(query)
        full_url = f"{url}?{qs}" if qs else url
        req = urllib.request.Request(full_url, headers=self._headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status = resp.status
                headers = {k: v for k, v in resp.headers.items()}
                body = resp.read().decode("utf-8", errors="replace")
                return status, headers, body
        except urllib.error.HTTPError as e:
            status = e.code
            headers = {k: v for k, v in e.headers.items()} if e.headers else {}
            body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
            return status, headers, body

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        as_df: bool = False,
        max_retries: int = 2,
    ) -> Any:
        """
        通用 GET 请求方法（支持 `/stable/<endpoint>` 全系接口）
        """
        ep = endpoint.strip().lstrip("/")
        if ep.startswith("stable/"):
            ep = ep[len("stable/"):]
        url = f"{self.base_url}/{ep}"
        query = self.build_query_params(params)

        for attempt in range(max_retries + 1):
            status_code, resp_headers, resp_text = self._http_get(url, query)
            if status_code == 200:
                data = json.loads(resp_text)
                if as_df:
                    try:
                        import pandas as pd
                    except ImportError as exc:
                        raise ImportError(
                            "转为 DataFrame 需要安装 pandas：pip install pandas"
                        ) from exc
                    return pd.DataFrame(data)
                return data

            err_msg = resp_text
            try:
                payload = json.loads(resp_text)
                if isinstance(payload, dict):
                    err_msg = (
                        payload.get("Error Message")
                        or payload.get("error")
                        or payload.get("message")
                        or resp_text
                    )
            except ValueError:
                pass

            if status_code in (400, 401, 403):
                raise FMPAPIError(status_code, err_msg, endpoint=ep)

            if status_code == 429:
                if "Demo key" in err_msg or "Bandwidth" in err_msg or "体验" in err_msg:
                    raise FMPAPIError(status_code, err_msg, endpoint=ep)
                if attempt < max_retries:
                    retry_after = float(resp_headers.get("Retry-After", 2 ** (attempt + 1)))
                    time.sleep(min(retry_after, 10.0))
                    continue
                raise FMPAPIError(status_code, err_msg, endpoint=ep)

            raise FMPAPIError(status_code, err_msg, endpoint=ep)

    def quote(self, symbol: str = "AAPL", as_df: bool = False) -> Any:
        """获取股票、ETF、指数、外汇、加密货币最新实时报价（`/stable/quote`）"""
        return self.get("quote", {"symbol": symbol}, as_df=as_df)

    def income_statement(
        self,
        symbol: str = "AAPL",
        period: str = "annual",
        limit: int = 5,
        as_df: bool = False,
    ) -> Any:
        """获取利润表数据（支持年报 `annual` / 季报 `quarter`，含 SEC `acceptedDate` 披露时间戳）"""
        return self.get(
            "income-statement",
            {"symbol": symbol, "period": period, "limit": limit},
            as_df=as_df,
        )

    def balance_sheet(
        self,
        symbol: str = "AAPL",
        period: str = "annual",
        limit: int = 5,
        as_df: bool = False,
    ) -> Any:
        """获取资产负债表数据（`/stable/balance-sheet-statement`）"""
        return self.get(
            "balance-sheet-statement",
            {"symbol": symbol, "period": period, "limit": limit},
            as_df=as_df,
        )

    def cash_flow(
        self,
        symbol: str = "AAPL",
        period: str = "annual",
        limit: int = 5,
        as_df: bool = False,
    ) -> Any:
        """获取现金流量表数据（`/stable/cash-flow-statement`）"""
        return self.get(
            "cash-flow-statement",
            {"symbol": symbol, "period": period, "limit": limit},
            as_df=as_df,
        )

    def ratios_ttm(self, symbol: str = "NVDA", as_df: bool = False) -> Any:
        """获取滚动十二个月（TTM）核心财务比率（PE/PB/ROE/ROIC/毛利率/净利率等）"""
        return self.get("ratios-ttm", {"symbol": symbol}, as_df=as_df)

    def key_metrics_ttm(self, symbol: str = "NVDA", as_df: bool = False) -> Any:
        """获取 TTM 关键经营与估值指标（EV/EBITDA、自由现金流收益率、研发强度等）"""
        return self.get("key-metrics-ttm", {"symbol": symbol}, as_df=as_df)

    def dcf(self, symbol: str = "AAPL", as_df: bool = False) -> Any:
        """获取 DCF 自由现金流折现估值测算结果（`/stable/discounted-cash-flow`）"""
        return self.get("discounted-cash-flow", {"symbol": symbol}, as_df=as_df)

    def eod_chart(
        self,
        symbol: str = "AAPL",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        as_df: bool = False,
    ) -> Any:
        """获取历史日线 OHLCV 行情序列（`/stable/historical-price-eod/full`）"""
        return self.get(
            "historical-price-eod/full",
            {"symbol": symbol, "from": from_date, "to": to_date},
            as_df=as_df,
        )

    def earnings_transcript(
        self,
        symbol: str = "NVDA",
        year: int = 2025,
        quarter: int = 4,
        as_df: bool = False,
    ) -> Any:
        """获取公司财报电话会议纪要全文（管理层陈述与分析师 Q&A 问答实录）"""
        return self.get(
            "earning-call-transcript",
            {"symbol": symbol, "year": year, "quarter": quarter},
            as_df=as_df,
        )

    def treasury_rates(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        as_df: bool = False,
    ) -> Any:
        """获取美国国债全期限收益率曲线（1月期至30年期）"""
        return self.get(
            "treasury-rates",
            {"from": from_date, "to": to_date},
            as_df=as_df,
        )


# ---------------------------------------------------------------------------
# 顶层快捷函数
# ---------------------------------------------------------------------------
_default_client = FMPClient()


def quote(symbol: str = "AAPL", as_df: bool = False, api_key: Optional[str] = None) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.quote(symbol=symbol, as_df=as_df)


def income_statement(
    symbol: str = "AAPL",
    period: str = "annual",
    limit: int = 5,
    as_df: bool = False,
    api_key: Optional[str] = None,
) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.income_statement(symbol=symbol, period=period, limit=limit, as_df=as_df)


def balance_sheet(
    symbol: str = "AAPL",
    period: str = "annual",
    limit: int = 5,
    as_df: bool = False,
    api_key: Optional[str] = None,
) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.balance_sheet(symbol=symbol, period=period, limit=limit, as_df=as_df)


def cash_flow(
    symbol: str = "AAPL",
    period: str = "annual",
    limit: int = 5,
    as_df: bool = False,
    api_key: Optional[str] = None,
) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.cash_flow(symbol=symbol, period=period, limit=limit, as_df=as_df)


def ratios_ttm(symbol: str = "NVDA", as_df: bool = False, api_key: Optional[str] = None) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.ratios_ttm(symbol=symbol, as_df=as_df)


def key_metrics_ttm(symbol: str = "NVDA", as_df: bool = False, api_key: Optional[str] = None) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.key_metrics_ttm(symbol=symbol, as_df=as_df)


def dcf(symbol: str = "AAPL", as_df: bool = False, api_key: Optional[str] = None) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.dcf(symbol=symbol, as_df=as_df)


def eod_chart(
    symbol: str = "AAPL",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    as_df: bool = False,
    api_key: Optional[str] = None,
) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.eod_chart(symbol=symbol, from_date=from_date, to_date=to_date, as_df=as_df)


def earnings_transcript(
    symbol: str = "NVDA",
    year: int = 2025,
    quarter: int = 4,
    as_df: bool = False,
    api_key: Optional[str] = None,
) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.earnings_transcript(symbol=symbol, year=year, quarter=quarter, as_df=as_df)


def treasury_rates(
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    as_df: bool = False,
    api_key: Optional[str] = None,
) -> Any:
    client = FMPClient(api_key=api_key) if api_key else _default_client
    return client.treasury_rates(from_date=from_date, to_date=to_date, as_df=as_df)
