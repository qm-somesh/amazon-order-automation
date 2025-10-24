# 📦 Amazon India Order Automation - Dual Implementation

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Enabled-green.svg)](https://playwright.dev/)
[![Browser Use AI](https://img.shields.io/badge/Browser%20Use-AI%20Powered-purple.svg)](https://browser-use.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Two powerful automation implementations for extracting Amazon India orders:**
1. **Playwright** - Fast, traditional browser automation
2. **Browser Use** - AI-powered natural language automation

*Author: qm-somesh*  
*Date: 2025-10-24*

---

## � Choose Your Implementation

| Feature | Playwright 🎭 | Browser Use 🤖 |
|---------|--------------|----------------|
| **Speed** | ⚡ Very Fast | 🐢 Moderate |
| **Reliability** | 🔧 Good | 🌟 Excellent |
| **Maintenance** | 🛠️ High | ✨ Low |
| **Cost** | � Free | � ~$0.05/run |
| **Setup** | ✅ Easy | ✅ Easy |
| **AI-Powered** | ❌ No | ✅ Yes |
| **Self-Healing** | ❌ No | ✅ Yes |

### Quick Start

```bash
# Run Playwright (fast & free)
python run.py --mode playwright

# Run Browser Use (AI-powered)
python run.py --mode browseruse

# Run both and compare
python run.py --mode both
```

---

## 🌟 Why Two Implementations?

### Playwright Version
**Best for**: Speed, local testing, cost-sensitive scenarios
- Direct browser control with CSS selectors
- Fastest execution (~2-3 seconds)
- No API costs
- Great for stable websites

### Browser Use Version
**Best for**: Production, reliability, low maintenance
- Natural language commands
- Self-healing when UI changes
- AI-powered element detection
- Handles errors automatically

**See detailed comparison**: [COMPARISON.md](COMPARISON.md)

---

## 🚀 Features

- 🎭 **Dual Implementation**: Choose between Playwright or Browser Use
- 🤖 **AI-Powered Option**: Natural language commands (Browser Use)
- ⚡ **Fast Option**: Direct control with selectors (Playwright)
- 🔐 **Smart Login**: Automatically logs into Amazon India
- 📊 **Order Extraction**: Extracts recent order details
- 📄 **PDF Reports**: Generates professional, styled PDF reports
- 💾 **JSON Backup**: Saves raw order data in JSON format
- 📸 **Error Screenshots**: Captures screenshots on errors for debugging
- ⚡ **Async/Await**: Modern Python async patterns for better performance
- 🎯 **Robust Error Handling**: Comprehensive logging and error management

---

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 16+** (for Stagehand AI)
- **wkhtmltopdf** (for PDF generation)
- Amazon India account credentials

---

## 🛠️ Installation

### Quick Setup (Recommended)

#### Windows:
```bash
cd amazon-order-automation
scripts\setup.bat
```

#### Linux/macOS:
```bash
cd amazon-order-automation
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/qm-somesh/amazon-order-automation.git
   cd amazon-order-automation
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Stagehand AI:**
   ```bash
   npm install @browserbasehq/stagehand
   ```

5. **Install wkhtmltopdf:**
   - **Ubuntu/Debian:** `sudo apt-get install wkhtmltopdf`
   - **macOS:** `brew install wkhtmltopdf`
   - **Windows:** [Download installer](https://wkhtmltopdf.org/downloads.html)

6. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

---

## ⚙️ Configuration

Edit `.env` file with your credentials:

```env
# Amazon India Credentials
AMAZON_EMAIL=your_email@example.com
AMAZON_PASSWORD=your_secure_password

# For Browser Use AI (get free key from: https://aistudio.google.com/apikey)
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**Note**: The Browser Use implementation requires a Google Gemini API key. Get your free API key from [Google AI Studio](https://aistudio.google.com/apikey).

### Advanced Configuration

Edit `config/settings.py` to customize:

- **Stagehand settings**: Headless mode, caching, verbosity
- **PDF options**: Page size, margins, DPI
- **Automation parameters**: Max orders, timeouts, retries
- **Director.ai integration**: Scheduling and orchestration

---

## 🎮 Usage

### Basic Usage

```bash
python src/amazon_automation.py
```

### With Director.ai (Scheduling)

```python
from director_ai import Director
from src.amazon_automation import AmazonOrderAutomation

# Schedule to run daily at 9 AM IST
director = Director()
director.schedule(
    task=AmazonOrderAutomation,
    cron="0 9 * * *",
    timezone="Asia/Kolkata"
)
```

### Programmatic Usage

```python
import asyncio
from src.amazon_automation import AmazonOrderAutomation
from config.settings import STAGEHAND_CONFIG

async def main():
    automation = AmazonOrderAutomation(config=STAGEHAND_CONFIG)
    await automation.run(max_orders=20)

asyncio.run(main())
```

---

## 📁 Project Structure

```
amazon-order-automation/
│
├── src/
│   ├── __init__.py
│   └── amazon_automation.py       # Main automation script
│
├── config/
│   ├── __init__.py
│   └── settings.py                # Configuration settings
│
├── scripts/
│   ├── setup.sh                   # Setup script (Linux/macOS)
│   └── setup.bat                  # Setup script (Windows)
│
├── output/                        # Generated PDFs and JSON files
├── screenshots/                   # Error and progress screenshots
│
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── LICENSE                       # MIT License
```

---

## 📊 Output

The automation generates:

1. **PDF Report** (`output/amazon_orders_report_YYYYMMDD_HHMMSS.pdf`)
   - Professional styling with gradient headers
   - Order summary and details table
   - Timestamp and metadata

2. **JSON Data** (`output/orders_YYYYMMDD_HHMMSS.json`)
   - Raw order data in structured format
   - Easy to parse and analyze

3. **Screenshots** (`screenshots/`)
   - Progress screenshots during automation
   - Error screenshots for debugging

---

## 🤖 How Stagehand AI Works

Stagehand AI uses advanced language models to:

1. **Understand Context**: Analyzes the DOM and understands page structure
2. **Natural Language**: Interprets commands like "Click on Sign In button"
3. **Smart Extraction**: Extracts data without selectors using AI
4. **Adaptive**: Automatically adjusts to UI changes

### Key Stagehand Methods

```python
# Navigate and act
await stagehand.act("Click on the Sign In button")

# Extract data with AI
data = await stagehand.extract("Get the order number and date from this order")

# Observe and verify
result = await stagehand.observe("Check if login was successful")
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use strong passwords** and enable 2FA on Amazon
3. **Rotate credentials** regularly
4. **Run in secure environment** (private network)
5. **Review generated PDFs** before sharing
6. **Enable logging masking** in production (`MASK_SENSITIVE_DATA_IN_LOGS=True`)

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Stagehand Not Found
```bash
# Install Stagehand
npm install @browserbasehq/stagehand
```

#### 2. wkhtmltopdf Not Found
```bash
# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# macOS
brew install wkhtmltopdf

# Windows: Download from wkhtmltopdf.org
```

#### 3. Login Fails
- Verify credentials in `.env`
- Check if Amazon requires CAPTCHA
- Try running in non-headless mode: Set `headless: False` in `config/settings.py`
- Review screenshots in `screenshots/` folder

#### 4. No Orders Extracted
- Check Amazon orders page manually
- Review Stagehand logs (`amazon_automation.log`)
- Increase `MAX_ORDERS_TO_SCRAPE` in config
- Take screenshots to see page state

#### 5. PDF Generation Fails
- Ensure wkhtmltopdf is installed
- Check file permissions in `output/` directory
- HTML fallback is automatically generated

### Debug Mode

Enable verbose logging:

```python
# In config/settings.py
STAGEHAND_CONFIG = {
    'verbose': 2,  # Maximum verbosity
    'debug_dom': True,
    'headless': False  # See browser actions
}
```

---

## 🧪 Testing

Run tests with pytest:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

---

## 🔄 Integration with Director.ai

Director.ai provides orchestration and scheduling capabilities:

```python
# Enable in config/settings.py
DIRECTOR_CONFIG = {
    'enabled': True,
    'schedule': '0 9 * * *',  # Daily at 9 AM
    'timezone': 'Asia/Kolkata',
    'retry_on_failure': True
}
```

### Scheduled Execution

```bash
# Install director.ai
pip install director-ai

# Run with director
director run src/amazon_automation.py
```

---

## 📈 Performance Tips

1. **Enable Caching**: Set `enable_caching: True` in Stagehand config
2. **Use Headless Mode**: Set `headless: True` for production
3. **Optimize Timeouts**: Adjust timeouts based on your connection speed
4. **Batch Operations**: Process multiple accounts in parallel (with caution)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Stagehand AI** by BrowserBase - Revolutionary browser automation
- **Amazon** - For the platform (please respect their ToS)
- **OpenAI** - Powering the AI behind Stagehand

---

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please:

- Respect Amazon's Terms of Service
- Use responsibly and ethically
- Don't abuse or overload Amazon's servers
- Keep your credentials secure

The author is not responsible for any misuse of this tool.

---

## 📧 Contact

**Author**: qm-somesh  
**GitHub**: [@qm-somesh](https://github.com/qm-somesh)

For issues and questions, please use the [GitHub Issues](https://github.com/qm-somesh/amazon-order-automation/issues) page.

---

## 🌟 Star This Repo!

If you find this project helpful, please give it a ⭐️ on GitHub!

---

**Made with ❤️ and 🤖 AI by qm-somesh**
