#!/bin/bash

# Create a global deepcast wrapper

echo "Creating global deepcast wrapper..."

# Create a directory for the module
mkdir -p ~/.local/lib/deepcast_post

# Copy the module files
cp -r deepcast_post/* ~/.local/lib/deepcast_post/

# Create the wrapper script
cat > ~/.local/bin/deepcast << 'EOF'
#!/bin/bash

# Add the module path to Python path
export PYTHONPATH="$HOME/.local/lib:$PYTHONPATH"

# Get the project directory for .env file
PROJECT_DIR="$HOME/code/deepcast_post"

# Run the CLI tool using the virtual environment Python
# The tool will handle .env loading internally
"$HOME/code/deepcast_post/.direnv/python-3.9/bin/python3" -m deepcast_post.cli "$@"
EOF

# Make it executable
chmod +x ~/.local/bin/deepcast

echo "✅ Global deepcast wrapper created!"
echo "You can now run 'deepcast' from anywhere."
echo ""
echo "Make sure your OpenAI API key is set in ~/code/deepcast_post/.env" 