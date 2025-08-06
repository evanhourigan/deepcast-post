#!/bin/bash

# Install deepcast_post CLI tool

echo "Installing deepcast_post CLI tool..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies using Poetry
echo "Installing dependencies..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        echo "Creating .env file from example..."
        cp env.example .env
        echo "✅ Created .env file"
        echo "⚠️  Please edit .env and add your OpenAI API key"
    else
        echo "Creating .env file..."
        echo "OPENAI_API_KEY=your-api-key-here" > .env
        echo "✅ Created .env file"
        echo "⚠️  Please edit .env and add your OpenAI API key"
    fi
else
    echo "✅ .env file already exists"
fi

# Create a simple wrapper script
cat > deepcast << 'EOF'
#!/bin/bash
# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

# Run the CLI tool directly with Python
cd "$PROJECT_DIR" && python3 -m deepcast_post.cli "$@"
EOF

# Make the script executable
chmod +x deepcast

# Move to a directory in PATH (if possible)
if [ -d "$HOME/.local/bin" ]; then
    mv deepcast "$HOME/.local/bin/"
    echo "✅ CLI tool installed to $HOME/.local/bin/deepcast"
    echo "You can now run: deepcast --help"
elif [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    sudo mv deepcast /usr/local/bin/
    echo "✅ CLI tool installed to /usr/local/bin/deepcast"
    echo "You can now run: deepcast --help"
else
    echo "✅ CLI script created in current directory"
    echo "You can run: ./deepcast --help"
    echo "Or add current directory to PATH to use 'deepcast' command"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run: deepcast --help"
echo ""
echo "If you're using direnv, the environment will be automatically loaded."
echo "Otherwise, run: poetry shell" 