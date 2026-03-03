import requests

response = requests.get("https://api.github.com/users/aditiabhang")
data = response.json()

print(f"Name:    {data['name']}")
print(f"Bio:     {data['bio']}")
print(f"Repos:   {data['public_repos']}")
print(f"Status:  {response.status_code}")

response_cat = requests.get("https://catfact.ninja/fact")
fact = response_cat.json()
print(f"🐱 {fact['fact']}")