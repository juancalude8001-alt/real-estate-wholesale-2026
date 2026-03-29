#!/bin/bash
# Real Estate Wholesale System - GitHub Push Script
# Run this to push your code to GitHub

cd "$(dirname "$0")" || exit 1

echo "🚀 Pushing Real Estate Wholesale System to GitHub..."
echo ""

# Configure git
git config --global user.email "juancalude8001@gmail.com"
git config --global user.name "Juan Claude Jordan"
git config --global credential.helper cache

echo "📍 Repo: https://github.com/juancalude8001-alt/real-estate-wholesale"
echo ""

# Show what we're about to push
echo "📊 Files to push:"
git status --short | wc -l
echo "files"
echo ""

# Push to GitHub
echo "Pushing..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Code is now on GitHub!"
else
    echo ""
    echo "❌ Push failed - provide GitHub token or use browser auth"
fi
