#!/bin/bash
# Wrapper script for cron job execution

# Set working directory
cd /Users/amandafernandez

# Initialize pyenv if available (for proper Python environment)
if [ -d "$HOME/.pyenv" ]; then
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Log file with date
LOG_FILE="logs/ny_alerts_$(date +%Y%m%d).log"

# Run the script and capture output
echo "=====================================================" >> "$LOG_FILE"
echo "New York Rare Bird Alert - $(date)" >> "$LOG_FILE"
echo "=====================================================" >> "$LOG_FILE"

/Users/amandafernandez/.pyenv/shims/python run_ny_alerts.py >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "Completed at $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
