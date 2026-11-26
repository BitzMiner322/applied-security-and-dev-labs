# 03 - QuantPilot MCP & QuantScript Trading Lab

An algorithmic trading and AI-agent lab demonstrating **QuantScript v2** strategy development, **QuantPilot MCP** integration, and risk-controlled perpetual liquidity turnover on **Hyperliquid**.

## Directory Structure
* `mcp/mcp.json` — Model Context Protocol (MCP) configuration for connecting Claude Code, Cursor, or Codex to QuantPilot's strategy validator and backtester.
* `strategies/hyperliquid_volume_grid.py` — Mean-reversion scalping strategy (`ETH-USD`, `1m`) with hard stop-loss and take-profit parameters.
* `scripts/volume_estimator.py` — CLI calculator to size positions and estimate fees for clearing the **10,000 USDC** QuantPilot Volume Arena threshold.

## Quickstart
```bash
# Calculate trades required to clear 10,000 USDC cumulative volume (\$250 USDC at 4x leverage)
python3 scripts/volume_estimator.py 250 4
```

## Disclaimer
For educational and research purposes only. Perpetual futures trading carries substantial risk.
