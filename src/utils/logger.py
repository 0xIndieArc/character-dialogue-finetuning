import logging
from typing import Optional

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        self.logger = logging.getLogger('MovieCharacterAI')
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def log(self, message: str, status: Optional[str] = None):
        if status == "success":
            self.logger.info(f"✓ {message}")
        elif status == "header":
            self.logger.info(f"\n→ {message}")
        else:
            self.logger.info(f"  {message}")
    
    def error(self, message: str):
        self.logger.error(f"× Error: {message}") 