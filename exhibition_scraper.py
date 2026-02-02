"""
Exhibition/Trade Show Web Scraper using Selenium

A robust Python + Selenium automation script that scrapes exhibition/trade show data
from a website with anti-bot avoidance, pagination handling, and real-time CSV export.

Author: Automation Team
Date: 2026-02-02
"""

import csv
import os
import random
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Target URL - Replace with your actual URL
target_url = "PASTE_PAGE_URL_HERE"

# CSV Configuration
CSV_FILENAME = "exhibitions_data.csv"
CSV_HEADERS = [
    "Exhibition Name",
    "Cycle",
    "Venue",
    "Date",
    "Description",
    "Related Industries",
    "Audience",
    "City",
    "Organizers",
    "Source URL"
]

# Failed URLs log file
FAILED_URLS_FILE = "failed_urls.txt"

# Scraping Configuration
TABLE_CLASS_NAME = "tradeshows"
NEXT_BUTTON_CLASS = "pages-links"
TIMEOUT = 15  # seconds
MIN_DELAY = 2  # seconds
MAX_DELAY = 5  # seconds

# ChromeDriver Configuration (Optional - Uncomment to use custom path)
# If you have chromedriver in the same folder or a specific location, set the path here
# Leave as None to use webdriver-manager for automatic driver management
CHROMEDRIVER_PATH = None  # Example: "./chromedriver" or "C:/path/to/chromedriver.exe"

# Proxy Configuration (Optional - Uncomment to use)
# PROXY = "http://your-proxy-server:port"
# PROXY_AUTH = {"username": "user", "password": "pass"}  # if needed

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# DRIVER SETUP
# ============================================================================

def setup_driver() -> webdriver.Chrome:
    """
    Setup Chrome WebDriver with anti-bot detection measures.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    logger.info("Setting up Chrome WebDriver...")
    
    # Chrome options for anti-bot avoidance
    chrome_options = Options()
    
    # Disable automation flags
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Set realistic User-Agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Additional stealth options
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    
    # Uncomment for headless mode (not recommended for anti-bot)
    # chrome_options.add_argument('--headless')
    
    # Proxy configuration (if needed)
    # Uncomment and configure the proxy settings below
    # if 'PROXY' in globals():
    #     chrome_options.add_argument(f'--proxy-server={PROXY}')
    
    # Initialize driver
    # Priority: 1. Custom path (if provided), 2. webdriver-manager, 3. System driver
    try:
        if CHROMEDRIVER_PATH and os.path.exists(CHROMEDRIVER_PATH):
            # Use custom ChromeDriver path
            logger.info(f"Using custom ChromeDriver from: {CHROMEDRIVER_PATH}")
            service = Service(executable_path=CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # Use webdriver-manager for automatic driver management
            logger.info("Using webdriver-manager for automatic ChromeDriver management")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logger.error(f"Failed to initialize driver: {e}")
        logger.info("Attempting to use system Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
    
    # Override navigator.webdriver flag
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    logger.info("Chrome WebDriver setup complete")
    return driver


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def human_delay(min_sec: float = MIN_DELAY, max_sec: float = MAX_DELAY) -> None:
    """
    Add random delay to simulate human behavior.
    
    Args:
        min_sec: Minimum delay in seconds
        max_sec: Maximum delay in seconds
    """
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)


def smooth_scroll(driver: webdriver.Chrome, element=None) -> None:
    """
    Scroll to element smoothly to simulate human behavior.
    
    Args:
        driver: WebDriver instance
        element: Element to scroll to (optional)
    """
    try:
        if element:
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            # Random scroll
            scroll_amount = random.randint(200, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        
        human_delay(0.5, 1.5)
    except Exception as e:
        logger.warning(f"Scroll error: {e}")


def safe_get_text(element) -> str:
    """
    Safely extract text from element with whitespace handling.
    
    Args:
        element: Selenium WebElement
        
    Returns:
        str: Cleaned text or empty string
    """
    try:
        return element.text.strip() if element else ""
    except Exception:
        return ""


def safe_click(driver: webdriver.Chrome, element) -> bool:
    """
    Safely click element using ActionChains with human-like behavior.
    
    Args:
        driver: WebDriver instance
        element: Element to click
        
    Returns:
        bool: True if click successful, False otherwise
    """
    try:
        # Scroll to element
        smooth_scroll(driver, element)
        human_delay(0.5, 1.0)
        
        # Use ActionChains for human-like click
        actions = ActionChains(driver)
        actions.move_to_element(element)
        human_delay(0.3, 0.7)
        actions.click()
        actions.perform()
        
        return True
    except Exception as e:
        logger.warning(f"Click failed: {e}")
        return False


def log_failed_url(url: str, reason: str) -> None:
    """
    Log failed URLs to a text file.
    
    Args:
        url: Failed URL
        reason: Reason for failure
    """
    try:
        with open(FAILED_URLS_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} | {url} | {reason}\n")
    except Exception as e:
        logger.error(f"Failed to log URL: {e}")


# ============================================================================
# CSV EXPORT
# ============================================================================

def initialize_csv() -> None:
    """
    Initialize CSV file with headers if it doesn't exist.
    Checks if file exists to avoid duplicate headers.
    """
    try:
        # Check if file exists and has content
        file_exists = os.path.exists(CSV_FILENAME) and os.path.getsize(CSV_FILENAME) > 0
        
        if not file_exists:
            with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)
            logger.info(f"CSV file initialized: {CSV_FILENAME}")
        else:
            logger.info(f"CSV file already exists: {CSV_FILENAME}")
    except Exception as e:
        logger.error(f"Failed to initialize CSV: {e}")
        raise


def write_to_csv(data: Dict[str, str]) -> None:
    """
    Write exhibition data to CSV file immediately (append mode).
    This ensures data safety in case of interruption.
    
    Args:
        data: Dictionary containing exhibition data
    """
    try:
        with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            row = [
                data.get('Exhibition Name', ''),
                data.get('Cycle', ''),
                data.get('Venue', ''),
                data.get('Date', ''),
                data.get('Description', ''),
                data.get('Related Industries', ''),
                data.get('Audience', ''),
                data.get('City', ''),
                data.get('Organizers', ''),
                data.get('Source URL', '')
            ]
            writer.writerow(row)
        logger.info(f"Data written to CSV: {data.get('Exhibition Name', 'Unknown')}")
    except Exception as e:
        logger.error(f"Failed to write to CSV: {e}")


# ============================================================================
# DETAIL PAGE SCRAPING
# ============================================================================

def scrape_detail_page(driver: webdriver.Chrome, exhibition_url: str) -> Dict[str, str]:
    """
    Scrape exhibition detail page for additional information.
    
    Args:
        driver: WebDriver instance
        exhibition_url: URL of the exhibition detail page
        
    Returns:
        dict: Dictionary containing detail page data
    """
    detail_data = {
        'Description': '',
        'Related Industries': '',
        'Audience': '',
        'City': '',
        'Organizers': ''
    }
    
    try:
        logger.info(f"Scraping detail page: {exhibition_url}")
        
        # Wait for page to load
        human_delay(1, 2)
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Smooth scroll to simulate reading
        smooth_scroll(driver)
        human_delay(1, 2)
        
        # Try to find and extract detail information
        # NOTE: These selectors are generic and may need adjustment based on actual website structure
        
        # Description
        try:
            description_selectors = [
                (By.CLASS_NAME, "description"),
                (By.CLASS_NAME, "exhibition-description"),
                (By.XPATH, "//div[contains(@class, 'desc')]"),
                (By.XPATH, "//p[contains(text(), 'Description')]/following-sibling::*"),
            ]
            for by, selector in description_selectors:
                try:
                    element = driver.find_element(by, selector)
                    detail_data['Description'] = safe_get_text(element)
                    if detail_data['Description']:
                        break
                except NoSuchElementException:
                    continue
        except Exception as e:
            logger.debug(f"Description not found: {e}")
        
        # Related Industries
        try:
            industries_selectors = [
                (By.CLASS_NAME, "industries"),
                (By.CLASS_NAME, "related-industries"),
                (By.XPATH, "//div[contains(@class, 'industry')]"),
                (By.XPATH, "//*[contains(text(), 'Industries')]/following-sibling::*"),
            ]
            for by, selector in industries_selectors:
                try:
                    element = driver.find_element(by, selector)
                    detail_data['Related Industries'] = safe_get_text(element)
                    if detail_data['Related Industries']:
                        break
                except NoSuchElementException:
                    continue
        except Exception as e:
            logger.debug(f"Related Industries not found: {e}")
        
        # Audience
        try:
            audience_selectors = [
                (By.CLASS_NAME, "audience"),
                (By.CLASS_NAME, "target-audience"),
                (By.XPATH, "//*[contains(text(), 'Audience')]/following-sibling::*"),
            ]
            for by, selector in audience_selectors:
                try:
                    element = driver.find_element(by, selector)
                    detail_data['Audience'] = safe_get_text(element)
                    if detail_data['Audience']:
                        break
                except NoSuchElementException:
                    continue
        except Exception as e:
            logger.debug(f"Audience not found: {e}")
        
        # City
        try:
            city_selectors = [
                (By.CLASS_NAME, "city"),
                (By.CLASS_NAME, "location-city"),
                (By.XPATH, "//*[contains(text(), 'City')]/following-sibling::*"),
            ]
            for by, selector in city_selectors:
                try:
                    element = driver.find_element(by, selector)
                    detail_data['City'] = safe_get_text(element)
                    if detail_data['City']:
                        break
                except NoSuchElementException:
                    continue
        except Exception as e:
            logger.debug(f"City not found: {e}")
        
        # Organizers
        try:
            organizers_selectors = [
                (By.CLASS_NAME, "organizers"),
                (By.CLASS_NAME, "organizer"),
                (By.XPATH, "//*[contains(text(), 'Organizer')]/following-sibling::*"),
            ]
            for by, selector in organizers_selectors:
                try:
                    element = driver.find_element(by, selector)
                    detail_data['Organizers'] = safe_get_text(element)
                    if detail_data['Organizers']:
                        break
                except NoSuchElementException:
                    continue
        except Exception as e:
            logger.debug(f"Organizers not found: {e}")
        
        logger.info(f"Detail page scraped successfully")
        
    except TimeoutException:
        logger.error(f"Timeout loading detail page: {exhibition_url}")
        log_failed_url(exhibition_url, "Timeout loading page")
    except Exception as e:
        logger.error(f"Error scraping detail page: {e}")
        log_failed_url(exhibition_url, str(e))
    
    return detail_data


# ============================================================================
# LISTING PAGE SCRAPING
# ============================================================================

def scrape_listing_page(driver: webdriver.Chrome) -> int:
    """
    Scrape all exhibitions from the current listing page.
    
    Args:
        driver: WebDriver instance
        
    Returns:
        int: Number of exhibitions scraped from this page
    """
    exhibitions_scraped = 0
    
    try:
        # Wait for table to load
        logger.info("Waiting for table to load...")
        table = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, TABLE_CLASS_NAME))
        )
        
        human_delay()
        smooth_scroll(driver, table)
        
        # Find all rows in the table (skip header row)
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header
        logger.info(f"Found {len(rows)} rows on this page")
        
        # Process each row
        for idx, row in enumerate(rows, 1):
            try:
                logger.info(f"Processing row {idx}/{len(rows)}")
                
                # Refresh row reference to avoid stale element
                try:
                    # Re-find the table and row
                    table = driver.find_element(By.CLASS_NAME, TABLE_CLASS_NAME)
                    rows_fresh = table.find_elements(By.TAG_NAME, "tr")[1:]
                    row = rows_fresh[idx - 1]
                except StaleElementReferenceException:
                    logger.warning(f"Stale element at row {idx}, re-finding...")
                    table = driver.find_element(By.CLASS_NAME, TABLE_CLASS_NAME)
                    rows_fresh = table.find_elements(By.TAG_NAME, "tr")[1:]
                    row = rows_fresh[idx - 1]
                
                # Extract cells from the row
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) < 4:
                    logger.warning(f"Row {idx} has insufficient cells, skipping")
                    continue
                
                # Extract listing page data
                exhibition_data = {
                    'Exhibition Name': safe_get_text(cells[0]),
                    'Cycle': safe_get_text(cells[1]),
                    'Venue': safe_get_text(cells[2]),
                    'Date': safe_get_text(cells[3]),
                    'Source URL': driver.current_url
                }
                
                logger.info(f"Exhibition: {exhibition_data['Exhibition Name']}")
                
                # Find and click exhibition name link for detail page
                try:
                    # Look for link in first cell
                    link = cells[0].find_element(By.TAG_NAME, "a")
                    exhibition_url = link.get_attribute('href')
                    
                    # Store current window handle
                    main_window = driver.current_window_handle
                    
                    # Click the link
                    smooth_scroll(driver, link)
                    if safe_click(driver, link):
                        human_delay(2, 3)
                        
                        # Check if new window/tab opened
                        if len(driver.window_handles) > 1:
                            # Switch to new window
                            driver.switch_to.window(driver.window_handles[-1])
                            
                            # Scrape detail page
                            detail_data = scrape_detail_page(driver, exhibition_url)
                            
                            # Close detail page and switch back
                            driver.close()
                            driver.switch_to.window(main_window)
                        else:
                            # Same window navigation
                            detail_data = scrape_detail_page(driver, exhibition_url)
                            
                            # Navigate back to listing page
                            driver.back()
                            human_delay(2, 3)
                            
                            # Wait for table to reload
                            WebDriverWait(driver, TIMEOUT).until(
                                EC.presence_of_element_located((By.CLASS_NAME, TABLE_CLASS_NAME))
                            )
                        
                        # Merge detail data with listing data
                        exhibition_data.update(detail_data)
                    
                except NoSuchElementException:
                    logger.warning(f"No link found in row {idx}")
                except Exception as e:
                    logger.error(f"Error accessing detail page for row {idx}: {e}")
                
                # Write data to CSV immediately
                write_to_csv(exhibition_data)
                exhibitions_scraped += 1
                
                # Human-like delay between rows
                human_delay()
                
            except StaleElementReferenceException:
                logger.error(f"Stale element exception for row {idx}, skipping")
                continue
            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
                log_failed_url(driver.current_url, f"Row {idx}: {str(e)}")
                continue
        
        logger.info(f"Scraped {exhibitions_scraped} exhibitions from this page")
        
    except TimeoutException:
        logger.error("Timeout waiting for table to load")
    except NoSuchElementException:
        logger.error(f"Table with class '{TABLE_CLASS_NAME}' not found")
    except Exception as e:
        logger.error(f"Error scraping listing page: {e}")
    
    return exhibitions_scraped


# ============================================================================
# PAGINATION HANDLING
# ============================================================================

def has_next_page(driver: webdriver.Chrome) -> bool:
    """
    Check if NEXT button exists and is clickable.
    
    Args:
        driver: WebDriver instance
        
    Returns:
        bool: True if NEXT button is available, False otherwise
    """
    try:
        # Scroll to bottom of page where pagination usually is
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(1, 2)
        
        # Find NEXT button
        next_buttons = driver.find_elements(By.CLASS_NAME, NEXT_BUTTON_CLASS)
        
        for button in next_buttons:
            button_text = safe_get_text(button).lower()
            if 'next' in button_text:
                # Check if button is enabled (not disabled)
                is_disabled = 'disabled' in button.get_attribute('class').lower() or \
                             button.get_attribute('disabled') == 'true'
                
                if not is_disabled:
                    logger.info("NEXT button found and enabled")
                    return True
        
        logger.info("NEXT button not found or disabled")
        return False
        
    except Exception as e:
        logger.warning(f"Error checking for NEXT button: {e}")
        return False


def click_next_page(driver: webdriver.Chrome) -> bool:
    """
    Click the NEXT button to navigate to next page.
    
    Args:
        driver: WebDriver instance
        
    Returns:
        bool: True if successfully navigated to next page, False otherwise
    """
    try:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(1, 2)
        
        # Find and click NEXT button
        next_buttons = driver.find_elements(By.CLASS_NAME, NEXT_BUTTON_CLASS)
        
        for button in next_buttons:
            button_text = safe_get_text(button).lower()
            if 'next' in button_text:
                # Check if button is enabled
                is_disabled = 'disabled' in button.get_attribute('class').lower() or \
                             button.get_attribute('disabled') == 'true'
                
                if not is_disabled:
                    logger.info("Clicking NEXT button...")
                    
                    # Scroll to button
                    smooth_scroll(driver, button)
                    
                    # Click using ActionChains
                    if safe_click(driver, button):
                        human_delay(3, 5)  # Wait for page to load
                        
                        # Wait for table to appear on new page
                        WebDriverWait(driver, TIMEOUT).until(
                            EC.presence_of_element_located((By.CLASS_NAME, TABLE_CLASS_NAME))
                        )
                        
                        logger.info("Successfully navigated to next page")
                        return True
        
        logger.info("Could not click NEXT button")
        return False
        
    except TimeoutException:
        logger.error("Timeout waiting for next page to load")
        return False
    except Exception as e:
        logger.error(f"Error clicking NEXT button: {e}")
        return False


# ============================================================================
# MAIN SCRAPING LOGIC
# ============================================================================

def main():
    """
    Main scraping orchestration function.
    """
    driver = None
    total_exhibitions = 0
    page_number = 1
    
    try:
        # Validate target URL
        if target_url == "PASTE_PAGE_URL_HERE":
            logger.error("Please set the target_url variable in the CONFIG section")
            print("\n" + "="*70)
            print("ERROR: Please update the target_url variable")
            print("="*70 + "\n")
            return
        
        logger.info("="*70)
        logger.info("Exhibition Scraper Started")
        logger.info("="*70)
        
        # Initialize CSV file
        initialize_csv()
        
        # Setup driver
        driver = setup_driver()
        
        # Navigate to target URL
        logger.info(f"Navigating to: {target_url}")
        driver.get(target_url)
        human_delay(3, 5)  # Initial page load delay
        
        # Main scraping loop with pagination
        while True:
            logger.info(f"\n{'='*70}")
            logger.info(f"Scraping Page {page_number}")
            logger.info(f"{'='*70}\n")
            
            # Scrape current page
            exhibitions_count = scrape_listing_page(driver)
            total_exhibitions += exhibitions_count
            
            logger.info(f"Total exhibitions scraped so far: {total_exhibitions}")
            
            # Check for next page
            if has_next_page(driver):
                logger.info("More pages available, continuing...")
                
                # Click next page
                if click_next_page(driver):
                    page_number += 1
                    human_delay(2, 4)  # Delay before starting next page
                else:
                    logger.info("Failed to navigate to next page, stopping")
                    break
            else:
                logger.info("No more pages available, scraping complete")
                break
        
        logger.info("\n" + "="*70)
        logger.info("Scraping Completed Successfully")
        logger.info(f"Total pages scraped: {page_number}")
        logger.info(f"Total exhibitions scraped: {total_exhibitions}")
        logger.info(f"Data saved to: {CSV_FILENAME}")
        logger.info("="*70 + "\n")
        
    except KeyboardInterrupt:
        logger.info("\nScraping interrupted by user")
        logger.info(f"Data saved up to this point in: {CSV_FILENAME}")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
    finally:
        # Cleanup
        if driver:
            logger.info("Closing browser...")
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
        
        logger.info("Scraper terminated")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Print banner
    print("\n" + "="*70)
    print("  EXHIBITION/TRADE SHOW WEB SCRAPER")
    print("  Powered by Selenium + Python")
    print("="*70 + "\n")
    
    # Legal & Ethical Notice
    print("LEGAL & ETHICAL NOTICE:")
    print("-" * 70)
    print("1. Ensure you have permission to scrape the target website")
    print("2. Review the website's robots.txt and Terms of Service")
    print("3. Respect rate limits and server resources")
    print("4. Use collected data responsibly and legally")
    print("5. Consider the website's bandwidth and server load")
    print("-" * 70 + "\n")
    
    # Best Practices Notice
    print("BEST PRACTICES:")
    print("-" * 70)
    print("1. Data is saved in real-time to prevent loss")
    print("2. Failed URLs are logged to 'failed_urls.txt'")
    print("3. Random delays simulate human behavior")
    print("4. Script can be interrupted safely (Ctrl+C)")
    print("5. Resume by checking last scraped exhibition in CSV")
    print("-" * 70 + "\n")
    
    input("Press Enter to start scraping...")
    
    # Run main scraping function
    main()
