# 🦅 NYC Rare Bird Alert

A beautiful, interactive web application for tracking rare and notable bird sightings across New York City using the eBird API.

![NYC Bird Alert](https://img.shields.io/badge/Birds-NYC-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 🗺️ Interactive Map
- **Real-time bird tracking** on an interactive Leaflet map
- **Custom markers** showing exact locations of rare bird sightings
- **Marker clustering** for better visualization of dense areas
- **Click markers** for detailed popup information

### 📊 Data Visualization
- **Live statistics dashboard** with animated counters
- **Interactive bar charts** showing top species
- **Daily timeline** view of historical sightings
- **Search and filter** by species or location
- **Date range filtering** (Today, Yesterday, Week, Month, All Time)

### 🎨 Beautiful Design
- **Modern gradient UI** with glass-morphism effects
- **Smooth animations** and hover effects
- **Responsive design** for desktop and mobile
- **Professional typography** (Poppins font)
- **Custom scrollbars** and styling

### 🔄 Automated Data Collection
- **Daily cron job** automatically fetches new bird data at 8 AM
- **eBird API integration** for official, reliable data
- **Historical data loading** to track trends over time
- **Automatic CSV/JSON exports** for data analysis

### 🚀 Sharing Features
- **Share to social media** (Twitter, Facebook)
- **Email sharing** with automatic templates
- **Copy link** functionality
- **Export data** in multiple formats

## 📋 Prerequisites

- Python 3.x
- eBird API key (free from [eBird API](https://ebird.org/api/keygen))
- Modern web browser
- macOS, Linux, or Windows

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nyc-rare-bird-alert.git
cd nyc-rare-bird-alert
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `config.json` file:

```json
{
  "ebird_api_key": "your_api_key_here"
}
```

Get your free API key at: https://ebird.org/api/keygen

### 4. Fetch Bird Data

```bash
python run_ny_alerts.py
```

### 5. Start the Web Server

```bash
python start_bird_website.py
```

Or use the convenient launcher:

```bash
./launch_bird_map.sh
```

### 6. Open in Browser

Visit: **http://localhost:8000/bird_map_premium.html**

## 📁 Project Structure

```
nyc-rare-bird-alert/
├── bird_map_premium.html      # Main interactive website (Premium Edition)
├── bird_map.html              # Alternative website version
├── ebird_api_client.py        # eBird API client library
├── run_ny_alerts.py           # Main script to fetch bird data
├── start_bird_website.py      # Web server for hosting the site
├── launch_bird_map.sh         # Convenient launcher script
├── setup_daily_alert.sh       # Cron job setup script
├── run_ny_alerts_cron.sh      # Cron wrapper for automated runs
├── config.json               # API credentials (not in repo)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── README_API.md            # API documentation
├── README_SCRAPER.md        # Original scraper docs
├── CRON_SETUP_COMPLETE.md   # Cron job documentation
└── WEBSITE_README.md        # Website features documentation
```

## 🎯 Usage

### Manual Data Refresh

```bash
python run_ny_alerts.py
```

### Set Up Automated Daily Updates

```bash
./setup_daily_alert.sh
```

This sets up a cron job to automatically fetch new bird data every day at 8 AM.

### View Cron Jobs

```bash
crontab -l
```

### Stop the Web Server

```bash
kill $(lsof -ti:8000)
```

## 🗺️ Website Features

### Interactive Controls

- **Search Box** - Filter birds by species name or location
- **Date Range Filter** - View sightings from specific time periods
- **Refresh Button** - Reload the latest data
- **History Button** - Load all historical sightings
- **Share Button** - Share sightings on social media
- **Cluster/Heatmap** - Toggle map visualization modes

### Map Features

- **Zoom and Pan** - Explore different areas of NYC
- **Click Markers** - View detailed bird information
- **Click Bird Cards** - Zoom to specific sighting locations
- **Responsive** - Works on desktop and mobile devices

## 📊 Data Format

The application fetches data from eBird API and filters for NYC locations including:
- Manhattan
- Queens
- Brooklyn
- Bronx
- Staten Island
- Major parks (Central Park, Prospect Park, etc.)

Each sighting includes:
- Species name (common and scientific)
- Location with coordinates
- Date and time of observation
- Number of birds observed
- Observer information

## 🔧 Customization

### Change Region

Edit `run_ny_alerts.py` to change the region code:

```python
REGION_CODE = "US-NY"  # Change to your desired region
```

### Change Update Time

Edit the cron schedule:

```bash
crontab -e
# Change: 0 8 * * * to your preferred time
```

### Modify Map Center

Edit `bird_map_premium.html`:

```javascript
map = L.map('map').setView([40.7128, -74.0060], 11);
//                          [latitude, longitude], zoom
```

## 📈 API Rate Limits

The eBird API has reasonable rate limits:
- Be respectful and don't make excessive requests
- The automated script runs once daily
- Manual refreshes are fine for reasonable use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Cornell Lab of Ornithology** - For the eBird API and data
- **Leaflet.js** - For the interactive maps
- **Chart.js** - For data visualizations
- **OpenStreetMap** - For map tiles
- **Font Awesome** - For icons

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation files (README_API.md, WEBSITE_README.md)
- Visit [eBird API Documentation](https://documenter.getpostman.com/view/664302/S1ENwy59)

## 🐦 Happy Bird Watching!

Enjoy discovering the rare and beautiful birds of New York City! 🗽

---

**Note:** This application is for educational and personal use. Please respect eBird's Terms of Service and API usage guidelines.
