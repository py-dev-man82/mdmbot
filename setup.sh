#!/bin/bash
set -e

echo "=== MDM Telegram Bot Setup ==="

# 1. Ensure Python 3.10+ is installed
PYTHON=$(which python3)
if ! $PYTHON --version | grep -qE "3\.(1[0-9]|[2-9][0-9])"; then
    echo "Error: Python 3.10 or higher is required."
    exit 1
fi

# 2. Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON -m venv venv
fi

source venv/bin/activate

# 3. Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Prompt for config values
echo "---- Configuration ----"
read -p "Enter your Telegram Bot Token: " TELEGRAM_BOT_TOKEN
read -p "Enter your MDM API URL (e.g. https://your-mdm.com/rest): " MDM_API_URL
read -p "Enter your MDM API Username: " MDM_USER
read -sp "Enter your MDM API Password: " MDM_PASS
echo
read -p "Enable DEBUG mode? (y/N): " DEBUG_ANSWER
DEBUG_MODE="False"
if [[ "$DEBUG_ANSWER" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    DEBUG_MODE="True"
fi

# 5. Write .env file
cat > .env <<EOF
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
MDM_API_URL=$MDM_API_URL
MDM_USER=$MDM_USER
MDM_PASS=$MDM_PASS
DEBUG_MODE=$DEBUG_MODE
EOF

echo "Saved configuration to .env"

echo
echo "=== Setup complete! ==="
echo "To start the bot:"
echo "  source venv/bin/activate"
echo "  python3 bot.py"
echo
echo "For production/autostart, consider using a systemd service."
