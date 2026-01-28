# eBird API Client

A Python client for fetching bird observation data using the official eBird API 2.0.

## Why Use the API Instead of Scraping?

- **Official & Legal**: Supported by Cornell Lab of Ornithology
- **No Authentication Issues**: Simple API key (no login credentials needed)
- **More Reliable**: Structured JSON data, no HTML parsing
- **Better Performance**: Faster and more efficient
- **No Account Required**: Just need a free API key

## Quick Start

### 1. Get Your Free API Key

Visit https://ebird.org/api/keygen and request a free API key. You'll receive it instantly.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Edit `config.json` and add your API key:

```json
{
  "ebird_api_key": "your_actual_api_key_here"
}
```

Or set as environment variable:

```bash
export EBIRD_API_KEY="your_actual_api_key_here"
```

### 4. Run the Client

```bash
python ebird_api_client.py
```

## Features

The client supports multiple types of queries:

### Get Recent Observations by Region

```python
from ebird_api_client import EBirdAPIClient

client = EBirdAPIClient("your_api_key")

# Get recent observations for California
observations = client.get_recent_observations("US-CA", days_back=14)
```

### Get Notable/Rare Sightings

```python
# Get notable observations (rare birds)
notable = client.get_notable_observations("US-CA", days_back=7)
```

### Get Observations from a Specific Hotspot

```python
# Get observations from a specific location
# The location ID can be found in eBird URLs (e.g., L99381)
observations = client.get_recent_observations_hotspot("L99381", days_back=7)
```

### Get Observations of a Specific Species

```python
# Get recent sightings of Black-capped Chickadee
observations = client.get_species_observations("US-CA", "bkcchi", days_back=14)
```

### Get Nearby Observations

```python
# Get observations within 25km of coordinates
observations = client.get_nearby_observations(
    latitude=37.7749,
    longitude=-122.4194,
    distance_km=25,
    days_back=7
)
```

## Understanding Region Codes

Region codes follow a hierarchical format:

- **Country**: `US`, `CA`, `MX`
- **State/Province**: `US-CA` (California), `US-NY` (New York)
- **County**: `US-CA-037` (Los Angeles County)
- **Hotspot**: `L99381` (specific location ID)

Find region codes at: https://ebird.org/region/world

## Finding Your Location from the Alert URL

Your original URL was: `https://ebird.org/alert/summary?sid=SN35466`

The `sid=SN35466` parameter is a location identifier. To use it with the API:

1. Visit the eBird page for that location
2. Look for the location ID in the URL (usually starts with 'L')
3. Or use the region code visible on the page

You can also use the API's nearby observations feature if you have coordinates.

## Output Formats

The client can save data in two formats:

### CSV Format
```python
client.save_to_csv(observations, "my_birds.csv")
```

Contains columns:
- species_code
- common_name
- scientific_name
- location_name
- observation_date
- how_many (count)
- latitude/longitude
- observer_id
- And more...

### JSON Format
```python
client.save_to_json(observations, "my_birds.json")
```

Full raw data from the API for advanced processing.

## API Rate Limits

The eBird API has reasonable rate limits:
- Don't make excessive requests
- Cache results when possible
- Be respectful of the service

## Example Use Cases

### Monitor Rare Birds in Your Area

```python
client = EBirdAPIClient(api_key)
notable = client.get_notable_observations("US-CA-037", days_back=1)
client.save_to_csv(notable, "rare_birds_today.csv")
```

### Track a Specific Species

```python
# Monitor Anna's Hummingbird sightings
observations = client.get_species_observations("US-CA", "annhum", days_back=7)
```

### Create a Local Bird Alert System

```python
# Check for new sightings near you
observations = client.get_nearby_observations(
    latitude=your_lat,
    longitude=your_lon,
    distance_km=10,
    days_back=1
)
```

## Troubleshooting

### "No API key found" Error

Make sure you've:
1. Generated an API key at https://ebird.org/api/keygen
2. Added it to `config.json` or set `EBIRD_API_KEY` environment variable

### "Region code not found" Error

- Check the region code format
- Use region browser: https://ebird.org/region/world
- Country codes are two letters: `US`, `CA`
- State codes add hyphen and state: `US-CA`

### No Results Returned

- Try increasing `days_back` parameter
- Try a larger region (state instead of county)
- Use `get_nearby_observations()` with a larger radius

## Resources

- eBird API Documentation: https://documenter.getpostman.com/view/664302/S1ENwy59
- Get API Key: https://ebird.org/api/keygen
- Region Codes: https://ebird.org/region/world
- Species Codes: https://ebird.org/science/use-ebird-data/the-ebird-taxonomy

## Advantages Over Web Scraping

✅ No browser automation needed
✅ No dealing with login/authentication
✅ Structured, reliable data
✅ Officially supported by Cornell Lab
✅ Much faster
✅ Won't break when website changes
✅ Free and legal to use
