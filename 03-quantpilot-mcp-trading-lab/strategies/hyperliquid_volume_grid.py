"""
QuantScript v2 Strategy: Tight RSI + EMA Mean Reversion for Hyperliquid Perps
Designed for consistent liquidity turnover and strict risk controls in QuantPilot Volume Arena.
"""

STRATEGY_CONFIG = {
    "name": "Hyperliquid_MeanReversion_Volume_v1",
    "exchange": "hyperliquid",
    "market_type": "perpetual",
    "symbol": "ETH-USD",
    "timeframe": "1m",
    "leverage": 3,
    "position_size_pct": 0.25,
    "stop_loss_pct": 0.004,     # 0.40% hard stop-loss
    "take_profit_pct": 0.0035,  # 0.35% quick scalp target
}

def on_candle(ctx):
    close = ctx.close
    ema_slow = ctx.ema(close, period=21)
    rsi = ctx.rsi(close, period=14)

    if ctx.has_position:
        return

    if close > ema_slow and rsi < 32:
        ctx.buy(
            size_pct=STRATEGY_CONFIG["position_size_pct"],
            stop_loss=close * (1 - STRATEGY_CONFIG["stop_loss_pct"]),
            take_profit=close * (1 + STRATEGY_CONFIG["take_profit_pct"]),
        )
    elif close < ema_slow and rsi > 68:
        ctx.sell(
            size_pct=STRATEGY_CONFIG["position_size_pct"],
            stop_loss=close * (1 + STRATEGY_CONFIG["stop_loss_pct"]),
            take_profit=close * (1 - STRATEGY_CONFIG["take_profit_pct"]),
        )
