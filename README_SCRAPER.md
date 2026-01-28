# eBird Alert Scraper

Automated scraper for extracting bird alert data from eBird.org.

## Features

- Logs into eBird automatically
- Scrapes bird species, dates/times, locations, and observer information
- Exports data to CSV format
- Includes debugging features (screenshots, HTML dumps)
- Secure credential handling

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver

The scraper uses Chrome/Chromium. You need ChromeDriver installed:

**Option A: Using webdriver-manager (automatic)**
```bash
pip install webdriver-manager
```

Then update the script to use webdriver-manager by replacing:
```python
self.driver = webdriver.Chrome(options=chrome_options)
```

with:
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=chrome_options)
```

**Option B: Manual installation**
- Download ChromeDriver from https://chromedriver.chromium.org/
- Add it to your PATH

## Usage

### Method 1: Environment Variables (Recommended)

Set your credentials as environment variables:

```bash
export EBIRD_USERNAME="your_email@example.com"
export EBIRD_PASSWORD="your_password"
python ebird_scraper.py
```

### Method 2: Interactive Prompt

Simply run the script and enter credentials when prompted:

```bash
python ebird_scraper.py
```

### Method 3: Import as Module

```python
from ebird_scraper import EBirdScraper

with EBirdScraper("your_email@example.com", "your_password") as scraper:
    scraper.login()
    alerts = scraper.scrape_alerts()
    scraper.save_to_csv(alerts, "my_alerts.csv")
```

## Output

The scraper generates a CSV file named `ebird_alerts_YYYYMMDD_HHMMSS.csv` containing:

- Species names
- Date and time of observation
- Location information
- Observer details
- Bird counts (if available)
- Coordinates (if available)

## Troubleshooting

### Debugging Mode

Run with `headless=False` to see the browser:

```python
scraper = EBirdScraper(username, password, headless=False)
```

### Check Debug Files

If scraping fails, the script creates:
- `ebird_page_debug.html` - The full page HTML for inspection
- `ebird_error_screenshot.png` - Screenshot of the page

### Update Selectors

If eBird changes their page structure, you'll need to:

1. Open `ebird_page_debug.html` in a browser
2. Inspect the HTML structure to find the correct element selectors
3. Update the XPath/CSS selectors in `_extract_alert_data()` method

## Security Notes

- Never commit credentials to version control
- Use environment variables or secure credential management
- Consider using eBird's official API if available for your use case

## Ethical Considerations

- Respect eBird's Terms of Service
- Don't run the scraper too frequently (rate limiting)
- Consider using the official eBird API 2.0 instead: https://documenter.getpostman.com/view/664302/S1ENwy59
- This scraper is for personal use only

## Customization

### Change Target Alert

Modify the `alert_url` in the `__init__` method:

```python
self.alert_url = "https://ebird.org/alert/summary?sid=YOUR_REGION_CODE"
```

### Adjust Wait Times

If pages load slowly, increase timeout values:

```python
self.wait = WebDriverWait(self.driver, 20)  # Increase from 10 to 20 seconds
```

### Custom Output Format

Modify `save_to_csv()` or add new methods for JSON/database output.
