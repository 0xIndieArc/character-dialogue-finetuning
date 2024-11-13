# Character Dialogue Fine-tuning

This project provides tools to fine-tune Large Language Models (LLMs) to emulate characters from movie scripts. It uses the Together AI platform to fine-tune a Llama 2 model using dialogue from movies.

## Overview

The project consists of three main components:
1. Data preparation script that processes the movie dialogue
2. Training script that handles the fine-tuning process
3. Training data in JSONL format

## Prerequisites

- Python 3.8+
- Together AI API key
- Required Python packages (install via `pip install -r requirements.txt`):
  - pandas
  - together
  - python-dotenv
  - requests

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/0xIndieArc/character-dialogue-finetuning.git
   cd character-dialogue-finetuning
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # OR
   venv\Scripts\activate     # On Windows
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your Together AI API key
   ```

## Usage

1. Configure the target character in `config/config.yaml`:
   ```yaml
   character:
     target_speaker: "Theodore"  # Change to any character name (e.g., "Samantha")
   ```

2. Run the training pipeline:
   ```bash
   python train.py
   ```

The script will:
1. Download the dialogue dataset
2. Process and prepare the training data for the specified character
3. Upload the data to Together AI
4. Start the fine-tuning process

## Project Structure

```
theodore-ai/
├── config/
│   ├── config.yaml            # Training and model configurations
│   └── .env.example           # Example environment variables
├── data/
│   └── training.jsonl         # Generated training data
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_processor.py  # Data processing logic
│   ├── training/
│   │   ├── __init__.py
│   │   └── trainer.py         # Training pipeline logic
│   └── utils/
│       ├── __init__.py
│       └── logger.py          # Logging utilities
├── .gitignore
├── LICENSE
├── README.md                  # Project documentation
├── requirements.txt           # Project dependencies
└── train.py                   # Main entry point
```

## Configuration

You can modify the training parameters in `config/config.yaml`:
- Model selection
- Number of epochs
- Batch size
- Learning rate
- Warmup ratio

### Planned Improvements
- [ ] Input Validation
  - CSV format validation
  - Character name verification
  - Required columns validation
- [ ] Testing
  - Data processing tests
  - Training pipeline tests
  - Config validation tests
- [ ] Documentation
  - Custom dataset preparation guide
  - Supported dialogue formats
  - Character selection best practices
- [ ] Features
  - Multiple dialogue format support
  - Model evaluation metrics
  - Data preprocessing options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Together AI for their fine-tuning platform
- Her movie dataset from HuggingFace