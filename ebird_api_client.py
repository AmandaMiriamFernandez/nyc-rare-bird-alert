#!/usr/bin/env python3
"""
eBird API Client
Fetches recent bird observations and notable sightings using the official eBird API 2.0
"""

import requests
import csv
import json
from datetime import datetime
import os


class EBirdAPIClient:
    """Client for interacting with eBird API 2.0"""

    BASE_URL = "https://api.ebird.org/v2"

    def __init__(self, api_key):
        """
        Initialize the eBird API client

        Args:
            api_key: Your eBird API key (get from https://ebird.org/api/keygen)
        """
        self.api_key = api_key
        self.headers = {
            'X-eBirdApiToken': api_key
        }

    def get_recent_observations(self, region_code, days_back=14, notable_only=False, max_results=100):
        """
        Get recent bird observations for a region

        Args:
            region_code: Region code (e.g., 'US-CA' for California, 'US-CA-037' for Los Angeles County)
            days_back: Number of days back to search (1-30, default: 14)
            notable_only: Only return notable/rare observations (default: False)
            max_results: Maximum number of results to return (default: 100)

        Returns:
            list: List of observation dictionaries
        """
        endpoint = f"{self.BASE_URL}/data/obs/{region_code}/recent"
        if notable_only:
            endpoint = f"{self.BASE_URL}/data/obs/{region_code}/recent/notable"

        params = {
            'back': days_back,
            'maxResults': max_results
        }

        print(f"Fetching {'notable' if notable_only else 'recent'} observations for region {region_code}...")

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            observations = response.json()
            print(f"Found {len(observations)} observations")
            return observations

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"Error: Region code '{region_code}' not found")
            else:
                print(f"HTTP Error: {e}")
            return []
        except Exception as e:
            print(f"Error fetching observations: {e}")
            return []

    def get_recent_observations_hotspot(self, location_id, days_back=14, max_results=100):
        """
        Get recent observations from a specific hotspot

        Args:
            location_id: Hotspot location ID (e.g., 'L99381' - the ID from the alert URL)
            days_back: Number of days back to search (1-30, default: 14)
            max_results: Maximum number of results to return (default: 100)

        Returns:
            list: List of observation dictionaries
        """
        endpoint = f"{self.BASE_URL}/data/obs/{location_id}/recent"

        params = {
            'back': days_back,
            'maxResults': max_results
        }

        print(f"Fetching recent observations for hotspot {location_id}...")

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            observations = response.json()
            print(f"Found {len(observations)} observations")
            return observations

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"Error: Location ID '{location_id}' not found")
            else:
                print(f"HTTP Error: {e}")
            return []
        except Exception as e:
            print(f"Error fetching observations: {e}")
            return []

    def get_notable_observations(self, region_code, days_back=14, max_results=100):
        """
        Get notable (rare/unusual) bird observations for a region

        Args:
            region_code: Region code (e.g., 'US-CA' for California)
            days_back: Number of days back to search (1-30, default: 14)
            max_results: Maximum number of results to return (default: 100)

        Returns:
            list: List of notable observation dictionaries
        """
        return self.get_recent_observations(region_code, days_back, notable_only=True, max_results=max_results)

    def get_species_observations(self, region_code, species_code, days_back=14, max_results=100):
        """
        Get recent observations of a specific species in a region

        Args:
            region_code: Region code (e.g., 'US-CA')
            species_code: Species code (e.g., 'bkcchi' for Black-capped Chickadee)
            days_back: Number of days back to search (1-30)
            max_results: Maximum number of results

        Returns:
            list: List of observation dictionaries
        """
        endpoint = f"{self.BASE_URL}/data/obs/{region_code}/recent/{species_code}"

        params = {
            'back': days_back,
            'maxResults': max_results
        }

        print(f"Fetching observations of species {species_code} in region {region_code}...")

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            observations = response.json()
            print(f"Found {len(observations)} observations")
            return observations

        except Exception as e:
            print(f"Error fetching species observations: {e}")
            return []

    def get_nearby_observations(self, latitude, longitude, distance_km=25, days_back=14, max_results=100):
        """
        Get recent observations near a specific location

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            distance_km: Search radius in kilometers (default: 25)
            days_back: Number of days back to search (1-30)
            max_results: Maximum number of results

        Returns:
            list: List of observation dictionaries
        """
        endpoint = f"{self.BASE_URL}/data/obs/geo/recent"

        params = {
            'lat': latitude,
            'lng': longitude,
            'dist': distance_km,
            'back': days_back,
            'maxResults': max_results
        }

        print(f"Fetching observations near ({latitude}, {longitude})...")

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            observations = response.json()
            print(f"Found {len(observations)} observations")
            return observations

        except Exception as e:
            print(f"Error fetching nearby observations: {e}")
            return []

    def format_observation(self, obs):
        """
        Format an observation dictionary into a more readable structure

        Args:
            obs: Raw observation dictionary from API

        Returns:
            dict: Formatted observation data
        """
        return {
            'species_code': obs.get('speciesCode', ''),
            'common_name': obs.get('comName', ''),
            'scientific_name': obs.get('sciName', ''),
            'location_id': obs.get('locId', ''),
            'location_name': obs.get('locName', ''),
            'observation_date': obs.get('obsDt', ''),
            'how_many': obs.get('howMany', ''),
            'latitude': obs.get('lat', ''),
            'longitude': obs.get('lng', ''),
            'location_private': obs.get('locationPrivate', False),
            'observation_reviewed': obs.get('obsReviewed', False),
            'observation_valid': obs.get('obsValid', True),
            'observer_id': obs.get('userDisplayName', ''),
            'subspecies_common_name': obs.get('subId', ''),
            'has_media': obs.get('hasComments', False) or obs.get('hasRichMedia', False)
        }

    def save_to_csv(self, observations, filename=None):
        """
        Save observations to CSV file

        Args:
            observations: List of observation dictionaries
            filename: Output filename (default: ebird_observations_TIMESTAMP.csv)
        """
        if not observations:
            print("No observations to save")
            return

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ebird_observations_{timestamp}.csv"

        # Format all observations
        formatted_obs = [self.format_observation(obs) for obs in observations]

        # Get all fieldnames
        fieldnames = sorted(set().union(*[obs.keys() for obs in formatted_obs]))

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(formatted_obs)

        print(f"Data saved to {filename}")

    def save_to_json(self, observations, filename=None):
        """
        Save observations to JSON file

        Args:
            observations: List of observation dictionaries
            filename: Output filename (default: ebird_observations_TIMESTAMP.json)
        """
        if not observations:
            print("No observations to save")
            return

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ebird_observations_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(observations, f, indent=2)

        print(f"Data saved to {filename}")


def main():
    """Main function to run the API client"""

    # Try to load API key from config.json
    api_key = None

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            api_key = config.get('ebird_api_key')
            if api_key:
                print("Loaded API key from config.json")
    except FileNotFoundError:
        print("config.json not found, checking environment variables...")
    except Exception as e:
        print(f"Error loading config.json: {e}")

    # Fallback to environment variable
    if not api_key:
        api_key = os.getenv('EBIRD_API_KEY')

    # Prompt user if still no API key
    if not api_key:
        print("\nNo API key found!")
        print("Get your free API key at: https://ebird.org/api/keygen")
        print("\nYou can provide it by:")
        print("1. Adding 'ebird_api_key' to config.json")
        print("2. Setting EBIRD_API_KEY environment variable")
        return 1

    # Create API client
    client = EBirdAPIClient(api_key)

    # Example: Get recent notable observations for a region
    # You can change this to match your needs

    print("\n" + "="*60)
    print("New York Rare Bird Alert - eBird API Client")
    print("Alert ID: SN35466 (New York State)")
    print("="*60 + "\n")

    # SN35466 = New York Rare Bird Alert
    # Using US-NY (New York State) region code
    region_code = "US-NY"

    print(f"Fetching notable/rare bird observations for New York State...")
    print(f"Region code: {region_code}")
    print()

    observations = client.get_notable_observations(region_code, days_back=7, max_results=100)

    if observations:
        # Save to CSV with New York specific filename
        csv_filename = f"ny_rare_birds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        client.save_to_csv(observations, csv_filename)

        # Also save to JSON for full data
        json_filename = f"ny_rare_birds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        client.save_to_json(observations, json_filename)

        # Print detailed summary
        print(f"\n" + "="*60)
        print(f"NEW YORK RARE BIRD ALERT SUMMARY")
        print("="*60)
        print(f"Total rare bird observations: {len(observations)}")
        species = set(obs.get('comName') for obs in observations)
        print(f"Unique rare species reported: {len(species)}")

        # Group by county
        counties = {}
        for obs in observations:
            loc = obs.get('locName', '')
            if 'US-NY' in loc or 'New York' in loc:
                # Try to extract county from location
                counties[loc] = counties.get(loc, 0) + 1

        print(f"\nMost recent rare bird sightings in NY:")
        for i, obs in enumerate(observations[:10], 1):
            species_name = obs.get('comName', 'Unknown')
            location = obs.get('locName', 'Unknown location')
            date = obs.get('obsDt', 'Unknown date')
            count = obs.get('howMany', '?')
            print(f"{i}. {species_name} ({count} bird{'s' if count != 1 else ''})")
            print(f"   Location: {location}")
            print(f"   Date/Time: {date}")
            print()

        print(f"Full data saved to:")
        print(f"  - {csv_filename}")
        print(f"  - {json_filename}")
    else:
        print("\nNo rare bird observations found for New York in the past 7 days.")

    return 0


if __name__ == "__main__":
    exit(main())
