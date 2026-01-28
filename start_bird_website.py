#!/usr/bin/env python3
"""
Start a simple web server for the Bird Map website
"""

import http.server
import socketserver
import json
import os
import glob
from urllib.parse import urlparse, parse_qs

PORT = 8000

class BirdMapHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve bird data"""

    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)

        # Special handler for getting latest bird data
        if parsed_path.path == '/get_latest_data.php':
            self.serve_latest_data()
        else:
            # Serve files normally
            super().do_GET()

    def serve_latest_data(self):
        """Serve the most recent bird data JSON file"""
        try:
            # Find all JSON files
            json_files = glob.glob('ny_rare_birds_*.json')

            if not json_files:
                self.send_error(404, "No bird data files found")
                return

            # Sort by modification time, most recent first
            json_files.sort(key=os.path.getmtime, reverse=True)
            latest_file = json_files[0]

            # Read and serve the file
            with open(latest_file, 'r') as f:
                data = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(data.encode())

            print(f"Served data from: {latest_file}")

        except Exception as e:
            self.send_error(500, f"Error serving data: {str(e)}")


def main():
    """Start the web server"""
    with socketserver.TCPServer(("", PORT), BirdMapHandler) as httpd:
        print("\n" + "="*70)
        print("🦅 NEW YORK RARE BIRD ALERT - WEB SERVER")
        print("="*70)
        print(f"\n✅ Server running at: http://localhost:{PORT}")
        print(f"\n📍 Open your browser and visit:")
        print(f"   http://localhost:{PORT}/bird_map.html")
        print(f"\n💡 The website will automatically load the latest bird data")
        print(f"\n🛑 Press Ctrl+C to stop the server")
        print("="*70 + "\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")
            return 0


if __name__ == "__main__":
    exit(main())
