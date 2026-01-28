#!/usr/bin/env python3
"""
eBird Alert Scraper
Scrapes bird alert data from eBird and saves to CSV
"""

import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os


class EBirdScraper:
    def __init__(self, username, password, headless=True):
        """
        Initialize the eBird scraper

        Args:
            username: eBird account username/email
            password: eBird account password
            headless: Run browser in headless mode (default: True)
        """
        self.username = username
        self.password = password
        self.alert_url = "https://ebird.org/alert/summary?sid=SN35466"

        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        """Login to eBird"""
        print("Logging in to eBird...")

        try:
            # Navigate to the alert page (will redirect to login)
            self.driver.get(self.alert_url)
            time.sleep(2)

            # Wait for login form
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "input_username"))
            )
            password_field = self.driver.find_element(By.ID, "input_password")

            # Enter credentials
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Submit login form
            login_button = self.driver.find_element(By.ID, "form_submit")
            login_button.click()

            # Wait for redirect back to alert page
            time.sleep(3)

            # Check if login was successful
            if "login" in self.driver.current_url.lower():
                raise Exception("Login failed. Please check your credentials.")

            print("Login successful!")

        except TimeoutException:
            raise Exception("Login page did not load properly")
        except NoSuchElementException as e:
            raise Exception(f"Could not find login elements: {e}")

    def scrape_alerts(self):
        """
        Scrape bird alert data from the page

        Returns:
            list: List of dictionaries containing alert data
        """
        print("Scraping alert data...")

        try:
            # Wait for alert content to load
            time.sleep(3)

            alerts = []

            # Try to find alert rows/cards (these selectors may need adjustment)
            # Common eBird alert structures to try
            selectors_to_try = [
                "//div[contains(@class, 'Alert')]",
                "//tr[contains(@class, 'alert')]",
                "//div[contains(@class, 'sighting')]",
                "//div[contains(@class, 'observation')]"
            ]

            alert_elements = []
            for selector in selectors_to_try:
                try:
                    alert_elements = self.driver.find_elements(By.XPATH, selector)
                    if alert_elements:
                        print(f"Found {len(alert_elements)} alerts using selector: {selector}")
                        break
                except:
                    continue

            if not alert_elements:
                # Fallback: try to extract from page source
                print("Using fallback extraction method...")
                page_source = self.driver.page_source

                # Save page source for debugging
                with open('ebird_page_debug.html', 'w', encoding='utf-8') as f:
                    f.write(page_source)
                print("Page source saved to ebird_page_debug.html for inspection")

                return self._extract_from_page_source(page_source)

            # Extract data from each alert element
            for element in alert_elements:
                alert_data = self._extract_alert_data(element)
                if alert_data:
                    alerts.append(alert_data)

            print(f"Successfully scraped {len(alerts)} alerts")
            return alerts

        except Exception as e:
            print(f"Error scraping alerts: {e}")
            # Save screenshot for debugging
            self.driver.save_screenshot('ebird_error_screenshot.png')
            print("Screenshot saved to ebird_error_screenshot.png")
            raise

    def _extract_alert_data(self, element):
        """
        Extract data from a single alert element

        Args:
            element: Selenium WebElement containing alert data

        Returns:
            dict: Alert data or None if extraction fails
        """
        try:
            alert = {
                'species': '',
                'common_name': '',
                'date': '',
                'time': '',
                'location': '',
                'observer': '',
                'count': '',
                'latitude': '',
                'longitude': ''
            }

            # Try to extract species name
            try:
                species_elem = element.find_element(By.XPATH, ".//span[contains(@class, 'species')] | .//a[contains(@class, 'species')]")
                alert['species'] = species_elem.text.strip()
            except:
                pass

            # Try to extract date/time
            try:
                date_elem = element.find_element(By.XPATH, ".//span[contains(@class, 'date')] | .//time")
                alert['date'] = date_elem.text.strip()
            except:
                pass

            # Try to extract location
            try:
                location_elem = element.find_element(By.XPATH, ".//span[contains(@class, 'location')] | .//a[contains(@class, 'location')]")
                alert['location'] = location_elem.text.strip()
            except:
                pass

            # Try to extract observer
            try:
                observer_elem = element.find_element(By.XPATH, ".//span[contains(@class, 'observer')] | .//a[contains(@class, 'observer')]")
                alert['observer'] = observer_elem.text.strip()
            except:
                pass

            # Get full text as fallback
            if not any(alert.values()):
                alert['raw_text'] = element.text.strip()

            return alert if any(alert.values()) else None

        except Exception as e:
            print(f"Error extracting alert data: {e}")
            return None

    def _extract_from_page_source(self, page_source):
        """
        Fallback method to extract data from page source
        This is a placeholder - you'll need to inspect the HTML structure
        and implement proper parsing logic
        """
        print("Please inspect ebird_page_debug.html to identify the correct selectors")
        print("Update the script with the correct CSS selectors or XPath expressions")
        return []

    def save_to_csv(self, alerts, filename=None):
        """
        Save alerts to CSV file

        Args:
            alerts: List of alert dictionaries
            filename: Output filename (default: ebird_alerts_TIMESTAMP.csv)
        """
        if not alerts:
            print("No alerts to save")
            return

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ebird_alerts_{timestamp}.csv"

        # Get all possible keys from all alerts
        fieldnames = set()
        for alert in alerts:
            fieldnames.update(alert.keys())
        fieldnames = sorted(fieldnames)

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(alerts)

        print(f"Data saved to {filename}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Main function to run the scraper"""

    # Try to load credentials from config.json first
    username = None
    password = None

    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
            username = config.get('ebird_username')
            password = config.get('ebird_password')
            print("Loaded credentials from config.json")
    except FileNotFoundError:
        print("config.json not found, checking environment variables...")
    except Exception as e:
        print(f"Error loading config.json: {e}")

    # Fallback to environment variables
    if not username:
        username = os.getenv('EBIRD_USERNAME')
    if not password:
        password = os.getenv('EBIRD_PASSWORD')

    # Fallback to interactive prompt (only if stdin is available)
    if not username:
        try:
            username = input("Enter your eBird username/email: ")
        except EOFError:
            print("Error: No credentials provided. Please create config.json or set environment variables.")
            return 1
    if not password:
        try:
            import getpass
            password = getpass.getpass("Enter your eBird password: ")
        except EOFError:
            print("Error: No password provided. Please create config.json or set environment variables.")
            return 1

    try:
        # Create scraper instance
        with EBirdScraper(username, password, headless=False) as scraper:
            # Login
            scraper.login()

            # Scrape alerts
            alerts = scraper.scrape_alerts()

            # Save to CSV
            if alerts:
                scraper.save_to_csv(alerts)
            else:
                print("\nNo alerts found. The page structure may have changed.")
                print("Check ebird_page_debug.html and update the selectors in the script.")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
