#!/usr/bin/env bash
# VoxaLab AI - Hugging Face Spaces Push Script

# This script prepares and pushes your application to HF Spaces

# 1. Verify files are ready
echo "📦 Verifying deployment package..."
test -f app.py && echo "  ✅ app.py found"
test -f requirements.txt && echo "  ✅ requirements.txt found"
test -d frontend/build && echo "  ✅ frontend/build found"
test -f .env && echo "  ✅ .env found"

# 2. Verify git is ready
echo "📝 Checking git status..."
git status

# 3. Instructions for pushing
echo ""
echo "🚀 Ready to Deploy!"
echo ""
echo "Next steps:"
echo "1. Go to https://huggingface.co/settings/tokens"
echo "2. Create a new token with WRITE permission"
echo "3. Run this command:"
echo ""
echo "   git push -u origin main"
echo ""
echo "4. When prompted:"
echo "   - Username: <your HF username>"
echo "   - Password: <paste your HF token>"
echo ""
echo "5. Wait 2-3 minutes for HF Spaces to build"
echo "6. Visit: https://huggingface.co/spaces/mistral-hackaton-2026/voxalab"
echo ""
echo "✅ Deployment will be automatic!"
