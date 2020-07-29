# 매시간마다 발생하는 이벤트중 "답변을 기다리는 이벤트"
import botTweeterAPI
import MeCabUtil
import TraceDataManager
# 입력받은 word의 text를 json에 저장하고 답장하기
# value엔 word 데이터(word['word','cnt','text(값은 없을것임)'] 1개가 들어있음.
def saveWordText(api,msg,value):
    parseStrArr = MeCabUtil.parseToArrStr(msg.text)
    value['text'] = parseStrArr
    flag = TraceDataManager.saveWordJson(value,msg.screen_name)
    if(flag==False):
        print("저장 실패 {0} : {1}".format(msg.screen_name,msg.text))
    # EVENTTWEETCODE03RE엔 그냥 알았다는 OK 답장만 담을것 (확인답장 받는게 구조적으로 조금 어려움)
    botTweeterAPI.sendBotAndTweetRespone(api, "EVENTTWEETCODE03RE",msg)
    return