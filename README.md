# 🚀 Investing AI Platform MVP

A comprehensive AI-powered investing platform that combines real-time stock data, intelligent analysis, and personal research management.

## ✨ Features

### 🧱 Building Block 1: Stock Lookup (Foundation)
- **Real-time Data**: Get current prices, market cap, P/E ratios, and 20+ key metrics
- **Reliable Source**: Uses Yahoo Finance API via yfinance library
- **Caching**: Intelligent caching for better performance
- **Error Handling**: Graceful fallbacks when data is unavailable

### 🧱 Building Block 2: LLM Stock Summary (AI Layer)
- **AI Analysis**: Convert raw financial data into understandable insights
- **OpenAI Integration**: Uses GPT-3.5-turbo for professional analysis
- **Fallback Mode**: Mock analysis when API keys aren't available
- **Structured Output**: Pros, cons, risks, and recommendations

### 🧱 Building Block 3: User Knowledge Base (Differentiator)
- **Personal Research**: Store notes, articles, and research
- **Smart Search**: AI-powered semantic search across your research
- **Tagging System**: Organize content with tags and tickers
- **Persistent Storage**: Local JSON-based storage with easy backup

### 🧱 Building Block 4: Simple UI (Delivery)
- **Streamlit Interface**: Beautiful, responsive web application
- **Real-time Updates**: Instant analysis and data refresh
- **Mobile Friendly**: Works on all devices
- **Professional Design**: Clean, modern interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd investing-ai-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🔑 API Keys

### OpenAI API Key (Recommended)
- Get your free API key at [OpenAI Platform](https://platform.openai.com/api-keys)
- Add it to your `.env` file
- Enables real AI-powered stock analysis

### Alternative LLMs
The platform is designed to work with other LLM providers:
- Anthropic Claude
- Mistral AI
- Local models (Llama, etc.)

## 📊 Usage Guide

### Stock Analysis
1. **Enter a ticker** (e.g., AAPL, MSFT, GOOGL)
2. **Click "Analyze Stock"**
3. **View results**:
   - Real-time financial metrics
   - AI-powered investment analysis
   - Pros, cons, and risks
   - Investment recommendation

### Knowledge Base Management
1. **Add Notes**: Personal insights and observations
2. **Save Articles**: Research links with summaries
3. **Store Research**: Detailed analysis and reports
4. **Search & Filter**: Find relevant information quickly

### Research Workflow
1. **Analyze a stock** using the AI platform
2. **Save insights** to your knowledge base
3. **Add external research** from articles and reports
4. **Query your research** alongside stock analysis
5. **Build your investment thesis** over time

## 🏗️ Architecture

```
investing-ai-platform/
├── app.py                 # Main Streamlit application
├── stock_data.py         # Stock data provider (yfinance)
├── ai_analysis.py        # AI-powered analysis engine
├── knowledge_base.py     # Personal research storage
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables template
├── README.md            # This file
└── data/                # Data storage (auto-created)
    ├── knowledge_base/   # User research storage
    └── chroma_db/       # Vector embeddings (future)
```

## 🔧 Configuration

### Environment Variables
```bash
# Required for real AI analysis
OPENAI_API_KEY=your_openai_api_key

# Optional: Alternative LLM providers
ANTHROPIC_API_KEY=your_anthropic_key
MISTRAL_API_KEY=your_mistral_key

# Database configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
```

### Customization
- **Models**: Change AI models in `ai_analysis.py`
- **Metrics**: Add/remove financial metrics in `stock_data.py`
- **Storage**: Modify storage backend in `knowledge_base.py`
- **UI**: Customize Streamlit interface in `app.py`

## 🧪 Testing

### Test Individual Modules
```bash
# Test stock data
python stock_data.py

# Test AI analysis
python ai_analysis.py

# Test knowledge base
python knowledge_base.py
```

### Test Full Application
```bash
streamlit run app.py
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud** (Recommended for MVPs)
   - Connect your GitHub repo
   - Automatic deployment
   - Free hosting

2. **Heroku**
   - Add `setup.sh` and `Procfile`
   - Deploy via Git

3. **Docker**
   - Create `Dockerfile`
   - Build and run container

## 🔮 Future Enhancements

### Phase 2: Advanced AI
- **Multi-model support**: Claude, Llama, local models
- **Custom prompts**: User-defined analysis criteria
- **Historical analysis**: Track analysis accuracy over time

### Phase 3: Enhanced Data
- **Real-time alerts**: Price and news notifications
- **Portfolio tracking**: Multi-stock analysis
- **Technical indicators**: Charts and patterns

### Phase 4: Collaboration
- **Team workspaces**: Share research with colleagues
- **API access**: Integrate with other tools
- **Mobile app**: Native iOS/Android applications

## 🐛 Troubleshooting

### Common Issues

1. **"No OpenAI API key found"**
   - Check your `.env` file
   - Verify the API key is valid
   - Platform will use mock analysis as fallback

2. **"Error fetching stock data"**
   - Check internet connection
   - Verify ticker symbol is correct
   - Yahoo Finance may be temporarily unavailable

3. **"Module not found"**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **"Streamlit not found"**
   - Install Streamlit: `pip install streamlit`
   - Or use: `python -m streamlit run app.py`

### Performance Tips
- **Cache results**: Stock data is automatically cached
- **Limit requests**: Don't hammer the APIs
- **Use tags**: Organize research for faster search

## 📚 API Reference

### Stock Data Provider
```python
from stock_data import StockDataProvider

provider = StockDataProvider()
data = provider.get_stock_data("AAPL")
```

### AI Analyzer
```python
from ai_analysis import StockAnalyzer

analyzer = StockAnalyzer()
analysis = analyzer.analyze_stock(stock_data)
```

### Knowledge Base
```python
from knowledge_base import create_knowledge_base

kb = create_knowledge_base()
note_id = kb.add_note("Title", "Content", tags=["tag1"], related_tickers=["AAPL"])
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Yahoo Finance**: Free stock data API
- **OpenAI**: AI analysis capabilities
- **Streamlit**: Rapid web app development
- **Python Community**: Excellent libraries and tools

## 📞 Support

- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact for business inquiries

---

**🚀 Ready to revolutionize your investment research? Get started today!**

*Built with ❤️ for the investing community*
