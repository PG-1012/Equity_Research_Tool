"""
Investing AI Platform - Main Application
A comprehensive MVP for AI-powered stock analysis and research management
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Import our modules
from stock_data import StockDataProvider, get_stock_data
from ai_analysis import StockAnalyzer, analyze_stock
from knowledge_base import KnowledgeBase, create_knowledge_base

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Investing AI Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .analysis-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .knowledge-item {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    .stButton > button {
        width: 100%;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'stock_analysis' not in st.session_state:
    st.session_state.stock_analysis = None
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = None

# Initialize components
@st.cache_resource
def init_components():
    """Initialize core components"""
    return {
        'stock_provider': StockDataProvider(),
        'stock_analyzer': StockAnalyzer(),
        'knowledge_base': create_knowledge_base()
    }

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Investing AI Platform</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize components
    components = init_components()
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Stock Analysis")
        
        # Stock input
        ticker = st.text_input("Enter Stock Ticker", placeholder="e.g., AAPL, MSFT, GOOGL")
        
        if st.button("🔍 Analyze Stock", type="primary"):
            if ticker:
                with st.spinner(f"Analyzing {ticker.upper()}..."):
                    try:
                        # Get stock data
                        stock_data = components['stock_provider'].get_stock_data(ticker.upper())
                        st.session_state.stock_data = stock_data
                        
                        # Generate AI analysis
                        stock_analysis = components['stock_analyzer'].analyze_stock(stock_data)
                        st.session_state.stock_analysis = stock_analysis
                        
                        st.success(f"Analysis complete for {ticker.upper()}!")
                    except Exception as e:
                        st.error(f"Error analyzing {ticker}: {str(e)}")
            else:
                st.warning("Please enter a stock ticker")
        
        st.markdown("---")
        
        # Knowledge Base section
        st.header("📚 Knowledge Base")
        
        # Add new note
        with st.expander("➕ Add Note"):
            note_title = st.text_input("Note Title")
            note_content = st.text_area("Note Content")
            note_tags = st.text_input("Tags (comma-separated)")
            note_tickers = st.text_input("Related Tickers (comma-separated)")
            
            if st.button("Save Note"):
                if note_title and note_content:
                    try:
                        tags = [tag.strip() for tag in note_tags.split(',')] if note_tags else []
                        tickers = [ticker.strip().upper() for ticker in note_tickers.split(',')] if note_tickers else []
                        
                        components['knowledge_base'].add_note(
                            title=note_title,
                            content=note_content,
                            tags=tags,
                            related_tickers=tickers
                        )
                        st.success("Note saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving note: {str(e)}")
                else:
                    st.warning("Please fill in title and content")
        
        # Add new article
        with st.expander("🔗 Add Article"):
            article_title = st.text_input("Article Title")
            article_url = st.text_input("Article URL")
            article_summary = st.text_area("Summary")
            article_tags = st.text_input("Tags (comma-separated)")
            article_tickers = st.text_input("Related Tickers (comma-separated)")
            
            if st.button("Save Article"):
                if article_title and article_url:
                    try:
                        tags = [tag.strip() for tag in article_tags.split(',')] if article_tags else []
                        tickers = [ticker.strip().upper() for ticker in article_tickers.split(',')] if article_tickers else []
                        
                        components['knowledge_base'].add_article(
                            title=article_title,
                            url=article_url,
                            summary=article_summary,
                            tags=tags,
                            related_tickers=tickers
                        )
                        st.success("Article saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving article: {str(e)}")
                else:
                    st.warning("Please fill in title and URL")
        
        # Search knowledge base
        st.markdown("---")
        search_query = st.text_input("🔍 Search Knowledge Base")
        if search_query:
            search_results = components['knowledge_base'].search_knowledge_base(search_query)
            st.write(f"Found {len(search_results)} results")
            
            for result in search_results[:5]:  # Show top 5 results
                with st.expander(f"{result['title']} ({result['collection']})"):
                    st.write(f"**Content:** {result.get('content', result.get('summary', 'No content'))[:200]}...")
                    st.write(f"**Tags:** {', '.join(result.get('tags', []))}")
                    st.write(f"**Tickers:** {', '.join(result.get('related_tickers', []))}")
                    st.write(f"**Score:** {result.get('relevance_score', 0):.2f}")
    
    # Main content area
    if st.session_state.stock_data and st.session_state.stock_analysis:
        display_stock_analysis(st.session_state.stock_data, st.session_state.stock_analysis)
    
    # Knowledge Base display
    display_knowledge_base(components['knowledge_base'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚀 Investing AI Platform MVP | Built with Streamlit, yfinance, and AI</p>
        <p>💡 Add your OpenAI API key to enable real AI analysis</p>
    </div>
    """, unsafe_allow_html=True)

def display_stock_analysis(stock_data, stock_analysis):
    """Display comprehensive stock analysis"""
    
    # Stock header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## 📊 {stock_data.get('company_name', stock_data['ticker'])} ({stock_data['ticker']})")
        st.markdown(f"**Sector:** {stock_data.get('sector', 'N/A')} | **Industry:** {stock_data.get('industry', 'N/A')}")
    
    with col2:
        if stock_data.get('current_price'):
            price_color = "green" if stock_data.get('price_change_pct', 0) >= 0 else "red"
            st.markdown(f"""
            <div style='text-align: center;'>
                <h2 style='color: {price_color};'>${stock_data['current_price']:,.2f}</h2>
                <p style='color: {price_color};'>{stock_data.get('price_change_pct', 0):+.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"**Last Updated:** {stock_data.get('last_updated', 'N/A')}")
    
    st.markdown("---")
    
    # Key metrics
    st.subheader("📈 Key Financial Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Market Cap</h4>
            <p>${stock_data.get('market_cap', 'N/A'):,}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>P/E Ratio</h4>
            <p>{stock_data.get('pe_ratio', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Forward P/E</h4>
            <p>{stock_data.get('forward_pe', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Price to Book</h4>
            <p>{stock_data.get('price_to_book', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>ROE</h4>
            <p>{stock_data.get('return_on_equity', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Profit Margins</h4>
            <p>{stock_data.get('profit_margins', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Dividend Yield</h4>
            <p>{stock_data.get('dividend_yield', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Beta</h4>
            <p>{stock_data.get('beta', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Analysis
    if stock_analysis and not stock_analysis.get('error'):
        st.subheader("🤖 AI Investment Analysis")
        
        # Summary
        if stock_analysis.get('summary'):
            st.markdown(f"""
            <div class="analysis-section">
                <h4>📋 Investment Summary</h4>
                <p>{stock_analysis['summary']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pros and Cons
        col1, col2 = st.columns(2)
        
        with col1:
            if stock_analysis.get('pros'):
                st.markdown("""
                <div class="analysis-section">
                    <h4>✅ Key Strengths</h4>
                """, unsafe_allow_html=True)
                for pro in stock_analysis['pros']:
                    st.markdown(f"• {pro}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            if stock_analysis.get('cons'):
                st.markdown("""
                <div class="analysis-section">
                    <h4>⚠️ Key Concerns</h4>
                """, unsafe_allow_html=True)
                for con in stock_analysis['cons']:
                    st.markdown(f"• {con}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Risks
        if stock_analysis.get('risks'):
            st.markdown("""
            <div class="analysis-section">
                <h4>🚨 Major Risks</h4>
            """, unsafe_allow_html=True)
            for risk in stock_analysis['risks']:
                st.markdown(f"• {risk}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Recommendation
        if stock_analysis.get('recommendation'):
            st.markdown(f"""
            <div class="analysis-section">
                <h4>🎯 Investment Recommendation</h4>
                <p><strong>{stock_analysis['recommendation']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Full analysis
        with st.expander("📄 View Full AI Analysis"):
            st.markdown(stock_analysis.get('analysis', 'Analysis not available'))
    
    elif stock_analysis and stock_analysis.get('error'):
        st.error(f"Analysis Error: {stock_analysis['error']}")

def display_knowledge_base(knowledge_base):
    """Display knowledge base content"""
    st.markdown("---")
    st.subheader("📚 Your Investment Research")
    
    # Get all items
    all_items = knowledge_base.get_all_items()
    
    if not all_items:
        st.info("No research items yet. Use the sidebar to add notes, articles, or research!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox("Filter by Type", ["All", "Notes", "Articles", "Research"])
    
    with col2:
        filter_ticker = st.text_input("Filter by Ticker")
    
    with col3:
        filter_tags = st.text_input("Filter by Tags (comma-separated)")
    
    # Apply filters
    filtered_items = all_items
    
    if filter_type != "All":
        type_map = {"Notes": "notes", "Articles": "articles", "Research": "research"}
        filtered_items = [item for item in filtered_items if item.get('collection') == type_map[filter_type]]
    
    if filter_ticker:
        filtered_items = [item for item in filtered_items 
                         if filter_ticker.upper() in [t.upper() for t in item.get('related_tickers', [])]]
    
    if filter_tags:
        filter_tag_list = [tag.strip().lower() for tag in filter_tags.split(',')]
        filtered_items = [item for item in filtered_items 
                         if any(tag.lower() in filter_tag_list for tag in item.get('tags', []))]
    
    # Display filtered items
    if filtered_items:
        for item in filtered_items:
            with st.expander(f"📝 {item['title']} ({item.get('collection', 'unknown').title()})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if item.get('content'):
                        st.write(f"**Content:** {item['content'][:300]}...")
                    elif item.get('summary'):
                        st.write(f"**Summary:** {item['summary']}")
                    
                    if item.get('url'):
                        st.write(f"**URL:** [{item['url']}]({item['url']})")
                    
                    if item.get('source'):
                        st.write(f"**Source:** {item['source']}")
                
                with col2:
                    st.write(f"**Created:** {item['created_at'][:10]}")
                    
                    if item.get('tags'):
                        st.write("**Tags:**")
                        for tag in item['tags']:
                            st.markdown(f"`{tag}`")
                    
                    if item.get('related_tickers'):
                        st.write("**Tickers:**")
                        for ticker in item['related_tickers']:
                            st.markdown(f"`{ticker}`")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{item['id']}"):
                        st.info("Edit functionality coming soon!")
                
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{item['id']}"):
                        try:
                            knowledge_base.delete_item(item['id'], item.get('collection', 'notes'))
                            st.success("Item deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting item: {str(e)}")
    else:
        st.info("No items match your current filters.")

if __name__ == "__main__":
    main()
