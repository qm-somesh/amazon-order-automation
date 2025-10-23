"""
Amazon India Order Automation with Stagehand AI
Author: qm-somesh
Date: 2025-10-23

This script uses Stagehand AI for intelligent browser automation to:
- Login to Amazon India using natural language commands
- Extract recent order details using AI-powered extraction
- Generate professional PDF reports
- Create JSON backups of order data
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pdfkit
from dotenv import load_dotenv

# Import Stagehand AI (assumed to be installed via npm/pip)
try:
    from stagehand import Stagehand
except ImportError:
    print("ERROR: Stagehand AI not installed. Run: npm install @browserbasehq/stagehand")
    exit(1)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('amazon_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AmazonOrderAutomation:
    """
    Amazon Order Automation using Stagehand AI for intelligent browser control.
    
    Uses natural language commands instead of brittle CSS selectors,
    making the automation more resilient to UI changes.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the automation with Stagehand configuration."""
        self.config = config or {}
        self.stagehand = None
        self.orders_data = []
        
        # Get credentials from environment
        self.email = os.getenv('AMAZON_EMAIL')
        self.password = os.getenv('AMAZON_PASSWORD')
        
        if not self.email or not self.password:
            raise ValueError("Amazon credentials not found in environment variables")
        
        # Create output directories
        self.output_dir = Path('output')
        self.screenshots_dir = Path('screenshots')
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        logger.info("AmazonOrderAutomation initialized")
    
    async def initialize_stagehand(self):
        """Initialize Stagehand AI browser automation."""
        try:
            logger.info("Initializing Stagehand AI...")
            
            # Initialize Stagehand with configuration
            self.stagehand = Stagehand(
                env="LOCAL",
                verbose=1,
                debugDom=True,
                headless=self.config.get('headless', False),
                enableCaching=self.config.get('enable_caching', True)
            )
            
            await self.stagehand.init()
            logger.info("Stagehand AI initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Stagehand: {e}")
            raise
    
    async def login_to_amazon(self) -> bool:
        """
        Login to Amazon India using natural language commands with Stagehand AI.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            logger.info("Navigating to Amazon India...")
            await self.stagehand.page.goto("https://www.amazon.in")
            
            # Take screenshot before login
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "01_homepage.png")
            )
            
            # Use natural language to find and click sign-in button
            logger.info("Looking for sign-in button...")
            await self.stagehand.act("Click on the Sign In button")
            
            # Wait for login page
            await asyncio.sleep(2)
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "02_login_page.png")
            )
            
            # Enter email using natural language
            logger.info("Entering email...")
            await self.stagehand.act(f"Type '{self.email}' in the email or mobile number field")
            await self.stagehand.act("Click the Continue button")
            
            # Wait for password page
            await asyncio.sleep(2)
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "03_password_page.png")
            )
            
            # Enter password using natural language
            logger.info("Entering password...")
            await self.stagehand.act(f"Type '{self.password}' in the password field")
            await self.stagehand.act("Click the Sign In button")
            
            # Wait for login to complete
            await asyncio.sleep(3)
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "04_logged_in.png")
            )
            
            # Verify login success by checking for account element
            verification = await self.stagehand.extract(
                "Find the user account name or 'Hello' greeting in the top navigation"
            )
            
            if verification:
                logger.info("Login successful!")
                return True
            else:
                logger.warning("Login verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "error_login.png")
            )
            return False
    
    async def scrape_recent_orders(self, max_orders: int = 10) -> List[Dict]:
        """
        Scrape recent orders using Stagehand AI's intelligent extraction.
        
        Args:
            max_orders: Maximum number of orders to scrape
            
        Returns:
            List of order dictionaries
        """
        try:
            logger.info("Navigating to orders page...")
            await self.stagehand.act("Click on Returns & Orders")
            
            # Wait for orders page to load
            await asyncio.sleep(3)
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "05_orders_page.png")
            )
            
            logger.info(f"Extracting up to {max_orders} recent orders...")
            
            # Use Stagehand's AI extraction to get order details
            # No need for brittle CSS selectors!
            orders_extraction_prompt = f"""
            Extract information from the {max_orders} most recent orders on this page.
            For each order, get:
            - Order number/ID
            - Order date
            - Product name(s)
            - Total amount/price
            - Order status (delivered, shipped, etc.)
            - Delivery date (if available)
            
            Return as a structured list of orders.
            """
            
            extracted_data = await self.stagehand.extract(orders_extraction_prompt)
            
            # Process extracted data
            if extracted_data:
                self.orders_data = self._process_extracted_orders(extracted_data)
                logger.info(f"Successfully extracted {len(self.orders_data)} orders")
                
                # Save raw JSON data
                json_path = self.output_dir / f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(self.orders_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved JSON data to {json_path}")
                
                return self.orders_data
            else:
                logger.warning("No orders extracted")
                return []
                
        except Exception as e:
            logger.error(f"Failed to scrape orders: {e}")
            await self.stagehand.page.screenshot(
                path=str(self.screenshots_dir / "error_scraping.png")
            )
            return []
    
    def _process_extracted_orders(self, extracted_data) -> List[Dict]:
        """
        Process and normalize extracted order data.
        
        Args:
            extracted_data: Raw data from Stagehand extraction
            
        Returns:
            List of normalized order dictionaries
        """
        processed_orders = []
        
        # Handle different extraction formats
        if isinstance(extracted_data, dict):
            orders_list = extracted_data.get('orders', [extracted_data])
        elif isinstance(extracted_data, list):
            orders_list = extracted_data
        else:
            orders_list = [extracted_data]
        
        for idx, order in enumerate(orders_list):
            if isinstance(order, dict):
                processed_order = {
                    'order_number': order.get('order_number', order.get('order_id', f'ORDER-{idx+1}')),
                    'order_date': order.get('order_date', 'N/A'),
                    'product_name': order.get('product_name', order.get('products', 'N/A')),
                    'total_amount': order.get('total_amount', order.get('price', 'N/A')),
                    'status': order.get('status', order.get('order_status', 'N/A')),
                    'delivery_date': order.get('delivery_date', order.get('delivered_on', 'N/A'))
                }
                processed_orders.append(processed_order)
        
        return processed_orders
    
    def generate_pdf_report(self, orders: Optional[List[Dict]] = None) -> str:
        """
        Generate a professional PDF report of orders.
        
        Args:
            orders: List of order dictionaries (uses self.orders_data if None)
            
        Returns:
            Path to generated PDF file
        """
        orders = orders or self.orders_data
        
        if not orders:
            logger.warning("No orders to generate report")
            return ""
        
        logger.info("Generating PDF report...")
        
        # Create HTML content with professional styling
        html_content = self._generate_html_report(orders)
        
        # PDF options
        pdf_options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Generate PDF
        pdf_filename = f"amazon_orders_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = self.output_dir / pdf_filename
        
        try:
            pdfkit.from_string(html_content, str(pdf_path), options=pdf_options)
            logger.info(f"PDF report generated: {pdf_path}")
            return str(pdf_path)
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            logger.info("Saving HTML version instead...")
            html_path = self.output_dir / pdf_filename.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return str(html_path)
    
    def _generate_html_report(self, orders: List[Dict]) -> str:
        """Generate HTML content for the PDF report."""
        
        # Build order rows
        order_rows = ""
        for idx, order in enumerate(orders, 1):
            order_rows += f"""
            <tr>
                <td>{idx}</td>
                <td><strong>{order['order_number']}</strong></td>
                <td>{order['order_date']}</td>
                <td>{order['product_name']}</td>
                <td>{order['total_amount']}</td>
                <td><span class="status-{order['status'].lower().replace(' ', '-')}">{order['status']}</span></td>
                <td>{order['delivery_date']}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }}
                .summary {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    border-left: 4px solid #667eea;
                }}
                .summary h2 {{
                    margin: 0 0 15px 0;
                    color: #667eea;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    border-radius: 8px;
                    overflow: hidden;
                }}
                th {{
                    background: #667eea;
                    color: white;
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                }}
                td {{
                    padding: 12px 15px;
                    border-bottom: 1px solid #e9ecef;
                }}
                tr:hover {{
                    background: #f8f9fa;
                }}
                tr:last-child td {{
                    border-bottom: none;
                }}
                .status-delivered {{
                    background: #d4edda;
                    color: #155724;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 600;
                }}
                .status-shipped {{
                    background: #fff3cd;
                    color: #856404;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 600;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #6c757d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📦 Amazon India Order Report</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p>Automated with Stagehand AI by qm-somesh</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Total Orders:</strong> {len(orders)}</p>
                <p><strong>Report Period:</strong> Recent orders</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Order Number</th>
                        <th>Order Date</th>
                        <th>Product</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Delivery Date</th>
                    </tr>
                </thead>
                <tbody>
                    {order_rows}
                </tbody>
            </table>
            
            <div class="footer">
                <p>This report was generated automatically using Stagehand AI</p>
                <p>Amazon Order Automation © 2025 qm-somesh</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    async def run(self, max_orders: int = 10):
        """
        Run the complete automation workflow.
        
        Args:
            max_orders: Maximum number of orders to scrape
        """
        try:
            logger.info("Starting Amazon Order Automation...")
            
            # Initialize Stagehand
            await self.initialize_stagehand()
            
            # Login
            login_success = await self.login_to_amazon()
            if not login_success:
                logger.error("Login failed, aborting automation")
                return
            
            # Scrape orders
            orders = await self.scrape_recent_orders(max_orders)
            
            if orders:
                # Generate PDF report
                pdf_path = self.generate_pdf_report(orders)
                logger.info(f"Automation completed! Report: {pdf_path}")
            else:
                logger.warning("No orders found")
            
        except Exception as e:
            logger.error(f"Automation failed: {e}")
            if self.stagehand:
                await self.stagehand.page.screenshot(
                    path=str(self.screenshots_dir / "error_final.png")
                )
            raise
        
        finally:
            # Cleanup
            if self.stagehand:
                logger.info("Closing browser...")
                await self.stagehand.close()


async def main():
    """Main entry point."""
    from config.settings import STAGEHAND_CONFIG, MAX_ORDERS_TO_SCRAPE
    
    try:
        automation = AmazonOrderAutomation(config=STAGEHAND_CONFIG)
        await automation.run(max_orders=MAX_ORDERS_TO_SCRAPE)
        
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
    except Exception as e:
        logger.error(f"Automation error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
