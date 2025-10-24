"""
Amazon Order Automation Launcher
Author: qm-somesh
Date: 2025-10-24

This script allows you to choose between different automation implementations:
1. Playwright - Fast, direct browser control with CSS selectors
2. Browser Use - AI-powered natural language automation

Usage:
    python run.py --mode playwright
    python run.py --mode browseruse
    python run.py --mode both  # Run both and compare
"""

import asyncio
import argparse
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def setup_colored_logging():
    """Setup colored console output (simplified without colorlog dependency)."""
    import logging
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


async def run_playwright():
    """Run the Playwright version."""
    print("\n" + "="*60)
    print("🎭 Running Playwright Version")
    print("="*60 + "\n")
    
    from amazon_automation import AmazonOrderAutomation, main
    
    start_time = time.time()
    try:
        await main()
        elapsed = time.time() - start_time
        print(f"\n✅ Playwright completed in {elapsed:.2f} seconds")
        return True, elapsed
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Playwright failed after {elapsed:.2f} seconds: {e}")
        return False, elapsed


async def run_browseruse():
    """Run the Browser Use version."""
    print("\n" + "="*60)
    print("🤖 Running Browser Use AI Version")
    print("="*60 + "\n")
    
    from amazon_automation_browseruse import AmazonOrderAutomationBrowserUse, main
    
    start_time = time.time()
    try:
        await main()
        elapsed = time.time() - start_time
        print(f"\n✅ Browser Use completed in {elapsed:.2f} seconds")
        return True, elapsed
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Browser Use failed after {elapsed:.2f} seconds: {e}")
        return False, elapsed


async def run_both():
    """Run both versions and compare."""
    print("\n" + "="*70)
    print("🔄 Running Both Implementations for Comparison")
    print("="*70 + "\n")
    
    results = {}
    
    # Run Playwright
    print("\n📊 Test 1/2: Playwright Implementation")
    print("-" * 70)
    pw_success, pw_time = await run_playwright()
    results['playwright'] = {'success': pw_success, 'time': pw_time}
    
    print("\n⏳ Waiting 5 seconds before next test...\n")
    await asyncio.sleep(5)
    
    # Run Browser Use
    print("\n📊 Test 2/2: Browser Use Implementation")
    print("-" * 70)
    bu_success, bu_time = await run_browseruse()
    results['browseruse'] = {'success': bu_success, 'time': bu_time}
    
    # Print comparison
    print("\n" + "="*70)
    print("📈 COMPARISON RESULTS")
    print("="*70)
    
    print(f"\n{'Implementation':<20} {'Status':<15} {'Time':<15} {'Notes'}")
    print("-" * 70)
    
    pw_status = "✅ Success" if pw_success else "❌ Failed"
    bu_status = "✅ Success" if bu_success else "❌ Failed"
    
    print(f"{'Playwright':<20} {pw_status:<15} {pw_time:>6.2f}s       Fast, direct control")
    print(f"{'Browser Use AI':<20} {bu_status:<15} {bu_time:>6.2f}s       AI-powered, adaptive")
    
    if pw_success and bu_success:
        faster = "Playwright" if pw_time < bu_time else "Browser Use"
        diff = abs(pw_time - bu_time)
        print(f"\n🏆 Winner: {faster} (faster by {diff:.2f} seconds)")
    
    print("\n💡 Key Differences:")
    print("   • Playwright: Uses CSS selectors, faster but brittle")
    print("   • Browser Use: Uses AI + natural language, more reliable")
    print("\n" + "="*70 + "\n")


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print(" " * 15 + "🚀 AMAZON ORDER AUTOMATION")
    print(" " * 20 + "Dual Implementation Launcher")
    print("="*70)
    print("\nAvailable Implementations:")
    print("  1. 🎭 Playwright    - Fast, direct browser control")
    print("  2. 🤖 Browser Use   - AI-powered natural language automation")
    print("  3. 🔄 Both          - Run and compare both implementations")
    print("="*70 + "\n")


def main():
    """Main launcher function."""
    setup_colored_logging()
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Launch Amazon Order Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --mode playwright    # Use Playwright (fast, traditional)
  python run.py --mode browseruse    # Use Browser Use (AI-powered)
  python run.py --mode both          # Run both and compare results

Default: Playwright
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['playwright', 'browseruse', 'both'],
        default='playwright',
        help='Choose automation implementation (default: playwright)'
    )
    
    args = parser.parse_args()
    
    print(f"🎯 Selected Mode: {args.mode.upper()}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        if args.mode == 'playwright':
            asyncio.run(run_playwright())
        elif args.mode == 'browseruse':
            asyncio.run(run_browseruse())
        elif args.mode == 'both':
            asyncio.run(run_both())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
    
    print(f"\n⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
