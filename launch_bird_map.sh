#!/bin/bash
# Launch the New York Rare Bird Alert Website

echo ""
echo "======================================================================"
echo "  🦅 NEW YORK RARE BIRD ALERT - Interactive Map 🗺️"
echo "======================================================================"
echo ""

# Check if data files exist
JSON_FILES=$(ls ny_rare_birds_*.json 2>/dev/null | wc -l)
if [ "$JSON_FILES" -eq 0 ]; then
    echo "⚠️  No bird data found!"
    echo ""
    echo "Running the bird alert script to fetch fresh data..."
    echo ""
    python run_ny_alerts.py
    echo ""
fi

# Check if server is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ Web server is already running!"
else
    echo "🚀 Starting web server..."
    python start_bird_website.py &
    SERVER_PID=$!
    sleep 2
    echo "✅ Server started (PID: $SERVER_PID)"
fi

echo ""
echo "======================================================================"
echo "  📍 Your bird map website is ready!"
echo "======================================================================"
echo ""
echo "  🌐 Open in your browser:"
echo "     http://localhost:8000/bird_map.html"
echo ""
echo "  Features:"
echo "    • 🗺️  Interactive map of all rare bird sightings"
echo "    • 🔍 Search and filter by species or location"
echo "    • 📍 Click markers for detailed information"
echo "    • 📊 Real-time statistics display"
echo "    • 🎨 Beautiful gradient design with bird graphics"
echo ""
echo "  💡 Tip: The website auto-loads the latest data file"
echo ""
echo "  🛑 To stop the server, run:"
echo "     kill \$(lsof -ti:8000)"
echo ""
echo "======================================================================"
echo ""

# Try to open in default browser (macOS)
if command -v open &> /dev/null; then
    echo "🌐 Opening in your default browser..."
    sleep 1
    open "http://localhost:8000/bird_map.html"
fi
