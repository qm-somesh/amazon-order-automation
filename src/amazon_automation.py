"""
Amazon India Order Automation with Playwright
Author: qm-somesh
Date: 2025-10-23

This script uses Playwright for browser automation to:
- Login to Amazon India
- Extract recent order details
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
from playwright.async_api import async_playwright, Page, Browser

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
    Amazon Order Automation using Playwright for browser control.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the automation with configuration."""
        self.config = config or {}
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
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
    
    async def initialize_browser(self, playwright):
        """Initialize Playwright browser."""
        try:
            logger.info("Initializing browser...")
            
            # Launch browser
            self.browser = await playwright.chromium.launch(
                headless=self.config.get('headless', False),
                slow_mo=100  # Slow down by 100ms for stability
            )
            
            # Create context with viewport
            context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
            
            # Create page
            self.page = await context.new_page()
            logger.info("Browser initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise
    
    async def login_to_amazon(self) -> bool:
        """
        Login to Amazon India.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            logger.info("Navigating to Amazon India...")
            await self.page.goto("https://www.amazon.in", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(2)
            
            # Take screenshot before login
            await self.page.screenshot(path=str(self.screenshots_dir / "01_homepage.png"))
            
            # Click sign-in button
            logger.info("Looking for sign-in button...")
            try:
                # Try different possible selectors for sign-in
                await self.page.click("#nav-link-accountList", timeout=10000)
            except:
                try:
                    # Alternative selector
                    await self.page.click("a[data-nav-role='signin']", timeout=10000)
                except:
                    # Another alternative
                    await self.page.click("text=Sign in", timeout=10000)
            
            # Wait for login page
            await asyncio.sleep(2)
            await self.page.screenshot(path=str(self.screenshots_dir / "02_login_page.png"))
            
            # Enter email
            logger.info("Entering email...")
            await self.page.fill("input[type='email'], input[name='email'], #ap_email", self.email, timeout=10000)
            await self.page.click("input[type='submit'], #continue", timeout=10000)
            
            # Wait for password page
            await asyncio.sleep(2)
            await self.page.screenshot(path=str(self.screenshots_dir / "03_password_page.png"))
            
            # Enter password
            logger.info("Entering password...")
            await self.page.fill("input[type='password'], input[name='password'], #ap_password", self.password, timeout=10000)
            await self.page.click("input[type='submit'], #signInSubmit", timeout=10000)
            
            # Wait for login to complete
            await asyncio.sleep(3)
            await self.page.screenshot(path=str(self.screenshots_dir / "04_logged_in.png"))
            
            # Verify login success by checking for account element
            logger.info("Verifying login...")
            try:
                # Check if we're logged in by looking for account/hello element
                account_elem = await self.page.query_selector("#nav-link-accountList")
                if account_elem:
                    logger.info("Login successful!")
                    return True
                else:
                    logger.warning("Login verification failed")
                    return False
            except:
                logger.warning("Could not verify login")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            await self.page.screenshot(path=str(self.screenshots_dir / "error_login.png"))
            return False
    
    async def scrape_recent_orders(self, max_orders: int = 10) -> List[Dict]:
        """
        Scrape recent orders from Amazon.
        
        Args:
            max_orders: Maximum number of orders to scrape
            
        Returns:
            List of order dictionaries
        """
        try:
            logger.info("Navigating to orders page...")
            
            # Navigate to orders page
            try:
                await self.page.click("#nav-orders", timeout=10000)
                await asyncio.sleep(2)
            except:
                # Alternative: direct URL navigation
                await self.page.goto("https://www.amazon.in/gp/your-account/order-history", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
            
            # Wait for orders page to load
            await asyncio.sleep(2)
            await self.page.screenshot(path=str(self.screenshots_dir / "05_orders_page.png"))
            
            logger.info(f"Extracting up to {max_orders} recent orders...")
            
            # Extract order cards
            order_cards = await self.page.query_selector_all(".order-card, .order")
            
            if not order_cards:
                # Try alternative selector
                order_cards = await self.page.query_selector_all("[data-order-id]")
            
            orders_data = []
            for idx, card in enumerate(order_cards[:max_orders]):
                try:
                    order_info = await self._extract_order_info(card, idx + 1)
                    if order_info:
                        orders_data.append(order_info)
                except Exception as e:
                    logger.warning(f"Failed to extract order {idx + 1}: {e}")
                    continue
            
            self.orders_data = orders_data
            logger.info(f"Successfully extracted {len(self.orders_data)} orders")
            
            # Save raw JSON data
            if self.orders_data:
                json_path = self.output_dir / f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(self.orders_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved JSON data to {json_path}")
            
            return self.orders_data
                
        except Exception as e:
            logger.error(f"Failed to scrape orders: {e}")
            await self.page.screenshot(path=str(self.screenshots_dir / "error_scraping.png"))
            return []
    
    async def _extract_order_info(self, card, index: int) -> Optional[Dict]:
        """Extract information from a single order card."""
        try:
            # Extract order number
            order_number = "N/A"
            order_elem = await card.query_selector(".order-info, [data-order-id], .yohtmlc-order-id")
            if order_elem:
                order_text = await order_elem.inner_text()
                # Extract order number from text
                if "ORDER" in order_text or "#" in order_text:
                    order_number = order_text.split()[-1] if order_text else f"ORDER-{index}"
                else:
                    order_number = f"ORDER-{index}"
            else:
                order_number = f"ORDER-{index}"
            
            # Extract date
            order_date = "N/A"
            date_elem = await card.query_selector(".order-date, .a-color-secondary")
            if date_elem:
                order_date = (await date_elem.inner_text()).strip()
            
            # Extract product name
            product_name = "N/A"
            product_elem = await card.query_selector(".product-title, .yohtmlc-product-title, a.a-link-normal")
            if product_elem:
                product_name = (await product_elem.inner_text()).strip()
            
            # Extract amount
            total_amount = "N/A"
            amount_elem = await card.query_selector(".order-total, .yohtmlc-order-total, .a-color-price")
            if amount_elem:
                total_amount = (await amount_elem.inner_text()).strip()
            
            # Extract status
            status = "N/A"
            status_elem = await card.query_selector(".order-status, .delivery-box")
            if status_elem:
                status = (await status_elem.inner_text()).strip()
            
            # Extract delivery date
            delivery_date = "N/A"
            delivery_elem = await card.query_selector(".delivery-date, .shipment")
            if delivery_elem:
                delivery_date = (await delivery_elem.inner_text()).strip()
            
            return {
                'order_number': order_number,
                'order_date': order_date,
                'product_name': product_name,
                'total_amount': total_amount,
                'status': status,
                'delivery_date': delivery_date
            }
            
        except Exception as e:
            logger.error(f"Error extracting order info: {e}")
            return None
    
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
        
        # Configure wkhtmltopdf path
        import platform
        if platform.system() == "Windows":
            wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            if Path(wkhtmltopdf_path).exists():
                config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            else:
                config = None
        else:
            config = None
        
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
            if config:
                pdfkit.from_string(html_content, str(pdf_path), options=pdf_options, configuration=config)
            else:
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
        playwright = None
        try:
            logger.info("Starting Amazon Order Automation...")
            
            # Initialize Playwright
            playwright = await async_playwright().start()
            await self.initialize_browser(playwright)
            
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
            if self.page:
                await self.page.screenshot(path=str(self.screenshots_dir / "error_final.png"))
            raise
        
        finally:
            # Cleanup
            if self.browser:
                logger.info("Closing browser...")
                await self.browser.close()
            if playwright:
                await playwright.stop()


async def main():
    """Main entry point."""
    import sys
    from pathlib import Path
    
    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    try:
        from config.settings import STAGEHAND_CONFIG, MAX_ORDERS_TO_SCRAPE
        
        automation = AmazonOrderAutomation(config=STAGEHAND_CONFIG)
        await automation.run(max_orders=MAX_ORDERS_TO_SCRAPE)
        
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
    except Exception as e:
        logger.error(f"Automation error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
