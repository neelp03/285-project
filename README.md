# Stock Portfolio Suggestion Engine

CMPE 285 term project. A Python web application that suggests a stock and ETF portfolio.

> This document uses ASD-STE100 Simplified Technical English.

## What the application does

1. The user types an amount in USD. The minimum amount is $5,000.
2. The user selects one or two investment strategies: Ethical, Growth, Index, Quality or Value.
3. The engine shows:
   - The stocks and ETFs for each strategy.
   - How it divides the money.
   - The live value of the portfolio. The value updates every 15 seconds.
   - The portfolio value for the last 5 trading days, as a chart and a table.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:8000> in a web browser.

- To use a different port, type `PORT=8080 python app.py`.
- To use the application without the internet, type `PORTFOLIO_OFFLINE=1 python app.py`. This mode uses fixed sample prices.

## Deploy on Render

The file `render.yaml` sets up the application as a Render web service.

1. Push the repository to GitHub.
2. In the Render dashboard, select **New > Blueprint**.
3. Connect the GitHub repository. Render reads `render.yaml`.
4. Select **Apply**.

Render installs the packages, makes a random `SECRET_KEY` and starts the application with Gunicorn.

## Run the tests

```bash
python -m pytest -q
```

The tests do not need the internet.

## Documents

- [docs/PART1.md](docs/PART1.md) – Part 1 deliverable: research, design decisions, setup and the ten test cases.

## Make the zip file for submission

```bash
git archive --format=zip -o ../cmpe285-project.zip --prefix=cmpe285-project/ HEAD
```
