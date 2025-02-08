import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import LinkedInConfig, UserSearchCriteria
import logging
from typing import List, Dict
import os
import asyncio
import random

class LinkedInAPI:
    def __init__(self, driver):
        self.driver = driver
        self.config = LinkedInConfig()
        self.logger = logging.getLogger(__name__)
        self._setup_logging()

    def _setup_logging(self):
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            filename='logs/linkedin_api.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def search_profiles(self, criteria: UserSearchCriteria) -> List[Dict]:
        """Search for profiles based on given criteria"""
        try:
            search_url = self._build_search_url(criteria)
            logging.info(f"Navigating to: {search_url}")
            self.driver.get(search_url)
            time.sleep(5)
            
            profiles = []
            processed_urls = set()
            valid_profiles_found = 0

            while valid_profiles_found < criteria.max_requests:
                # Get all profile elements
                profile_elements = self.driver.find_elements(
                    By.CLASS_NAME,
                    "KTFkSmBsFiTakUskYzRRttbsRKpwUqQBGWLss"
                )
                
                logging.info(f"Found {len(profile_elements)} profile elements on current page")

                for element in profile_elements:
                    try:
                        # First get the button to check connection status
                        action_button = element.find_element(
                            By.CSS_SELECTOR,
                            "button.artdeco-button"
                        )
                        button_text = action_button.find_element(By.CLASS_NAME, "artdeco-button__text").text.strip()
                        
                        # Skip if not a "Connect" button
                        if button_text != "Connect":
                            logging.debug(f"Skipping profile with button text: {button_text}")
                            continue

                        # Get profile URL
                        link = element.find_element(
                            By.CLASS_NAME,
                            "TYwFhGrAOkNlxnxENufwIbYSlSJAqSIcLM"
                        ).get_attribute("href")
                        
                        if link in processed_urls:
                            continue
                        processed_urls.add(link)

                        # Rest of the profile data collection...
                        name = element.find_element(
                            By.XPATH,
                            ".//span[@dir='ltr']/span"
                        ).text.strip()
                        
                        title = element.find_element(
                            By.CLASS_NAME,
                            "wYqQQrAssqySWkRKiEeCRBSojQuRYgic"
                        ).text.strip()
                        
                        location = element.find_element(
                            By.CLASS_NAME,
                            "fdFsuoIEaDmDhLQhinTwYZqfClTHklvH"
                        ).text.strip()

                        profile_data = {
                            'name': name,
                            'profile_url': link,
                            'title': title,
                            'location': location
                        }
                        profiles.append(profile_data)
                        valid_profiles_found += 1
                        logging.info(f"Added new profile to connect: {name} ({title})")

                        if valid_profiles_found >= criteria.max_requests:
                            break

                    except Exception as e:
                        logging.error(f"Error extracting profile data: {str(e)}")
                        continue

                if valid_profiles_found >= criteria.max_requests:
                    break

                # Try next page if needed
                try:
                    next_button = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "button.artdeco-pagination__button--next"
                    )
                    if not next_button.is_enabled():
                        break
                    next_button.click()
                    time.sleep(3)
                except Exception:
                    break

            logging.info(f"Successfully found {valid_profiles_found} new profiles to connect")
            return profiles

        except Exception as e:
            logging.error(f"Error during profile search: {str(e)}")
            logging.error(f"Exception details: {str(e.__class__.__name__)}")
            return []

    def send_connection_request(self, profile_url: str) -> bool:
        """Send a connection request"""
        try:
            # Navigate to profile
            self.driver.get(profile_url)
            time.sleep(3)

            # Look for the Connect button with exact class
            connect_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.XSUzzrFLlBaUcRcaQFkhBSVLQreKMBFjRPzsuU"
                ))
            )
            
            # Double check it's the Connect button by checking text
            button_text = connect_button.find_element(By.CLASS_NAME, "artdeco-button__text").text.strip()
            if button_text != "Connect":
                logging.info(f"Found button but text was '{button_text}' instead of 'Connect'")
                return False

            # Click the Connect button
            connect_button.click()
            time.sleep(2)

            # Wait for the modal to appear and find the "Add a note" button
            add_note_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "button.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary[aria-label='Add a note']"
                ))
            )
            
            # Click the "Add a note" button
            add_note_button.click()
            time.sleep(1)

            # Find and fill the note textarea using its full class name
            note_textarea = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "textarea.ember-text-area.ember-view.connect-button-send-invite__custom-message"
                ))
            )
            note_textarea.clear()
            
            # Get message from config
            message = self.config._get_connection_message()  # Call the method directly
            if not message:
                logging.error("No connection message found in config")
                return False
            
            note_textarea.send_keys(message)
            logging.info(f"Successfully added note to connection request for profile: {profile_url}")
            return True

        except Exception as e:
            logging.error(f"Failed to click buttons: {str(e)}")
            logging.error(f"Exception details: {str(e.__class__.__name__)}")
            return False

    async def process_search_results(self, criteria):
        """Process search results and send connection requests"""
        try:
            profiles = self.search_profiles(criteria)
            successful_requests = 0
            attempted_profiles = 0

            for profile in profiles:
                if attempted_profiles >= criteria.max_requests:
                    break

                result = self.send_connection_request(profile['profile_url'])
                if result:  # Only increment successful_requests if connection was actually sent
                    successful_requests += 1
                    time.sleep(random.uniform(3, 5))  # Random delay between requests
                
                attempted_profiles += 1

            self.sent_requests = successful_requests
            return successful_requests

        except Exception as e:
            logging.error(f"Error processing search results: {str(e)}")
            return 0

    def _build_search_url(self, criteria: UserSearchCriteria) -> str:
        """Build search URL with filters"""
        company = urllib.parse.quote("Dell Technologies")
        keywords = urllib.parse.quote("Software Engineer")
        location = urllib.parse.quote("India")
        
        url = (f"{self.config.SEARCH_URL}"
               f"?company={company}"
               f"&keywords={keywords}"
               f"&location={location}"
               f"&network=%5B%22S%22%5D"
               f"&origin=FACETED_SEARCH"
               f"&sid=@L4")
        
        logging.info(f"Built search URL: {url}")
        return url 