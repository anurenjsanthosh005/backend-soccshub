import requests
import random

API_URL = "http://localhost:8000/api/products/"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzE5MjUxLCJpYXQiOjE3NjEzMTU2NTEsImp0aSI6ImVjNmQyOGIyZWI2OTRjMDNiNDUxMzk3OTdlMGQ1ZTc0IiwidXNlcl9pZCI6IjEifQ.6V0xH-P3Z6gTWnmYV2jbWto9KlYaM3aSiSFjNRodhHc"
headers = {
    "Authorization": f"Bearer {TOKEN}",
}

length_types = ["low_cut", "ankle", "crew"]

for i in range(1, 51):
    data = {
        "name": f"Soccs {i}",
        "description": f"Unisex socks model {i}",
        "price": f"{random.randint(100, 999)}.00",
        "stock": random.randint(1, 100),
        "discount": f"{random.randint(0, 20)}.00",
        "is_active": random.choice([True, False]),
        "length_type": random.choice(length_types),
    }

    response = requests.post(API_URL, data=data, headers=headers)

    if response.status_code == 201:
        print(f"✅ Product {i} created successfully")
    else:
        print(f"❌ Failed to create product {i}: {response.status_code} - {response.text}")
