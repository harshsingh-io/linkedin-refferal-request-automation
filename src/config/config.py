import os
import yaml
import logging

class LinkedInConfig:
    def __init__(self):
        try:
            # Load config first
            config_path = os.path.join(os.path.dirname(__file__), '../../config/config.yaml')
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
                logging.info("Successfully loaded config file")
                
            # Set URL and message
            self.SEARCH_URL = "https://www.linkedin.com/search/results/people/"
            self.connection_message = self._config.get('connection_message')
            
            if not self.connection_message:
                logging.error("Connection message not found in config.yaml")
            else:
                logging.info("Successfully loaded connection message")
                
        except Exception as e:
            logging.error(f"Failed to initialize config: {str(e)}")
            raise

    @property
    def config(self):
        """Access to raw config data"""
        return self._config 