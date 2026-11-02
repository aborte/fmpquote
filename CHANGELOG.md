# Changelog

All notable changes to `fmpquote` will be documented in this file.

## [0.2.2] - 2026-11-02

### Changed
- 将 `requires-python` 版本要求统一收窄为 `>=3.10`（与 Python 3.10–3.12 矩阵测试保持一致）。
- 统一源码、标签与发布包版本号为 `0.2.2`。

## [0.2.1] - 2026-11-02

### Changed
- 精简快速上手示例脚本 `examples/quickstart.py` 与文档注释说明。
- 更新包元信息与作者署名。

## [0.2.0] - 2026-11-02

### Added
- 新增 `normalize_hk_symbol()` 辅助函数与 `FMPClient.build_query_params()` 方法，支持港股 5 位代码（如 `00700.HK`）自动归一化为上游标准 4 位代码（`0700.HK`）。
- 新增离线单元测试套件 `tests/test_client.py` 与 GitHub Actions 多版本矩阵 CI 流水线（Python 3.10–3.12）。
- 新增独立接口路径速查目录 `docs/API_CATALOG.md`。

### Changed
- 完善 `README.md` 快速上手示例与接口参数说明。
- 将 `pyproject.toml` 中的成熟度分类调整为 `Development Status :: 4 - Beta`。

## [0.1.0] - 2026-11-02

### Added
- 初始版本发布：支持零第三方依赖调用 `/stable/` 全系接口（`quote`、`income_statement`、`balance_sheet`、`cash_flow`、`ratios_ttm`、`key_metrics_ttm`、`dcf`、`eod_chart`、`earnings_transcript`、`treasury_rates`）。
