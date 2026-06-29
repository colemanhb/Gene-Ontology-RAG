import requests

API_KEY = "622683ad-2781-4efd-96b6-af9c82bf31d6"

HEADERS = {
    "Authorization": f"apikey token={API_KEY}"
}

url = "https://data.bioontology.org/ontologies/XAO/latest_submission"

r = requests.get(url, headers=HEADERS)

print(r.json().keys())

print(r.json()["description"])