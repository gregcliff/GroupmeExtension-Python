import requests
import json

def user_id():
    return "505442"

#def group_id():
#    return "7178650"

def get_key():
    with open('C:\\Users\\Gregory\\groupme-key.txt', 'r') as f:
       content = f.read()
    return content

base_url = 'https://api.groupme.com/v3'

def add_access_token(url):
    return url + '?token=' + get_key()

def get_groups():
    j = json.loads(requests.get(add_access_token(base_url+"/groups")).text)
    name_to_id_map = {}
    for i in j['response']:
        name_to_id_map[i['name']] = i['id']
    return name_to_id_map

def get_group_by_name(name):
    return get_groups()[name]

print(requests.get(add_access_token(base_url+"/bots")).text)