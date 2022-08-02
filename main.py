import requests
import json
response_API = requests.get('https://environment.data.gov.uk/flood-monitoring/data/readings?latest')
print(response_API.text)