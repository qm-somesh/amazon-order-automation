"""
Quick test to verify setup is complete
"""
import sys
import os

print("=" * 70)
print("SETUP VERIFICATION")
print("=" * 70)
print()

# Check Python version
print(f"✅ Python Version: {sys.version.split()[0]}")

# Check if .env exists
if os.path.exists('.env'):
    print("✅ .env file exists")
    
    # Check if credentials are configured
    from dotenv import load_dotenv
    load_dotenv()
    
    email = os.getenv('AMAZON_EMAIL')
    password = os.getenv('AMAZON_PASSWORD')
    
    if email and email != 'your_email@example.com':
        print(f"✅ Amazon email configured: {email[:3]}***{email[-10:]}")
    else:
        print("⚠️  Amazon email NOT configured - please edit .env file")
        
    if password and password != 'your_secure_password':
        print("✅ Amazon password configured: ***")
    else:
        print("⚠️  Amazon password NOT configured - please edit .env file")
else:
    print("❌ .env file NOT found - please create it from .env.example")

# Check dependencies
print()
print("Checking Python dependencies...")
try:
    import pdfkit
    print("✅ pdfkit installed")
except ImportError:
    print("❌ pdfkit NOT installed")

try:
    import aiohttp
    print("✅ aiohttp installed")
except ImportError:
    print("❌ aiohttp NOT installed")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv installed")
except ImportError:
    print("❌ python-dotenv NOT installed")

# Check Node modules
print()
print("Checking Node.js dependencies...")
if os.path.exists('node_modules/@browserbasehq/stagehand'):
    print("✅ Stagehand AI installed")
else:
    print("❌ Stagehand AI NOT installed")

# Check directories
print()
print("Checking directories...")
if os.path.exists('output'):
    print("✅ output/ directory exists")
else:
    print("⚠️  output/ directory missing")
    
if os.path.exists('screenshots'):
    print("✅ screenshots/ directory exists")
else:
    print("⚠️  screenshots/ directory missing")

print()
print("=" * 70)
print("SETUP STATUS")
print("=" * 70)

# Final check
load_dotenv()
email = os.getenv('AMAZON_EMAIL', '')
password = os.getenv('AMAZON_PASSWORD', '')

if (email and email != 'your_email@example.com' and 
    password and password != 'your_secure_password'):
    print("✅ Setup looks good! Ready to run automation.")
    print()
    print("Next step: python src\\amazon_automation.py")
else:
    print("⚠️  Please configure your Amazon credentials in .env file")
    print()
    print("Edit .env and add:")
    print("  AMAZON_EMAIL=your_email@example.com")
    print("  AMAZON_PASSWORD=your_password")

print("=" * 70)
