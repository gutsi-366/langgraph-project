<p align="center">
  <img src="docs/banner.svg" alt="LangGraph AI E-commerce Analytics banner" width="100%">
</p>

<p align="center">
  <a href="https://langgraph-project-azegang.streamlit.app">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit">
  </a>
  <br/>
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white">
  </a>
  <a href="https://streamlit.io/">
    <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white">
  </a>
  <a href="https://github.com/langchain-ai/langgraph">
    <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-enabled-4B8BBE">
  </a>
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg">
  </a>
</p>

---

## ?? Overview
**LangGraph AI E-commerce Analytics** is a Streamlit-powered project that analyzes data, crawls competitors, and generates AI-driven insights for e-commerce businesses.

- ?? Interactive analytics dashboard  
- ??? Competitor crawling & data extraction  
- ?? LangGraph-based AI agent for planning and insights  
- ??? Save, export, and review results  

---

## ?? Live Demo
**Open the App:** [langgraph-project-azegang.streamlit.app](https://langgraph-project-azegang.streamlit.app)

---

## ?? Tech Stack
- **Streamlit** � UI framework  
- **LangGraph** � AI agent logic  
- **BeautifulSoup + Requests** � web crawling  
- **Pandas, NumPy, Matplotlib** � data analysis  
- **scikit-learn** � ML-based insights  

---

## ?? Setup (Local)

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (for LLM features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/gutsi-366/langgraph-project.git
cd langgraph-project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your API keys
# OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

### Optional: Run Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

## 🧪 Experiment Demo

Run the complete LangGraph agent experiment as described in the documentation:

```bash
python experiment_demo.py
```

This demonstrates:
- ✅ Multi-agent LangGraph architecture
- ✅ LLM-powered code generation and execution  
- ✅ Advanced e-commerce data analysis
- ✅ Automated visualization generation
- ✅ Comprehensive business intelligence reports

## 🚀 New Features (v2.0)

### ✨ Enhanced Analytics
- **Advanced ML Models**: K-means clustering, Isolation Forest, Random Forest
- **Customer Segmentation**: Automated customer grouping with insights
- **Anomaly Detection**: Identify unusual customer behavior patterns
- **CLV Prediction**: Predict customer lifetime value with feature importance
- **Comprehensive Reports**: Executive summaries with actionable recommendations

### ⚡ Performance Optimizations
- **Intelligent Caching**: Multi-level caching system with TTL and compression
- **Parallel Processing**: Concurrent analysis operations
- **Memory Optimization**: Efficient DataFrame operations
- **Performance Monitoring**: Real-time operation timing and metrics

### 🎨 Enhanced UI/UX
- **Modern Design**: Gradient backgrounds, animations, and hover effects
- **Loading States**: Spinners and progress indicators
- **Status Badges**: Visual feedback for operations
- **Data Quality Indicators**: Real-time data validation metrics
- **Responsive Layout**: Optimized for different screen sizes

### 🔒 Security Enhancements
- **Input Validation**: Comprehensive file upload and data validation
- **Data Sanitization**: XSS and injection prevention
- **Rate Limiting**: Request throttling and abuse prevention
- **Security Auditing**: Event logging and monitoring
- **Access Control**: Authentication and authorization framework

### 🧪 Testing Framework
- **Comprehensive Test Suite**: Unit, integration, and performance tests
- **Test Fixtures**: Reusable test data and configurations
- **Coverage Reporting**: Code coverage analysis
- **CI/CD Ready**: Automated testing pipeline support

## 📚 Documentation

- **[API Documentation](docs/API.md)**: Complete API reference with examples
- **[Architecture Guide](docs/ARCHITECTURE.md)**: System design and component overview
- **[Security Guide](docs/SECURITY.md)**: Security features and best practices

## 🔧 Configuration

### Environment Variables
See [`.env.template`](.env.template) for all available configuration options.

### Key Settings
- `OPENAI_API_KEY`: Required for LLM-powered features
- `MAX_FILE_SIZE_MB`: Maximum file upload size (default: 100MB)
- `CACHE_TTL_SECONDS`: Cache expiration time (default: 3600s)
- `DEBUG`: Enable debug mode (default: False)

## 🏗️ Architecture

The platform follows a modern, layered architecture:

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│  Streamlit UI + Enhanced Components    │
├─────────────────────────────────────────┤
│           Application Layer             │
│  Enhanced Agent + Advanced Analytics   │
├─────────────────────────────────────────┤
│          Infrastructure Layer           │
│  LangGraph + ML + Cache + Security     │
└─────────────────────────────────────────┘
```

## 🤖 AI Features

### LangGraph Integration
- **Multi-Agent Workflow**: Planning, code generation, execution, and reporting
- **Dynamic Code Generation**: AI-generated Python code for analysis
- **Safe Execution**: Sandboxed code execution with timeouts
- **Intelligent Fallbacks**: Graceful degradation when LLM is unavailable

### Machine Learning Pipeline
1. **Data Validation**: Quality assessment and cleaning
2. **Feature Engineering**: Automated feature extraction
3. **Model Training**: ML model selection and training
4. **Prediction**: Real-time predictions and insights
5. **Visualization**: Automated chart and report generation

## 📊 Supported Analytics

### Customer Analytics
- Customer segmentation and profiling
- Lifetime value prediction
- Purchase behavior analysis
- Churn prediction and prevention

### Business Intelligence
- Revenue analysis and forecasting
- Market trend identification
- Competitive analysis
- Performance benchmarking

### Data Quality
- Missing data detection
- Outlier identification
- Data consistency checks
- Quality score calculation

## 🛡️ Security Features

### Data Protection
- File type validation and sanitization
- SQL injection prevention
- XSS protection
- Data encryption in transit and at rest

### Access Control
- Session-based authentication
- Rate limiting and throttling
- Audit logging
- Role-based permissions

### Privacy Compliance
- Data anonymization
- GDPR compliance features
- Secure data deletion
- Privacy impact assessment

## 🔍 Monitoring & Observability

### Performance Metrics
- Cache hit rates and efficiency
- Operation timing and bottlenecks
- Memory usage optimization
- Error rates and patterns

### Security Monitoring
- Failed authentication attempts
- Suspicious file uploads
- Rate limit violations
- Security event logging

## 🚀 Deployment

### Streamlit Cloud
The application is optimized for Streamlit Cloud deployment with:
- Environment variable configuration
- Persistent storage for outputs
- Automatic scaling
- Built-in monitoring

### Local Development
- Hot reloading for development
- Debug mode with detailed logging
- Test environment setup
- Development server configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure security best practices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for the AI agent framework
- [Streamlit](https://streamlit.io/) for the web application framework
- [scikit-learn](https://scikit-learn.org/) for machine learning capabilities
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Plotly](https://plotly.com/) for interactive visualizations
