#!/bin/bash
# Setup Docker buildx for multi-platform builds (Apple Silicon support)

set -e

echo "🔧 Setting up Docker buildx for multi-platform builds..."

# Create a new builder instance
echo "📦 Creating buildx builder instance..."
docker buildx create --name llb-builder --driver docker-container --bootstrap --use

# Inspect the builder
echo "🔍 Inspecting builder capabilities..."
docker buildx inspect --bootstrap

# Enable experimental features
echo "🧪 Enabling experimental Docker features..."
export DOCKER_CLI_EXPERIMENTAL=enabled

echo ""
echo "✅ Docker buildx setup complete!"
echo ""
echo "🚀 Available platforms:"
docker buildx inspect | grep Platforms

echo ""
echo "📋 Usage examples:"
echo "  # Build for Apple Silicon:"
echo "  docker buildx build --platform linux/arm64 -t llb-backend:arm64 ./backend"
echo ""
echo "  # Build for multiple platforms:"
echo "  docker buildx build --platform linux/amd64,linux/arm64 -t llb-backend:latest ./backend"
echo ""
echo "  # Use with docker-compose:"
echo "  DOCKER_DEFAULT_PLATFORM=linux/arm64 docker-compose up --build"