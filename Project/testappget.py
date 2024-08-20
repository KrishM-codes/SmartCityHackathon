import requests
import json

URL = "http://127.0.0.1:8000/queryapiview"

def getquery(username=None):
    data={}
    if username is not None:
        data={'uname':username}
    jsondata = json.dumps(data)
    headers = {'content-Type':'application/json'}

    print(jsondata)
    r = requests.get(url=URL,headers=headers,data=jsondata)
    data = r.json()
    print(data)

# getquery()

def update():
    data = {
        'id' : 7,
        'Location':' Main Street'
    }

    headers = {'content-Type':'application/json'}

    json_data = json.dumps(data)
    r = requests.put(url=URL, headers=headers ,data=json_data)
    data = r.json()
    print(data)

# update()

def delete():
    data = {'id' : 8}
    json_data = json.dumps(data)
    headers = {'content-Type':'application/json'}
    r = requests.delete(url=URL,headers=headers, data=json_data)
    data = r.json()
    print(data)

delete()