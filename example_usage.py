"""
Example script showing how to use the Amazon Order Automation
Author: qm-somesh
Date: 2025-10-23
"""

import asyncio
from src.amazon_automation import AmazonOrderAutomation
from config.settings import STAGEHAND_CONFIG, MAX_ORDERS_TO_SCRAPE


async def example_basic_usage():
    """Basic usage example."""
    print("Example 1: Basic Usage")
    print("-" * 50)
    
    automation = AmazonOrderAutomation(config=STAGEHAND_CONFIG)
    await automation.run(max_orders=5)


async def example_custom_config():
    """Example with custom configuration."""
    print("\nExample 2: Custom Configuration")
    print("-" * 50)
    
    custom_config = {
        'headless': True,  # Run in headless mode
        'enable_caching': True,
        'verbose': 2  # Maximum verbosity
    }
    
    automation = AmazonOrderAutomation(config=custom_config)
    await automation.run(max_orders=20)


async def example_error_handling():
    """Example with error handling."""
    print("\nExample 3: Error Handling")
    print("-" * 50)
    
    try:
        automation = AmazonOrderAutomation(config=STAGEHAND_CONFIG)
        await automation.run(max_orders=10)
        print("✓ Automation completed successfully!")
        
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
    except Exception as e:
        print(f"✗ Automation error: {e}")
        print("Check screenshots/ folder for debug information")


async def example_step_by_step():
    """Example running steps individually."""
    print("\nExample 4: Step-by-Step Execution")
    print("-" * 50)
    
    automation = AmazonOrderAutomation(config=STAGEHAND_CONFIG)
    
    try:
        # Initialize
        print("1. Initializing Stagehand...")
        await automation.initialize_stagehand()
        
        # Login
        print("2. Logging in...")
        login_success = await automation.login_to_amazon()
        
        if login_success:
            print("✓ Login successful")
            
            # Scrape orders
            print("3. Scraping orders...")
            orders = await automation.scrape_recent_orders(max_orders=5)
            print(f"✓ Found {len(orders)} orders")
            
            # Generate report
            if orders:
                print("4. Generating PDF report...")
                pdf_path = automation.generate_pdf_report(orders)
                print(f"✓ Report saved: {pdf_path}")
        else:
            print("✗ Login failed")
            
    finally:
        if automation.stagehand:
            await automation.stagehand.close()


def main():
    """Run examples."""
    print("=" * 50)
    print("Amazon Order Automation - Usage Examples")
    print("=" * 50)
    
    # Choose which example to run
    print("\nSelect example to run:")
    print("1. Basic Usage")
    print("2. Custom Configuration")
    print("3. Error Handling")
    print("4. Step-by-Step Execution")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    examples = {
        '1': example_basic_usage,
        '2': example_custom_config,
        '3': example_error_handling,
        '4': example_step_by_step
    }
    
    example_func = examples.get(choice)
    
    if example_func:
        asyncio.run(example_func())
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
