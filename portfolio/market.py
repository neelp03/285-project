"""Get market prices for stocks and ETFs.

LiveMarket gets data from Yahoo Finance through the yfinance package.
OfflineMarket gives fixed sample data. Use it when no internet is available.
"""

import logging
import math
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone

log = logging.getLogger(__name__)

HISTORY_DAYS = 5


class MarketDataError(Exception):
    """The market data source did not give a usable price."""


class LiveMarket:
    """Market data from Yahoo Finance."""

    source = "Yahoo Finance (live)"

    def live_prices(self, symbols):
        """Return {symbol: last price} for each symbol."""
        with ThreadPoolExecutor(max_workers=8) as pool:
            prices = dict(zip(symbols, pool.map(self._last_price, symbols)))
        return prices

    def _last_price(self, symbol):
        import yfinance as yf

        try:
            price = yf.Ticker(symbol).fast_info["last_price"]
        except Exception as exc:  # yfinance raises many error types
            raise MarketDataError(f"Cannot get price for {symbol}: {exc}") from exc
        if price is None or not math.isfinite(price) or price <= 0:
            raise MarketDataError(f"Cannot get price for {symbol}")
        return float(price)

    def daily_closes(self, symbols, days=HISTORY_DAYS):
        """Return (dates, {symbol: [close, ...]}) for the last `days` trading days."""
        import yfinance as yf

        try:
            frame = yf.download(
                list(symbols),
                period="1mo",
                interval="1d",
                progress=False,
                auto_adjust=False,
                group_by="column",
            )
        except Exception as exc:
            raise MarketDataError(f"Cannot get price history: {exc}") from exc
        if frame is None or frame.empty:
            raise MarketDataError("Price history is empty")

        closes = frame["Close"]
        if not hasattr(closes, "columns"):  # one symbol gives a Series
            closes = closes.to_frame(name=symbols[0])
        closes = closes.reindex(columns=list(symbols)).ffill().dropna()
        closes = closes.tail(days)
        if closes.empty:
            raise MarketDataError("Price history is empty")

        dates = [d.strftime("%Y-%m-%d") for d in closes.index]
        return dates, {s: [float(v) for v in closes[s]] for s in symbols}


# Sample prices for offline mode. The values are close to market prices in 2026.
SAMPLE_PRICES = {
    "AAPL": 342.37, "ADBE": 405.10, "NSRGY": 104.30, "ESGU": 148.20,
    "NVDA": 212.45, "MSFT": 512.80, "AMZN": 245.60, "VUG": 470.15,
    "VTI": 361.93, "IXUS": 82.40, "ILTB": 49.85,
    "JNJ": 188.70, "V": 352.25, "COST": 935.40, "QUAL": 196.30,
    "BRK-B": 570.89, "JPM": 305.15, "PG": 152.60, "VTV": 190.75,
}


class OfflineMarket:
    """Fixed sample data. The data does not come from the internet."""

    source = "Offline sample data (not live)"

    def live_prices(self, symbols):
        prices = {}
        for symbol in symbols:
            if symbol not in SAMPLE_PRICES:
                raise MarketDataError(f"No sample price for {symbol}")
            prices[symbol] = SAMPLE_PRICES[symbol]
        return prices

    def daily_closes(self, symbols, days=HISTORY_DAYS):
        dates = _last_weekdays(days)
        # A small fixed pattern of daily moves, so the chart has a trend.
        pattern = [-0.021, -0.008, 0.012, -0.004, 0.0]
        pattern = pattern[-days:]
        closes = {}
        for symbol in symbols:
            base = self.live_prices([symbol])[symbol]
            closes[symbol] = [round(base * (1 + move), 2) for move in pattern]
        return dates, closes


def _last_weekdays(count):
    day = date.today()
    result = []
    while len(result) < count:
        if day.weekday() < 5:
            result.append(day.strftime("%Y-%m-%d"))
        day -= timedelta(days=1)
    return list(reversed(result))


def now_utc():
    return datetime.now(timezone.utc)


def default_market():
    """Return OfflineMarket if PORTFOLIO_OFFLINE=1. Else return LiveMarket."""
    if os.environ.get("PORTFOLIO_OFFLINE", "").strip() == "1":
        return OfflineMarket()
    return LiveMarket()
