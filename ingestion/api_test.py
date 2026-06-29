import requests

url = "https://data.bioontology.org/ontologies"
headers = {"Authorization": "apikey token=622683ad-2781-4efd-96b6-af9c82bf31d6"}

resp = requests.get(url, headers=headers)
data = resp.json()

print(data[0])