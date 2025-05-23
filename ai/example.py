"""
Example usage of the AI components in the LLB application.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any

from loguru import logger

# Add the parent directory to the path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai.factory import AIFactory


def setup_logger():
    """Set up the logger configuration."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )


def text_generation_example(ai_factory: AIFactory, prompt: str):
    """
    Demonstrate text generation using Gemma.
    
    Args:
        ai_factory: AIFactory instance
        prompt: Input prompt
    """
    logger.info(f"Generating text for prompt: {prompt[:30]}...")
    
    # Generate text
    response = ai_factory.generate_text(
        prompt=prompt,
        max_length=512,
        temperature=0.7,
    )
    
    print("\n--- Generated Text ---")
    print(response)
    print("---------------------\n")


def chat_example(ai_factory: AIFactory, user_input: str):
    """
    Demonstrate chat functionality.
    
    Args:
        ai_factory: AIFactory instance
        user_input: User message
    """
    logger.info(f"Chat example with input: {user_input[:30]}...")
    
    # Create a conversation
    messages = [
        {"role": "system", "content": "You are a helpful educational assistant for sex education."},
        {"role": "user", "content": user_input},
    ]
    
    # Generate response
    response = ai_factory.chat(
        messages=messages,
        temperature=0.7,
    )
    
    print("\n--- Chat Response ---")
    print(f"User: {user_input}")
    print(f"Assistant: {response}")
    print("--------------------\n")


def language_detection_example(ai_factory: AIFactory, text: str):
    """
    Demonstrate language detection.
    
    Args:
        ai_factory: AIFactory instance
        text: Input text
    """
    logger.info(f"Detecting language for: {text[:30]}...")
    
    result = ai_factory.detect_language(text)
    
    print("\n--- Language Detection ---")
    print(f"Text: {text}")
    print(f"Detected language: {result['language']}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print("--------------------------\n")


def pdf_processing_example(ai_factory: AIFactory, pdf_path: str):
    """
    Demonstrate PDF processing.
    
    Args:
        ai_factory: AIFactory instance
        pdf_path: Path to the PDF file
    """
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    logger.info(f"Processing PDF: {pdf_path}")
    
    result = ai_factory.process_document(pdf_path, is_file_path=True)
    
    if "error" in result:
        logger.error(f"Error processing PDF: {result['error']}")
        return
    
    print("\n--- PDF Processing ---")
    print(f"Title: {result.get('title', 'Unknown')}")
    print(f"Author: {result.get('author', 'Unknown')}")
    print(f"Pages: {result.get('num_pages', 0)}")
    
    # Print first page text
    if result.get('pages'):
        print("\nExcerpt from first page:")
        first_page_text = result['pages'][0]['text']
        print(first_page_text[:200] + "..." if len(first_page_text) > 200 else first_page_text)
    
    print("---------------------\n")


def audio_transcription_example(ai_factory: AIFactory, audio_path: str):
    """
    Demonstrate audio transcription.
    
    Args:
        ai_factory: AIFactory instance
        audio_path: Path to the audio file
    """
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return
    
    logger.info(f"Transcribing audio: {audio_path}")
    
    result = ai_factory.transcribe_audio(audio_path, is_file_path=True)
    
    if "error" in result:
        logger.error(f"Error transcribing audio: {result['error']}")
        return
    
    print("\n--- Audio Transcription ---")
    print(f"Transcription: {result.get('text', 'No text')}")
    print(f"Language: {result.get('language', 'Unknown')}")
    print("---------------------------\n")


def main():
    """Run the example."""
    setup_logger()
    
    parser = argparse.ArgumentParser(description="LLB AI Components Example")
    parser.add_argument("--text", help="Text generation prompt")
    parser.add_argument("--chat", help="Chat input message")
    parser.add_argument("--language", help="Text for language detection")
    parser.add_argument("--pdf", help="Path to PDF file for processing")
    parser.add_argument("--audio", help="Path to audio file for transcription")
    
    args = parser.parse_args()
    
    # Initialize AI factory
    ai_factory = AIFactory()
    
    try:
        # Run requested examples
        if args.text:
            text_generation_example(ai_factory, args.text)
        
        if args.chat:
            chat_example(ai_factory, args.chat)
        
        if args.language:
            language_detection_example(ai_factory, args.language)
        
        if args.pdf:
            pdf_processing_example(ai_factory, args.pdf)
        
        if args.audio:
            audio_transcription_example(ai_factory, args.audio)
        
        # If no arguments provided, show help
        if not any(vars(args).values()):
            parser.print_help()
    
    finally:
        # Clean up resources
        ai_factory.shutdown()


if __name__ == "__main__":
    main() 