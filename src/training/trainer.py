import os
from pathlib import Path
import yaml
import together
from ..utils.logger import Logger

class ModelTrainer:
    def __init__(self, config_path: str):
        self.logger = Logger()
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def setup_api(self):
        """Sets up the Together AI API key."""
        api_key = os.getenv('TOGETHER_API_KEY')
        if not api_key:
            api_key = input("Enter Together AI API key: ")
        os.environ['TOGETHER_API_KEY'] = api_key
    
    def fine_tune(self, training_file: str):
        """Runs the fine-tuning process."""
        self.logger.log("Starting fine-tuning", "header")
        
        self.setup_api()
        
        self.logger.log("Uploading training file")
        file_response = together.Files.upload(file=training_file)
        file_id = file_response['id']
        self.logger.log(f"File uploaded (ID: {file_id})", "success")

        self.logger.log("Creating fine-tuning job")
        
        model_config = self.config['model']
        character_name = self.config['character']['target_speaker'].lower()
        
        command = (
            f"together fine-tuning create "
            f"--training-file {file_id} "
            f"--model {model_config['base_model']} "
            f"--suffix {character_name}-character "
            f"--n-epochs {model_config['n_epochs']} "
            f"--batch-size {model_config['batch_size']} "
            f"--learning-rate {model_config['learning_rate']} "
            f"--warmup-ratio {model_config['warmup_ratio']} "
            f"--confirm"
        )
        
        process = os.system(command)
        if process != 0:
            raise Exception("Fine-tuning job creation failed")
            
        self.logger.log("Fine-tuning job created successfully", "success") 