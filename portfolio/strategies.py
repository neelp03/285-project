"""Map each investment strategy to a set of stocks and ETFs.

Each holding has a weight. The weights in one strategy add up to 1.0.
"""

STRATEGIES = {
    "ethical": {
        "name": "Ethical Investing",
        "description": (
            "Buy companies with good environmental, social and governance "
            "(ESG) records. Add an ESG index ETF for spread."
        ),
        "holdings": [
            {"symbol": "AAPL", "name": "Apple Inc.", "type": "Stock", "weight": 0.25},
            {"symbol": "ADBE", "name": "Adobe Inc.", "type": "Stock", "weight": 0.25},
            {"symbol": "NSRGY", "name": "Nestle S.A. (ADR)", "type": "Stock", "weight": 0.25},
            {"symbol": "ESGU", "name": "iShares ESG Aware MSCI USA ETF", "type": "ETF", "weight": 0.25},
        ],
    },
    "growth": {
        "name": "Growth Investing",
        "description": (
            "Buy companies with fast revenue and earnings growth. "
            "These companies usually put profits back into the business."
        ),
        "holdings": [
            {"symbol": "NVDA", "name": "NVIDIA Corp.", "type": "Stock", "weight": 0.25},
            {"symbol": "MSFT", "name": "Microsoft Corp.", "type": "Stock", "weight": 0.25},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "Stock", "weight": 0.25},
            {"symbol": "VUG", "name": "Vanguard Growth ETF", "type": "ETF", "weight": 0.25},
        ],
    },
    "index": {
        "name": "Index Investing",
        "description": (
            "Buy low-cost funds that follow the full market. "
            "Mix US stocks, international stocks and bonds."
        ),
        "holdings": [
            {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF", "type": "ETF", "weight": 0.50},
            {"symbol": "IXUS", "name": "iShares Core MSCI Total Intl Stock ETF", "type": "ETF", "weight": 0.30},
            {"symbol": "ILTB", "name": "iShares Core 10+ Year USD Bond ETF", "type": "ETF", "weight": 0.20},
        ],
    },
    "quality": {
        "name": "Quality Investing",
        "description": (
            "Buy companies with high return on equity, stable earnings "
            "and low debt."
        ),
        "holdings": [
            {"symbol": "JNJ", "name": "Johnson & Johnson", "type": "Stock", "weight": 0.25},
            {"symbol": "V", "name": "Visa Inc.", "type": "Stock", "weight": 0.25},
            {"symbol": "COST", "name": "Costco Wholesale Corp.", "type": "Stock", "weight": 0.25},
            {"symbol": "QUAL", "name": "iShares MSCI USA Quality Factor ETF", "type": "ETF", "weight": 0.25},
        ],
    },
    "value": {
        "name": "Value Investing",
        "description": (
            "Buy companies that trade below their real (intrinsic) value. "
            "Look for a low price-to-earnings or price-to-book ratio."
        ),
        "holdings": [
            {"symbol": "BRK-B", "name": "Berkshire Hathaway Inc. (Class B)", "type": "Stock", "weight": 0.25},
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "type": "Stock", "weight": 0.25},
            {"symbol": "PG", "name": "Procter & Gamble Co.", "type": "Stock", "weight": 0.25},
            {"symbol": "VTV", "name": "Vanguard Value ETF", "type": "ETF", "weight": 0.25},
        ],
    },
}


def get_strategy(key):
    """Return the strategy for the key. Raise KeyError if the key is not known."""
    return STRATEGIES[key]


def all_symbols():
    """Return a sorted list of all symbols in all strategies."""
    symbols = set()
    for strategy in STRATEGIES.values():
        for holding in strategy["holdings"]:
            symbols.add(holding["symbol"])
    return sorted(symbols)
