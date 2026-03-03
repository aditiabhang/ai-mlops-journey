import requests

try:
    response = requests.get("https://api.github.com/users/aditiabhang369", timeout=5)
    response.raise_for_status()
    data = response.json()
    print(f"✅ Got data for {data['name']}")
except requests.exceptions.ConnectionError:
    print("❌ Can't reach the server — check your internet")
except requests.exceptions.Timeout:
    print("❌ Request timed out — server too slow")
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")