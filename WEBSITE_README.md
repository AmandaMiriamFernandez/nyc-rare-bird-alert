# 🦅 New York Rare Bird Alert - Interactive Website

Beautiful interactive website with real-time bird tracking map!

## ✨ Features

### 🗺️ Interactive Map
- **Leaflet-powered map** centered on New York State
- **Red markers** showing exact locations of rare bird sightings
- **Click markers** for detailed popup information
- **Zoom and pan** to explore different areas
- **Responsive design** works on desktop and mobile

### 📊 Live Statistics
- **Total sightings** counter
- **Unique species** count
- **Last updated** timestamp
- Real-time updates when you refresh

### 🔍 Search & Filter
- **Search box** to filter by species name or location
- **Instant filtering** as you type
- **Click bird cards** to zoom to location on map

### 🎨 Beautiful Design
- **Gradient purple background** (modern aesthetic)
- **Flying bird animations** in header
- **Smooth hover effects** on bird cards
- **Custom scrollbars** and styling
- **Professional color scheme**

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
```bash
./launch_bird_map.sh
```

This will:
1. Check for bird data (fetch if needed)
2. Start the web server
3. Open your browser automatically

### Option 2: Manual Start
```bash
# 1. Make sure you have bird data
python run_ny_alerts.py

# 2. Start the web server
python start_bird_website.py

# 3. Open your browser to:
#    http://localhost:8000/bird_map.html
```

## 📂 Files

- **bird_map.html** - Main website (interactive map + UI)
- **start_bird_website.py** - Python web server
- **launch_bird_map.sh** - Easy launcher script
- **get_latest_data.php** - Data endpoint (PHP fallback)

## 🌐 How It Works

1. The Python script serves the HTML file and bird data
2. The website loads the most recent `ny_rare_birds_*.json` file
3. Bird locations are plotted on an interactive Leaflet map
4. You can search, filter, and explore the sightings

## 🎯 Map Features Explained

### Navigation
- **Scroll to zoom** in/out
- **Click and drag** to pan around
- **Click red markers** to see bird details
- **Click bird cards** in sidebar to jump to location

### Popup Information
Each marker shows:
- Species name (common + scientific)
- Exact location
- Number of birds observed
- Date and time of sighting
- GPS coordinates

### Search Function
Type in the search box to filter by:
- Species name (e.g., "Harlequin Duck")
- Location (e.g., "Inwood Hill Park")
- Partial matches work too!

## 🔧 Customization

### Change Map Center
Edit `bird_map.html` line ~394:
```javascript
map = L.map('map').setView([43.0, -75.5], 7);
//                          [lat,   lng  ], zoom
```

### Change Color Scheme
Edit the CSS in `bird_map.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change these hex colors to your preference */
```

### Change Port
Edit `start_bird_website.py` line ~11:
```python
PORT = 8000  # Change to any available port
```

## 📱 Mobile Responsive

The website automatically adapts to smaller screens:
- Stacked layout on mobile
- Touch-friendly controls
- Readable text sizes
- Optimized for phones and tablets

## 🛑 Stop the Server

```bash
# Find and kill the server process
kill $(lsof -ti:8000)

# Or press Ctrl+C in the terminal where it's running
```

## 🔄 Refresh Data

The website has a "Refresh Data" button, or you can:

1. Run the Python script again to get new data:
   ```bash
   python run_ny_alerts.py
   ```

2. Click the refresh button on the website

3. Reload the page in your browser (F5 or Cmd+R)

## 🎨 Design Details

### Color Palette
- **Primary Purple**: #667eea
- **Secondary Purple**: #764ba2
- **Dark Text**: #2c3e50
- **Light Text**: #7f8c8d
- **Accent Red**: #e74c3c (markers)

### Typography
- **Font**: Segoe UI (fallback to system fonts)
- **Responsive sizing** for headers and text
- **Bold emphasis** on important information

### Animations
- **Flying birds** in header (subtle bounce)
- **Hover effects** on bird cards (slide and shadow)
- **Smooth transitions** throughout

## 🐛 Troubleshooting

### "Unable to load bird data"
- Make sure you've run `python run_ny_alerts.py` first
- Check that JSON files exist: `ls ny_rare_birds_*.json`
- Verify the server is running: `lsof -ti:8000`

### Port Already in Use
```bash
# Check what's using port 8000
lsof -ti:8000

# Kill the process
kill $(lsof -ti:8000)

# Or change the port in start_bird_website.py
```

### Map Not Loading
- Check browser console (F12) for errors
- Verify internet connection (needs Leaflet CDN)
- Try a different browser

### No Markers on Map
- Check that bird data has lat/lng coordinates
- Look at the JSON file to verify data format
- Check browser console for JavaScript errors

## 🌟 Advanced Features

### Auto-Update Setup

To automatically update the website data, combine with the cron job:

The daily cron job (8 AM) will fetch new data, and the website will automatically load the latest file when you refresh!

### Custom Data Source

To use different bird data:
1. Ensure JSON format matches eBird API structure
2. Name files: `ny_rare_birds_YYYYMMDD_HHMMSS.json`
3. Place in the same directory
4. Refresh the website

### Embed in Another Site

The map can be embedded using an iframe:
```html
<iframe src="http://localhost:8000/bird_map.html"
        width="100%"
        height="800px"
        frameborder="0">
</iframe>
```

## 📊 Data Format

The website expects JSON with this structure:
```json
[
  {
    "comName": "Harlequin Duck",
    "sciName": "Histrionicus histrionicus",
    "locName": "Ontario Beach",
    "obsDt": "2026-01-27 15:50",
    "howMany": 1,
    "lat": 43.2625,
    "lng": -77.6088
  }
]
```

## 🎁 Bonus Features

- **Custom scrollbars** (purple theme)
- **Gradient stat boxes** with live counters
- **Legend** in map corner
- **Responsive grid layout**
- **Shadow effects** for depth
- **Professional styling** throughout

## 📝 Browser Compatibility

Tested and working on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🔗 Technologies Used

- **HTML5** - Structure
- **CSS3** - Styling (Grid, Flexbox, Animations)
- **JavaScript (ES6+)** - Interactivity
- **Leaflet.js** - Interactive maps
- **OpenStreetMap** - Map tiles
- **Python HTTP Server** - Backend

## 💡 Tips

1. **Bookmark** `http://localhost:8000/bird_map.html` for quick access
2. **Keep the server running** in a terminal for continuous access
3. **Set up the cron job** for automatic daily data updates
4. **Share on local network** by using your computer's IP instead of localhost
5. **Take screenshots** of interesting sightings to share with fellow birders!

## 🦜 Happy Bird Watching!

Enjoy exploring the rare birds of New York State! 🗽🐦
