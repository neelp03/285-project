"""Stock Portfolio Suggestion Engine - Flask web application.

Start the application:
    python app.py
Then open http://127.0.0.1:8000 in a web browser.
"""

import csv
import io
import os

from flask import (
    Flask,
    Response,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from portfolio.engine import (
    MAX_SPLIT,
    MIN_AMOUNT,
    MIN_SPLIT,
    InputError,
    build_portfolio,
    current_value,
    weekly_history,
)
from portfolio.market import MarketDataError, default_market
from portfolio.strategies import STRATEGIES

REFRESH_SECONDS = 15


def create_app(market=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cmpe285-dev-key")
    app.config["MARKET"] = market or default_market()

    def get_market():
        return app.config["MARKET"]

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            strategies=STRATEGIES,
            min_amount=MIN_AMOUNT,
            min_split=MIN_SPLIT,
            max_split=MAX_SPLIT,
            form=session.get("last_form", {}),
            has_portfolio="portfolio" in session,
        )

    @app.post("/suggest")
    def suggest():
        form = {
            "amount": request.form.get("amount", ""),
            "strategies": request.form.getlist("strategies"),
            "split": request.form.get("split", "50"),
        }
        session["last_form"] = form
        try:
            portfolio = build_portfolio(
                form["amount"], form["strategies"], form["split"], get_market()
            )
        except InputError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))
        except MarketDataError as exc:
            flash(f"Market data is not available now. {exc}", "error")
            return redirect(url_for("index"))
        session["portfolio"] = portfolio
        return redirect(url_for("show_portfolio"))

    @app.get("/portfolio")
    def show_portfolio():
        portfolio = session.get("portfolio")
        if not portfolio:
            flash("Make a portfolio first.", "error")
            return redirect(url_for("index"))
        try:
            value = current_value(portfolio, get_market())
            history = weekly_history(portfolio, get_market())
        except MarketDataError as exc:
            flash(f"Market data is not available now. {exc}", "error")
            return redirect(url_for("index"))
        return render_template(
            "portfolio.html",
            p=portfolio,
            value=value,
            history=history,
            refresh_seconds=REFRESH_SECONDS,
        )

    @app.get("/portfolio.csv")
    def download_csv():
        portfolio = session.get("portfolio")
        if not portfolio:
            return redirect(url_for("index"))
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(
            ["Symbol", "Name", "Type", "Strategy", "Percent", "Dollars",
             "Buy Price", "Shares", "Cost"]
        )
        for h in portfolio["holdings"]:
            writer.writerow(
                [h["symbol"], h["name"], h["type"], " + ".join(h["strategies"]),
                 h["percent"], h["target"], h["price"], h["shares"], h["cost"]]
            )
        writer.writerow(["CASH", "Money not used", "", "", "", portfolio["cash"], "", "", ""])
        return Response(
            out.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=portfolio.csv"},
        )

    @app.post("/reset")
    def reset():
        session.pop("portfolio", None)
        session.pop("last_form", None)
        return redirect(url_for("index"))

    # ---- JSON API ----

    @app.post("/api/suggest")
    def api_suggest():
        data = request.get_json(silent=True) or {}
        try:
            portfolio = build_portfolio(
                data.get("amount"), data.get("strategies") or [], data.get("split"),
                get_market(),
            )
        except InputError as exc:
            return jsonify(error=str(exc)), 400
        except MarketDataError as exc:
            return jsonify(error=str(exc)), 503
        session["portfolio"] = portfolio
        return jsonify(portfolio)

    @app.get("/api/value")
    def api_value():
        portfolio = session.get("portfolio")
        if not portfolio:
            return jsonify(error="No portfolio. Make a portfolio first."), 404
        try:
            return jsonify(current_value(portfolio, get_market()))
        except MarketDataError as exc:
            return jsonify(error=str(exc)), 503

    @app.get("/api/history")
    def api_history():
        portfolio = session.get("portfolio")
        if not portfolio:
            return jsonify(error="No portfolio. Make a portfolio first."), 404
        try:
            return jsonify(weekly_history(portfolio, get_market()))
        except MarketDataError as exc:
            return jsonify(error=str(exc)), 503

    @app.get("/api/strategies")
    def api_strategies():
        return jsonify(STRATEGIES)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="127.0.0.1", port=port, debug=False)
