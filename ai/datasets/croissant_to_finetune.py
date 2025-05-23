#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import pandas as pd
from typing import Dict, List, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CroissantConverter:
    def __init__(self, input_dir: str, output_dir: str):
        """Initialize the converter with input and output directories."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a Croissant metadata JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading metadata file {file_path}: {e}")
            return {}

    def extract_dataset_info(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant information from metadata."""
        return {
            'name': metadata.get('name', ''),
            'description': metadata.get('description', ''),
            'keywords': metadata.get('keywords', []),
            'license': metadata.get('license', {}).get('name', ''),
            'record_sets': metadata.get('recordSet', [])
        }

    def create_instruction_template(self, dataset_info: Dict[str, Any]) -> str:
        """Create an instruction template based on dataset information."""
        template = f"""You are a sexual health education assistant. 
        Based on the following information about {dataset_info['name']}, 
        provide accurate and educational responses.
        
        Context: {dataset_info['description']}
        
        Keywords: {', '.join(dataset_info['keywords'])}
        
        Please provide information that is:
        1. Factual and medically accurate
        2. Age-appropriate
        3. Culturally sensitive
        4. Based on scientific evidence
        
        Response:"""
        return template

    def process_record_set(self, record_set: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process a record set into training examples."""
        training_examples = []
        
        for field in record_set.get('field', []):
            if field.get('name') and field.get('description'):
                example = {
                    'instruction': f"Explain the concept of {field['name']} in sexual health education.",
                    'input': field['description'],
                    'output': f"{field['name']} is an important aspect of sexual health education. {field['description']}"
                }
                training_examples.append(example)
        
        return training_examples

    def convert_dataset(self, metadata_file: str) -> None:
        """Convert a single dataset from Croissant format to fine-tuning format."""
        metadata_path = self.input_dir / metadata_file
        if not metadata_path.exists():
            logger.error(f"Metadata file not found: {metadata_path}")
            return

        # Load and process metadata
        metadata = self.load_metadata(metadata_path)
        dataset_info = self.extract_dataset_info(metadata)
        
        # Create training examples
        training_examples = []
        for record_set in dataset_info['record_sets']:
            examples = self.process_record_set(record_set)
            training_examples.extend(examples)

        # Add instruction template
        instruction_template = self.create_instruction_template(dataset_info)
        
        # Create output format
        output_data = {
            'instruction_template': instruction_template,
            'training_examples': training_examples,
            'metadata': {
                'name': dataset_info['name'],
                'license': dataset_info['license'],
                'keywords': dataset_info['keywords']
            }
        }

        # Save to output file
        output_file = self.output_dir / f"{metadata_file.replace('-metadata.json', '')}_finetune.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Converted {metadata_file} to {output_file}")

    def convert_all_datasets(self) -> None:
        """Convert all Croissant format datasets in the input directory."""
        metadata_files = list(self.input_dir.glob('*-metadata.json'))
        
        for metadata_file in metadata_files:
            logger.info(f"Processing {metadata_file.name}")
            self.convert_dataset(metadata_file.name)

def main():
    # Set up directories
    current_dir = Path(__file__).parent
    input_dir = current_dir
    output_dir = current_dir / 'finetune_data'
    
    # Create converter and process datasets
    converter = CroissantConverter(input_dir, output_dir)
    converter.convert_all_datasets()

if __name__ == "__main__":
    main() 