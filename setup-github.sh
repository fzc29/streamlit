#!/bin/bash
# Script to set up GitHub repository

echo "🚀 Setting up GitHub repository..."

# Navigate to project directory
cd "$(dirname "$0")"

# Initialize git (if not already)
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
else
    echo "Git repository already initialized"
fi

# Check if .env exists and warn
if [ -f ".env" ]; then
    echo "⚠️  WARNING: .env file exists!"
    echo "   Make sure .env is in .gitignore (it should be)"
    echo ""
fi

# Show what will be committed
echo "📋 Files that will be committed:"
git status --short | head -20

echo ""
echo "✅ Next steps:"
echo "1. Review the files above"
echo "2. Make sure .env is NOT listed (it should be ignored)"
echo "3. Run: git add ."
echo "4. Run: git commit -m 'Initial commit'"
echo "5. Create a repo on GitHub, then:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "📖 See GITHUB_SETUP.md for detailed instructions"

