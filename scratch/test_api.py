import httpx
import asyncio

async def test():
    url = "http://127.0.0.1:8000/api/locations/?type=lang_quan_ho"
    print(f"Testing {url}...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            print(f"Status: {response.status_code}")
            print(f"Data: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
