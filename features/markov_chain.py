import random
import re

def message_list_to_text_chunk(messages):
    message_text_chunk = ""
    for message in messages:
        if message.has_text() and not message.is_from_bot():
            message_text_chunk += message.text + '.'
    return message_text_chunk

def generate(messages, output_sentences=2, order=2):
    message_text_chunk = message_list_to_text_chunk(messages)
    return generate_from_text(message_text_chunk, output_sentences, order)

def build_markov_chain(messages, order):
    inputs = message_list_to_text_chunk(messages)

    if type(inputs) == str:
        inputs = build_input_list([inputs])

    root_node = MarkovNode(order)
    for i in inputs:
        splits = i.split(" ")
        if len(splits) > 0:
            prev_list = [""]
            for split in splits:
                prev_list.append(split)
                if len(prev_list) > order:
                    del prev_list[0]
                root_node.add(prev_list)
            prev_list.append('.')
            if len(prev_list) > order:
                del prev_list[0]
            root_node.add(prev_list)
    return root_node

def generate_from_markov_chain(markov_root_node, num_sentences, order):
    n = num_sentences
    current_list = [""]
    output = ""
    sentence = ""
    while n > 0:
        current = markov_root_node.generate_next(current_list)
        if current == "." or current == '':
            # get rid of the last ' '
            sentence = sentence[:len(sentence) - 1]
            if len(output) == 0:
                output += sentence
            else:
                output += ".  " + sentence
            current_list = [""]
            sentence = ""
            n -= 1
            continue

        sentence += current + " "
        current_list.append(current)
        if len(current_list) > order:
            del current_list[0]
    return output

def generate_from_text(inputs, num_sentences, order):
    if type(inputs) == str:
        inputs = build_input_list([inputs])

    root_node = MarkovNode(order)
    for i in inputs:
        splits = i.split(" ")
        if len(splits) > 0:
            prev_list = [""]
            for split in splits:
                prev_list.append(split)
                if len(prev_list) > order:
                    del prev_list[0]
                root_node.add(prev_list)
            prev_list.append('.')
            if len(prev_list) > order:
                del prev_list[0]
            root_node.add(prev_list)
    n = num_sentences
    current_list = [""]
    output = ""
    sentence = ""
    while n > 0:
        current = root_node.generate_next(current_list)
        if current == "." or current == '':
            # get rid of the last ' '
            sentence = sentence[:len(sentence)-1]
            if len(output) == 0:
                output += sentence
            else:
                output += ".  " + sentence
            current_list = [""]
            sentence = ""
            n -= 1
            continue

        sentence += current + " "
        current_list.append(current)
        if len(current_list) > order:
            del current_list[0]
    return output

class MarkovNode(object):
    def __init__(self, order):
        self.order = order
        self.children = {}
        self.values = []
        self.names = []
        self.total = 0

    def _index_of_name(self, val):
        low = 0
        high = len(self.names) - 1
        while low <= high:
            mid = low + int((high - low) / 2)
            if self.names[mid] > val:
                high = mid - 1
            elif self.names[mid] < val:
                low = mid + 1
            else:
                return True, mid
        else:
            return False, high + 1

    def add(self, vals):
        self.total += 1
        val = vals[0]

        contains_val = self._index_of_name(val)
        if not contains_val[0]:
            # reorder both arrays
            f = self.names[:contains_val[1]]
            d = self.names[contains_val[1]:]
            self.names = f + [val] + d
            self.values = self.values[contains_val[1]:] \
                          + [0] + self.values[:contains_val[1]]

        self.values[contains_val[1]] += 1

        if self.order > 1:
            if len(vals) > 1:
                if val not in self.children:
                    self.children[val] = MarkovNode(self.order - 1)
                self.children[val].add(vals[1:])

    def generate_next(self, prev_list):
        node = self
        for prev in prev_list:
            if prev not in node.children:
                return self.generate_next(prev_list[1:])
            node = node.children[prev]
        rand_int = random.randint(0, node.total)
        for i, value in enumerate(node.values):
            if rand_int - value <= 0:
                return node.names[i]
            rand_int -= value
        else:
            raise Exception("Logic error!")

def build_input_list(raw_messages):
    processed_input = []
    for raw_message in raw_messages:
        processed_input += process_message(raw_message)
    return processed_input

def process_message(raw_message):
    processed_messages = []
    processed_message = re.sub(r'\.\.+', '.', raw_message)
    processed_message = re.sub(r'  +', ' ', processed_message)
    processed_message = processed_message.replace('.', '\n')
    for split in processed_message.split('\n'):
        if split.startswith(' '):
            processed_messages.append(split[1:])
        else:
            processed_messages.append(split)
    return processed_messages