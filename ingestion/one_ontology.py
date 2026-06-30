import requests

API_KEY = "622683ad-2781-4efd-96b6-af9c82bf31d6"

HEADERS = {
    "Authorization": f"apikey token={API_KEY}"
}

url = "https://data.bioontology.org/ontologies/APRO/groups"

r = requests.get(url, headers=HEADERS)

data = r.json()

#print(data.keys())

#print(data["links"].keys())

#categories_url = data["links"]["categories"]

#r = requests.get(categories_url, headers=HEADERS)
#categories = r.json()

print(data)

#print(data["links"].keys())

#print(data.get("@type"))

#print(data["description"])