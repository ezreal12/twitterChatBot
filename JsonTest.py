import json
from collections import OrderedDict


def saveJson(data,fileName):
    with open(fileName, 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t")

def listParseToJson(list):
    data = OrderedDict()
    i=0
    for l in list:
        i=i+1
        data[l]=i
    return data

def jsonPrintTest(fileName):
    with open(fileName, 'r') as f:
        json_data = json.load(f)
    print(json_data)
    return json_data

if __name__ == '__main__':
    file_data = OrderedDict()
    file_data["name"] = "COMPUTER"
    file_data["language"] = "kor"
    file_data["words"] = {'ram': '램', 'process': '프로세스', 'processor': '프로세서', 'CPU': '씨피유'}
    file_data["number"] = 4

    print(json.dumps(file_data, ensure_ascii=False, indent="\t"))

    # json 파일로 저장

    with open('test.json', 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, indent="\t")

    # 저장한 파일 출력하기

    with open('test.json', 'r') as f:
        json_data = json.load(f)

    print(json_data)

