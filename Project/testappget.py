import requests
import json

URL = "http://127.0.0.1:8000/queries"

def getquery(username=None):
    data={}
    if username is not None:
        data={'uname':username}
    jsondata = json.dumps(data)
    print(jsondata)
    r = requests.get(url=URL,data=jsondata)
    data = r.json()
    print(data)

getquery()

def update():
    data = {
        'id' : 6,
        'Location':' Main Street'
    }

    json_data = json.dumps(data)
    r = requests.put(url=URL, data=json_data)
    data = r.json()
    print(data)

# update()

def delete():
    data = {'id' : 6}
    json_data = json.dumps(data)
    r = requests.delete(url=URL, data=json_data)
    data = r.json()
    print(data)

# delete()