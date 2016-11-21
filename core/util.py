import requests
import json
import os
import importlib
from core.message import Message

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

def get_handler_instances():
    handler_list = []
    handler_dict = get_config_info()['handlers']
    for key in handler_dict:
        package = key[:key.rfind('.')]
        handler_class = key[key.rfind('.')+1:]
        try:
            handler_class = getattr(importlib.import_module(package), handler_class)
            params = handler_dict[key]
            handler_list.append(handler_class(params if params is not None else {}))
        except ImportError as import_err:
            print(import_err)
            print("Could not find " + handler_class)
    return handler_list

def add_access_token(url):
    return url + '?token=' + get_config_info()['access_key']

def get_groups():
    j = json.loads(requests.get(add_access_token(base_url+"/groups")).text)
    name_to_id_map = {}
    for i in j['response']:
        name_to_id_map[i['name']] = i['id']
    return name_to_id_map

def get_messages(group_id, number_of_messages, user_ids=[]):
    if len(user_ids) == 0:
        user_ids = get_users_in_group(group_id)
    num_requests = 0
    message_list = []
    remaining = number_of_messages
    last_message_id = None
    while remaining > 0 and num_requests < 50:
        ask_for = 100 if remaining > 100 else remaining
        j = json.loads(requests.get(
            add_access_token(base_url + "/groups/" + group_id + "/messages"),
            params={'limit': int(ask_for),
                    'before_id': None if last_message_id is None else str(last_message_id)})
                       .text)['response']
        potential_messages = [Message(message) for message in j['messages']]
        last_message_id = potential_messages[len(potential_messages) - 1].raw_message['id']
        for potential_message in potential_messages:
            if potential_message.sender_id in user_ids:
                message_list.append(potential_message)
        num_requests += 1
        remaining = number_of_messages - len(message_list)
    return message_list

def get_users_in_group(group_id=None):
    if group_id is None:
        group_id = get_config_info()['real_group_id']
    response = json.loads(requests.get(add_access_token(base_url + "/groups")).text)['response']
    return [g for g in response if g['id'] == group_id][0]['members']

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