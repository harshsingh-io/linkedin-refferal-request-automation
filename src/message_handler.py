import os
from string import Template
import logging
from typing import Dict

class MessageHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()

    def _setup_logging(self):
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            filename='logs/message_handler.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def personalize_message(self, template, profile):
        """
        Personalize connection message template with profile data
        """
        try:
            # Replace placeholders with profile data
            message = template.replace("$name", profile['name'])
            message = message.replace("$title", profile['title'])
            
            # Ensure message is within LinkedIn's character limit (300 chars)
            if len(message) > 300:
                message = message[:297] + "..."
                
            return message
            
        except Exception as e:
            self.logger.error(f"Error personalizing message: {str(e)}")
            return template 