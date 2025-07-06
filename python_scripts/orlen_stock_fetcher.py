import yfinance as yf
import sys
from datetime import datetime

def fetch_orlen_stock_data():
    """Fetch Orlen stock data using yfinance"""
    try:
        # PKN Orlen ticker on Warsaw Stock Exchange
        ticker = "PKN.WA"
        stock = yf.Ticker(ticker)
        
        # Get current data
        info = stock.info
        hist = stock.history(period="2d")
        
        if hist.empty:
            raise Exception('No historical data available for Orlen stock')
        
        # Get latest data
        latest_data = hist.iloc[-1]
        previous_data = hist.iloc[-2] if len(hist) > 1 else latest_data
        
        current_price = latest_data['Close']
        previous_close = previous_data['Close']
        change = current_price - previous_close
        change_percent = (change / previous_close * 100) if previous_close != 0 else 0
        
        result = {
            'symbol': 'PKN.WA',
            'company': 'PKN Orlen',
            'last_price': round(current_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': int(latest_data['Volume']),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        raise Exception(f'Error fetching Orlen stock data: {str(e)}')

def main():
    """Main function for local execution"""
    try:
        stock_data = fetch_orlen_stock_data()
        
        print("=== PKN Orlen Stock Data ===")
        print(f"Last Price: {stock_data['last_price']} PLN")
        print(f"Change: {stock_data['change']} PLN ({stock_data['change_percent']:+.2f}%)")
        print(f"Volume: {stock_data['volume']:,}")
        print(f"Timestamp: {stock_data['timestamp']}")
        
        return stock_data
        
    except Exception as e:
        print(f"Failed to fetch stock data: {str(e)}", file=sys.stderr)
        sys.exit(1)

def n8n_execute():
    """Function for n8n execution"""
    try:
        stock_data = fetch_orlen_stock_data()
        return [{"json": stock_data}]
    except Exception as e:
        raise Exception(f"Orlen stock fetch failed: {str(e)}")

if __name__ == "__main__":
    main()
