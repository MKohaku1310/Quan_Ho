import httpx
from typing import List, Dict, Any, Optional, Union
from nicegui import app, ui
import os

# Use environment variable for API URL, default to localhost
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")
if API_BASE_URL.endswith('/'):
    API_BASE_URL = API_BASE_URL[:-1]

class APIClient:
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, use_token: bool = False) -> Any:
        try:
            headers = {}
            if use_token:
                token = app.storage.user.get('access_token')
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                # Some FastAPI routes handle slashes strictly, some don't.
                # Standardizing to NO forced trailing slash here, as httpx handles it better.
                url = f"{API_BASE_URL}/{endpoint}"
                response = await client.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"GET error {response.status_code} for {url}: {response.text}")
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}. Ensure backend is running.")
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

            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"{API_BASE_URL}/{endpoint}"
                response = await client.post(url, json=data, headers=headers)
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    print(f"Post error {response.status_code}: {response.text}")
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
        except Exception as e:
            print(f"Error posting to {API_BASE_URL}/{endpoint}: {e}")
        return None

    async def _patch(self, endpoint: str, data: Dict[str, Any], use_token: bool = True) -> Optional[Dict[str, Any]]:
        try:
            headers = {}
            if use_token:
                token = app.storage.user.get('access_token')
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"{API_BASE_URL}/{endpoint}"
                response = await client.patch(url, json=data, headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Patch error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error patching to {API_BASE_URL}/{endpoint}: {e}")
        return None

    async def _put(self, endpoint: str, data: Dict[str, Any], use_token: bool = True) -> Optional[Dict[str, Any]]:
        try:
            headers = {}
            if use_token:
                token = app.storage.user.get('access_token')
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"{API_BASE_URL}/{endpoint}"
                response = await client.put(url, json=data, headers=headers)
                if response.status_code in [200, 204]:
                    return response.json()
                else:
                    print(f"Put error {response.status_code}: {response.text}")
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
        except Exception as e:
            print(f"Error putting to {API_BASE_URL}/{endpoint}: {e}")
        return None

    async def _delete(self, endpoint: str, use_token: bool = True) -> Optional[Dict[str, Any]]:
        try:
            headers = {}
            if use_token:
                token = app.storage.user.get('access_token')
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"{API_BASE_URL}/{endpoint}"
                response = await client.delete(url, headers=headers)
                if response.status_code in [200, 204]:
                    return {"message": "Deleted successfully"}
                else:
                    print(f"Delete error {response.status_code}: {response.text}")
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
        except Exception as e:
            print(f"Error deleting to {API_BASE_URL}/{endpoint}: {e}")
        return None

    async def login(self, username: str, password: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.post(
                    f"{API_BASE_URL}/auth/login", 
                    data={"username": username, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    app.storage.user.update(data)
                    app.storage.user['access_token'] = data.get('access_token')
                    app.storage.user['is_authenticated'] = True
                    app.storage.user['role'] = data.get('role', 'user')
                    app.storage.user['user_name'] = data.get('name', 'User')
                    app.storage.user['email'] = data.get('email', '')
                    app.storage.user['user_id'] = data.get('id')
                    return True
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
        except Exception as e:
            print(f"Login error: {e}")
        return False

    async def register(self, name: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        return await self._post("auth/register", {"name": name, "email": email, "password": password})

    async def logout(self):
        app.storage.user.clear()
        app.storage.user.update({'access_token': None, 'is_authenticated': False, 'role': None, 'user_name': None})
        ui.navigate.to('/')

    async def get_me(self) -> Optional[Dict[str, Any]]:
        return await self._get("auth/me", use_token=True)

    async def update_profile(self, data: Dict[str, Any]) -> bool:
        res = await self._patch("auth/me", data, use_token=True)
        if res:
            app.storage.user['user_name'] = res.get('name', app.storage.user.get('user_name'))
            return True
        return False

    async def change_password(self, old_p: str, new_p: str) -> bool:
        res = await self._post("auth/me/change-password", {"old_password": old_p, "new_password": new_p}, use_token=True)
        return res is not None

    async def get_activities(self) -> List[Dict[str, Any]]:
        return await self._get("auth/me/activities")

    # Administrative APIs
    async def get_users(self) -> List[Dict[str, Any]]:
        return await self._get("auth/users", use_token=True)

    async def delete_user(self, user_id: int) -> bool:
        res = await self._delete(f"auth/users/{user_id}", use_token=True)
        return res is not None

    async def ask_chatbot(self, message: str) -> Optional[str]:
        res = await self._post("chatbot", {"message": message})
        return res.get('response') if res else None



    async def get_melodies(self) -> List[Dict[str, Any]]:
        return await self._get("melodies")

    async def get_artists(self) -> List[Dict[str, Any]]:
        return await self._get("artists")

    async def get_locations(self) -> List[Dict[str, Any]]:
        return await self._get("locations")

    async def get_villages(self, district: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if district and district != 'Tất cả':
            params['district'] = district
        return await self._get("locations", params=params)

    async def get_village(self, village_id: int) -> Optional[Dict[str, Any]]:
        # Ensure we always treat village_id as an integer and fetch directly
        return await self._get(f"locations/{int(village_id)}", use_token=False)

    async def get_articles(self, article_type: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {"category": article_type} if article_type else {}
        return await self._get("articles", params=params)

    async def get_events(self) -> List[Dict[str, Any]]:
        return await self._get("events")

    async def register_event(self, event_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # The endpoint argument for _post will have unexpected / injected if we append query params directly 
        # so we rely on _post ensuring the URL looks like /events/{event_id}/register
        return await self._post(f"events/{event_id}/register", data, use_token=True)

    async def search_melodies(self, query: str) -> List[Dict[str, Any]]:
        if not query:
            return await self.get_melodies()
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(f"{API_BASE_URL}/melodies/search/", params={"search": query})
                if response.status_code == 200:
                    return response.json()
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
        except Exception as e:
            print(f"Error searching melodies: {e}")
        return []


    async def create_melody(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._post("melodies", data, use_token=True)

    async def update_melody(self, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._put(f"melodies/{id}", data, use_token=True)

    async def delete_melody(self, id: int) -> bool:
        res = await self._delete(f"melodies/{id}", use_token=True)
        return res is not None

    async def create_artist(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._post("artists", data, use_token=True)

    async def update_artist(self, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._put(f"artists/{id}", data, use_token=True)

    async def delete_artist(self, id: int) -> bool:
        res = await self._delete(f"artists/{id}", use_token=True)
        return res is not None

    async def create_location(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._post("locations", data, use_token=True)

    async def update_location(self, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._put(f"locations/{id}", data, use_token=True)

    async def delete_location(self, id: int) -> bool:
        res = await self._delete(f"locations/{id}", use_token=True)
        return res is not None

    async def create_article(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._post("articles", data, use_token=True)

    async def update_article(self, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._put(f"articles/{id}", data, use_token=True)

    async def delete_article(self, id: int) -> bool:
        res = await self._delete(f"articles/{id}", use_token=True)
        return res is not None

    async def get_melody(self, melody_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(f"{API_BASE_URL}/melodies/{melody_id}/")
                if response.status_code == 200:
                    return response.json()
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
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
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(f"{API_BASE_URL}/events/{event_id}/")
                if response.status_code == 200:
                    return response.json()
        except httpx.ConnectError:
            print(f"CRITICAL: Could not connect to backend at {API_BASE_URL}")
        except Exception as e:
            print(f"Error fetching event {event_id}: {e}")
        return None

    async def get_comments(self, melody_id: Optional[int] = None, article_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params = {}
        if melody_id: params['melody_id'] = melody_id
        if article_id: params['article_id'] = article_id
        return await self._get("comments", params=params)


    async def create_comment(self, content: str, melody_id: Optional[int] = None, article_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {"content": content}
        if melody_id: data['melody_id'] = melody_id
        if article_id: data['article_id'] = article_id
        return await self._post("comments/", data, use_token=True)

    async def get_my_activities(self) -> List[Dict[str, Any]]:
        return await self._get("auth/me/activities", use_token=True)

api_client = APIClient()
