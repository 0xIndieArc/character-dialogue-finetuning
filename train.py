from src.data.data_processor import DataProcessor
from src.training.trainer import ModelTrainer
from src.utils.logger import Logger
from pathlib import Path

def main():
    logger = Logger()
    config_path = "config/config.yaml"
    
    try:
        # Initialize processors
        data_processor = DataProcessor(config_path)
        trainer = ModelTrainer(config_path)
        
        # Run pipeline
        csv_path = data_processor.download_dataset()
        jsonl_path = data_processor.prepare_training_data(csv_path)
        trainer.fine_tune(jsonl_path)
        
        logger.log("Training pipeline completed", "success")
    except Exception as e:
        logger.error(str(e))

if __name__ == "__main__":
    main() 