#!/bin/bash
set -e  # Exit if any command fails

# Start from home directory to avoid relative path issues
cd ~ || { echo "❌ Cannot go to home directory"; exit 1; }

# GlobalSoft server path (where docker-compose.yml lives)
GS_PATH="/var/www/global-soft"

echo "📡 Navigating to GlobalSoft folder..."
cd $GS_PATH || { echo "❌ GlobalSoft folder not found at $GS_PATH"; exit 1; }

# Pull latest code from Git
echo "📥 Pulling latest code from Git..."
git pull || echo "⚠️ Git pull failed or no repo detected, skipping."

# Stop existing containers
echo "📦 Stopping existing containers..."
docker-compose down

# Rebuild and start containers
echo "📦 Rebuilding and starting containers..."
docker-compose up -d --build

echo "✅ Deployment complete!"