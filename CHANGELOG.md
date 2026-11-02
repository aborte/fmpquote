# Changelog

All notable changes to `fmpquote` will be documented in this file.

## [0.2.0] - 2026-11-02

### Added
- 新增 `normalize_hk_symbol()` 辅助函数与 `FMPClient.build_query_params()` 方法，支持港股 5 位代码（如 `00700.HK`）自动归一化为上游标准 4 位代码（`0700.HK`）。
- 新增离线单元测试套件 `tests/test_client.py` 与 GitHub Actions 多版本矩阵 CI 流水线（Python 3.9–3.12）。
- 新增独立接口路径速查目录 `docs/API_CATALOG.md`，大幅精简主 `README.md` 篇幅。

### Changed
- 统一标题为《FMP Ultimate API 中文接口文档（附开箱即用 SDK）》，优化 GitHub / Gitee / PyPI 三端文档结构分工。
- 将 `pyproject.toml` 中的成熟度分类调整为 `Development Status :: 4 - Beta`。

## [0.1.0] - 2026-11-02

### Added
- 初始版本发布：支持零第三方依赖调用 `/stable/` 全系接口（`quote`、`income_statement`、`balance_sheet`、`cash_flow`、`ratios_ttm`、`key_metrics_ttm`、`dcf`、`eod_chart`、`earnings_transcript`、`treasury_rates`）。
- 内置公用 FMP Ultimate 体验 Key 与备用 Key 手动切换说明。
