import httpx
from typing import List, Dict, Any, Optional
from nicegui import app

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

    async def _post(self, endpoint: str, data: Dict[str, Any], use_token: bool = False) -> Optional[Dict[str, Any]]:
        try:
            headers = {}
            if use_token:
                token = app.storage.user.get('access_token')
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_BASE_URL}/{endpoint}/", json=data, headers=headers)
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    print(f"Post error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error posting to {API_BASE_URL}/{endpoint}: {e}")
        return None

    async def _put(self, endpoint: str, data: Dict[str, Any], use_token: bool = True) -> Optional[Dict[str, Any]]:
        try:
            headers = {}
            if use_token:
                token = app.storage.user.get('access_token')
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            async with httpx.AsyncClient() as client:
                response = await client.put(f"{API_BASE_URL}/{endpoint}/", json=data, headers=headers)
                if response.status_code in [200, 204]:
                    return response.json()
                else:
                    print(f"Put error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error putting to {API_BASE_URL}/{endpoint}: {e}")
        return None

    async def login(self, username: str, password: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/auth/login", 
                    data={"username": username, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    app.storage.user['access_token'] = data.get('access_token')
                    app.storage.user['is_authenticated'] = True
                    app.storage.user['role'] = data.get('role', 'user')
                    app.storage.user['user_name'] = data.get('name', 'User')
                    return True
        except Exception as e:
            print(f"Login error: {e}")
        return False

    async def register(self, name: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        return await self._post("auth/register", {"name": name, "email": email, "password": password})

    async def logout(self):
        app.storage.user.update({'access_token': None, 'is_authenticated': False, 'role': None, 'user_name': None})

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

    async def search_melodies(self, query: str) -> List[Dict[str, Any]]:
        if not query:
            return await self.get_melodies()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/melodies/search/", params={"search": query})
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error searching melodies: {e}")
        return []

    async def create_melody(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._post("melodies", data, use_token=True)

    async def update_melody(self, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._put(f"melodies/{id}", data)

    async def create_artist(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._post("artists", data, use_token=True)

    async def update_artist(self, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._put(f"artists/{id}", data)

    async def get_melody(self, melody_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/melodies/{melody_id}")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching melody {melody_id}: {e}")
        return None

    async def get_artist(self, artist_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/artists/{artist_id}")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching artist {artist_id}: {e}")
        return None

    async def get_article(self, article_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/articles/{article_id}")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching article {article_id}: {e}")
        return None

    async def get_event(self, event_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/events/{event_id}")
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching event {event_id}: {e}")
    async def get_comments(self, melody_id: Optional[int] = None, article_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params = {}
        if melody_id: params['melody_id'] = melody_id
        if article_id: params['article_id'] = article_id
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/comments/", params=params)
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching comments: {e}")
        return []

    async def create_comment(self, content: str, melody_id: Optional[int] = None, article_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {"content": content}
        if melody_id: data['melody_id'] = melody_id
        if article_id: data['article_id'] = article_id
        return await self._post("comments", data, use_token=True)

api_client = APIClient()
