import httpx

# Create a global async client
client = httpx.AsyncClient()

# Function to close the client
async def close_client():
    await client.aclose()