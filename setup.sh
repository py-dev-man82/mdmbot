#!/bin/bash
set -e

echo "=== MDM Telegram Bot Setup ==="

# 1. Ensure Python 3.10+ is installed
PYTHON=$(which python3)
if ! $PYTHON --version | grep -qE "3\.(1[0-9]|[2-9][0-9])"; then
    echo "Error: Python 3.10 or higher is required."
    exit 1
fi

# 2. Create virtual environment if needed
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

# 6. Offer to set up as a systemd service
echo
read -p "Set up the bot to autostart on boot using systemd? (y/N): " AUTOSTART
if [[ "$AUTOSTART" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    SERVICE_NAME="mdm-bot"
    SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"
    BOT_DIR="$(pwd)"
    USERNAME="$(whoami)"

    echo "Creating systemd service file at $SERVICE_PATH"
    sudo bash -c "cat > $SERVICE_PATH" <<EOF
[Unit]
Description=MDM Telegram Bot
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$BOT_DIR
Environment=\"PATH=$BOT_DIR/venv/bin\"
ExecStart=$BOT_DIR/venv/bin/python3 $BOT_DIR/bot.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

    echo "Reloading systemd, enabling and starting $SERVICE_NAME..."
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl restart $SERVICE_NAME

    echo
    echo "Bot will now start automatically on boot and restart if it crashes."
    echo "Check logs with: sudo journalctl -u $SERVICE_NAME -f"
fi

echo
echo "=== Setup complete! ==="
echo "To run the bot manually:"
echo "  source venv/bin/activate"
echo "  python3 bot.py"
echo
echo "You can edit the .env file to change settings."
echo "To update the bot code, just restart the systemd service or rerun manually."
