#!/bin/bash

# IELTS Study Buddy Bot - Start Script

echo "🤖 IELTS Study Buddy Bot"
echo "========================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Please create .env file:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env and add your bot token and user IDs"
    exit 1
fi

# Check if docker is available
if command -v docker-compose &> /dev/null; then
    echo "🐳 Starting bot with Docker..."
    docker-compose up -d
    echo ""
    echo "✅ Bot started!"
    echo ""
    echo "📝 View logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "🛑 Stop bot:"
    echo "  docker-compose down"
elif command -v docker &> /dev/null; then
    echo "🐳 Starting bot with Docker..."
    docker compose up -d
    echo ""
    echo "✅ Bot started!"
    echo ""
    echo "📝 View logs:"
    echo "  docker compose logs -f"
    echo ""
    echo "🛑 Stop bot:"
    echo "  docker compose down"
else
    echo "🐍 Starting bot with Python..."

    # Check if venv exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate venv
    source venv/bin/activate

    # Install dependencies
    echo "Installing dependencies..."
    pip install -q -r requirements.txt

    # Run bot
    echo ""
    echo "✅ Starting bot..."
    python main.py
fi
