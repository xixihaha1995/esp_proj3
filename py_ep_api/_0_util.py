import os, json
def saveJSON(data, name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    with open(os.path.join(script_dir, '../py_ep_outputs',name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def loadJSONFromOutputs(name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    with open(os.path.join(script_dir, '../py_ep_outputs',name + '.json'), 'w+') as f:
        try:
            testDict = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            testDict = {}
    return testDict