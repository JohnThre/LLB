#!/bin/bash
# Clean setup script for KerasHub-based Gemma fine-tuning environment
# Handles CUDA 12.8 and resolves dependency conflicts

echo "🚀 Setting up clean KerasHub environment for Gemma fine-tuning..."

# Activate the virtual environment
source llb-env/bin/activate

# Set CUDA 12.8 environment variables
echo "🔧 Setting CUDA 12.8 environment variables..."
export CUDA_HOME=/usr/local/cuda-12.8
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH

# Also set for current session
echo "export CUDA_HOME=/usr/local/cuda-12.8" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=\$CUDA_HOME/lib64:\$LD_LIBRARY_PATH" >> ~/.bashrc
echo "export PATH=\$CUDA_HOME/bin:\$PATH" >> ~/.bashrc

# Clean up conflicting packages
echo "🧹 Cleaning up conflicting packages..."
pip uninstall -y torch torchvision torchaudio transformers peft bitsandbytes trl

# Upgrade pip and setuptools
echo "📦 Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install TensorFlow with CUDA support first
echo "🤖 Installing TensorFlow with CUDA support..."
pip install --upgrade tensorflow[and-cuda]==2.19.0

# Install Keras and KerasHub
echo "🔧 Installing Keras and KerasHub..."
pip install --upgrade keras==3.10.0
pip install --upgrade keras-hub==0.20.0

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install --upgrade numpy==1.26.3
pip install --upgrade pandas==2.2.0
pip install --upgrade sentencepiece==0.1.99
pip install --upgrade protobuf==4.25.2
pip install --upgrade tqdm==4.67.1
pip install --upgrade safetensors==0.5.3
pip install --upgrade datasets==3.6.0

# Verify CUDA setup
echo "🔍 Verifying CUDA setup..."
nvcc --version
nvidia-smi

# Test TensorFlow GPU
echo "🧪 Testing TensorFlow GPU support..."
python -c "
import tensorflow as tf
print(f'TensorFlow version: {tf.__version__}')
print(f'CUDA built: {tf.test.is_built_with_cuda()}')
print(f'GPU devices: {tf.config.list_physical_devices(\"GPU\")}')

# Configure GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print('✅ GPU memory growth configured successfully')
    except RuntimeError as e:
        print(f'⚠️ GPU configuration warning: {e}')
else:
    print('⚠️ No GPU detected')
"

# Test Keras and KerasHub
echo "🧪 Testing Keras and KerasHub..."
python -c "
import keras
import keras_hub
print(f'Keras version: {keras.__version__}')
print(f'KerasHub version: {keras_hub.__version__}')
print('✅ Keras and KerasHub imported successfully')
"

echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Run: cd ai/datasets && python test_keras_setup.py"
echo "2. If tests pass, run: python finetune_gemma_keras.py"
echo ""
echo "💡 Tips:"
echo "- Use batch_size=1 for 16GB RAM systems"
echo "- Use batch_size=2-4 for 32GB+ RAM systems"
echo "- Monitor GPU memory usage during training" 