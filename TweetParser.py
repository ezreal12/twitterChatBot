import MeCabUtil
import TraceDataManager
import random
import SocketSendModule
def encodeTweetData(data):
    try:
        data = data.encode('utf-8')
        data = data.decode('unicode_escape')
    except:
        return "Err"

    return data


# 입력된 텍스트를 Okt/komoran로 형태소 분석되어 분리된 문자로 리턴하기
def parseFromOkt(text):
    str = MeCabUtil.parseToArrStr(text)
    result = ' '.join(str)
    return result


# 프로토콜에 쓰여진대로 봇의 특수문자를 처리하기위한 함수
# 트윗 조작 후 처리 프로토콜 : 트위터의 조작 후 처리 보고를 표현하는 프로토콜
# 예 (안화 봇) : 트윗 CODET01 처리 완료 했다. -> 트윗 삭제 처리 완료 했다.
# CODES01 = (
# CODES02 = )
# CODET01 = 삭제 (트윗 조작 후 처리 프로토콜)
# CODEU01 = 스크립트에서 유저 이름을 나타내는것 : 주의 : name은 None일수있음 체크필수
# 여기서 data는 봇이 말했던 텍스트 / name = CODEU01에서 치환될 유저 이름 / (중요)eventManager = 이벤트 추가를 해야하는 대사인경우 들엉모
# screen_name = 유저 스크린 네임 -> 태그할때쓰임
def parseBotScriptProtocol(data, name=None, eventManager=None, screen_name=None):
    data = data.replace("CODES01", "(")
    data = data.replace("CODES02", ")")
    data = data.replace("CODET01", "삭제")
    # nam
    if (name != None):
        data = data.replace("CODEU01", name)
        
    if (eventManager != None and screen_name != None):
        data = parseEventCode(data, eventManager, screen_name)
        
    return data


# 이벤트 코드 파싱하기
# EVENT_TIME_1 : 스케쥴러에의한 랜덤 이벤트중 (시간 확인) 오늘 많이 힘들었어? (폐기)
# EVENT_TIME_2 : 스케쥴러에의한 랜덤 이벤트중 사람은 꿈을꾼다는데 너는 무슨 꿈을꿔? (폐기)
# EVENTLIKE1 : 사용자가 오늘 기뻤다는 말을 했을때 봇의 질문 -> 뭐가 그렇게 기뻤어?
# EVENTSAD1 : 사용자가 오늘 슬펐다는 말을 했을때 봇의 질문 -> 뭐가 그렇게 슬펐어?
# EVENT_ 코드들은 screen_name이 꼭 필요함.
# 한번의 봇 대사에 1개의 이벤트코드만 들어가야함(유저문자말고 이벤트문자)
# def addEvent(self,screen_name, event_code,value=None):
def parseEventCode(data, eventManager, screen_name):
    if "EVENTLIKE1" in data:
        data = data.replace("EVENTLIKE1", "")
        eventManager.addEvent(screen_name, "EVENTLIKE1")
    elif "EVENTSAD1" in data:
        data = data.replace("EVENTSAD1", "")
        eventManager.addEvent(screen_name, "EVENTSAD1")
    elif "ANSERNOTFOUNDRE01" in data:
        # 사용자가 원래 했던 답 || 봇이 대답한 답  이 묶여서 나올텐데 이걸 나눠서 
        # 사용자가 원래 했던 답은 딥러닝 챗봇한테 보내고 봇이 대답한 답을 파싱해서 치환
        resultArr = data.split("||")
        resultArr[1] = resultArr[1].replace("ANSERNOTFOUNDRE01", "")
        # 1. 소켓과 통신해서 답신 가져오기
        reple = SocketSendModule.sendMessage(resultArr[0])
        # 2. word를 답신으로 치환하기
        if(reple!=None):
            data = resultArr[1].replace("word", reple)
        else:
            # 3. 만약 답신이 None이면 서버와의 에러 발생으로 텍스트 변경
            data = "서버 통신 에러 발생. 긴급 조치를 요청합니다."

    #addEvent(self,screen_name, event_code,value=None):
    #EVENTTWEETCODE03 일때 처리하기
    elif "EVENTTWEETCODE03" in data:
        #일단 봇 대사에 포함된 이벤트코드 제거하기
        data = data.replace("EVENTTWEETCODE03", "")
        dataSp = data.split('||')
        # screen_name으로 해당 유저의 word.json에서 랜덤하게 word 데이터 가져오기(word,cnt,text)
        wordDataArr = TraceDataManager.getWordJsonData(screen_name)
        # word.json 파일은 존재하는데 안에 데이터가 0인경우(없는경우)가 있을수있나? -> 아직은 없다고 가정
        wordData = random.choice(wordDataArr)
        # 이미 text가 있을경우 봇의 대답에 text 내용을 끼워넣어서 말해야함.
        # 봇의 대사도 text가 있을경우||없을경우가 나뉘어있어야할듯
        # 트위터의 140자 제한도 있고 ||로 묶은 데이터의 한계상 봇의 대사도 짧게할것
        # EVENTTWEETCODE03 word 는 text 야? || word 가 뭐야?
        # word에 replace로 word 넣고 text에 완성된 str 넣기
        # || 앞쪽엔 text가 있을때 대사를 짧게, 뒤쪽엔 text 없을때 질문대사를 짧게
        if(len(wordData['text'])>0):
            str = ""
            for t in wordData['text']:
                str+=t+" "
            data = dataSp[0].replace("word",wordData['word'])
            data = data.replace("text",str)
        # text가 없을경우 질문-답변-회신 이벤트 발생
        else:
            data = dataSp[1].replace("word",wordData['word'])
            eventManager.addEvent(screen_name, "EVENTTWEETCODE03", wordData)
    return data


# 사용자가 봇한테 건네는 메시지를 먼저 가져와서
# 트위터에 사용하는 특수 기능을 요구하는 내용인지 확인함
# 특수기능을 요구하는 내용이면 해당 코드를 리턴하고 아니면 null 리턴
# 특수기능의 처리 혹은 null 일때 처리는 호출부에서 알아서 할것
# CODET01 = 최근 트윗 제거
# CODET02 = 관리자가 아닌데 명령해서 거절트윗
def parseUserMsgForTweet(msg):
    # 트윗 보낸자가 관리자가 아닐경우 명령어 인식을 할수없다.
    removeCode1 = "트윗"
    removeCode2 = "지워"
    if removeCode1 in msg.text:
        if removeCode2 in msg.text:
            # 트윗 / 지워가 다 있을경우 삭제 명령으로 취급
            # 관리자면 명령수행코드 리턴 아니면 거절코드 리턴
            if msg.isAdmin:
                return "CODET01"
            else:
                return "CODET02"
    return "null"

# data = 스트리머를 통해 들어온 트윗 데이터
# id = 찾으려는 키워드 text , id_str, screen_name 등
# dataLimit = 데이터는 여러개가 있을수 있다. 예를들어 id_str의 경우 "트윗 자체의 고유 ID"와 "작성자의 유저 id_str"이 있는데
# word를 통해 찾으려는 '몇번째 word의 내용물을 가져올것이냐"를 정의함.
# 예를들어 dataLimit 가 2이고 word가 id_str이면 검색된 id_str 중에서 2번째 id_str을 리턴함.
def parseTweetData(data, id, dataLimit=1):
    arr = data.split(',')
    formatId = '"' + id + '"'
    result = []
    for i in arr:
        # print(i)
        arr2 = i.split(':')
        # ['{"created_at"', '"Thu Sep 26 04', '53', '06 +0000 2019"']
        # ['"text"', '"테스트하다 하루종일 다가갯다"']

        # print (arr2[0]+ ':' + arr2[1]) 내용 출력해서 보고싶으면 주석해제

        if arr2[0] == formatId:
            serchData = arr2[1]
            # 문자열 데이터에 들어있을 쌍따옴표 제거
            serchData = serchData.replace('"', "")
            # 문자열 데이터의 개행문자를 띄어쓰기 문자로 치환
            serchData = serchData.replace('\n', " ")
            result.append(serchData)
    
    
    if(len(result)==0):
        return "null"
    else:
        # 검색하려는 dataLimit번째 데이터가 없을경우
        if(len(result)<dataLimit):
            return "null"
        else:
            return result[dataLimit-1]


if __name__ == '__main__':
    data = '{"created_at":"Thu Sep 26 04:53:06 +0000 2019","id":1177083652120825856,"id_str":"1177083652120825856","text":"\ud14c\uc2a4\ud2b8\ud558\ub2e4 \ud558\ub8e8\uc885\uc77c \ub2e4\uac00\uac2f\ub2e4","source":"\u003ca href=\"https:\/\/mobile.twitter.com\" rel=\"nofollow\"\u003eTwitter Web App\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":937835196568571904,"id_str":"937835196568571904","name":"\uc2dc\uc6b0\ucd08\ub144\uc0dd","screen_name":"Cyphers_SiuKim","location":null,"url":null,"description":"\uc0ac\uc774\ud37c\uc988 \ub2c9\ub124\uc784 \uc2dc\uc6b0\ucd08\ub144\uc0dd 53\uae09 \uc131\uc778\ub0a8\uc131\n\ub9c8\ube44\ub178\uae30 \uacc4\uc815 @Mabinogi_SiuKim","translator_type":"none","protected":false,"verified":false,"followers_count":23,"friends_count":110,"listed_count":0,"favourites_count":6310,"statuses_count":9599,"created_at":"Tue Dec 05 00:05:09 +0000 2017","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"F5F8FA","profile_background_image_url":"","profile_background_image_url_https":"","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/1176355093391663105\/NvyK8Qdl_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/1176355093391663105\/NvyK8Qdl_normal.jpg","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"ko","timestamp_ms":"1569473586479"}"'

    result = parseTweetData(data, "id_str",2)

    print("--------------------- result !! = {}".format(result))







