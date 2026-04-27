#!/bin/bash

# PythonAnywhere Deployment Script for Peyem Project
# Replace 'your-username' with your actual PythonAnywhere username

echo "🚀 Starting PythonAnywhere deployment for Peyem Project..."

# Create and activate virtual environment
echo "📦 Creating virtual environment..."
mkvirtualenv --python=python3.10 peyem_env
workon peyem_env

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/PeterEdisonSultan/peyem_project.git
cd peyem_project/

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Setup database
echo "🗄️ Setting up database..."
python manage.py migrate

# Create superuser (interactive)
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Update configuration files with actual username
echo "⚙️ Updating configuration files..."
# Note: Replace 'your-username' with your actual username in the commands below
sed -i 's/your-username/YOUR_ACTUAL_USERNAME/g' peyem/wsgi.py
sed -i 's/your-username/YOUR_ACTUAL_USERNAME/g' peyem/settings_production.py

# Test the application
echo "🧪 Testing application..."
python manage.py check

echo "✅ Deployment script completed!"
echo "📋 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Add new web app with manual configuration"
echo "3. Set source code path to: /home/YOUR_USERNAME/peyem_project"
echo "4. Set WSGI file path to: /home/YOUR_USERNAME/peyem_project/peyem/wsgi.py"
echo "5. Set virtualenv path to: /home/YOUR_USERNAME/.virtualenvs/peyem_env"
echo "6. Configure static files"
echo "7. Reload the web app"