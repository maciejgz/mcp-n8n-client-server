# Orlen Stock Fetcher

Python script to fetch PKN Orlen stock data using yfinance library.

## Installation

```bash
pip install -r requirements.txt
```

## Local Usage

```bash
python orlen_stock_fetcher.py
```

## n8n Usage

In n8n Code node (Python):
```python
from python_scripts.orlen_stock_fetcher import n8n_execute
return n8n_execute()
```

## Output

- Last closing price (PLN)
- Price change (PLN and percentage)
- Trading volume
- Timestamp
