#!/bin/bash

echo "🚀 Setting up Ara Hackathon Project..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Don't forget to add your API keys to .env!"
fi

# Create data directory
mkdir -p data

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your ANTHROPIC_API_KEY to .env"
echo "2. Run: source venv/bin/activate"
echo "3. Run: uvicorn main:app --reload"
echo "4. Open: http://localhost:8000"
echo ""
echo "Good luck at the hackathon! 🎉"
