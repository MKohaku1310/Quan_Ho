import asyncio
import httpx

async def test_api():
    async with httpx.AsyncClient() as client:
        # Test Village 2
        resp = await client.get("http://127.0.0.1:8000/api/locations/2")
        print(f"API Locations 2: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Data name: {resp.json().get('name')}")
        
        # Test Auth Me (if token found, but we can't easily get it here)
        
        # Test Village List
        resp = await client.get("http://127.0.0.1:8000/api/locations")
        print(f"API Locations List: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Count: {len(resp.json())}")
            for v in resp.json():
                print(f" - ID {v['id']}: {v['name']} ({v.get('type')})")

if __name__ == "__main__":
    asyncio.run(test_api())
