# 매시간마다 발생하는 이벤트중 "답변을 기다리는 이벤트"
import botTweeterAPI
# EVENTLIKE1 : 사용자가 오늘 기뻤다는 말을 했을때 봇의 질문 -> 뭐가 그렇게 기뻤어?
# EVENTSAD1 : 사용자가 오늘 슬펐다는 말을 했을때 봇의 질문 -> 뭐가 그렇게 슬펐어?
# EVENTLIKE1RE : EVENTLIKE1에 대한 사용자의 답장
# EVENTSAD1RE : EVENTSAD1RE 대한 사용자의 답장
def homeEventReLike(api,msg):
    botTweeterAPI.sendBotAndTweetRespone(api, "EVENTLIKE1RE",msg)
    return

def homeEventReSad(api,msg):
    botTweeterAPI.sendBotAndTweetRespone(api, "EVENTSAD1RE", msg)
    return