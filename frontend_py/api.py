import httpx
from typing import List, Dict, Any, Optional

API_BASE_URL = "http://127.0.0.1:8000/api"

class APIClient:
    async def _get(self, endpoint: str) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                # Ensure endpoint has trailing slash for FastAPI
                path = endpoint if endpoint.endswith('/') else f"{endpoint}/"
                response = await client.get(f"{API_BASE_URL}/{path}")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching from {API_BASE_URL}/{endpoint}: {e}")
        return []

    async def get_melodies(self) -> List[Dict[str, Any]]:
        return await self._get("melodies")

    async def get_artists(self) -> List[Dict[str, Any]]:
        return await self._get("artists")

    async def get_locations(self) -> List[Dict[str, Any]]:
        return await self._get("locations")

    async def get_articles(self) -> List[Dict[str, Any]]:
        return await self._get("articles")

    async def get_events(self) -> List[Dict[str, Any]]:
        return await self._get("events")

    async def get_melody(self, melody_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/melodies/{melody_id}")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching melody {melody_id}: {e}")
        return None

api_client = APIClient()
