# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

```powershell
# Check Python (need 3.9+)
python --version

# Check Node.js (need 16+)
node --version

# If missing, install from:
# Python: https://www.python.org/downloads/
# Node.js: https://nodejs.org/
```

## Step 1: Clone or Use Local Project

```powershell
cd "d:\Info\Learn to Evolve team\AI\amazon-order-automation"
```

## Step 2: Run Setup Script

```powershell
.\scripts\setup.bat
```

This will:
- ✅ Create Python virtual environment
- ✅ Install Python dependencies
- ✅ Install Stagehand AI
- ✅ Create output directories
- ✅ Create .env file from template

## Step 3: Configure Credentials

Edit `.env` file:
```env
AMAZON_EMAIL=your_email@example.com
AMAZON_PASSWORD=your_secure_password
```

## Step 4: Run!

```powershell
# Activate virtual environment (if not already active)
.\venv\Scripts\activate

# Run automation
python src\amazon_automation.py
```

## Expected Output

The script will:
1. 🌐 Open browser (or run headless)
2. 🔐 Login to Amazon India
3. 📊 Extract recent orders
4. 📄 Generate PDF report in `output/`
5. 💾 Save JSON data in `output/`
6. 📸 Save screenshots in `screenshots/`

## Troubleshooting

### Issue: Module not found
```powershell
pip install -r requirements.txt
```

### Issue: Stagehand not found
```powershell
npm install @browserbasehq/stagehand
```

### Issue: wkhtmltopdf error
Download and install: https://wkhtmltopdf.org/downloads.html

### Issue: Login fails
- Check credentials in `.env`
- Set `headless: False` in `config/settings.py` to see browser
- Check `screenshots/` folder for debug info

## What's Next?

### Try Examples
```powershell
python example_usage.py
```

### Customize Settings
Edit `config/settings.py`:
- Change max orders to scrape
- Enable/disable headless mode
- Adjust timeouts
- Configure PDF options

### Schedule with Director.ai
```python
# In config/settings.py
DIRECTOR_CONFIG = {
    'enabled': True,
    'schedule': '0 9 * * *',  # Daily at 9 AM
}
```

### Push to GitHub
See `GITHUB_SETUP.md` for detailed instructions.

## Getting Help

1. 📖 Read `README.md` for full documentation
2. 🔍 Check `GITHUB_SETUP.md` for GitHub instructions
3. 💡 Review `example_usage.py` for code examples
4. 🐛 Open an issue on GitHub
5. 📧 Contact qm-somesh

## Quick Commands Cheat Sheet

```powershell
# Activate venv
.\venv\Scripts\activate

# Run automation
python src\amazon_automation.py

# Run examples
python example_usage.py

# Install dependencies
pip install -r requirements.txt

# Run tests (if you add them)
pytest tests/ -v

# Format code
black src/ config/

# Lint code
flake8 src/ config/

# Check git status
git status

# Push to GitHub
git push origin main
```

## Success! 🎉

You should now have:
- ✅ PDF report in `output/amazon_orders_report_*.pdf`
- ✅ JSON data in `output/orders_*.json`
- ✅ Screenshots in `screenshots/`
- ✅ Logs in `amazon_automation.log`

**Happy Automating!** 🤖✨
