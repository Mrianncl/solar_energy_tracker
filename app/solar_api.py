import openmeteo_requests
import requests
from datetime import date

def get_solar_data(location, max_retries=3):
    """
    Fetches solar energy potential using Open-Meteo API.
    
    Args:
        location (str): City or location name
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        tuple: (dict, None) if successful, (None, str) if failed
    """
    retries = 0
    
    while retries < max_retries:
        try:
            # Step 1: Geocoding to get coordinates
            geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
            geo_response = requests.get(geocode_url, timeout=10).json()

            if not geo_response.get("results"):
                return None, "Location not found. Please try a different or more specific name."

            result = geo_response["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            location_name = f"{result.get('name', 'Unknown')}, {result.get('country', 'Unknown')}"

            # Step 2: Use Open-Meteo API to fetch solar data
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "shortwave_radiation_sum",
                "timezone": "auto",
                "start_date": str(date.today()),
                "end_date": str(date.today())
            }

            # Using regular requests instead of SDK for simplicity
            response = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()

            if "daily" not in response:
                return None, "Solar data not available for this location."

            wh_per_m2 = response["daily"]["shortwave_radiation_sum"][0]
            kwh_per_m2 = round(wh_per_m2 / 1000, 2)

            # Estimate recommended usage (75% efficiency)
            recommended_kwh = round(kwh_per_m2 * 0.75, 2)

            return {
                "location": location_name,
                "daily_solar_kwh": kwh_per_m2,
                "recommended_usage_kwh": recommended_kwh
            }, None

        except requests.exceptions.RequestException as e:
            retries += 1
            if retries < max_retries:
                continue
            else:
                return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    return None, "Failed to fetch solar data after multiple attempts."


