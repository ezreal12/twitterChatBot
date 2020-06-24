# 매시간마다 발생하는 이벤트중 "답변을 기다리는 이벤트"
import botTweeterClient
import botTweeterAPI
# EVENT_TIME_1를 입력받아서 유저가 한 말에 따라 다른 EVENT_TIME_RE_1 혹은 EVENT_TIME_RE_2 를 보냄
# EVENT_TIME_1 : 스케쥴러에의한 랜덤 이벤트중 (시간 확인) 오늘 많이 힘들었어?
# EVENT_TIME_1_RE_1 : 긍정
# EVENT_TIME_1_RE_2 : 부정

# 긍정을 먼저 찾는거보다 그냥 부정만 찾아서 부정이 아니라면 긍정을 찾고 긍정도 못찾는다면
# 이벤트에 맞는 대사가 아니라고 생각하고 그냥 흘러보내자.
yes=["응","yes","맞아","힘들었어"]
no=["아냐","괜찮아","안 힘들었어","아니","아뇨","아니요","아닙니다","no","않아요","않습니다"]
def startTimeEventOne(api,msg):
    for n in no:
        if n in msg.text:
            #부정 대사 적중
            botTweeterAPI.sendBotAndTweetRespone(api, "EVENT_TIME_1_RE_2",msg)
            return
    for y in yes:
        if y in msg.text:
            #긍정 대사 적중
            botTweeterAPI.sendBotAndTweetRespone(api, "EVENT_TIME_1_RE_1",msg)
            return
    #긍정도 부정도 못찾았을때 -> 그냥 대사 흘려보냄
    #그냥 대사 흘려보냄 = 이 msg로 형태소분석 등등을 거쳐서 원래 프로세스로 보냄
    botTweeterClient.sendMsg(msg)
    return
# EVENT_TIME_2 : 스케쥴러에의한 랜덤 이벤트중 사람은 꿈을꾼다는데 너는 무슨 꿈을꿔?
# 대답이 어떻든 참고하겠다고 말하는 EVENT_TIME_2_RE 를 보냄
def startTimeEventTwo(api,msg):
    botTweeterAPI.sendBotAndTweetRespone(api, "EVENT_TIME_2_RE", msg)
    return