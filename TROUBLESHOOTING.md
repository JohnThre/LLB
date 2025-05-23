# LLB Fine-tuning Troubleshooting Guide

## Current Issues and Solutions

### 1. CUDA Version Conflicts

**Problem**: PyTorch expects CUDA 12.1, but you have CUDA 12.8 installed.

**Solution**: Use the clean setup script that removes PyTorch and uses only TensorFlow:

```bash
./clean_setup_keras.sh
```

This script:
- Removes conflicting PyTorch packages
- Sets CUDA 12.8 environment variables
- Installs TensorFlow 2.19.0 with CUDA support
- Configures GPU memory growth

### 2. Deprecated tensorflow-gpu Package

**Problem**: `tensorflow-gpu>=2.15.0` package doesn't exist for newer versions.

**Solution**: Use `tensorflow[and-cuda]` instead, which includes GPU support:

```bash
pip install tensorflow[and-cuda]>=2.15.0
```

### 3. GPU Memory Issues

**Problem**: GPU runs out of memory during training.

**Solutions**:
- Use batch_size=1 for 16GB RAM systems
- Use float16 precision
- Enable GPU memory growth
- Close other GPU-intensive applications

### 4. Model Loading Errors

**Problem**: KerasHub can't load the Gemma model.

**Solutions**:
1. Verify model path: `ai/models/gemma3-keras-gemma3_1b-v3/`
2. Check required files exist:
   - `config.json`
   - `tokenizer.json` 
   - `task.json`
   - `assets/tokenizer/vocabulary.spm`

## Step-by-Step Fix Process

### Step 1: Clean Environment Setup

```bash
# Run the clean setup script
./clean_setup_keras.sh
```

### Step 2: Verify Setup

```bash
cd ai/datasets
python test_keras_setup.py
```

### Step 3: Test Fine-tuning

```bash
python finetune_gemma_keras.py
```

## Environment Variables for CUDA 12.8

Add these to your `~/.bashrc`:

```bash
export CUDA_HOME=/usr/local/cuda-12.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH
```

Then reload:
```bash
source ~/.bashrc
```

## Memory Optimization Settings

### For 16GB RAM Systems:
```python
batch_size = 1
dtype = "float16"
max_length = 512
```

### For 32GB+ RAM Systems:
```python
batch_size = 2-4
dtype = "float16"
max_length = 512
```

## GPU Configuration

```python
import tensorflow as tf

# Configure GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
```

## Common Error Messages and Solutions

### Error: "Unable to register cuFFT factory"
**Solution**: This is a warning, not an error. TensorFlow will still work.

### Error: "No module named 'keras_hub'"
**Solution**: 
```bash
pip install keras-hub>=0.17.0
```

### Error: "Model path does not exist"
**Solution**: Verify the Gemma model is extracted to:
```
ai/models/gemma3-keras-gemma3_1b-v3/
```

### Error: "No training data found"
**Solution**: Ensure JSON files are in `ai/datasets/` directory with proper format.

### Error: "CUDA out of memory"
**Solutions**:
1. Reduce batch size to 1
2. Use float16 precision
3. Close other applications
4. Restart the system

## Verification Commands

### Check CUDA Installation:
```bash
nvcc --version
nvidia-smi
```

### Check TensorFlow GPU:
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Check Package Versions:
```bash
python -c "
import tensorflow as tf
import keras
import keras_hub
print(f'TensorFlow: {tf.__version__}')
print(f'Keras: {keras.__version__}')
print(f'KerasHub: {keras_hub.__version__}')
"
```

## Performance Monitoring

### Monitor GPU Usage:
```bash
watch -n 1 nvidia-smi
```

### Monitor Memory Usage:
```bash
htop
```

## If All Else Fails

### Nuclear Option - Complete Reset:

1. **Backup your datasets**:
   ```bash
   cp ai/datasets/*.json ~/backup/
   ```

2. **Remove virtual environment**:
   ```bash
   rm -rf llb-env
   ```

3. **Create new environment**:
   ```bash
   python3 -m venv llb-env
   source llb-env/bin/activate
   ```

4. **Run clean setup**:
   ```bash
   ./clean_setup_keras.sh
   ```

5. **Restore datasets**:
   ```bash
   cp ~/backup/*.json ai/datasets/
   ```

## Contact Information

If issues persist:
1. Run the test script: `python test_keras_setup.py`
2. Check the logs for specific error messages
3. Verify all prerequisites are met
4. Consider using CPU-only mode for testing

## Hardware-Specific Notes

### For RTX 3060 12GB:
- Use batch_size=2
- Enable mixed precision
- Monitor VRAM usage

### For Integrated Graphics:
- Use CPU-only mode
- Increase batch_size to 4-8
- Expect slower training

### For WSL2:
- Ensure CUDA is properly installed in WSL2
- Use Windows NVIDIA drivers
- Check WSL2 GPU support is enabled 