# CMPE 285 Term Project – Part 1: Stock Portfolio Suggestion Engine

**Group name:** `<GROUP NAME>`

**Group members:**

| Name | Student ID | Email |
|------|------------|-------|
| `<Member 1>` | `<ID>` | `<email>` |
| `<Member 2>` | `<ID>` | `<email>` |
| `<Member 3>` | `<ID>` | `<email>` |

**Email title:** `CMPE285 Term Project Part 1 – <GROUP NAME> – <Member 1>, <Member 2>, <Member 3>`

> **Writing standard:** This document uses ASD-STE100 Simplified Technical English.

---

## 1. Summary

This project is a stock portfolio suggestion engine. The engine is a web application. We wrote it in Python.

The user does these steps:

1. Type an amount in USD. The minimum amount is $5,000.
2. Select one or two investment strategies.

The engine shows these items:

- The stocks and ETFs that it selects for each strategy.
- How it divides the money between the stocks and ETFs.
- The current value of the full portfolio. The value comes from the internet and updates every 15 seconds.
- The weekly trend of the portfolio value. The trend shows the value at the close of the last 5 trading days.

---

## 2. Setup Instructions

### 2.1 Requirements

- Python 3.10 or later. We tested with Python 3.12.
- An internet connection. The engine gets live prices from Yahoo Finance.
- A web browser (Chrome, Firefox, Safari or Edge).

### 2.2 Install the application

1. Unzip the project file.
2. Open a terminal.
3. Go to the project folder:

   ```bash
   cd cmpe285-project
   ```

4. Make a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

5. Start the virtual environment.
   - On macOS or Linux, type:

     ```bash
     source .venv/bin/activate
     ```

   - On Windows, type:

     ```bat
     .venv\Scripts\activate
     ```

6. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

### 2.3 Start the application

1. In the project folder, type:

   ```bash
   python app.py
   ```

2. Make sure that the terminal shows `Running on http://127.0.0.1:8000`.
3. Open a web browser.
4. Go to <http://127.0.0.1:8000>.

> **NOTE:** If port 8000 is not available, start the application on a different port. For example, type `PORT=8080 python app.py` (macOS or Linux) or `set PORT=8080 && python app.py` (Windows). Then go to `http://127.0.0.1:8080`.

> **NOTE:** If the internet is not available, use the offline mode. Type `PORTFOLIO_OFFLINE=1 python app.py` (macOS or Linux) or `set PORTFOLIO_OFFLINE=1 && python app.py` (Windows). The offline mode uses fixed sample prices. The page shows "Offline sample data (not live)" as the source. Use the live mode for all test cases if possible.

### 2.4 Stop the application

1. In the terminal, push **Ctrl + C**.

### 2.5 Run the automatic tests (optional)

1. In the project folder, type:

   ```bash
   python -m pytest -q
   ```

2. Make sure that all tests pass. The tests do not need the internet.

---

## 3. Research

### 3.1 Python APIs and packages

| Package | Version | Use in this project |
|---------|---------|---------------------|
| **yfinance** | 0.2.40 or later | Gets live prices (`Ticker.fast_info["last_price"]`) and daily closing prices (`yf.download`) from Yahoo Finance. It does not need an API key. |
| **Flask** | 3.0 or later | Web server. It shows the HTML pages and gives a JSON API. |
| **pandas** | 2.0 or later | yfinance gives price history as a pandas DataFrame. We use it to select the last 5 trading days. |
| **pytest** | 8.0 or later | Automatic unit tests. |
| **Chart.js** (JavaScript, from CDN) | 4.4 | Draws the allocation chart and the weekly trend chart in the browser. |

We also looked at these data sources:

| Source | Result |
|--------|--------|
| Alpha Vantage | Needs an API key. The free plan allows only 25 requests each day. This is not sufficient for live updates. |
| Finnhub | Needs an API key. Gives real-time US quotes. It is a good backup source. |
| IEX Cloud | The service stopped in 2024. |
| **Yahoo Finance (yfinance)** | **Selected.** It is free and does not need an API key. It has US stocks, ETFs and ADRs (for example, NSRGY). |

### 3.2 Investment methodology

**Diversification.** Do not put all the money in one company. Each strategy in this engine has 3 or 4 holdings. Each strategy except Index Investing has one ETF. The ETF gives a wide spread of companies in the same style.

**Asset allocation.** Divide the money between different asset types (stocks, international stocks and bonds). Bonds usually decrease the risk of the portfolio.

The five strategies:

| Strategy | Methodology | How we select the holdings |
|----------|-------------|----------------------------|
| **Ethical Investing** | Buy companies with good Environmental, Social and Governance (ESG) scores. Do not buy companies that cause damage to people or the environment. | Large companies with high ESG ratings, plus an ESG index ETF. |
| **Growth Investing** | Buy companies with revenue and earnings that increase faster than the market. These companies usually do not pay large dividends. The risk is high. | Large technology companies with fast growth, plus a growth ETF. |
| **Index Investing** | Do not try to select the best companies. Buy low-cost funds that follow the full market. This is a passive strategy. The cost is low. | Total US market, total international market, and a long-term bond fund. This is the example from the project description. |
| **Quality Investing** | Buy companies with a high return on equity, stable earnings, strong cash flow and low debt. | Companies with a strong brand and stable profits, plus a quality-factor ETF. |
| **Value Investing** | Buy companies that trade at a price below their real (intrinsic) value. Look for a low price-to-earnings (P/E) ratio or price-to-book (P/B) ratio. This is the method of Benjamin Graham and Warren Buffett. | Companies with a low P/E ratio and stable dividends, plus a value ETF. |

---

## 4. Design Decisions

### 4.1 User interface

We use a **web interface** (Flask, HTML, CSS and Chart.js). Reasons:

- The user does not need to install a desktop program.
- Charts show the allocation and the weekly trend clearly.
- The page can update the live value without a full reload.
- The page supports light mode and dark mode. The page follows the setting of the computer.

Page layout (we made the design with the SuperDesign tool):

- Both pages have two columns. On a phone, the columns are one above the other.
- **Home page:** The left column has the amount field, the money split slider, the error messages and the **Suggest portfolio** button. The right column has the five strategy cards.
- **Portfolio page:** The top bar has the **Download CSV**, **Change input** and **New portfolio** buttons. The left column has the four key values, the live update status and the selected strategies. The right column has the charts and the tables.

### 4.2 Map from strategy to stocks and ETFs

| Strategy | Holdings (weight) |
|----------|-------------------|
| Ethical Investing | AAPL Apple (25%), ADBE Adobe (25%), NSRGY Nestle (25%), ESGU iShares ESG Aware MSCI USA ETF (25%) |
| Growth Investing | NVDA NVIDIA (25%), MSFT Microsoft (25%), AMZN Amazon (25%), VUG Vanguard Growth ETF (25%) |
| Index Investing | VTI Vanguard Total Stock Market ETF (50%), IXUS iShares Core MSCI Total Intl Stock ETF (30%), ILTB iShares Core 10+ Year USD Bond ETF (20%) |
| Quality Investing | JNJ Johnson & Johnson (25%), V Visa (25%), COST Costco (25%), QUAL iShares MSCI USA Quality Factor ETF (25%) |
| Value Investing | BRK-B Berkshire Hathaway B (25%), JPM JPMorgan Chase (25%), PG Procter & Gamble (25%), VTV Vanguard Value ETF (25%) |

> **NOTE:** The project description shows "APPL" for Apple. The correct symbol is **AAPL**. The engine uses AAPL.

The map is in the file `portfolio/strategies.py`. To change the map, edit this file.

### 4.3 How the engine divides the money

1. **Between strategies.** If the user selects one strategy, the strategy gets 100% of the money. If the user selects two strategies, the user sets the split with a slider. The default split is 50% / 50%. The range is 10% to 90%. The slider moves in steps of 5%.
2. **Between holdings.** Each strategy divides its money by the weights in the table in 4.2. The Index strategy uses a 50 / 30 / 20 split. This is a usual mix of US stocks, international stocks and bonds. The other strategies use equal weights (25% each).
3. **Number of shares.** The engine buys **fractional shares** at the live price. The engine rounds the number of shares down to 4 decimal places. Thus, the cost is never more than the planned amount.
4. **Cash.** The small amount of money that is not used (usually less than $1) shows as "Cash not used". The engine adds this cash to the portfolio value.

Formula for each holding:

```
planned dollars = amount × strategy percent × holding weight
shares          = round_down(planned dollars ÷ live price, 4 decimals)
cost            = shares × live price
```

### 4.4 Current value

- The engine gets the last price of each holding from Yahoo Finance.
- Current value = Σ (shares × live price) + cash.
- The page updates the value automatically every **15 seconds**. The user can also click **Update now**.
- The page shows the time of the last update and the data source.
- The table shows the live price, the live value and the gain or loss of each holding.

> **NOTE:** When the market is closed, the live price does not change. The value then stays the same.

### 4.5 Weekly trend (5-day history)

- The engine gets the daily closing price of each holding for the last **5 trading days**.
- Value for each day = Σ (shares × closing price of that day) + cash.
- The engine uses the current number of shares for all 5 days. The trend thus shows how the selected portfolio changed during the week.
- The page shows the trend as a **line chart** and as a **table**. The table shows the daily change in dollars.

### 4.6 Extra features

1. **Custom split** between two strategies (slider from 10% to 90%).
2. **Automatic live update** of the portfolio value every 15 seconds, without a page reload.
3. **Gain or loss** for each holding and for the full portfolio.
4. **Allocation chart** (doughnut chart) that shows how the money is divided.
5. **CSV download** of the portfolio.
6. **JSON API** (`/api/suggest`, `/api/value`, `/api/history`, `/api/strategies`).
7. **Offline mode** with sample prices for use without the internet.
8. **Input memory.** The form keeps the last input. The user can change one value and try again.
9. **Light and dark mode.**
10. **Automatic unit tests** (19 tests with pytest).

### 4.7 Project files

```
cmpe285-project/
├── app.py                  Flask web application and JSON API
├── portfolio/
│   ├── strategies.py       Map from strategy to stocks and ETFs
│   ├── engine.py           Input checks, money division, value, history
│   └── market.py           Live data (yfinance) and offline sample data
├── templates/              HTML pages
├── static/style.css        Page style
├── tests/test_engine.py    Unit tests
├── requirements.txt        Python packages
└── docs/PART1.md           This document
```

---

## 5. Test Cases

### General instructions

- Do the setup in Section 2 before you start.
- Do the test cases in the given sequence.
- Use live mode (with the internet) unless the test case gives a different instruction.
- Prices change during market hours. Thus, the dollar values on your screen will be different from the examples. Use the formulas to examine the values.
- "Home page" means <http://127.0.0.1:8000>.

---

### TC-01: Start the application and open the home page

**Purpose:** Make sure that the application starts and shows the input form.

**Steps:**

1. Do the steps in Section 2.3.
2. Look at the home page.

**Expected result:**

1. The terminal shows `Running on http://127.0.0.1:8000`. The terminal shows no errors.
2. The page shows the title **Make a portfolio**.
3. The page shows the field **Amount to invest (USD, minimum $5,000)**.
4. The page shows five strategy cards: **Ethical Investing**, **Growth Investing**, **Index Investing**, **Quality Investing** and **Value Investing**.
5. Each card shows 3 or more symbols with their weights. For example, the Index Investing card shows `VTI 50%`, `IXUS 30%` and `ILTB 20%`.
6. The page shows the button **Suggest portfolio** in the left column.

---

### TC-02: Amount less than the minimum

**Purpose:** Make sure that the engine does not accept an amount less than $5,000.

**Steps:**

1. Go to the home page.
2. In the amount field, type `4999`.
3. Select the **Index Investing** card.
4. Click **Suggest portfolio**.
5. In the amount field, type `abc`. Click **Suggest portfolio**.
6. Clear the amount field. Click **Suggest portfolio**.

**Expected result:**

1. After step 4, the page stays on the home page. A red message shows above the **Suggest portfolio** button: **The minimum amount is $5,000 USD.**
2. The form keeps the input (`4999` and Index Investing).
3. After step 5 and step 6, the page shows a red error message. The engine does not make a portfolio.

> **NOTE:** Some browsers do not let you type letters in a number field. If you cannot type `abc`, continue to step 6.

---

### TC-03: No strategy selected

**Purpose:** Make sure that the engine needs one or more strategies.

**Steps:**

1. Go to the home page.
2. In the amount field, type `10000`.
3. Make sure that no strategy card is selected. If a card is selected, click it to clear it.
4. Click **Suggest portfolio**.

**Expected result:**

1. The page stays on the home page.
2. A red message shows: **Select one or two investment strategies.**

---

### TC-04: Not more than two strategies

**Purpose:** Make sure that the user can select only one or two strategies.

**Steps:**

1. Go to the home page.
2. Select **Growth Investing**.
3. Select **Value Investing**.
4. Try to select **Index Investing**.
5. Clear **Value Investing**.
6. (Optional, API test) Open a second terminal. Type this command:

   ```bash
   curl -s -X POST http://127.0.0.1:8000/api/suggest -H "Content-Type: application/json" -d "{\"amount\": 10000, \"strategies\": [\"growth\", \"value\", \"index\"]}"
   ```

**Expected result:**

1. After step 3, the two selected cards have a green border and a check mark. The other three cards become faded. You cannot select them.
2. After step 3, a **Money split** slider shows. The label shows `50% Growth Investing / 50% Value Investing`.
3. In step 4, the Index Investing card does not become selected.
4. After step 5, the three faded cards become available again. The split slider is not shown.
5. In step 6, the server sends this message: `{"error":"Select no more than two investment strategies."}`

---

### TC-05: One strategy – Index Investing with $10,000

**Purpose:** Make sure that the engine selects the correct ETFs and divides the money correctly for one strategy.

**Steps:**

1. Go to the home page.
2. In the amount field, type `10000`.
3. Select **Index Investing** only.
4. Click **Suggest portfolio**.

**Expected result:**

1. The portfolio page opens.
2. **Amount invested** shows `$10,000.00`.
3. **Selected strategies** shows `Index Investing — 100% · $10,000.00`.
4. The table **Suggested stocks and ETFs** shows 3 rows:

   | Symbol | Percent | Dollars (approximately) |
   |--------|---------|-------------------------|
   | VTI | 50.00% | $5,000.00 |
   | IXUS | 30.00% | $3,000.00 |
   | ILTB | 20.00% | $2,000.00 |

5. For each row, **Shares × Buy price = Dollars** (the difference is less than $0.01 for each share).
6. **Cash not used** is less than $1.00.
7. The sum of the Dollars column plus Cash not used is $10,000.00.
8. The doughnut chart shows VTI, IXUS and ILTB (and a very small Cash part).

---

### TC-06: Two strategies with the default 50/50 split – Ethical and Growth with $20,000

**Purpose:** Make sure that the engine divides the money equally between two strategies.

**Steps:**

1. Go to the home page.
2. In the amount field, type `20000`.
3. Select **Ethical Investing**.
4. Select **Growth Investing**.
5. Do not move the **Money split** slider. Make sure that it shows `50% Ethical Investing / 50% Growth Investing`.
6. Click **Suggest portfolio**.

**Expected result:**

1. **Selected strategies** shows two items:
   - `Ethical Investing — 50% · $10,000.00`
   - `Growth Investing — 50% · $10,000.00`
2. The holdings table shows 8 rows: AAPL, ADBE, NSRGY, ESGU (Strategy column: Ethical Investing) and NVDA, MSFT, AMZN, VUG (Strategy column: Growth Investing).
3. Each row shows **12.50%** and approximately **$2,500.00**.
4. The Type column shows **Stock** for AAPL, ADBE, NSRGY, NVDA, MSFT and AMZN. It shows **ETF** for ESGU and VUG.
5. **Cash not used** is less than $1.00.

---

### TC-07: Two strategies with a custom split – Value 70% and Quality 30% with $10,000

**Purpose:** Make sure that the split slider changes the division of money.

**Steps:**

1. Go to the home page.
2. In the amount field, type `10000`.
3. Select **Quality Investing**.
4. Select **Value Investing**.
5. Move the **Money split** slider to the left until the label shows `30% Quality Investing / 70% Value Investing`.
6. Click **Suggest portfolio**.

**Expected result:**

1. **Selected strategies** shows:
   - `Quality Investing — 30% · $3,000.00`
   - `Value Investing — 70% · $7,000.00`
2. The holdings table shows 8 rows:

   | Symbols | Percent | Dollars (approximately) |
   |---------|---------|-------------------------|
   | JNJ, V, COST, QUAL | 7.50% each | $750.00 each |
   | BRK-B, JPM, PG, VTV | 17.50% each | $1,750.00 each |

3. Cash not used is less than $1.00.

> **NOTE:** The first strategy is always the strategy that is higher in the list on the home page. The slider sets the percent of the first strategy.

---

### TC-08: Current value from the internet and automatic update

**Purpose:** Make sure that the page shows the live value of the portfolio and updates it.

**Preconditions:** Do TC-07 first. The portfolio page is open. The internet is available.

**Steps:**

1. In the left column, find the line under the four values (Amount invested, Current value, Gain / loss and Cash not used). It starts with **Last update**.
2. Read the time of the last update and the source.
3. Wait 15 seconds. Do not reload the page.
4. Read the time of the last update again.
5. Click **Update now**.
6. Open <https://finance.yahoo.com/quote/VTV> in a different browser tab. Compare the price with the **Live price** of VTV in the table.
7. For one row, multiply **Shares** by **Live price**. Compare the result with **Live value**.

**Expected result:**

1. The source shows **Yahoo Finance (live)**.
2. After step 3, the time changes to a new time. The time changes approximately every 15 seconds.
3. After step 5, the time changes immediately.
4. The green dot shows that the last update was successful. The dot becomes red if the update fails.
5. In step 6, the two prices are the same or almost the same (Yahoo Finance updates its page at a different time).
6. In step 7, Shares × Live price = Live value.
7. **Current value** = sum of the Live value column + Cash not used.
8. **Gain / loss** = Current value − Amount invested. The color is green for a gain and red for a loss.

> **NOTE:** When the US market is closed (weekends, holidays, and outside 9:30 AM to 4:00 PM Eastern Time), the prices do not change. The time of the last update still changes.

---

### TC-09: Weekly trend of the portfolio value

**Purpose:** Make sure that the page shows the portfolio value for the last 5 trading days.

**Preconditions:** A portfolio page is open (for example, from TC-05).

**Steps:**

1. Find the box **Weekly trend (last 5 trading days)**.
2. Look at the line chart.
3. Put the mouse pointer on a point of the line chart.
4. Find the table with the column **Date (close)**. It is at the bottom of the right column.
5. (Optional, API test) Type this URL in the same browser: <http://127.0.0.1:8000/api/history>

**Expected result:**

1. The line chart shows 5 points. Each point has a date on the horizontal axis.
2. The dates are the last 5 trading days. The dates do not include Saturday, Sunday or market holidays.
3. In step 3, a label shows the portfolio value in dollars for that day.
4. The table shows 5 rows with **Date (close)**, **Portfolio value** and **Daily change**.
5. The first row shows `—` for Daily change. Each other row shows the difference from the day before. A positive change is green. A negative change is red.
6. The values in the table and in the chart are the same.
7. In step 5, the browser shows JSON with 5 `dates` and 5 `values`.

---

### TC-10: CSV download, change input and new portfolio

**Purpose:** Make sure that the user can save the portfolio and make a new portfolio.

**Preconditions:** A portfolio page is open (for example, from TC-06).

**Steps:**

1. In the top bar, click **Download CSV**.
2. Open the file `portfolio.csv` in a spreadsheet program or a text editor.
3. Go back to the portfolio page. In the top bar, click **Change input**.
4. Look at the form.
5. Change the amount to `5000`. Click **Suggest portfolio**.
6. In the top bar, click **New portfolio**.

**Expected result:**

1. In step 1, the browser saves the file `portfolio.csv`.
2. The file has the columns Symbol, Name, Type, Strategy, Percent, Dollars, Buy Price, Shares and Cost. It has one row for each holding and one **CASH** row.
3. The values in the file are the same as the values in the table on the portfolio page.
4. After step 3, the home page shows the last input. The amount, the strategies and the split are the same as before. The top bar shows the button **View last portfolio**.
5. After step 5, the engine accepts $5,000 (the minimum). The portfolio page shows **Amount invested** `$5,000.00`.
6. After step 6, the home page shows an empty form. The button **View last portfolio** is not shown.

---

## 6. Known Limits

- Yahoo Finance is not an official API. Sometimes the service is slow or does not answer. If this occurs, the page shows the message "Market data is not available now". Wait a short time and try again. Or use the offline mode (Section 2.3).
- The engine does not include trade fees or taxes.
- This project is for education only. It is not financial advice.
