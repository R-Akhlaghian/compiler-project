import json

grammar = dict()
def read_txt_file(file_name):
    file = open(file_name , 'r')
    lines = file.readlines()
    file.close()
    return lines

def read_json_file(file_name):
    with open(file_name) as f:
        d = json.load(f)
        f.close()
        return d

def load_grammar():
    global grammar
    rules = read_txt_file("grammer.txt")
    for item in rules:
        nt, rule = item.strip().split(" -> ")
        grammar[nt] = {
            "rules": rule.split(" | ")
        }

def load_first():
    global grammar
    json_file = read_json_file("first_follow.json")
    for item in json_file:
        grammar[item["Non-Terminal"]]["first"] = item["First"].split()
        grammar[item["Non-Terminal"]]["follow"] = item["Follow"].split()

def get_rules(none_terminal):
    return grammar[none_terminal]["rules"]

def get_first_set(none_terminal):
    if is_terminal(none_terminal):
        return [none_terminal]
    return grammar[none_terminal]["first"]

def get_follow_set(none_terminal):
    return grammar[none_terminal]["follow"]

def get_start_rule():
    return "Program"

def is_terminal(key):
    if key in grammar:
        return False
    return True