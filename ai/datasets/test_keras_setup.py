#!/usr/bin/env python3
"""
Test script to verify KerasHub setup and Gemma model loading
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required packages can be imported"""
    logger.info("Testing package imports...")
    
    try:
        import tensorflow as tf
        logger.info(f"✓ TensorFlow {tf.__version__} imported successfully")
        
        import keras
        logger.info(f"✓ Keras {keras.__version__} imported successfully")
        
        import keras_hub
        logger.info(f"✓ KerasHub {keras_hub.__version__} imported successfully")
        
        import numpy as np
        logger.info(f"✓ NumPy {np.__version__} imported successfully")
        
        import pandas as pd
        logger.info(f"✓ Pandas {pd.__version__} imported successfully")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False

def test_gpu_availability():
    """Test GPU availability and configuration"""
    logger.info("Testing GPU availability...")
    
    try:
        import tensorflow as tf
        
        # Check for GPU devices
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            logger.info(f"✓ Found {len(gpus)} GPU(s):")
            for i, gpu in enumerate(gpus):
                logger.info(f"  GPU {i}: {gpu}")
                
            # Test GPU memory configuration
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logger.info("✓ GPU memory growth configured")
            except Exception as e:
                logger.warning(f"⚠ GPU memory configuration warning: {e}")
                
        else:
            logger.warning("⚠ No GPU devices found, will use CPU")
            
        return True
        
    except Exception as e:
        logger.error(f"✗ GPU test error: {e}")
        return False

def test_cuda_compatibility():
    """Test CUDA compatibility"""
    logger.info("Testing CUDA compatibility...")
    
    try:
        import tensorflow as tf
        
        # Check if CUDA is built with TensorFlow
        cuda_built = tf.test.is_built_with_cuda()
        logger.info(f"TensorFlow built with CUDA: {cuda_built}")
        
        if cuda_built:
            # Check CUDA version
            cuda_version = tf.sysconfig.get_build_info().get('cuda_version', 'Unknown')
            cudnn_version = tf.sysconfig.get_build_info().get('cudnn_version', 'Unknown')
            logger.info(f"CUDA version: {cuda_version}")
            logger.info(f"cuDNN version: {cudnn_version}")
            
        return True
        
    except Exception as e:
        logger.error(f"✗ CUDA compatibility test error: {e}")
        return False

def test_model_path():
    """Test if the Gemma model path exists and has required files"""
    logger.info("Testing model path...")
    
    model_path = Path("../models/gemma3-keras-gemma3_1b-v3")
    
    if not model_path.exists():
        logger.error(f"✗ Model path does not exist: {model_path}")
        return False
        
    logger.info(f"✓ Model path exists: {model_path}")
    
    # Check for required files
    required_files = [
        "config.json",
        "tokenizer.json",
        "task.json"
    ]
    
    for file_name in required_files:
        file_path = model_path / file_name
        if file_path.exists():
            logger.info(f"✓ Found: {file_name}")
        else:
            logger.warning(f"⚠ Missing: {file_name}")
    
    # Check assets directory
    assets_path = model_path / "assets"
    if assets_path.exists():
        logger.info(f"✓ Assets directory exists")
        
        # Check tokenizer assets
        tokenizer_path = assets_path / "tokenizer"
        if tokenizer_path.exists():
            vocab_file = tokenizer_path / "vocabulary.spm"
            if vocab_file.exists():
                logger.info(f"✓ Vocabulary file exists: {vocab_file}")
            else:
                logger.warning(f"⚠ Vocabulary file missing: {vocab_file}")
        else:
            logger.warning(f"⚠ Tokenizer assets missing: {tokenizer_path}")
    else:
        logger.warning(f"⚠ Assets directory missing: {assets_path}")
    
    return True

def test_datasets():
    """Test if datasets are available and properly formatted"""
    logger.info("Testing datasets...")
    
    datasets_path = Path(".")
    
    # Look for JSON files
    json_files = list(datasets_path.glob("*.json"))
    
    if not json_files:
        logger.warning("⚠ No JSON dataset files found")
        return False
        
    logger.info(f"✓ Found {len(json_files)} JSON dataset files:")
    
    total_examples = 0
    for json_file in json_files:
        try:
            import json
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                count = 1
            else:
                count = 0
                
            total_examples += count
            logger.info(f"  {json_file.name}: {count} examples")
            
        except Exception as e:
            logger.warning(f"⚠ Error reading {json_file.name}: {e}")
            
    logger.info(f"✓ Total training examples: {total_examples}")
    return total_examples > 0

def test_simple_model_loading():
    """Test basic model loading without full initialization"""
    logger.info("Testing basic model loading...")
    
    try:
        import keras_hub
        
        model_path = "../models/gemma3-keras-gemma3_1b-v3"
        
        # Try to load just the tokenizer first
        logger.info("Testing tokenizer loading...")
        try:
            tokenizer = keras_hub.models.Gemma3Tokenizer.from_preset(
                model_path
            )
            logger.info("✓ Tokenizer loaded successfully")
            logger.info(f"✓ Vocabulary size: {tokenizer.vocabulary_size}")
            
            # Test tokenization
            test_text = "Hello, world!"
            tokens = tokenizer(test_text)
            logger.info(f"✓ Tokenization test passed: '{test_text}' -> {len(tokens)} tokens")
            
            # Try to load the preprocessor
            logger.info("Testing preprocessor loading...")
            try:
                preprocessor = keras_hub.models.Gemma3CausalLMPreprocessor.from_preset(
                    model_path
                )
                logger.info("✓ Preprocessor loaded successfully")
                
                # Test preprocessing
                processed = preprocessor(test_text)
                logger.info("✓ Preprocessing test passed")
                
                return True
                
            except Exception as e:
                logger.error(f"✗ Preprocessor loading failed: {e}")
                return False
            
        except Exception as e:
            logger.error(f"✗ Tokenizer loading failed: {e}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Model loading test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting KerasHub setup verification...")
    logger.info("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("CUDA Compatibility", test_cuda_compatibility),
        ("GPU Availability", test_gpu_availability),
        ("Model Path", test_model_path),
        ("Datasets", test_datasets),
        ("Basic Model Loading", test_simple_model_loading),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"✗ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("TEST SUMMARY:")
    logger.info("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Ready for fine-tuning.")
    elif passed >= total - 1:
        logger.info("✅ Most tests passed. You can proceed with caution.")
    else:
        logger.warning("⚠ Several tests failed. Please check the issues above.")
        
    return passed >= total - 1  # Allow one test to fail

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 