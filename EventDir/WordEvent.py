# 매시간마다 발생하는 이벤트중 "답변을 기다리는 이벤트"
import botTweeterAPI
import MeCabUtil
import TraceDataManager


no_answer=["아니","아냐","아니야","안할래","안 할래","말못해","말 못해"]

# 입력받은 word의 text를 json에 저장하고 답장하기
# value엔 word 데이터(word['word','cnt','text(값은 없을것임)'] 1개가 들어있음.
def saveWordText(api,msg,value):
    
    noAnswer = isNoAnswer(msg.text)

    # 대답이 부정문이 아닌경우
    if(noAnswer==False):
        parseStrArr = MeCabUtil.parseToArrStr(msg.text)
        value['text'] = parseStrArr
        flag = TraceDataManager.saveWordJson(value, msg.screen_name)
        if (flag == False):
            print("저장 실패 {0} : {1}".format(msg.screen_name, msg.text))
        # EVENTTWEETCODE03RE엔 그냥 알았다는 OK 답장만 담을것 (확인답장 받는게 구조적으로 조금 어려움)
        botTweeterAPI.sendBotAndTweetRespone(api, "EVENTTWEETCODE03RE", msg)
    # 대답이 부정문일경우 대답 저장하지않음.
    else:
        # 대답을 부정했다는걸 확인했다는 OK 사인을 보내고 해당 word 제거
        flag = TraceDataManager.removeWordJson(value, msg.screen_name)
        if (flag == False):
            print("워드 삭제 실패 실패 {0} {1}: {2}".format(msg.screen_name,value['word'],msg.text))
        botTweeterAPI.sendBotAndTweetRespone(api, "EVENTTWEETCODE03NOTRE", msg)
    return

# 사용자가 한 대답에서 부정문의 존재여부를 찾아서 리턴함
# 사용자가 한 대답에서 부정문이 포함된경우 True, 아니면 False 리턴
# 사용자가 한 대답이 부정문이 아닐경우 대답을 저장하기위해 사용
def isNoAnswer(text):
    for n in no_answer:
        if n in text:
           return True

    return False