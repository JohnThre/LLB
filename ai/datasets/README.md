# LLB AI Fine-tuning with KerasHub

This directory contains the fine-tuning scripts and datasets for the LLB (爱学伴) sexual health education AI model using Google's Gemma 3 1B model with KerasHub.

## Overview

The fine-tuning system has been updated to use KerasHub instead of HuggingFace Transformers to properly work with the Keras-based Gemma model downloaded from Kaggle.

## Files Structure

```
ai/datasets/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── finetune_gemma_keras.py     # New KerasHub-based fine-tuning script
├── finetune_gemma.py           # Original HF script (deprecated)
├── *.json                      # Training datasets
└── test_keras_setup.py         # Setup verification script
```

## Prerequisites

1. **Virtual Environment**: Ensure you have activated the `llb-env` virtual environment:
   ```bash
   source llb-env/bin/activate
   ```

2. **Gemma Model**: The Keras-based Gemma 3 1B model should be extracted in:
   ```
   ai/models/gemma3-keras-gemma3_1b-v3/
   ```

3. **Hardware Requirements**:
   - Minimum: 16GB RAM, 8th Gen Intel i7
   - Recommended: 32GB RAM, NVIDIA RTX 3060 12GB or better

## Setup Instructions

### 1. Install Dependencies

Run the setup script from the project root:
```bash
./setup_keras_env.sh
```

Or manually install:
```bash
source llb-env/bin/activate
pip install --upgrade pip
pip install tensorflow[and-cuda]>=2.15.0
pip install keras>=3.0.0
pip install keras-hub>=0.17.0
pip install -r ai/datasets/requirements.txt
```

### 2. Verify Setup

Run the verification script:
```bash
cd ai/datasets
python ../../test_keras_setup.py
```

This will test:
- Package imports
- GPU availability
- Model path and files
- Dataset availability
- Model loading capability

## Fine-tuning Process

### 1. Prepare Datasets

Ensure your training data is in JSON format with one of these structures:

**Instruction-Response format:**
```json
[
  {
    "instruction": "什么是安全性行为？",
    "response": "安全性行为是指采取预防措施来降低性传播疾病和意外怀孕风险的性活动..."
  }
]
```

**Question-Answer format:**
```json
[
  {
    "question": "What is safe sex?",
    "answer": "Safe sex refers to sexual practices that reduce the risk of transmitting or acquiring sexually transmitted infections..."
  }
]
```

**Input-Output format:**
```json
[
  {
    "input": "如何预防性传播疾病？",
    "output": "预防性传播疾病的方法包括：1. 使用安全套..."
  }
]
```

### 2. Run Fine-tuning

```bash
cd ai/datasets
python finetune_gemma_keras.py
```

### 3. Configuration Options

You can modify the fine-tuning parameters in the `main()` function:

```python
# Fine-tune the model
history = fine_tuner.fine_tune(
    train_dataset,
    epochs=3,              # Number of training epochs
    batch_size=1,          # Batch size (adjust based on memory)
    learning_rate=5e-5,    # Learning rate
    max_length=512         # Maximum sequence length
)
```

### 4. Memory Optimization

For systems with limited memory:
- Use `batch_size=1`
- Use `dtype="float16"` for the model
- Enable GPU memory growth
- Close other applications during training

## Output

The fine-tuned model will be saved to:
```
ai/models/fine_tuned/fine_tuned_gemma/
```

This includes:
- Model weights and configuration
- Tokenizer
- Training information (`training_info.json`)

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'keras_hub'**
   ```bash
   pip install keras-hub>=0.17.0
   ```

2. **CUDA/GPU Issues**
   ```bash
   # Check GPU availability
   python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
   ```

3. **Memory Issues**
   - Reduce batch size to 1
   - Use float16 precision
   - Close other applications
   - Consider using CPU-only mode

4. **Model Loading Issues**
   - Verify model path: `ai/models/gemma3-keras-gemma3_1b-v3/`
   - Check if all required files exist
   - Run the test script to diagnose

### Error Messages

**"No training data found!"**
- Ensure JSON files are in the `ai/datasets/` directory
- Check JSON file format matches expected structure

**"Model path does not exist"**
- Verify the Gemma model is extracted correctly
- Check the path in the script matches your setup

**"Insufficient memory"**
- Reduce batch size
- Use float16 precision
- Enable GPU memory growth

## Performance Tips

1. **GPU Optimization**:
   - Use NVIDIA RTX 3060 or better
   - Enable CUDA memory growth
   - Use mixed precision training

2. **CPU Optimization**:
   - Use multiple CPU cores
   - Enable TensorFlow optimizations
   - Close unnecessary applications

3. **Data Optimization**:
   - Preprocess datasets
   - Use appropriate sequence lengths
   - Balance dataset sizes

## Testing the Fine-tuned Model

After fine-tuning, test the model with sample prompts:

```python
# The script automatically tests with these prompts:
test_prompts = [
    "什么是安全性行为？",
    "What is safe sex?",
    "如何预防性传播疾病？",
    "How to prevent sexually transmitted diseases?",
    "青少年性教育的重要性是什么？"
]
```

## Integration with Web Application

The fine-tuned model can be integrated into the LLB web application:

1. Update the model path in the backend configuration
2. Use the same KerasHub loading mechanism
3. Implement the chat interface with the fine-tuned model

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Run the verification script: `python test_keras_setup.py`
3. Review the training logs for specific error messages
4. Ensure all prerequisites are met

## License

This project uses Google's Gemma model under the Gemma Terms of Use. 