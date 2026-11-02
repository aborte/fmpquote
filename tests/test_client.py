"""
fmpquote 单元测试套件
运行方式：python -m unittest discover -s tests -v
"""

import os
import unittest
from fmpquote import (
     DEFAULT_API_KEY,
     GATEWAY_BASE_URL,
     FMPAPIError,
     FMPClient,
     doc_url,
     format_cik,
     normalize_hk_symbol,
)


class TestFMPQuoteClient(unittest.TestCase):
    def test_default_and_custom_api_key(self):
        old_env = os.environ.pop("FMP_API_KEY", None)
        try:
            c1 = FMPClient()
            self.assertEqual(c1.api_key, DEFAULT_API_KEY)
            self.assertEqual(c1.base_url, GATEWAY_BASE_URL)

            c2 = FMPClient(api_key="  custom_key_123  ")
            self.assertEqual(c2.api_key, "custom_key_123")
        finally:
            if old_env is not None:
                os.environ["FMP_API_KEY"] = old_env

    def test_env_api_key_priority(self):
        old_env = os.environ.get("FMP_API_KEY")
        os.environ["FMP_API_KEY"] = "env_priority_key"
        try:
            c = FMPClient()
            self.assertEqual(c.api_key, "env_priority_key")
        finally:
            if old_env is None:
                os.environ.pop("FMP_API_KEY", None)
            else:
                os.environ["FMP_API_KEY"] = old_env

    def test_normalize_hk_symbol(self):
        self.assertEqual(normalize_hk_symbol("00700.HK"), "0700.HK")
        self.assertEqual(normalize_hk_symbol("09988.HK"), "9988.HK")
        self.assertEqual(normalize_hk_symbol("0700.HK"), "0700.HK")
        self.assertEqual(normalize_hk_symbol("AAPL"), "AAPL")
        self.assertEqual(normalize_hk_symbol("600519.SS"), "600519.SS")

    def test_build_query_params(self):
        c = FMPClient(api_key="test_k")
        q = c.build_query_params({"symbol": "00700.HK", "period": "annual", "empty": None})
        self.assertEqual(q, {"symbol": "0700.HK", "period": "annual", "apikey": "test_k"})

    def test_format_cik(self):
        self.assertEqual(format_cik(1067983), "0001067983")
        self.assertEqual(format_cik("320193"), "0000320193")

    def test_doc_url(self):
        self.assertEqual(
            doc_url("income-statement"),
            "https://fmpquote.com/apis/income-statement/",
        )

    def test_fmp_api_error(self):
        err = FMPAPIError(403, "Demo key only supports sample tickers", endpoint="quote")
        self.assertEqual(err.status_code, 403)
        self.assertEqual(err.endpoint, "quote")
        self.assertIn("[HTTP 403]", str(err))


if __name__ == "__main__":
    unittest.main()
