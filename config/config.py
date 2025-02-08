from dataclasses import dataclass
from typing import Optional
import yaml
import os

@dataclass
class LinkedInConfig:
    MAX_DAILY_REQUESTS = 30
    REQUEST_DELAY = 60  # seconds between requests
    SEARCH_DELAY = 2    # seconds between search operations
    
    # LinkedIn URLs
    BASE_URL = "https://www.linkedin.com"
    LOGIN_URL = f"{BASE_URL}/login"
    SEARCH_URL = f"{BASE_URL}/search/results/people/"

@dataclass
class UserSearchCriteria:
    company_name: str
    location: str
    role_category: str
    connection_message: str
    max_requests: int
    mutual_connections: bool

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_search_criteria(self) -> UserSearchCriteria:
        search = self.config['search']
        return UserSearchCriteria(
            company_name=search['company_name'],
            location=search['location'],
            role_category=search['role_category'],
            connection_message=self.config['connection_message'],
            max_requests=search['max_requests'],
            mutual_connections=search['mutual_connections']
        )

    def get_credentials(self):
        # Environment variables take precedence over config file
        return {
            'email': os.getenv('LINKEDIN_EMAIL') or self.config['credentials']['email'],
            'password': os.getenv('LINKEDIN_PASSWORD') or self.config['credentials']['password']
        }

    def get_delays(self):
        return self.config['delays'] 