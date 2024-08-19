import requests
import json

# URL = "http://127.0.0.1:8000/queries"
URL = "http://127.0.0.1:8000/queryapiview"

data = {
    "Title":"Broken Divider",
    "Description":"A long patch of road has non continous divider",
    "Location":"AB River Front",
    "Posted_by":"Abc_xyZ"
}

headers = {'content-Type':'application/json'}

json_data = json.dumps(data)
r = requests.post(url=URL, headers=headers ,data=json_data)
pdata = r.json()

print(pdata)