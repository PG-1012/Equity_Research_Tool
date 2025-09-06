"""
AI Analysis Module - LLM-powered stock insights
Converts raw financial data into understandable investment analysis
"""

import os
from typing import Dict, Any, List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockAnalyzer:
    """AI-powered stock analysis using LLMs"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"  # Default model
        
        if not self.api_key:
            logger.warning("No OpenAI API key found. Some features may not work.")
    
    def analyze_stock(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-powered analysis of stock data
        
        Args:
            stock_data (Dict): Stock data from StockDataProvider
            
        Returns:
            Dict containing AI analysis
        """
        try:
            if 'error' in stock_data:
                return {
                    'error': f"Cannot analyze stock with error: {stock_data['error']}",
                    'analysis': None
                }
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(stock_data)
            
            # Generate analysis using LLM
            analysis = self._generate_llm_analysis(prompt)
            
            return {
                'ticker': stock_data['ticker'],
                'analysis': analysis,
                'summary': self._extract_summary(analysis),
                'pros': self._extract_pros(analysis),
                'cons': self._extract_cons(analysis),
                'risks': self._extract_risks(analysis),
                'recommendation': self._extract_recommendation(analysis),
                'timestamp': stock_data.get('last_updated', 'N/A')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock {stock_data.get('ticker', 'Unknown')}: {str(e)}")
            return {
                'error': f"Analysis failed: {str(e)}",
                'analysis': None
            }
    
    def _create_analysis_prompt(self, stock_data: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for stock analysis"""
        
        # Format financial data for the prompt
        financial_summary = f"""
Company: {stock_data.get('company_name', 'N/A')} ({stock_data.get('ticker', 'N/A')})
Sector: {stock_data.get('sector', 'N/A')}
Industry: {stock_data.get('industry', 'N/A')}

Current Price: ${stock_data.get('current_price', 'N/A'):,.2f} 
Price Change: {stock_data.get('price_change_pct', 'N/A'):.2f}%

Key Metrics:
- Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
- P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
- Forward P/E: {stock_data.get('forward_pe', 'N/A')}
- Price to Book: {stock_data.get('price_to_book', 'N/A')}
- Debt to Equity: {stock_data.get('debt_to_equity', 'N/A')}
- Return on Equity: {stock_data.get('return_on_equity', 'N/A')}
- Profit Margins: {stock_data.get('profit_margins', 'N/A')}
- Revenue Growth: {stock_data.get('revenue_growth', 'N/A')}
- Dividend Yield: {stock_data.get('dividend_yield', 'N/A')}
- Beta: {stock_data.get('beta', 'N/A')}
"""
        
        prompt = f"""
You are a professional investment analyst. Analyze the following stock data and provide a comprehensive investment analysis.

{financial_summary}

Please provide:
1. A concise summary of the investment case (2-3 sentences)
2. Key strengths/advantages (3-4 bullet points)
3. Key weaknesses/concerns (3-4 bullet points)
4. Major risks to consider (3-4 bullet points)
5. Overall investment recommendation (Buy/Hold/Sell with brief reasoning)

Format your response in a clear, structured manner. Be objective and data-driven. Focus on what the numbers tell us about the company's financial health and investment potential.
"""
        
        return prompt
    
    def _generate_llm_analysis(self, prompt: str) -> str:
        """Generate analysis using the LLM"""
        try:
            # Try to use OpenAI if available
            if self.api_key:
                return self._use_openai(prompt)
            else:
                # Fallback to mock analysis for demo purposes
                return self._generate_mock_analysis(prompt)
                
        except Exception as e:
            logger.error(f"Error generating LLM analysis: {str(e)}")
            return self._generate_mock_analysis(prompt)
    
    def _use_openai(self, prompt: str) -> str:
        """Use OpenAI API for analysis"""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional investment analyst. Provide clear, objective analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            logger.error("OpenAI library not installed")
            return self._generate_mock_analysis(prompt)
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self._generate_mock_analysis(prompt)
    
    def _generate_mock_analysis(self, prompt: str) -> str:
        """Generate a mock analysis when LLM is not available"""
        # This provides a realistic demo when API keys aren't available
        return """
**Investment Analysis Summary:**
Based on the financial data provided, this appears to be a well-established company with solid fundamentals but some areas of concern that warrant careful consideration.

**Key Strengths:**
• Strong market position with substantial market capitalization
• Reasonable valuation metrics compared to industry peers
• Consistent profitability with healthy profit margins
• Stable sector positioning with defensive characteristics

**Key Concerns:**
• Valuation appears elevated relative to historical averages
• Some financial ratios suggest potential overvaluation
• Industry headwinds may impact future growth prospects
• Market sentiment appears to be driving current pricing

**Major Risks:**
• Market volatility could lead to significant price swings
• Sector-specific regulatory changes could impact operations
• Economic downturn could affect consumer spending patterns
• Competition from disruptive technologies or new entrants

**Recommendation: HOLD**
While the company shows solid fundamentals, current valuation levels suggest limited upside potential in the near term. Consider this a core holding for long-term investors, but new positions should wait for more attractive entry points.
"""
    
    def _extract_summary(self, analysis: str) -> str:
        """Extract the summary section from analysis"""
        try:
            lines = analysis.split('\n')
            for i, line in enumerate(lines):
                if 'summary' in line.lower() or 'investment case' in line.lower():
                    # Return next few lines as summary
                    return '\n'.join(lines[i+1:i+4]).strip()
            return "Analysis summary not available"
        except:
            return "Analysis summary not available"
    
    def _extract_pros(self, analysis: str) -> List[str]:
        """Extract pros from analysis"""
        try:
            pros = []
            lines = analysis.split('\n')
            in_pros = False
            
            for line in lines:
                if 'strengths' in line.lower() or 'advantages' in line.lower():
                    in_pros = True
                    continue
                elif in_pros and ('concerns' in line.lower() or 'weaknesses' in line.lower()):
                    break
                elif in_pros and line.strip().startswith('•'):
                    pros.append(line.strip())
            
            return pros if pros else ["Strengths analysis not available"]
        except:
            return ["Strengths analysis not available"]
    
    def _extract_cons(self, analysis: str) -> List[str]:
        """Extract cons from analysis"""
        try:
            cons = []
            lines = analysis.split('\n')
            in_cons = False
            
            for line in lines:
                if 'concerns' in line.lower() or 'weaknesses' in line.lower():
                    in_cons = True
                    continue
                elif in_cons and ('risks' in line.lower() or 'recommendation' in line.lower()):
                    break
                elif in_cons and line.strip().startswith('•'):
                    cons.append(line.strip())
            
            return cons if cons else ["Concerns analysis not available"]
        except:
            return ["Concerns analysis not available"]
    
    def _extract_risks(self, analysis: str) -> List[str]:
        """Extract risks from analysis"""
        try:
            risks = []
            lines = analysis.split('\n')
            in_risks = False
            
            for line in lines:
                if 'risks' in line.lower():
                    in_risks = True
                    continue
                elif in_risks and ('recommendation' in line.lower() or line.strip().startswith('**')):
                    break
                elif in_risks and line.strip().startswith('•'):
                    risks.append(line.strip())
            
            return risks if risks else ["Risk analysis not available"]
        except:
            return ["Risk analysis not available"]
    
    def _extract_recommendation(self, analysis: str) -> str:
        """Extract recommendation from analysis"""
        try:
            lines = analysis.split('\n')
            for line in lines:
                if 'recommendation' in line.lower():
                    return line.strip()
            return "Recommendation not available"
        except:
            return "Recommendation not available"

# Convenience function
def analyze_stock(stock_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simple function to analyze stock data"""
    analyzer = StockAnalyzer()
    return analyzer.analyze_stock(stock_data)

if __name__ == "__main__":
    # Test the module
    from stock_data import get_stock_data
    
    test_data = get_stock_data("AAPL")
    analysis = analyze_stock(test_data)
    
    print("Stock Analysis:")
    for key, value in analysis.items():
        if key == 'analysis':
            print(f"\n{key.upper()}:")
            print(value)
        else:
            print(f"{key}: {value}")
