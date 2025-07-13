import os
import requests
from typing import Optional, Dict, Any

class SerpApiFlightsService:
    """
    Service for querying Google Flights data from SerpApi.
    """
    BASE_URL = "https://serpapi.com/search"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("SerpApi API key must be provided via argument or SERPAPI_KEY env variable.")

    def search_flights(self,
                       departure_id: str,
                       arrival_id: str,
                       departure_date: str,
                       gl: Optional[str] = None,
                       hl: Optional[str] = None,
                       currency: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
        """
        Query SerpApi for flight results.
        Args:
            departure_id: 3-letter airport code or kgmid for departure.
            arrival_id: 3-letter airport code or kgmid for arrival.
            departure_date: Date of departure in YYYY-MM-DD format.
            gl: Country code (optional).
            hl: Language code (optional).
            currency: Currency code (optional).
            **kwargs: Any additional SerpApi parameters.
        Returns:
            JSON response from SerpApi as dict.
        Raises:
            requests.HTTPError: For HTTP errors.
            ValueError: For missing API key.
        """
        params = {
            "engine": "google_flights",
            "api_key": self.api_key,
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": departure_date,
            "output": "json"
        }
        if "return_date" in kwargs and kwargs["return_date"]:
            params["return_date"] = kwargs["return_date"]
        if "type" in kwargs and kwargs["type"]:
            params["type"] = kwargs["type"]
        if gl:
            params["gl"] = gl
        if hl:
            params["hl"] = hl
        if currency:
            params["currency"] = currency
        params.update(kwargs)

        response = requests.get(self.BASE_URL, params=params, timeout=30)
        if not response.ok:
            try:
                logger.error(f"SerpApi error response: {response.json()}")
            except Exception:
                logger.error(f"SerpApi error response (non-JSON): {response.text}")
            response.raise_for_status()
        return response.json()
