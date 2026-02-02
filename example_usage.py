"""
Example Usage of Exhibition Scraper

This file demonstrates how to use the exhibition scraper with different configurations.
"""

# ============================================================================
# EXAMPLE 1: Basic Usage
# ============================================================================

# 1. Edit exhibition_scraper.py
# 2. Update the target_url variable:
#    target_url = "https://www.example-exhibitions.com/trade-shows"
# 3. Run the script:
#    python exhibition_scraper.py

# ============================================================================
# EXAMPLE 2: Using Custom ChromeDriver Path
# ============================================================================

# If you have chromedriver installed in the same folder:
# In exhibition_scraper.py CONFIG section:
# CHROMEDRIVER_PATH = "./chromedriver"  # Linux/Mac
# Or
# CHROMEDRIVER_PATH = "./chromedriver.exe"  # Windows

# If you have chromedriver installed in a specific location:
# CHROMEDRIVER_PATH = "C:/tools/chromedriver.exe"  # Windows full path
# CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # Linux/Mac full path

# To verify your chromedriver:
# On Linux/Mac: ls -la chromedriver
# On Windows: dir chromedriver.exe
# Make sure it has execute permissions on Linux/Mac: chmod +x chromedriver

# ============================================================================
# EXAMPLE 3: Using with Proxy
# ============================================================================

# In exhibition_scraper.py, uncomment and configure:
# PROXY = "http://proxy.example.com:8080"
# 
# In setup_driver() function, uncomment:
# chrome_options.add_argument(f'--proxy-server={PROXY}')

# ============================================================================
# EXAMPLE 4: Headless Mode (No Browser Window)
# ============================================================================

# In setup_driver() function, uncomment:
# chrome_options.add_argument('--headless')

# ============================================================================
# EXAMPLE 5: Custom Delays for Slower Websites
# ============================================================================

# In exhibition_scraper.py CONFIG section, modify:
# MIN_DELAY = 5  # Increase from 2 to 5 seconds
# MAX_DELAY = 10  # Increase from 5 to 10 seconds
# TIMEOUT = 30  # Increase from 15 to 30 seconds

# ============================================================================
# EXAMPLE 6: Resuming After Interruption
# ============================================================================

# 1. Open exhibitions_data.csv
# 2. Note the last exhibition scraped
# 3. Manually navigate to that page on the website
# 4. Update target_url to that specific page
# 5. Run the script again

# Example:
# If you scraped pages 1-5 and it crashed, check CSV for last entry
# Then update target_url to page 6:
# target_url = "https://www.example-exhibitions.com/trade-shows?page=6"

# ============================================================================
# EXAMPLE 7: Checking Failed URLs
# ============================================================================

# After scraping completes, review failed_urls.txt:
# cat failed_urls.txt

# Or in Python:
"""
with open('failed_urls.txt', 'r') as f:
    for line in f:
        print(line.strip())
"""

# ============================================================================
# EXAMPLE 8: Custom CSV Filename
# ============================================================================

# In exhibition_scraper.py CONFIG section:
# CSV_FILENAME = "my_custom_exhibitions_2024.csv"

# ============================================================================
# EXAMPLE 9: Programmatic Usage (Import as Module)
# ============================================================================

"""
from exhibition_scraper import (
    setup_driver,
    scrape_listing_page,
    initialize_csv
)

# Setup
driver = setup_driver()
initialize_csv()

# Navigate to custom URL
driver.get("https://example.com/exhibitions")

# Scrape single page
exhibitions_count = scrape_listing_page(driver)
print(f"Scraped {exhibitions_count} exhibitions")

# Cleanup
driver.quit()
"""

# ============================================================================
# EXAMPLE 10: Testing with Small Sample
# ============================================================================

# To test without scraping all pages, modify the main() function:
# In the pagination loop, add a page limit:

"""
# In main() function, after page_number initialization:
MAX_PAGES_TO_SCRAPE = 2  # Only scrape 2 pages for testing

# Then in the while loop:
while page_number <= MAX_PAGES_TO_SCRAPE:
    # ... existing code ...
"""

# ============================================================================
# EXAMPLE 11: Monitoring Progress
# ============================================================================

# Watch the log file in real-time:
# On Linux/Mac:
# tail -f scraper.log

# On Windows (PowerShell):
# Get-Content scraper.log -Wait

# Or check CSV row count:
# On Linux/Mac:
# wc -l exhibitions_data.csv

# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
1. Always test with a small sample first (1-2 pages)
2. Check the website's robots.txt before scraping
3. Use appropriate delays to avoid overloading servers
4. Monitor the script during initial runs
5. Keep backup copies of CSV files
6. Review failed_urls.txt after each run
7. Respect the website's Terms of Service
8. Use proxy rotation for large-scale scraping
9. Run during off-peak hours when possible
10. Keep Chrome browser updated
"""

# ============================================================================
# TROUBLESHOOTING COMMON ISSUES
# ============================================================================

"""
Issue 1: Chrome driver version mismatch
Solution: Update Chrome browser or use webdriver-manager (already included)

Issue 2: Elements not found
Solution: Increase TIMEOUT value or check if website structure changed

Issue 3: Bot detection
Solution: Increase delays, use proxy, avoid headless mode

Issue 4: Stale element references
Solution: Already handled in code with retry logic

Issue 5: CSV encoding issues
Solution: Script uses UTF-8, ensure your viewer supports it

Issue 6: Memory issues on large scrapes
Solution: Process in batches by setting max pages limit
"""

print("Review the examples above and modify exhibition_scraper.py accordingly")
