import requests
import sys
import json

org = "griff182uk0203"
project = "hungovercoders"
pat = ""
work_item_id = 302  # Replace with a real Objective ID

url = f"https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.0&$expand=relations"
resp = requests.get(url, auth=('', pat))
print(json.dumps(resp.json(), indent=2))
