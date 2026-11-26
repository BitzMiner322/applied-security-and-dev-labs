#!/usr/bin/env python3
import sys

def estimate_arena_target(collateral_usdc: float, leverage: int, target_volume: float = 10000.0):
    notional_per_side = collateral_usdc * leverage
    round_trip_volume = notional_per_side * 2
    round_trips_needed = target_volume / round_trip_volume
    est_taker_fees = target_volume * 0.00035

    print(f"Collateral:         ${collateral_usdc:,.2f} USDC")
    print(f"Leverage:           {leverage}x")
    print(f"Notional per side:  ${notional_per_side:,.2f} USDC")
    print(f"Round-trip volume:  ${round_trip_volume:,.2f} USDC (open + close)")
    print(f"Round-trips needed: {round_trips_needed:.1f} trades to hit ${target_volume:,.0f} USDC")
    print(f"Est. Taker Fees:    ~${est_taker_fees:,.2f} USDC (use Limit/Maker orders to reduce)")

if __name__ == "__main__":
    cap = float(sys.argv[1]) if len(sys.argv) > 1 else 250.0
    lev = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    estimate_arena_target(cap, lev)
