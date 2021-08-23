import json

conf = None

def config(dir):
    with open(dir, mode="r", encoding='utf-8') as f:
        global conf
        conf = json.loads(f.read())
    return conf