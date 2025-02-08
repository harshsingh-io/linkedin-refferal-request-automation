import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import LinkedInConfig
import logging

class LinkedInAuth:
    def __init__(self):
        self.driver = None
        self.config = LinkedInConfig()
        # Create chrome data directory if it doesn't exist
        os.makedirs('./chrome-data', exist_ok=True)
        self._setup_logging()

    def _setup_logging(self):
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            filename='logs/linkedin_auth.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def initialize_driver(self):
        """Initialize the Selenium WebDriver with appropriate options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')  # Disable notifications
        options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        options.add_argument('--start-maximized')  # Start with maximized window
        
        # Add user data directory to maintain session
        options.add_argument('--user-data-dir=./chrome-data')
        
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    async def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn using provided credentials
        Returns True if login successful, False otherwise
        """
        try:
            # First check if we're already logged in
            self.driver.get(self.config.BASE_URL)
            try:
                # Wait a short time to see if we're already logged in
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "global-nav"))
                )
                logging.info("Already logged in to LinkedIn")
                return True
            except:
                # Not logged in, proceed with login
                self.driver.get(self.config.LOGIN_URL)
                
                # Wait for and fill in email
                email_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                email_field.send_keys(email)

                # Fill in password
                password_field = self.driver.find_element(By.ID, "password")
                password_field.send_keys(password)

                # Click login button
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()

                # Wait for successful login (check for home page element)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "global-nav"))
                )
                
                logging.info("Successfully logged in to LinkedIn")
                return True

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def get_session_cookies(self):
        """Return current session cookies"""
        return self.driver.get_cookies()

    def __del__(self):
        """Cleanup driver on object destruction"""
        if self.driver:
            self.driver.quit() 