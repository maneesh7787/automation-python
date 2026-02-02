# Exhibition/Trade Show Web Scraper

A robust Python + Selenium automation script for scraping exhibition/trade show data from websites with anti-bot avoidance, pagination handling, and real-time CSV export.

## 🔹 Features

- **Anti-Bot Detection Avoidance**: Implements multiple techniques to avoid being detected as a bot
- **Real-Time CSV Export**: Data is saved immediately to prevent loss during interruptions
- **Pagination Support**: Automatically navigates through multiple pages
- **Detail Page Scraping**: Clicks on exhibition names to extract detailed information
- **Error Handling**: Comprehensive exception handling with failed URL logging
- **Human-Like Behavior**: Random delays, smooth scrolling, and ActionChains for natural interaction
- **Resume Capability**: Can resume scraping by checking the last entry in CSV
- **Data Safety**: Append mode prevents data loss from crashes or interruptions

## 🔹 Requirements

- Python 3.7 or higher
- Chrome browser installed
- Internet connection

## 🔹 Installation

1. Clone the repository:
```bash
git clone https://github.com/maneesh7787/automation-python.git
cd automation-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔹 Configuration

Edit `exhibition_scraper.py` and update the `target_url` variable in the CONFIG section:

```python
# Replace this with your actual target URL
target_url = "https://example.com/exhibitions"
```

### Optional Configuration

- **CSV Filename**: Change `CSV_FILENAME` to customize output file name
- **Timeouts**: Adjust `TIMEOUT`, `MIN_DELAY`, `MAX_DELAY` for different sites
- **Proxy**: Uncomment and configure proxy settings if needed
- **Headless Mode**: Uncomment headless option in `setup_driver()` function

## 🔹 Usage

Run the scraper:
```bash
python exhibition_scraper.py
```

The script will:
1. Display legal and ethical notices
2. Wait for you to press Enter
3. Start scraping from the target URL
4. Save data to `exhibitions_data.csv` in real-time
5. Log failed URLs to `failed_urls.txt`
6. Create a log file `scraper.log` with detailed execution logs

### Interrupting the Scraper

Press `Ctrl+C` to safely stop the scraper. All data scraped up to that point will be saved.

## 🔹 Output Files

### exhibitions_data.csv
Contains scraped exhibition data with columns:
- Exhibition Name
- Cycle
- Venue
- Date
- Description
- Related Industries
- Audience
- City
- Organizers
- Source URL

### failed_urls.txt
Logs any URLs that failed to scrape with timestamp and error reason.

### scraper.log
Detailed execution log with timestamps for debugging.

## 🔹 How It Works

1. **Table Scraping**: Finds table with class `tradeshows` and extracts row data
2. **Detail Navigation**: Clicks exhibition name links to access detail pages
3. **Data Extraction**: Scrapes additional information from detail pages
4. **CSV Writing**: Immediately writes each row to CSV (append mode)
5. **Pagination**: Finds and clicks NEXT button (class `pages-links`)
6. **Loop**: Continues until no more pages are available

## 🔹 Anti-Bot Measures

The script implements several techniques to avoid bot detection:

- Disables automation flags (`--disable-blink-features=AutomationControlled`)
- Sets realistic User-Agent string
- Overrides `navigator.webdriver` property
- Random delays between actions (2-5 seconds)
- Smooth scrolling behavior
- ActionChains for human-like clicks
- Randomized mouse movements

## 🔹 Error Handling

- **Timeout Exceptions**: Waits up to 15 seconds for elements
- **Stale Elements**: Re-finds elements if they become stale
- **Missing Elements**: Continues to next row if elements are missing
- **Failed URLs**: Logs to `failed_urls.txt` for later review
- **Crashes**: Data saved in real-time prevents loss

## 🔹 Customization

### Modifying Selectors

If the target website uses different HTML structure, update these selectors in the code:

```python
TABLE_CLASS_NAME = "tradeshows"  # Table class name
NEXT_BUTTON_CLASS = "pages-links"  # Pagination button class
```

Detail page selectors can be modified in the `scrape_detail_page()` function.

### Adding Proxy Support

Uncomment proxy configuration in `setup_driver()`:

```python
PROXY = "http://your-proxy-server:port"
chrome_options.add_argument(f'--proxy-server={PROXY}')
```

### Headless Mode

For running without GUI, uncomment in `setup_driver()`:

```python
chrome_options.add_argument('--headless')
```

## 🔹 Legal & Ethical Considerations

⚠️ **Important Notice**:

1. Ensure you have permission to scrape the target website
2. Review the website's `robots.txt` and Terms of Service
3. Respect rate limits and server resources
4. Use collected data responsibly and legally
5. Consider the website's bandwidth and server load
6. Be aware of copyright and data protection laws
7. Do not overload servers with too many requests

## 🔹 Best Practices for Long-Running Jobs

1. **Monitor Resources**: Keep an eye on memory and CPU usage
2. **Network Stability**: Use stable internet connection
3. **Error Logs**: Regularly check `scraper.log` and `failed_urls.txt`
4. **Resume Strategy**: Check last entry in CSV before restarting
5. **Backup Data**: Periodically backup the CSV file
6. **Rate Limiting**: Adjust delays if website shows signs of blocking

## 🔹 Troubleshooting

### Chrome Driver Issues
If you get Chrome driver errors:
```bash
# Update Chrome to latest version
# Or specify Chrome driver version manually
```

### Element Not Found
- Website structure may have changed
- Update selectors in the code
- Increase timeout values

### Bot Detection
- Increase random delays
- Add more human-like behaviors
- Use proxy rotation
- Reduce scraping speed

### CSV Encoding Issues
The script uses UTF-8 encoding. If you see garbled characters:
- Open CSV in Excel using "Get Data" → "From Text/CSV"
- Select UTF-8 encoding

## 🔹 Performance Optimization

- Use headless mode for faster execution (but less bot-resistant)
- Adjust delays based on website response time
- Consider parallel scraping with multiple instances (careful with rate limits)
- Use caching for repeated detail page visits

## 🔹 Script Structure

```
exhibition_scraper.py
├── CONFIGURATION SECTION
│   └── Settings and constants
├── DRIVER SETUP
│   └── setup_driver() - Chrome WebDriver initialization
├── UTILITY FUNCTIONS
│   ├── human_delay() - Random delays
│   ├── smooth_scroll() - Scroll simulation
│   ├── safe_click() - Human-like clicks
│   └── log_failed_url() - Error logging
├── CSV EXPORT
│   ├── initialize_csv() - CSV file setup
│   └── write_to_csv() - Real-time data writing
├── DETAIL PAGE SCRAPING
│   └── scrape_detail_page() - Extract detail information
├── LISTING PAGE SCRAPING
│   └── scrape_listing_page() - Extract table data
├── PAGINATION HANDLING
│   ├── has_next_page() - Check for next button
│   └── click_next_page() - Navigate to next page
└── MAIN LOGIC
    └── main() - Orchestration function
```

## 🔹 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🔹 License

This project is provided as-is for educational purposes. Use responsibly and ethically.

## 🔹 Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the log files for error details

---

**Disclaimer**: This tool is for educational purposes. Users are responsible for ensuring their use complies with applicable laws and website terms of service.