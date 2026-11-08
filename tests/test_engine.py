"""Unit tests for the engine and the web application.

The tests use OfflineMarket. They do not need the internet.
Run: python -m pytest -q
"""

import pytest

from app import create_app
from portfolio.engine import (
    InputError,
    build_portfolio,
    current_value,
    validate,
    weekly_history,
)
from portfolio.market import SAMPLE_PRICES, OfflineMarket
from portfolio.strategies import STRATEGIES, all_symbols


@pytest.fixture
def market():
    return OfflineMarket()


@pytest.fixture
def client(market):
    app = create_app(market)
    app.config["TESTING"] = True
    return app.test_client()


def test_each_strategy_has_three_or_more_holdings():
    assert len(STRATEGIES) == 5
    for strategy in STRATEGIES.values():
        assert len(strategy["holdings"]) >= 3


def test_weights_add_up_to_one():
    for strategy in STRATEGIES.values():
        assert sum(h["weight"] for h in strategy["holdings"]) == pytest.approx(1.0)


def test_sample_prices_cover_all_symbols():
    assert set(all_symbols()) <= set(SAMPLE_PRICES)


@pytest.mark.parametrize("amount", ["4999.99", "0", "-10", "abc", "", "nan"])
def test_bad_amount_is_rejected(amount):
    with pytest.raises(InputError):
        validate(amount, ["index"])


def test_minimum_amount_is_accepted():
    assert validate("5000", ["index"])[0] == 5000.0
    assert validate("$5,000", ["index"])[0] == 5000.0


def test_strategy_count_rules():
    with pytest.raises(InputError):
        validate(5000, [])
    with pytest.raises(InputError):
        validate(5000, ["index", "growth", "value"])
    with pytest.raises(InputError):
        validate(5000, ["crypto"])
    assert validate(5000, ["index", "index"])[1] == ["index"]


def test_split_rules():
    assert validate(5000, ["index"], 30)[2] == 100
    assert validate(5000, ["index", "value"], None)[2] == 50
    with pytest.raises(InputError):
        validate(5000, ["index", "value"], 95)


def test_single_strategy_allocation(market):
    p = build_portfolio(10000, ["index"], None, market)
    targets = {h["symbol"]: h["target"] for h in p["holdings"]}
    assert targets == {"VTI": 5000.0, "IXUS": 3000.0, "ILTB": 2000.0}
    assert p["invested"] + p["cash"] == pytest.approx(10000, abs=0.01)
    assert 0 <= p["cash"] < 1


def test_two_strategy_split(market):
    p = build_portfolio(20000, ["ethical", "growth"], 70, market)
    by_strategy = {s["key"]: s["amount"] for s in p["strategies"]}
    assert by_strategy == {"ethical": 14000.0, "growth": 6000.0}
    assert len(p["holdings"]) == 8
    aapl = next(h for h in p["holdings"] if h["symbol"] == "AAPL")
    assert aapl["target"] == 3500.0


def test_shares_never_cost_more_than_target(market):
    p = build_portfolio(7777.77, ["quality", "value"], 40, market)
    for h in p["holdings"]:
        assert h["shares"] * h["price"] <= h["target"] + 0.005


def test_current_value_and_history(market):
    p = build_portfolio(10000, ["index"], None, market)
    value = current_value(p, market)
    assert value["total"] == pytest.approx(10000, abs=0.05)
    history = weekly_history(p, market)
    assert len(history["dates"]) == 5
    assert len(history["values"]) == 5
    assert history["values"][-1] == pytest.approx(value["total"], abs=0.05)


def test_web_flow(client):
    assert client.get("/").status_code == 200
    r = client.post("/suggest", data={"amount": "10000", "strategies": ["index"]})
    assert r.status_code == 302
    page = client.get("/portfolio")
    assert page.status_code == 200
    assert b"VTI" in page.data and b"Weekly trend" in page.data
    csv_text = client.get("/portfolio.csv").data.decode()
    assert csv_text.splitlines()[0].startswith("Symbol,Name")


def test_web_rejects_small_amount(client):
    r = client.post(
        "/suggest", data={"amount": "100", "strategies": ["index"]}, follow_redirects=True
    )
    assert b"The minimum amount is $5,000 USD." in r.data


def test_api(client):
    assert client.get("/api/value").status_code == 404
    r = client.post("/api/suggest", json={"amount": 5000, "strategies": ["a", "b", "c"]})
    assert r.status_code == 400
    r = client.post("/api/suggest", json={"amount": 5000, "strategies": ["value"]})
    assert r.status_code == 200
    assert client.get("/api/value").json["total"] > 0
    assert len(client.get("/api/history").json["values"]) == 5
