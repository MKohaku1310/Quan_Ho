import httpx
import asyncio

async def test_event_registration():
    # Test login first
    async with httpx.AsyncClient() as client:
        # Login to get token
        login_response = await client.post(
            "http://127.0.0.1:8000/api/auth/login",
            data={"username": "admin@example.com", "password": "admin123"}
        )
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return
        
        login_data = login_response.json()
        token = login_data.get("access_token")
        print(f"Login successful, token: {token[:20]}...")
        
        # Get events
        events_response = await client.get("http://127.0.0.1:8000/api/events")
        if events_response.status_code != 200:
            print(f"Get events failed: {events_response.status_code} - {events_response.text}")
            return
        
        events = events_response.json()
        if not events:
            print("No events found")
            return
        
        event_id = events[0]["id"]
        print(f"Found event: {events[0]['title']} (ID: {event_id})")
        
        # Try to register for event
        headers = {"Authorization": f"Bearer {token}"}
        register_data = {
            "name": "Test User",
            "email": "test@example.com", 
            "phone": "0123456789",
            "note": "Test registration"
        }
        
        register_response = await client.post(
            f"http://127.0.0.1:8000/api/events/{event_id}/register",
            json=register_data,
            headers=headers
        )
        
        print(f"Registration response: {register_response.status_code} - {register_response.text}")

if __name__ == "__main__":
    asyncio.run(test_event_registration())
