#!/bin/bash

# IELTS Study Buddy Bot - Stop Script

echo "🛑 Stopping IELTS Study Buddy Bot..."

if command -v docker-compose &> /dev/null; then
    docker-compose down
    echo "✅ Bot stopped (docker-compose)"
elif command -v docker &> /dev/null; then
    docker compose down
    echo "✅ Bot stopped (docker compose)"
else
    # Kill Python process
    pkill -f "python main.py"
    echo "✅ Bot stopped (python)"
fi
