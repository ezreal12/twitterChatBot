#특정 유저의 이벤트 대화 흐름을 관리하는 매니저
# 통신 자료구조  = (@닉네임,CODERE_1,값)
import Event
import EventDir.TimeEvent as TimeEvent
class EventManagerCore:
    eventQue = []
    def __init__(self,api):
        self.api = api

    # 주의 : 1개의 screen_name에 2개 이상의 이벤트는 추가될수없음
    # 중복에 주의할것
    def addEvent(self,screen_name, event_code, value=None):
        if (value != None):
            event = Event(screen_name, event_code, value)
        else:
            event = Event(screen_name, event_code)
        EventManagerCore.eventQue.append(event)

    # 트윗 파서가 봇의 이벤트 코드를 발견하면 처리를 부탁하는 코드
    # 트윗 파서는 이벤트 코드를 잘라내지 않고 이벤트 코드 잘라내기를 매니저한테 부탁함.
    # 이벤트가 발생하는 상황 1. 봇이 이벤트 코드가 포함된 대사를 할때
    # 이벤트가 발생하는 상황 2. 스케쥴어에 의해 이벤트가 발생했을 때
    def parseEventCode(self,text):
        pass
    # 유저가 대사를 할땐 *반드시* 해당 유저가 이벤트를 진행중은 아니였는지 확인해야함
    # 만약 유저가 이벤트를 진행중이 아니였으면 일반 대화로 흘러감
    # 유저가 이벤트중이였으면 해당 이벤트에 맞는 "코드"를 봇한테 전달해야함.
    # EVENT_TIME_1 : 스케쥴러에의한 랜덤 이벤트중 (시간 확인) 오늘 많이 힘들었어?
    # EVENT_TIME_2 : 스케쥴러에의한 랜덤 이벤트중 사람은 꿈을꾼다는데 너는 무슨 꿈을꿔?
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
                if(q.event_code=="EVENT_TIME_1"):
                    TimeEvent.startTimeEventOne(self.api,msg)
                    EventManagerCore.eventQue.remove(q)
                    return "EVENT_TIME_1"
                elif(q.event_code=="EVENT_TIME_2"):
                    TimeEvent.startTimeEventTwo(self.api,msg)
                    EventManagerCore.eventQue.remove(q)
                    return "EVENT_TIME_2"
        return None