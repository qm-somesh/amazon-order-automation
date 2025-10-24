"""
Configuration settings for Amazon Order Automation
Author: qm-somesh
Date: 2025-10-23
"""

# Stagehand AI Configuration
STAGEHAND_CONFIG = {
    # Browser settings
    'headless': False,  # Set to True for production/headless mode
    'enable_caching': True,  # Cache AI model responses for faster execution
    'verbose': 1,  # Logging verbosity (0=silent, 1=normal, 2=debug)
    'debug_dom': True,  # Enable DOM debugging
    
    # Browser viewport
    'viewport': {
        'width': 1920,
        'height': 1080
    },
    
    # User agent (simulate real browser)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# PDF Generation Options
PDF_OPTIONS = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': 'UTF-8',
    'no-outline': None,
    'enable-local-file-access': None,
    'print-media-type': None,
    'dpi': 300
}

# Automation Settings
MAX_ORDERS_TO_SCRAPE = 5  # Maximum number of orders to scrape (reduced to avoid rate limits)
DEFAULT_TIMEOUT = 30000  # Default timeout in milliseconds (30 seconds)
PAGE_LOAD_TIMEOUT = 60000  # Page load timeout (60 seconds)

# Retry Configuration
MAX_RETRIES = 3  # Maximum number of retry attempts
RETRY_DELAY = 5  # Delay between retries in seconds

# Amazon URLs
AMAZON_BASE_URL = 'https://www.amazon.in'
AMAZON_ORDERS_URL = 'https://www.amazon.in/gp/your-account/order-history'

# Output Settings
OUTPUT_DIR = 'output'
SCREENSHOTS_DIR = 'screenshots'
LOG_FILE = 'amazon_automation.log'

# Date Format
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
PDF_DATE_FORMAT = '%B %d, %Y at %I:%M %p'

# Stagehand AI Model Settings
STAGEHAND_MODEL = 'gpt-4'  # AI model for Stagehand (gpt-4, gpt-3.5-turbo, etc.)
STAGEHAND_TEMPERATURE = 0.1  # Lower temperature for more consistent results

# Error Handling
TAKE_SCREENSHOT_ON_ERROR = True
SAVE_HTML_ON_PDF_ERROR = True

# Security Settings
MASK_SENSITIVE_DATA_IN_LOGS = True  # Mask passwords/emails in logs

# Director.ai Integration Settings (for scheduling)
DIRECTOR_CONFIG = {
    'enabled': False,  # Set to True to enable director.ai scheduling
    'schedule': '0 9 * * *',  # Cron expression (daily at 9 AM)
    'timezone': 'Asia/Kolkata',  # IST timezone
    'retry_on_failure': True,
    'max_execution_time': 600  # 10 minutes max execution time
}

# Notification Settings (optional)
NOTIFICATION_CONFIG = {
    'enabled': False,
    'email': '',  # Email for notifications
    'slack_webhook': '',  # Slack webhook URL
    'notify_on_success': True,
    'notify_on_failure': True
}
