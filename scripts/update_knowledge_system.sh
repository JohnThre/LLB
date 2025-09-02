#!/bin/bash

# Update Knowledge System Script
# Date: 2025-09-02

echo "🚀 Updating LLB Knowledge System..."

# Navigate to backend directory
cd backend

# Run database migration
echo "📊 Running database migration..."
alembic upgrade head

# Navigate back to root
cd ..

# Add all changes to git
echo "📝 Adding changes to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "feat: Add AI-powered knowledge search and update system

- Add knowledge_entries and knowledge_updates database tables
- Implement KnowledgeService for AI-powered content generation
- Add SchedulerService for automated daily updates
- Create knowledge API endpoints for manual triggers
- Integrate scheduler with main application lifecycle
- Support both English and Chinese content generation
- Add quality scoring and verification system

Date: 2025-09-02"

echo "✅ Knowledge system update completed!"
echo ""
echo "🔗 New API endpoints available:"
echo "  - GET  /api/v1/knowledge/entries - Get knowledge entries"
echo "  - POST /api/v1/knowledge/update - Trigger manual update"
echo "  - GET  /api/v1/knowledge/updates - Get update history"
echo "  - GET  /api/v1/knowledge/scheduler/status - Get scheduler status"
echo ""
echo "📚 The system will automatically search and update sexual health knowledge daily."