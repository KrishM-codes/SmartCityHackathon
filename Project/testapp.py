import requests
import json

URL = "http://127.0.0.1:8000/queries"

data = {
    "Title":"Broken Divider",
    "Description":"A long patch of road has non continous divider",
    "Location":"AB River Front",
    "Posted_by":"Abc_xyZ"
}

json_data = json.dumps(data)
r = requests.post(url=URL, data=json_data)
pdata = r.json()
print(pdata)