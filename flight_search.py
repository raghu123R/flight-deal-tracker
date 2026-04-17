import os
import requests
from dotenv import load_dotenv

load_dotenv()


class FlightSearch:
    """Handles flight search using SerpAPI (Google Flights engine)"""

    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        self.endpoint = os.getenv("SERP_ENDPOINT")

        if not self.api_key:
            raise ValueError("SERP_API_KEY not found in environment variables")

        if not self.endpoint:
            raise ValueError("SERP_ENDPOINT not found in environment variables")

    def check_flight(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """Search for flights between two cities"""

        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",   # round trip
            "adults": 1,
            "currency": "INR",
            "api_key": self.api_key,
        }

        # Add direct flight filter (optional)
        if is_direct:
            query["stops"] = "1"

        try:
            response = requests.get(self.endpoint, params=query, timeout=30)
            response.raise_for_status()

            data = response.json()

            # API-level error handling
            if "error" in data:
                print(f"API error: {data['error']}")
                return None

            return data

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None