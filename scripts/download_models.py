#!/usr/bin/env python3
"""
Script to download AI models for LLB application.

This script downloads the required AI models and caches them locally.
"""

import os
import sys
import argparse
import tarfile
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from transformers import AutoTokenizer, AutoModelForCausalLM, WhisperProcessor, WhisperForConditionalGeneration
from loguru import logger

from ai.config import (
    GEMMA_MODEL_ID,
    WHISPER_MODEL,
    CACHE_DIR,
    MODELS_DIR,
)


def setup_logger():
    """Set up the logger configuration."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
    )


def extract_gemma_model(tar_path):
    """
    Extract the Gemma model from tar.gz file.
    
    Args:
        tar_path (str): Path to the tar.gz file
    """
    logger.info(f"Extracting Gemma model from {tar_path}")
    
    try:
        # Create models directory if it doesn't exist
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        # Extract the tar.gz file
        with tarfile.open(tar_path, "r:gz") as tar:
            # Validate and sanitize all paths to prevent traversal attacks
            safe_members = []
            for member in tar.getmembers():
                # Check for absolute paths or path traversal attempts
                if os.path.isabs(member.name) or ".." in member.name or member.name.startswith("/"):
                    raise ValueError(f"Unsafe path in tar file: {member.name}")
                
                # Normalize the path and ensure it's within bounds
                normalized_path = os.path.normpath(member.name)
                if normalized_path.startswith("../") or normalized_path == "..":
                    raise ValueError(f"Path traversal attempt detected: {member.name}")
                
                safe_members.append(member)
            
            # Get the root directory name from first safe member
            root_dir = safe_members[0].name.split('/')[0]
            target_dir = os.path.join(MODELS_DIR, "gemma-3-1b")
            
            # Extract only validated members
            tar.extractall(path=MODELS_DIR, members=safe_members)
            
            # Rename the extracted directory if needed
            extracted_dir = os.path.join(MODELS_DIR, root_dir)
            if extracted_dir != target_dir:
                if os.path.exists(target_dir):
                    import shutil
                    shutil.rmtree(target_dir)
                os.rename(extracted_dir, target_dir)
        
        logger.info("Successfully extracted Gemma model")
        return True
    
    except Exception as e:
        logger.error(f"Error extracting Gemma model: {str(e)}")
        return False


def download_whisper_model(model_size=WHISPER_MODEL):
    """
    Download Whisper model.
    
    Args:
        model_size: Size of the model to download
    """
    model_id = f"openai/whisper-{model_size}"
    logger.info(f"Downloading Whisper model: {model_id}")
    
    try:
        # Download processor
        logger.info(f"Downloading processor for {model_id}")
        processor = WhisperProcessor.from_pretrained(model_id, cache_dir=CACHE_DIR)
        
        # Download model
        logger.info(f"Downloading model {model_id}")
        model = WhisperForConditionalGeneration.from_pretrained(
            model_id,
            device_map="auto",
            cache_dir=CACHE_DIR,
        )
        
        logger.info(f"Successfully downloaded Whisper model: {model_id}")
        return True
    
    except Exception as e:
        logger.error(f"Error downloading Whisper model: {str(e)}")
        return False


def download_fasttext():
    """Download fastText language detection model."""
    try:
        import fasttext
        model_path = os.path.join(MODELS_DIR, "lid.176.bin")
        
        if not os.path.exists(model_path):
            logger.info("Downloading fastText language detection model")
            model = fasttext.download_model('lid.176.bin', if_exists='ignore')
            os.rename(model, model_path)
            logger.info("Successfully downloaded fastText model")
        else:
            logger.info("FastText model already exists")
        
        return True
    
    except Exception as e:
        logger.error(f"Error downloading fastText model: {str(e)}")
        return False


def main():
    """Main function."""
    setup_logger()
    
    parser = argparse.ArgumentParser(description="Download AI models for LLB application")
    parser.add_argument("--whisper", choices=["tiny", "base", "small", "medium", "large"], default=WHISPER_MODEL,
                        help="Whisper model size to download")
    parser.add_argument("--fasttext", action="store_true",
                        help="Download fastText language detection model")
    parser.add_argument("--all", action="store_true",
                        help="Download all models")
    parser.add_argument("--gemma-tar", type=str,
                        help="Path to the Gemma model tar.gz file")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    if args.gemma_tar:
        extract_gemma_model(args.gemma_tar)
    
    if args.all:
        # Download all models
        if not args.gemma_tar:
            logger.error("Please provide the Gemma model tar.gz file with --gemma-tar")
            sys.exit(1)
        download_whisper_model(args.whisper)
        download_fasttext()
    else:
        # Download specific models
        if args.whisper:
            download_whisper_model(args.whisper)
        
        if args.fasttext:
            download_fasttext()


if __name__ == "__main__":
    main() 