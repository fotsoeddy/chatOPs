#!/bin/bash
set -e  # Stop if any command fails

echo "📡 Going to GlobalSoft folder..."
cd /var/www/global-soft

echo "📥 Pull latest code..."
git pull origin main

echo "🛑 Bring down existing containers..."
docker compose down

echo "📦 Build and restart containers..."
docker compose up -d --build

echo "✅ Deployment done!"