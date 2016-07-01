
import requests
import json
import os
import logging
import os
import importlib

GROUPME_INIT_FILE_VAR = "GROUPME_CONFIG_FILE"
default_file = os.path.expanduser('~'+os.path.sep+'groupme-ext.conf')
base_url = 'https://api.groupme.com/v3'

def get_config_info():
    if GROUPME_INIT_FILE_VAR in os.environ:
        file = os.environ[GROUPME_INIT_FILE_VAR]
    else:
        if os.path.exists(default_file):
            file = default_file
        else:
            raise Exception("Need a config file.  Specify file location with \'GROUPME_CONFIG_FILE\' or put "
                            "\'groupme-ext.conf\' in " + str(os.path.abspath(os.path.expanduser("~"))) + ".")
    with open(file, 'r') as f:
       content = f.read()
    j = json.loads(content)
    return j

def get_handler_instances(handler_list):
    handler_dict = get_config_info()['handlers']
    for key in handler_dict:
        package = key[:key.rfind('.')]
        handler_class = key[key.rfind('.')+1:]
        handler_class = getattr(importlib.import_module(package), handler_class)
        params = handler_dict[key]
        handler_list.append(handler_class(handler_dict[key]))
    return handler_list

def add_access_token(url):
    return url + '?token=' + get_config_info()['access_key']

def get_groups():
    j = json.loads(requests.get(add_access_token(base_url+"/groups")).text)
    name_to_id_map = {}
    for i in j['response']:
        name_to_id_map[i['name']] = i['id']
    return name_to_id_map

def get_group_by_name(name):
    groups = get_groups()
    if name in groups:
        return get_groups()[name]
    return None

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

def create_bot(name, group_id):
    bots = get_bots()['response']
    if name in [b['name'] for b in bots]:
        raise Exception("Bot name already taken.  Must be unique name.")
    url = add_access_token(base_url + "/bots")
    print(url)
    j = json.loads(requests.post(url, json={"bot":{"name":name,"group_id":group_id}}).text)
    if int(j['meta']['code']) != 201:
        raise Exception("Bot was not successfully created: " + str(j))
    else:
        return j['response']['bot']

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