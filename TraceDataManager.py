# 트윗 추적 서버에서 이벤트가 발생했을때 데이터들을 관리하는 매니저
# 임시파일의 저장, 임시파일을 읽어들여 본 파일을 저장하는등의 작업을 처리한다.
# 트레이스데이터 매니저에 본파일 저장을 요구하는건 스케쥴러가 한다.
import MeCabUtil
import JsonUtil

#-> 임시파일 : "(screen_name)_tmp.json"
#전처리 후 명사만 남겨서 해당 단어를 key value 형식의 단어:출현횟수로 기록

#라면:3
#와타리:25
#이자크:3


# 트윗 내용과 secreen_name을 읽어들여 임시파일에 저장하기
def saveTweetTmp(text,screen_name):
    # 0. text에서 명사만 뽑아내기
    textNN_arr = MeCabUtil.parseToArrStrNN(text)
    # 1. screen_name_tmp.json 파일 읽어오기
    fileName = screen_name+"_tmp.json"
    data = JsonUtil.loadJsonFile(fileName)

    # QuestionJson 데이터를 담아줄 배열
    if (data == None):
        print("json is None")
        data = []
        for n in textNN_arr:
            q = dict()
            q['word'] = n
            q['text'] = ""
            q['cnt'] = 0
            data.append(q)

    else:
        print("json is Not None")
        for n in textNN_arr:
            # 기존 json에서 해당 단어 n과 일치하는 word가 있나 탐색시작
            findWord = False
            for d in data:
                if (n == d['word']):
                    # 카운트 1 증가
                    d['cnt'] = d['cnt'] + 1
                    findWord = True
            # 파싱해서 얻은 단어를 다 뒤져도 기존 word를 찾지못한경우
            if (findWord == False):
                # 새로운 word 정보 추가
                newDict = dict()
                newDict['word'] = n
                newDict['text'] = ""
                newDict['cnt'] = 0
                data.append(newDict)

    JsonUtil.saveJsonFile(data,fileName)


    # 3. 읽어온 json 객체에서 textNN_arr 데이터가 있나 확인하기
    # 3-1. 데이터가 있을경우 카운트 늘리기
    # 3-1. 데이터가 없을경우 새로 등록하기
    # 4. 다시 json 객체 파일로 저장하기


if __name__ == '__main__':
    #saveTweetTmp("이건 테스트 데이터입니다.","test_screen123");
    saveTweetTmp("이건  데이터입니다.", "test_screen123");
    test = JsonUtil.loadJsonFile("test_screen123_tmp.json");
    print(test)