"""
Stock Data Module - Foundation layer for reliable financial data
Uses yfinance to fetch current prices, financials, and key metrics
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataProvider:
    """Provides reliable stock data using Yahoo Finance API"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get comprehensive stock data for a given ticker
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dict containing stock information
        """
        try:
            # Clean ticker
            ticker = ticker.upper().strip()
            
            # Check cache first
            if ticker in self.cache:
                return self.cache[ticker]
            
            logger.info(f"Fetching data for {ticker}")
            
            # Get stock info
            stock = yf.Ticker(ticker)
            
            # Get current price and basic info
            info = stock.info
            
            # Get financial data
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow
            
            # Get recent price history
            hist = stock.history(period="1mo")
            
            # Calculate additional metrics
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[-2] if len(hist) > 1 else 0
            price_change_pct = (price_change / hist['Close'].iloc[-2] * 100) if len(hist) > 1 and hist['Close'].iloc[-2] != 0 else 0
            
            # Compile comprehensive data
            stock_data = {
                'ticker': ticker,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'current_price': current_price,
                'price_change': price_change,
                'price_change_pct': price_change_pct,
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'forward_pe': info.get('forwardPE', 'N/A'),
                'price_to_book': info.get('priceToBook', 'N/A'),
                'debt_to_equity': info.get('debtToEquity', 'N/A'),
                'return_on_equity': info.get('returnOnEquity', 'N/A'),
                'profit_margins': info.get('profitMargins', 'N/A'),
                'revenue_growth': info.get('revenueGrowth', 'N/A'),
                'earnings_growth': info.get('earningsGrowth', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'beta': info.get('beta', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'avg_volume': info.get('averageVolume', 'N/A'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
                'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Cache the result
            self.cache[ticker] = stock_data
            
            logger.info(f"Successfully fetched data for {ticker}")
            return stock_data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return {
                'ticker': ticker,
                'error': f"Failed to fetch data: {str(e)}",
                'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def get_multiple_stocks(self, tickers: list) -> Dict[str, Dict]:
        """Get data for multiple stocks at once"""
        results = {}
        for ticker in tickers:
            results[ticker] = self.get_stock_data(ticker)
        return results
    
    def clear_cache(self):
        """Clear the data cache"""
        self.cache.clear()
        logger.info("Cache cleared")

# Convenience function
def get_stock_data(ticker: str) -> Dict[str, Any]:
    """Simple function to get stock data for a ticker"""
    provider = StockDataProvider()
    return provider.get_stock_data(ticker)

if __name__ == "__main__":
    # Test the module
    test_ticker = "AAPL"
    data = get_stock_data(test_ticker)
    print(f"Data for {test_ticker}:")
    for key, value in data.items():
        print(f"{key}: {value}")
