# 트윗 추적 서버에서 이벤트가 발생했을때 데이터들을 관리하는 매니저
# 임시파일의 저장, 임시파일을 읽어들여 본 파일을 저장하는등의 작업을 처리한다.
# 트레이스데이터 매니저에 본파일 저장을 요구하는건 스케쥴러가 한다.
import MeCabUtil
import JsonUtil
import os
#-> 임시파일 : "(screen_name)_tmp.json"
#전처리 후 명사만 남겨서 해당 단어를 key value 형식의 단어:출현횟수로 기록

#라면:3
#와타리:25
#이자크:3
#tmp json이 들어가는 경로
TmpFilePath = "./tmp"
# tmp가 아닌 json이 들어가는 경로
JsonFilePath = "./word"


# tmp 폴더속 모든 json을 체크하고 진짜 json으로 변경하기
def checkTmpFiles():
    print("-- checkTmpFiles")
    # 공통으로 cnt 내림차순으로 몇위까지 잘라낼지 제어하는 변수
    rankRange = 5
    #1. tmp 폴더속 모든 파일들 가져오기 (주의:json만 들어있어야함.)
    tmp_list = os.listdir(TmpFilePath)
    tmpFileList = [file for file in tmp_list if file.endswith(".json")]
    for idx,file in enumerate(tmpFileList) :
        #1. 해당 json 파일 읽어오기
        tmpFileFullPath = TmpFilePath + "/" + file
        print("-- read tmp File {0} : {1}".format(idx,tmpFileFullPath))
        data = JsonUtil.loadJsonFile(tmpFileFullPath)
        # cnt를 기준으로 오름차순 정렬
        sortData =sorted(data,key=(lambda x: x['cnt']))
        # actor_name[1:2] 배열자르기 예제 -> 해당 예제는 요소 1개만 가져옴 즉, 시작값은 0부터 끝은 아님 국루
        sortDataLen = len(sortData)
        # cnt 내림차순으로 몇위까지 잘라낼지 표시하는 변수
        # 만약 word가 잘라낼 순위보다도 적을경우 cnt 순위 상관없이 전부 잘라냄
        if(sortDataLen<rankRange):
            #cnt 내림차순으로 몇위까지 잘라낼지 표시하는 변수
            sortDownLank=sortDataLen
        else:
            sortDownLank=rankRange
        
        #2. cnt가 가장많은 5개 찾기
        #3. 해당 word 갖고있기
        # cnt rank에서 내림차순으로 rankRange 갯수만큼 뽑아낸 데이터 배열
        sortData = sortData[(sortDataLen-(sortDownLank)):sortDataLen]



        # _tmp.json 만 파일이름에서 도려내면 screen_name
        screen_name = file.replace("_tmp.json","")
        jsonFileName = screen_name +".json"
        jsonFilePullPath = JsonFilePath + "/" + jsonFileName

        # 5. screen_name의 json에 word 저장하기
        data = JsonUtil.loadJsonFile(jsonFilePullPath)
        # json 폴더가 존재하지않으면 생성해주고 이미 있으면 아무것도 안하기
        os.makedirs(JsonFilePath, exist_ok=True)

        if(data==None):
            #저장하기 전 cnt나 text는 0이랑 빈값으로 초기화
            for sd in sortData:
                sd['cnt'] = 0
                sd['text'] = ""
            # 기존 json이 없었을경우 새로 만들어주기
            JsonUtil.saveJsonFile(sortData, jsonFilePullPath)
        # 기존 json이 이미 있을경우 cnt만 올리기
        else:
            for sd in sortData:
                # 기존 json에서 해당 단어 sd랑 일치하는 word가 있나 탐색시작
                findWord = False
                for d in data:
                    if (sd['word'] == d['word']):
                        # 카운트 1 증가
                        d['cnt'] = d['cnt'] + 1
                        findWord = True
                if(findWord==False):
                    #단어 정보가 없었으면 단어 추가
                    sd['cnt'] = 0
                    sd['text'] = ""
                    data.append(sd)
            JsonUtil.saveJsonFile(data, jsonFilePullPath)
        print("-- save json File {0} : {1}".format(idx, jsonFilePullPath))
        #5. tmp 파일은 잊지말고 지우기
        os.remove(tmpFileFullPath)

                




# 트윗 내용과 secreen_name을 읽어들여 임시파일에 저장하기
def saveTweetTmp(text,screen_name):
    # 0. text에서 명사만 뽑아내기
    textNN_arr = MeCabUtil.parseToArrStrNN(text)
    # 1. screen_name_tmp.json 파일 읽어오기
    fileName = screen_name+"_tmp.json"
    fileFullPath = TmpFilePath + "/" + fileName
    # tmp폴더가 존재하지않으면 생성해주고 이미 있으면 아무것도 안하기
    os.makedirs(TmpFilePath, exist_ok=True)

    data = JsonUtil.loadJsonFile(fileFullPath)

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

    JsonUtil.saveJsonFile(data,fileFullPath)



if __name__ == '__main__':
    saveTweetTmp("이건 테스트 데이터입니다.","test_screen123");
    saveTweetTmp("이건  데이터입니다.", "test_screen123");
    test = JsonUtil.loadJsonFile("./tmp/test_screen123_tmp.json");
    print(test)
    checkTmpFiles()