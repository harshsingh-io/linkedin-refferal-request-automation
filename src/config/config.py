import os
import yaml
import logging

class LinkedInConfig:
    def __init__(self):
        self.config = self._load_config()
        self.SEARCH_URL = "https://www.linkedin.com/search/results/people/"
        self.connection_message = self._get_connection_message()

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '../../config/config.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
            
    def _get_connection_message(self):
        """Get connection message from config"""
        try:
            # The message is directly in the root of the YAML
            message = self.config.get('connection_message')
            if not message:
                logging.error("connection_message not found in config.yaml")
                return None
            return message
        except Exception as e:
            logging.error(f"Error getting connection message: {str(e)}")
            return None 