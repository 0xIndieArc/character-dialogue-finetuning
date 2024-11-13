import pandas as pd
import json
import requests
from typing import Dict, List
import yaml
from pathlib import Path
from ..utils.logger import Logger

class DataProcessor:
    def __init__(self, config_path: str):
        self.logger = Logger()
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
    def download_dataset(self) -> str:
        """Downloads the dataset from the configured URL."""
        self.logger.log("Downloading dataset", "header")
        url = self.config['character']['dataset_url']
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            csv_path = Path("data") / "dialogue.csv"
            csv_path.parent.mkdir(exist_ok=True)
            
            with open(csv_path, "w", encoding='utf-8') as f:
                f.write(response.text)
            self.logger.log("Dataset downloaded", "success")
            return str(csv_path)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Download failed: {str(e)}")

    def prepare_training_data(self, csv_path: str) -> str:
        """Prepares training data in JSONL format for the target character."""
        self.logger.log("Preparing training data", "header")
        df = pd.read_csv(csv_path, encoding='utf-8')
        conversations = []
        
        config = self.config['character']
        target_speaker = config['target_speaker']
        template = self.config['training']['prompt_template']
        
        # Clean the column names and data
        df = df.fillna('')
        for col in df.columns:
            df[col] = df[col].astype(str).apply(lambda x: " ".join(x.strip().split()))
        
        # Process conversations
        for _, row in df.iterrows():
            # Check if the target speaker is speaking
            if row[config['speaker_column']] == target_speaker and row[config['text_column']]:
                # Get the corresponding prompt from the other speaker
                prompt = row[config['other_text_column']]
                completion = row[config['text_column']]
                
                if prompt and completion:
                    conversation_text = {
                        "text": template.format(
                            prompt=prompt,
                            completion=completion
                        )
                    }
                    conversations.append(conversation_text)
            
            # Also check the other speaker columns for target speaker
            elif row[config['other_speaker_column']] == target_speaker and row[config['other_text_column']]:
                prompt = row[config['text_column']]
                completion = row[config['other_text_column']]
                
                if prompt and completion:
                    conversation_text = {
                        "text": template.format(
                            prompt=prompt,
                            completion=completion
                        )
                    }
                    conversations.append(conversation_text)

        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        jsonl_path = output_dir / f"{target_speaker.lower()}_training.jsonl"
        
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for conv in conversations:
                f.write(json.dumps(conv) + '\n')

        self.logger.log(f"Processed {len(conversations)} conversations for {target_speaker}", "success")
        return str(jsonl_path) 