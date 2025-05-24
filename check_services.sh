#!/bin/bash

echo "🔍 Checking LLB Services Status..."
echo ""

# Check if processes are running
echo "📊 Process Status:"
if pgrep -f "uvicorn app.main:app" > /dev/null; then
    echo "✅ Backend (uvicorn) is running"
else
    echo "❌ Backend (uvicorn) is not running"
fi

if pgrep -f "vite.*--port 3000" > /dev/null; then
    echo "✅ Frontend (vite) is running"
else
    echo "❌ Frontend (vite) is not running"
fi

echo ""
echo "🌐 Service Connectivity:"

# Check frontend
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "✅ Frontend accessible at http://localhost:3000 (Status: $FRONTEND_STATUS)"
else
    echo "❌ Frontend not accessible at http://localhost:3000 (Status: $FRONTEND_STATUS)"
fi

# Check backend
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
if [ "$BACKEND_STATUS" = "200" ]; then
    echo "✅ Backend accessible at http://localhost:8000 (Status: $BACKEND_STATUS)"
    echo "📚 API Documentation: http://localhost:8000/docs"
else
    echo "❌ Backend not accessible at http://localhost:8000 (Status: $BACKEND_STATUS)"
fi

echo ""
echo "🔗 Access URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""

# Check if running in WSL
if grep -q microsoft /proc/version; then
    echo "💡 WSL Detected: You can also access from Windows at:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
fi 