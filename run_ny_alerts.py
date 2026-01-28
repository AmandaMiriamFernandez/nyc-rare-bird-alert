#!/usr/bin/env python3
"""
New York Rare Bird Alert - Customizable Runner
Quick script to fetch NY rare bird alerts with custom settings
"""

from ebird_api_client import EBirdAPIClient
from datetime import datetime
import json
import os


def main():
    # ===== CUSTOMIZE THESE SETTINGS =====

    # Days to look back (1-30)
    DAYS_BACK = 7

    # Maximum number of results to fetch
    MAX_RESULTS = 100

    # Region code (US-NY = New York State)
    # You can also use county codes like 'US-NY-061' for Manhattan
    REGION_CODE = "US-NY"

    # Filter by specific counties (optional, leave empty for all NY)
    # Example: ['Manhattan', 'Queens', 'Brooklyn', 'Bronx', 'Staten Island']
    COUNTY_FILTER = []

    # ===== END CUSTOMIZATION =====

    # Load API key
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            api_key = config.get('ebird_api_key')
    except:
        api_key = os.getenv('EBIRD_API_KEY')

    if not api_key:
        print("Error: No API key found in config.json")
        return 1

    # Create client
    client = EBirdAPIClient(api_key)

    print("\n" + "="*70)
    print(f"  NEW YORK RARE BIRD ALERT (SN35466)")
    print("="*70)
    print(f"Region: {REGION_CODE}")
    print(f"Looking back: {DAYS_BACK} days")
    print(f"Max results: {MAX_RESULTS}")
    if COUNTY_FILTER:
        print(f"Filtering by: {', '.join(COUNTY_FILTER)}")
    print("="*70 + "\n")

    # Fetch observations
    observations = client.get_notable_observations(
        REGION_CODE,
        days_back=DAYS_BACK,
        max_results=MAX_RESULTS
    )

    if not observations:
        print("No rare birds found in the specified timeframe.")
        return 0

    # Filter by county if specified
    if COUNTY_FILTER:
        filtered_obs = []
        for obs in observations:
            location = obs.get('locName', '')
            if any(county.lower() in location.lower() for county in COUNTY_FILTER):
                filtered_obs.append(obs)
        observations = filtered_obs
        print(f"Filtered to {len(observations)} observations in specified counties.\n")

    # Generate filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"ny_rare_birds_{timestamp}.csv"
    json_file = f"ny_rare_birds_{timestamp}.json"

    # Save data
    client.save_to_csv(observations, csv_file)
    client.save_to_json(observations, json_file)

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total rare bird observations: {len(observations)}")

    # Count unique species
    species_counts = {}
    for obs in observations:
        species = obs.get('comName', 'Unknown')
        species_counts[species] = species_counts.get(species, 0) + 1

    print(f"Unique species: {len(species_counts)}")

    # Show top species
    print("\nMost frequently reported rare species:")
    sorted_species = sorted(species_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (species, count) in enumerate(sorted_species[:10], 1):
        print(f"  {i}. {species} - {count} observation(s)")

    # Show recent sightings
    print("\n" + "="*70)
    print("RECENT SIGHTINGS (Last 10)")
    print("="*70 + "\n")

    for i, obs in enumerate(observations[:10], 1):
        species = obs.get('comName', 'Unknown')
        location = obs.get('locName', 'Unknown')
        date = obs.get('obsDt', 'Unknown')
        count = obs.get('howMany', '?')

        print(f"{i}. {species} ({count} individual{'s' if count != 1 else ''})")
        print(f"   📍 {location}")
        print(f"   🕒 {date}")
        print()

    print("="*70)
    print(f"✅ Data saved to:")
    print(f"   📄 {csv_file}")
    print(f"   📄 {json_file}")
    print("="*70 + "\n")

    return 0


if __name__ == "__main__":
    exit(main())
