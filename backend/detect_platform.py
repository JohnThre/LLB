#!/usr/bin/env python3
"""
Platform detection utility for LLB Backend
Optimizes dependencies and configurations for Apple Silicon
"""

import platform
import sys
import subprocess
import os

def detect_platform():
    """Detect the current platform and architecture"""
    system = platform.system()
    machine = platform.machine()
    
    print(f"System: {system}")
    print(f"Architecture: {machine}")
    print(f"Python version: {sys.version}")
    
    # Check for Apple Silicon
    is_apple_silicon = system == "Darwin" and machine == "arm64"
    
    if is_apple_silicon:
        print("🍎 Apple Silicon (M1/M2/M3) detected!")
        return "apple_silicon"
    elif system == "Darwin" and machine == "x86_64":
        print("🍎 Intel Mac detected")
        return "intel_mac"
    elif system == "Linux" and machine == "x86_64":
        print("🐧 Linux x86_64 detected")
        return "linux_x64"
    elif system == "Linux" and machine == "aarch64":
        print("🐧 Linux ARM64 detected")
        return "linux_arm64"
    else:
        print(f"⚠️ Unknown platform: {system} {machine}")
        return "unknown"

def check_torch_compatibility():
    """Check PyTorch installation and Apple Silicon compatibility"""
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} installed")
        
        # Check for MPS (Metal Performance Shaders) support on Apple Silicon
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("🚀 Apple Metal Performance Shaders (MPS) available!")
            print("   GPU acceleration enabled for Apple Silicon")
        elif torch.cuda.is_available():
            print("🚀 CUDA GPU acceleration available")
        else:
            print("💻 CPU-only PyTorch installation")
            
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    
    return True

def optimize_for_platform():
    """Provide platform-specific optimization recommendations"""
    platform_type = detect_platform()
    
    if platform_type == "apple_silicon":
        print("\n🔧 Apple Silicon Optimizations:")
        print("  • Use native ARM64 Python and packages when possible")
        print("  • PyTorch with MPS support for GPU acceleration")
        print("  • Consider using Accelerate framework for ML operations")
        
        # Check if running under Rosetta
        try:
            result = subprocess.run(['sysctl', '-n', 'sysctl.proc_translated'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() == '1':
                print("  ⚠️ Running under Rosetta 2 - consider native ARM64 Python")
        except:
            pass
            
    elif platform_type == "intel_mac":
        print("\n🔧 Intel Mac Optimizations:")
        print("  • Standard x86_64 optimizations apply")
        print("  • Consider upgrading to Apple Silicon for better ML performance")
        
    print(f"\n📊 Platform Summary:")
    print(f"  Platform: {platform_type}")
    check_torch_compatibility()

if __name__ == "__main__":
    optimize_for_platform()