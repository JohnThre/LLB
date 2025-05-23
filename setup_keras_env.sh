#!/bin/bash
# Setup script for KerasHub-based Gemma fine-tuning environment

echo "Setting up KerasHub environment for Gemma fine-tuning..."

# Activate the virtual environment
source llb-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Set CUDA environment variables for CUDA 12.8
export CUDA_HOME=/usr/local/cuda-12.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH

# Uninstall conflicting PyTorch packages to avoid CUDA conflicts
echo "Removing conflicting PyTorch packages..."
pip uninstall -y torch torchvision torchaudio

# Install TensorFlow with CUDA support (works with CUDA 12.x)
echo "Installing TensorFlow with CUDA support..."
pip install tensorflow[and-cuda]>=2.15.0

# Install Keras and KerasHub
echo "Installing Keras and KerasHub..."
pip install keras>=3.0.0
pip install keras-hub>=0.17.0

# Install other required packages
echo "Installing other dependencies..."
pip install -r ai/datasets/requirements.txt

# Verify installations
echo "Verifying installations..."
python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')"
python -c "import keras; print(f'Keras version: {keras.__version__}')"
python -c "import keras_hub; print(f'KerasHub version: {keras_hub.__version__}')"

# Test GPU availability
echo "Testing GPU availability..."
python -c "
import tensorflow as tf
print(f'GPU devices: {tf.config.list_physical_devices(\"GPU\")}')
if tf.config.list_physical_devices('GPU'):
    print('✓ GPU is available for TensorFlow')
    # Configure GPU memory growth
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print('✓ GPU memory growth configured')
        except RuntimeError as e:
            print(f'GPU configuration warning: {e}')
else:
    print('⚠ No GPU detected, will use CPU')
"

echo "Setup completed!"
echo "To activate the environment, run: source llb-env/bin/activate"
echo "To run fine-tuning, navigate to ai/datasets/ and run: python finetune_gemma_keras.py" 