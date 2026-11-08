"""Portfolio suggestion engine.

The engine does these steps:
1. Make sure that the input is correct.
2. Divide the money between the selected strategies.
3. Divide the money of each strategy between its stocks and ETFs.
4. Buy fractional shares at the live price.
5. Calculate the current value and the value for the last 5 trading days.
"""

import math

from .market import HISTORY_DAYS, now_utc
from .strategies import STRATEGIES

MIN_AMOUNT = 5000.0
MAX_STRATEGIES = 2
SHARE_DECIMALS = 4
MIN_SPLIT = 10
MAX_SPLIT = 90


class InputError(ValueError):
    """The user input is not correct."""


def validate(amount, strategy_keys, split=None):
    """Check the user input. Return (amount, strategy_keys, split_percent).

    split is the percent of money for the first strategy. Use it only when
    there are two strategies.
    """
    try:
        amount = float(str(amount).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        raise InputError("Type a number for the amount.")
    if not math.isfinite(amount):
        raise InputError("Type a number for the amount.")
    if amount < MIN_AMOUNT:
        raise InputError(f"The minimum amount is ${MIN_AMOUNT:,.0f} USD.")

    keys = []
    for key in strategy_keys:
        if key not in keys:
            keys.append(key)
    if not keys:
        raise InputError("Select one or two investment strategies.")
    if len(keys) > MAX_STRATEGIES:
        raise InputError("Select no more than two investment strategies.")
    for key in keys:
        if key not in STRATEGIES:
            raise InputError(f"The strategy '{key}' is not known.")

    if len(keys) == 1:
        split = 100
    else:
        if split in (None, ""):
            split = 50
        try:
            split = int(float(split))
        except (TypeError, ValueError):
            raise InputError("The split must be a number.")
        if not MIN_SPLIT <= split <= MAX_SPLIT:
            raise InputError(
                f"The split must be between {MIN_SPLIT}% and {MAX_SPLIT}%."
            )
    return amount, keys, split


def floor_to(value, decimals):
    factor = 10 ** decimals
    return math.floor(value * factor + 1e-9) / factor


def build_portfolio(amount, strategy_keys, split, market):
    """Make the suggested portfolio. Return a dict that can go into JSON."""
    amount, keys, split = validate(amount, strategy_keys, split)

    strategy_share = {keys[0]: split / 100.0}
    if len(keys) == 2:
        strategy_share[keys[1]] = (100 - split) / 100.0

    # Collect the planned dollars for each symbol. A symbol can be in two strategies.
    plan = {}
    for key in keys:
        strategy = STRATEGIES[key]
        strategy_amount = amount * strategy_share[key]
        for holding in strategy["holdings"]:
            item = plan.setdefault(
                holding["symbol"],
                {
                    "symbol": holding["symbol"],
                    "name": holding["name"],
                    "type": holding["type"],
                    "strategies": [],
                    "target": 0.0,
                },
            )
            item["strategies"].append(strategy["name"])
            item["target"] += strategy_amount * holding["weight"]

    prices = market.live_prices(list(plan))

    holdings = []
    invested = 0.0
    for symbol, item in plan.items():
        price = prices[symbol]
        shares = floor_to(item["target"] / price, SHARE_DECIMALS)
        cost = round(shares * price, 2)
        invested += cost
        holdings.append(
            {
                **item,
                "target": round(item["target"], 2),
                "price": round(price, 4),
                "shares": shares,
                "cost": cost,
                "percent": round(item["target"] / amount * 100, 2),
            }
        )

    cash = round(amount - invested, 2)
    return {
        "amount": round(amount, 2),
        "strategies": [
            {
                "key": k,
                "name": STRATEGIES[k]["name"],
                "description": STRATEGIES[k]["description"],
                "percent": round(strategy_share[k] * 100),
                "amount": round(amount * strategy_share[k], 2),
            }
            for k in keys
        ],
        "holdings": holdings,
        "invested": round(invested, 2),
        "cash": cash,
        "created": now_utc().isoformat(timespec="seconds"),
        "source": market.source,
    }


def current_value(portfolio, market):
    """Return the live value of each holding and of the full portfolio."""
    symbols = [h["symbol"] for h in portfolio["holdings"]]
    prices = market.live_prices(symbols)
    rows = []
    total = portfolio["cash"]
    for h in portfolio["holdings"]:
        price = prices[h["symbol"]]
        value = h["shares"] * price
        total += value
        rows.append(
            {
                "symbol": h["symbol"],
                "price": round(price, 4),
                "value": round(value, 2),
                "change": round(value - h["cost"], 2),
            }
        )
    total = round(total, 2)
    return {
        "time": now_utc().isoformat(timespec="seconds"),
        "holdings": rows,
        "total": total,
        "change": round(total - portfolio["amount"], 2),
        "change_percent": round((total - portfolio["amount"]) / portfolio["amount"] * 100, 2),
        "source": market.source,
    }


def weekly_history(portfolio, market, days=HISTORY_DAYS):
    """Return the portfolio value at the close of each of the last `days` trading days.

    The calculation uses the current number of shares for each day.
    """
    symbols = [h["symbol"] for h in portfolio["holdings"]]
    dates, closes = market.daily_closes(symbols, days)
    values = []
    for i in range(len(dates)):
        total = portfolio["cash"]
        for h in portfolio["holdings"]:
            total += h["shares"] * closes[h["symbol"]][i]
        values.append(round(total, 2))
    return {"dates": dates, "values": values}
