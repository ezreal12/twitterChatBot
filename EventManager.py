#특정 유저의 이벤트 대화 흐름을 관리하는 매니저
# 통신 자료구조  = (@닉네임,CODERE_1,값)
from pytz import timezone
from datetime import datetime
import Event
import EventDir.HomeEvent
import EventDir.WordEvent
class EventManagerCore:
    eventQue = []
    def __init__(self,api):
        self.api = api

    # 주의 : 1개의 screen_name에 2개 이상의 이벤트는 추가될수없음
    # 중복에 주의할것
    def addEvent(self,screen_name, event_code,value=None):
        kst = datetime.now(timezone('Asia/Seoul'))
        if (value != None):
            event = Event.EventClass(screen_name, event_code,kst,value)
        else:
            event = Event.EventClass(screen_name, event_code,kst)
        EventManagerCore.eventQue.append(event)

    # 유저가 대사를 할땐 *반드시* 해당 유저가 이벤트를 진행중은 아니였는지 확인해야함
    # 만약 유저가 이벤트를 진행중이 아니였으면 일반 대화로 흘러감
    # 유저가 이벤트중이였으면 해당 이벤트에 맞는 "코드"를 봇한테 전달해야함.
    # EVENT_TIME_1 : 스케쥴러에의한 랜덤 이벤트중 (시간 확인) 오늘 많이 힘들었어? (폐기)
    # EVENT_TIME_2 : 스케쥴러에의한 랜덤 이벤트중 사람은 꿈을꾼다는데 너는 무슨 꿈을꿔? (폐기)
    # EVENTLIKE1 : 사용자가 오늘 기뻤다는 말을 했을때 봇의 질문 -> 뭐가 그렇게 기뻤어?
    # EVENTSAD1 : 사용자가 오늘 슬펐다는 말을 했을때 봇의 질문 -> 뭐가 그렇게 슬펐어?
    # EVENTLIKE1RE : EVENTLIKE1에 대한 사용자의 답장
    # EVENTSAD1RE : EVENTSAD1RE 대한 사용자의 답장
    # 봇이 코드가 담긴 대사를 내뱉었을때나 스케쥴러에 의해 이벤트가 발생했을때 봇은 말을 해놓고 기다리는 상태임.
    # 시나리오 1. 봇이 이벤트 코드가 담긴 대사를 함-> 이벤트 코드를 여기 삽입 -> 답변 기다림 -> 답변 옴 -> 여기서 이벤트 처리 -> 이벤트 처리 코드를 봇한테 전달
    # 시나리오 2. 스케쥴러에서 이벤트 발생 -> 해당 이벤트 코드를 여기 삽입함 -> 봇이 이벤트 코드에 맞는 말을 함 -> 답변기다림 -> 답변 옴 -> 여기서 이벤트 처리 -> 이벤트 처리 코드를 봇한테 전달
    # checkUserEvent는 screen_name으로 큐에 이벤트가 있는지 체크해서 없으면 None을 있으면 해당 이벤트 코드를 리턴함.
    # 이벤트가 없으면(리턴값이 None이면) 그냥 평범하게 대화하면 되는거고
    # 리턴값이 있으면 대화하면 안됨. 대화는 여기서 처리할것.
    def checkUserEvent(self,msg):
        for q in EventManagerCore.eventQue:
            # 해당 사용자가 하고있던 이벤트를 확인
            if(q.screen_name==msg.screen_name):
                # 발생한지 3시간이 지난 이벤트는 무효
                kst = datetime.now(timezone('Asia/Seoul'))

                if(q.time==None or kst==None or (kst-q.time).seconds/3600>=3):
                    #무효가 된 큐 폐기
                    EventManagerCore.eventQue.remove(q)
                    # None을 리턴하게되면 botTweeterClient쪽에서 대화 그대로 흘러감
                    # 무효 큐가 걸리면 해당 큐를 폐기하고 다음 큐 탐색을 계속 이어감
                    continue
                if(q.event_code=="EVENTLIKE1"):
                    # 대화는 밑의 이벤트 클래스에서 직접 처리해줘야함.
                    EventDir.HomeEvent.homeEventReLike(self.api,msg)
                    EventManagerCore.eventQue.remove(q)
                    return "EVENTLIKE1RE"
                elif(q.event_code=="EVENTSAD1"):
                    #TimeEvent.startTimeEventTwo(self.api,msg)
                    EventDir.HomeEvent.homeEventReSad(self.api, msg)
                    EventManagerCore.eventQue.remove(q)
                    return "EVENTSAD1RE"

                elif(q.event_code=="EVENTTWEETCODE03"):
                    # 대화는 밑의 이벤트 클래스에서 직접 처리해줘야함.
                    # 입력받은 word의 text를 json에 저장하고 답장하기
                    # value엔 word 데이터(word['word','cnt','text(값은 없을것임)'] 1개가 들어있음.
                    #def saveWordText(api,msg,value):
                    EventDir.WordEvent.saveWordText(self.api, msg, q.value)
                    EventManagerCore.eventQue.remove(q)
                    return "EVENTTWEETCODE03RE"

        #None을 리턴하게되면 botTweeterClient쪽에서 대화 그대로 흘러감
        #큐가 검색되지 않았거나 폐기된 큐만 있을경우 None이 리턴됨.
        return None