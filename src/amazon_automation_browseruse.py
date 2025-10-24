"""
Amazon India Order Automation with Browser Use (AI-Powered)
Author: qm-somesh
Date: 2025-10-24

This script uses Browser Use AI Agent for intelligent browser automation to:
- Login to Amazon India using natural language commands
- Extract recent order details using AI-powered extraction
- Generate professional PDF reports
- Create JSON backups of order data

Key Advantages over Playwright:
- Natural language commands instead of brittle selectors
- Self-healing: adapts to Amazon UI changes automatically
- AI-powered element detection
- Built-in error recovery
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pdfkit
from browser_use import Agent, Browser, Tools, ActionResult
from browser_use.llm.google.chat import ChatGoogle
from dotenv import load_dotenv

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('amazon_automation_browseruse.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AmazonOrderAutomationBrowserUse:
    """
    Amazon Order Automation using Browser Use AI Agent.
    
    Uses natural language commands and AI-powered element detection,
    making the automation resilient to UI changes.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the automation with configuration."""
        self.config = config or {}
        self.orders_data = []
        
        # Get credentials from environment
        self.email = os.getenv('AMAZON_EMAIL')
        self.password = os.getenv('AMAZON_PASSWORD')
        
        if not self.email or not self.password:
            raise ValueError("Amazon credentials not found in environment variables")
        
        # Create output directories
        self.output_dir = Path('output')
        self.screenshots_dir = Path('screenshots_browseruse')
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Setup Browser Use custom tools
        self.tools = Tools()
        self._setup_custom_tools()
        
        logger.info("AmazonOrderAutomationBrowserUse initialized with AI agent")
    
    def _setup_custom_tools(self):
        """Setup custom tools for Browser Use agent."""
        
        @self.tools.action(description='Save extracted order data as JSON file')
        def save_orders_json(orders_json: str) -> ActionResult:
            """Save orders to JSON file."""
            try:
                orders = json.loads(orders_json)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                json_path = self.output_dir / f"orders_browseruse_{timestamp}.json"
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(orders, f, indent=2, ensure_ascii=False)
                
                self.orders_data = orders
                logger.info(f"Saved {len(orders)} orders to {json_path}")
                
                return ActionResult(
                    extracted_content=f"Successfully saved {len(orders)} orders to {json_path}",
                    include_in_memory=True
                )
            except Exception as e:
                logger.error(f"Failed to save JSON: {e}")
                return ActionResult(
                    extracted_content=f"Error saving JSON: {str(e)}",
                    error=str(e)
                )
        
        @self.tools.action(description='Generate PDF report from order data')
        def generate_pdf_report_tool(orders_json: str) -> ActionResult:
            """Generate PDF report from orders."""
            try:
                orders = json.loads(orders_json)
                pdf_path = self.generate_pdf_report(orders)
                
                return ActionResult(
                    extracted_content=f"Successfully generated PDF report: {pdf_path}",
                    include_in_memory=True,
                    is_done=True
                )
            except Exception as e:
                logger.error(f"Failed to generate PDF: {e}")
                return ActionResult(
                    extracted_content=f"Error generating PDF: {str(e)}",
                    error=str(e)
                )
    
    def generate_pdf_report(self, orders: List[Dict]) -> str:
        """
        Generate a professional PDF report of orders.
        
        Args:
            orders: List of order dictionaries
            
        Returns:
            Path to generated PDF file
        """
        if not orders:
            logger.warning("No orders to generate report")
            return ""
        
        logger.info("Generating PDF report...")
        
        # Create HTML content
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
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"amazon_orders_browseruse_{timestamp}.pdf"
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
                <td><strong>{order.get('order_number', 'N/A')}</strong></td>
                <td>{order.get('order_date', 'N/A')}</td>
                <td>{order.get('product_name', 'N/A')}</td>
                <td>{order.get('total_amount', 'N/A')}</td>
                <td><span class="status-{order.get('status', 'unknown').lower().replace(' ', '-')}">{order.get('status', 'N/A')}</span></td>
                <td>{order.get('delivery_date', 'N/A')}</td>
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
                    background: linear-gradient(135deg, #FF9900 0%, #FF6600 100%);
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
                .badge {{
                    background: rgba(255,255,255,0.2);
                    padding: 5px 15px;
                    border-radius: 20px;
                    display: inline-block;
                    margin-top: 10px;
                    font-size: 12px;
                }}
                .summary {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    border-left: 4px solid #FF9900;
                }}
                .summary h2 {{
                    margin: 0 0 15px 0;
                    color: #FF9900;
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
                    background: #FF9900;
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
                    background: #fff8f0;
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
                .status-pending {{
                    background: #cce5ff;
                    color: #004085;
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
                <span class="badge">🤖 Powered by Browser Use AI</span>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Total Orders:</strong> {len(orders)}</p>
                <p><strong>Report Period:</strong> Recent orders</p>
                <p><strong>Automation:</strong> AI-Powered Browser Use Agent</p>
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
                <p>This report was generated automatically using Browser Use AI Agent</p>
                <p>Amazon Order Automation © 2025 qm-somesh</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    async def run(self, max_orders: int = 10):
        """
        Run the complete automation workflow using Browser Use AI Agent.
        
        Args:
            max_orders: Maximum number of orders to extract
        """
        logger.info("🤖 Starting Amazon Order Automation with Browser Use AI...")
        
        try:
            # Create Browser instance
            browser = Browser(
                headless=self.config.get('headless', False),
                keep_alive=False,
                disable_security=False,
            )
            
            # Create AI-powered task with natural language
            task = f"""
            You are automating Amazon India order extraction. Follow these steps:
            
            1. Navigate to https://www.amazon.in
            
            2. Sign in to Amazon using these credentials:
               - Email/Phone: {self.email}
               - Password: {self.password}
               (Handle any 2FA, captcha, or security challenges if they appear)
            
            3. After successful login, navigate to "Returns & Orders" section
            
            4. Extract information from the {max_orders} most recent orders visible on the page.
               For each order, extract:
               - order_number: The order ID/number
               - order_date: When the order was placed
               - product_name: Name of the product(s)
               - total_amount: Total price paid
               - status: Order status (Delivered, Shipped, Pending, etc.)
               - delivery_date: When it was/will be delivered
            
            5. Format the extracted data as a JSON array of order objects
            
            6. Call the 'save_orders_json' tool with the JSON data
            
            7. Call the 'generate_pdf_report_tool' tool with the same JSON data
            
            8. Confirm completion with a summary
            
            Important notes:
            - Be patient with page loads
            - Look for order cards or order history items
            - Extract clean, accurate data
            - Handle any popups or dialogs that appear
            """
            
            # Get Google Gemini API key
            gemini_key = os.getenv('GOOGLE_API_KEY')
            if not gemini_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")
            
            # Create AI Agent with Browser Use's native Google Gemini support
            agent = Agent(
                task=task,
                llm=ChatGoogle(
                    model='gemini-2.0-flash-exp',  # Using experimental (works with v1beta API)
                    api_key=gemini_key,
                    temperature=0.1  # Low temperature for more consistent results
                ),
                browser=browser,
                tools=self.tools,
                use_vision=True,  # Enable screenshot analysis
                max_actions_per_step=3,  # Allow multiple actions per step
                save_conversation_path=self.screenshots_dir / f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            # Run the agent
            logger.info("🚀 Launching Browser Use AI Agent...")
            result = await agent.run(max_steps=30)
            
            logger.info("✅ Automation completed successfully!")
            logger.info(f"📊 Extracted {len(self.orders_data)} orders")
            
            if self.orders_data:
                logger.info(f"📄 Reports saved in: {self.output_dir}")
                logger.info(f"📸 Screenshots saved in: {self.screenshots_dir}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Automation failed: {e}", exc_info=True)
            raise


async def main():
    """Main entry point."""
    from config.settings import STAGEHAND_CONFIG, MAX_ORDERS_TO_SCRAPE
    
    try:
        automation = AmazonOrderAutomationBrowserUse(config=STAGEHAND_CONFIG)
        await automation.run(max_orders=MAX_ORDERS_TO_SCRAPE)
        
    except KeyboardInterrupt:
        logger.info("⚠️ Automation interrupted by user")
    except Exception as e:
        logger.error(f"❌ Automation error: {e}", exc_info=True)


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Amazon Order Automation - Browser Use AI Version")
    print("=" * 60)
    asyncio.run(main())
