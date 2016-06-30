
import requests
import json
import os

GROUPME_INIT_FILE_VAR = "GROUPME_FILE"

def get_connection_info():
    if GROUPME_INIT_FILE_VAR in os.environ:
        file = os.environ[GROUPME_INIT_FILE_VAR]
    else:
        file = 'C:\\Users\\Gregory\\groupme-key.txt'
    with open(file, 'r') as f:
       content = f.read()
    j = json.loads(content)
    return j['access_key'], j['user_id'], j['group_id']

base_url = 'https://api.groupme.com/v3'

def add_access_token(url):
    return url + '?token=' + get_connection_info()[0]

def get_groups():
    j = json.loads(requests.get(add_access_token(base_url+"/groups")).text)
    name_to_id_map = {}
    for i in j['response']:
        name_to_id_map[i['name']] = i['id']
    return name_to_id_map

def get_group_by_name(name):
    return get_groups()[name]

def get_bots():
    return json.loads(requests.get(add_access_token(base_url + "/bots")).text)

def get_bot_by_name(name):
    bot_data = get_bots()
    if 'response' in bot_data:
        bots = bot_data['response']
        for bot in bots:
            if bot['name'] == name:
                return bot
    return None

def publish_bot_message(bot_id, text, picture_url=None):
    j = {
        'bot_id':str(bot_id),
        'text':str(text)
    }
    if picture_url is not None:
        j['picture_url'] = str(picture_url)
    try:
        requests.post(add_access_token(base_url+"/bots/post"), json=j)
        return True
    except Exception:
        return False