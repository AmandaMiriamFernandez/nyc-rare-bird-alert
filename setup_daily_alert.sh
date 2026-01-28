#!/bin/bash
# Setup script for daily New York Rare Bird Alert

SCRIPT_DIR="/Users/amandafernandez"
PYTHON_PATH=$(which python3)

echo "======================================================"
echo "  New York Rare Bird Alert - Daily Cron Setup"
echo "======================================================"
echo ""
echo "This will set up a daily cron job to run at 8:00 AM"
echo ""

# Create a wrapper script that handles logging
cat > "$SCRIPT_DIR/run_ny_alerts_cron.sh" << 'EOF'
#!/bin/bash
# Wrapper script for cron job execution

# Set working directory
cd /Users/amandafernandez

# Create logs directory if it doesn't exist
mkdir -p logs

# Log file with date
LOG_FILE="logs/ny_alerts_$(date +%Y%m%d).log"

# Run the script and capture output
echo "=====================================================" >> "$LOG_FILE"
echo "New York Rare Bird Alert - $(date)" >> "$LOG_FILE"
echo "=====================================================" >> "$LOG_FILE"

python3 run_ny_alerts.py >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "Completed at $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
EOF

chmod +x "$SCRIPT_DIR/run_ny_alerts_cron.sh"

echo "✅ Created wrapper script: run_ny_alerts_cron.sh"
echo ""

# Show the cron entry that will be added
CRON_ENTRY="0 8 * * * $SCRIPT_DIR/run_ny_alerts_cron.sh"

echo "The following cron job will be added:"
echo "  Time: Daily at 8:00 AM"
echo "  Command: $CRON_ENTRY"
echo ""
echo "Logs will be saved to: $SCRIPT_DIR/logs/"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "run_ny_alerts_cron.sh"; then
    echo "⚠️  Cron job already exists!"
    echo ""
    read -p "Do you want to replace it? (y/n): " replace
    if [ "$replace" != "y" ]; then
        echo "Setup cancelled."
        exit 0
    fi
    # Remove old entry
    crontab -l 2>/dev/null | grep -v "run_ny_alerts_cron.sh" | crontab -
    echo "✅ Removed old cron job"
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job added successfully!"
echo ""
echo "======================================================"
echo "  Setup Complete!"
echo "======================================================"
echo ""
echo "Your NY Rare Bird Alert will now run daily at 8:00 AM"
echo ""
echo "Useful commands:"
echo "  • View cron jobs:    crontab -l"
echo "  • Edit cron jobs:    crontab -e"
echo "  • Remove cron job:   crontab -e (then delete the line)"
echo "  • View logs:         cat logs/ny_alerts_*.log"
echo "  • Test now:          ./run_ny_alerts_cron.sh"
echo ""
echo "Output files will be saved as:"
echo "  • ny_rare_birds_YYYYMMDD_HHMMSS.csv"
echo "  • ny_rare_birds_YYYYMMDD_HHMMSS.json"
echo ""
