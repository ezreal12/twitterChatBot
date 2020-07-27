import json
from collections import OrderedDict

# save/load시에 파일명엔 반드시 .json이 포함된다.
def saveJsonFile(data,fileName):
    with open(fileName, 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t")

def loadJsonFile(fileName):
    try:
        with open(fileName, 'r') as f:
            json_data = json.load(f)
            return json_data
    except BaseException:
        print("------ERROR loadJsonFile "+fileName)
        print(BaseException)
        return None