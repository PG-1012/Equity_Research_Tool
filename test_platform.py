"""
Test script for the Investing AI Platform
Run this to verify all components are working correctly
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from stock_data import StockDataProvider, get_stock_data
        print("✅ stock_data module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import stock_data: {e}")
        return False
    
    try:
        from ai_analysis import StockAnalyzer, analyze_stock
        print("✅ ai_analysis module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ai_analysis: {e}")
        return False
    
    try:
        from knowledge_base import KnowledgeBase, create_knowledge_base
        print("✅ knowledge_base module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import knowledge_base: {e}")
        return False
    
    return True

def test_stock_data():
    """Test stock data functionality"""
    print("\n📊 Testing stock data functionality...")
    
    try:
        provider = StockDataProvider()
        print("✅ StockDataProvider initialized")
        
        # Test with a well-known stock
        data = provider.get_stock_data("AAPL")
        
        if 'error' in data:
            print(f"⚠️ Stock data error: {data['error']}")
            return False
        
        print(f"✅ Retrieved data for AAPL:")
        print(f"   Company: {data.get('company_name', 'N/A')}")
        print(f"   Price: ${data.get('current_price', 'N/A')}")
        print(f"   Market Cap: ${data.get('market_cap', 'N/A'):,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Stock data test failed: {e}")
        return False

def test_ai_analysis():
    """Test AI analysis functionality"""
    print("\n🤖 Testing AI analysis functionality...")
    
    try:
        analyzer = StockAnalyzer()
        print("✅ StockAnalyzer initialized")
        
        # Create mock stock data for testing
        mock_data = {
            'ticker': 'TEST',
            'company_name': 'Test Company',
            'sector': 'Technology',
            'industry': 'Software',
            'current_price': 100.0,
            'price_change_pct': 5.0,
            'market_cap': 1000000000,
            'pe_ratio': 25.0,
            'forward_pe': 22.0,
            'price_to_book': 3.0,
            'debt_to_equity': 0.5,
            'return_on_equity': 0.15,
            'profit_margins': 0.20,
            'revenue_growth': 0.10,
            'earnings_growth': 0.12,
            'dividend_yield': 0.02,
            'beta': 1.1,
            'last_updated': '2024-01-01 00:00:00'
        }
        
        analysis = analyzer.analyze_stock(mock_data)
        
        if 'error' in analysis:
            print(f"⚠️ Analysis error: {analysis['error']}")
            return False
        
        print(f"✅ Generated analysis for TEST:")
        print(f"   Summary: {analysis.get('summary', 'N/A')[:100]}...")
        print(f"   Pros: {len(analysis.get('pros', []))} items")
        print(f"   Cons: {len(analysis.get('cons', []))} items")
        print(f"   Risks: {len(analysis.get('risks', []))} items")
        
        return True
        
    except Exception as e:
        print(f"❌ AI analysis test failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality"""
    print("\n📚 Testing knowledge base functionality...")
    
    try:
        kb = create_knowledge_base("./test_data/kb")
        print("✅ Knowledge base initialized")
        
        # Test adding a note
        note_id = kb.add_note(
            title="Test Note",
            content="This is a test note for testing purposes",
            tags=["test", "demo"],
            related_tickers=["TEST"]
        )
        print(f"✅ Added test note with ID: {note_id}")
        
        # Test adding an article
        article_id = kb.add_article(
            title="Test Article",
            url="https://example.com/test",
            summary="Test article summary",
            tags=["test", "article"],
            related_tickers=["TEST"]
        )
        print(f"✅ Added test article with ID: {article_id}")
        
        # Test search
        search_results = kb.search_knowledge_base("test")
        print(f"✅ Search returned {len(search_results)} results")
        
        # Test getting all items
        all_items = kb.get_all_items()
        print(f"✅ Retrieved {len(all_items)} total items")
        
        # Clean up test data
        import shutil
        if os.path.exists("./test_data"):
            shutil.rmtree("./test_data")
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Knowledge base test failed: {e}")
        return False

def test_streamlit():
    """Test Streamlit availability"""
    print("\n🌐 Testing Streamlit availability...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        print(f"   Version: {st.__version__}")
        return True
    except ImportError:
        print("❌ Streamlit not available")
        print("   Install with: pip install streamlit")
        return False

def main():
    """Run all tests"""
    print("🚀 Investing AI Platform - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Stock Data", test_stock_data),
        ("AI Analysis", test_ai_analysis),
        ("Knowledge Base", test_knowledge_base),
        ("Streamlit", test_streamlit)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your platform is ready to run.")
        print("\n🚀 To start the application:")
        print("   streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\n💡 Common solutions:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Check Python version (3.8+)")
        print("   - Verify internet connection for stock data")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
