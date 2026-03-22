#!/bin/bash
# ─────────────────────────────────────────
#  NK Facts – Quick Setup Script
# ─────────────────────────────────────────
echo "🌸 Setting up NK Facts..."

# 1. Install dependencies
pip install django pillow

# 2. Apply migrations
python manage.py migrate

# 3. Create a superuser (optional – for admin panel)
echo ""
echo "🔑 Creating superuser for /admin panel..."
echo "   (Press Ctrl+C to skip)"
python manage.py createsuperuser

# 4. Run dev server
echo ""
echo "🚀 Starting NK Facts at http://127.0.0.1:8000"
python manage.py runserver
