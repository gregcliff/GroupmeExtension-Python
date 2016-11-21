import core.util
import json

class User(object):

    def __init__(self, member_id, user_id, user_name):
        self.member_id = member_id
        self.user_id = user_id
        self.user_name = user_name

    def kick(self):
        pass

    def __str__(self):
        return "User: " + str(self.user_name) + " with id " + str(self.member_id) + \
            " and user_id " + str(self.user_id)

def get_user_by_name(user_name):
    all_users = core.util.get_users_in_group()
    for user in all_users:
        if user['nickname'] == user_name:
            return User(user['id'], user['user_id'], user['nickname'])
    return None

'''
# Train Markov chain with one particular user
user = "User"
lex_messages = core.util.get_messages(
    core.util.get_config_info()['real_group_id'],
    1000,
    [get_user_by_name(user).user_id])

import features.markov_chain

order = 2
chain = features.markov_chain.build_markov_chain(lex_messages, order)

c = 'y'
while c == 'y':
    print(features.markov_chain.generate_from_markov_chain(chain, 2, order))
    c = input("Continue? (y)")

'''