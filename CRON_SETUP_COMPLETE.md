# ✅ New York Rare Bird Alert - Automatic Daily Updates

Your daily bird alert system is now fully configured and running!

## 🎯 What's Configured

- **Location**: New York State (Alert ID: SN35466)
- **Schedule**: Every day at **8:00 AM**
- **Data**: Rare/notable bird sightings from the past 7 days
- **Max Results**: 100 observations per run

## 📁 File Locations

### Scripts
- `run_ny_alerts.py` - Main alert script (customizable)
- `run_ny_alerts_cron.sh` - Cron wrapper (handles logging)
- `ebird_api_client.py` - Full-featured API client
- `config.json` - Your API key (keep this secure!)

### Output Files (generated daily)
- `ny_rare_birds_YYYYMMDD_HHMMSS.csv` - Spreadsheet format
- `ny_rare_birds_YYYYMMDD_HHMMSS.json` - Full API data

### Log Files
- `logs/ny_alerts_YYYYMMDD.log` - Daily execution logs

## 🔧 Useful Commands

### View Your Cron Jobs
```bash
crontab -l
```

### Edit Cron Schedule
```bash
crontab -e
```
Then modify the time (currently: `0 8 * * *` = 8:00 AM daily)

Cron time format:
```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

Examples:
- `0 8 * * *` = 8:00 AM daily
- `0 6 * * *` = 6:00 AM daily
- `0 12 * * 1` = Noon every Monday
- `0 8 * * 1,3,5` = 8:00 AM Monday, Wednesday, Friday

### Test Manually
```bash
./run_ny_alerts_cron.sh
```

### View Recent Logs
```bash
cat logs/ny_alerts_$(date +%Y%m%d).log
```

Or view all logs:
```bash
ls -lt logs/
```

### Remove the Cron Job
```bash
crontab -e
# Delete the line with run_ny_alerts_cron.sh, save and exit
```

## ⚙️ Customization

Edit `run_ny_alerts.py` at the top to change settings:

```python
# Days to look back (1-30)
DAYS_BACK = 7

# Maximum number of results to fetch
MAX_RESULTS = 100

# Region code
REGION_CODE = "US-NY"  # New York State

# Filter by specific counties (optional)
COUNTY_FILTER = []  # e.g., ['Manhattan', 'Queens']
```

### Example: Get Only Today's Alerts
```python
DAYS_BACK = 1
```

### Example: Filter to NYC Boroughs Only
```python
COUNTY_FILTER = ['Manhattan', 'Queens', 'Brooklyn', 'Bronx', 'Staten Island']
```

### Example: Focus on a Specific County
```python
REGION_CODE = "US-NY-061"  # Manhattan (New York County)
```

Find county codes at: https://ebird.org/region/world

## 📊 What Data is Collected

Each observation includes:
- **Species name** (common and scientific)
- **Location** (name, coordinates)
- **Date and time** of observation
- **Number of individuals**
- **Observer information**
- **Review status**

## 🔍 Viewing the Data

### Quick view in terminal
```bash
# View CSV with column command
column -t -s, ny_rare_birds_*.csv | less -S

# Or just open in Excel/Numbers/Google Sheets
open ny_rare_birds_*.csv
```

### View JSON
```bash
cat ny_rare_birds_*.json | python -m json.tool | less
```

## 🚨 Troubleshooting

### Cron job didn't run
1. Check logs: `cat logs/ny_alerts_$(date +%Y%m%d).log`
2. Verify cron: `crontab -l`
3. Test manually: `./run_ny_alerts_cron.sh`

### No data returned
- Check your API key in `config.json`
- Verify you have `requests` installed: `pip list | grep requests`
- Try increasing `DAYS_BACK` in `run_ny_alerts.py`

### Permission denied
```bash
chmod +x run_ny_alerts_cron.sh
chmod +x setup_daily_alert.sh
```

## 📧 API Key Security

Your API key is stored in `config.json` and is protected by `.gitignore`.

**Never commit or share your API key publicly!**

To regenerate a new API key:
1. Visit https://ebird.org/api/keygen
2. Update `config.json` with the new key

## 🔄 Update Schedule

To change from 8:00 AM to a different time:

```bash
crontab -e
```

Change the hour (first 0 = midnight through 23 = 11 PM):
- `0 6 * * *` = 6:00 AM
- `0 12 * * *` = Noon
- `0 18 * * *` = 6:00 PM
- `30 7 * * *` = 7:30 AM

## ✅ Verification

Test everything is working:
```bash
# 1. Run manually
./run_ny_alerts_cron.sh

# 2. Check log was created
ls -l logs/

# 3. Check output files were created
ls -lt ny_rare_birds_*.csv

# 4. View the log
cat logs/ny_alerts_$(date +%Y%m%d).log
```

## 🎉 You're All Set!

Your New York Rare Bird Alert will now run automatically every day at 8:00 AM. Check your logs and data files to see the results!

Happy birding! 🐦
