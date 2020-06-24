import threading
import botTweeterAPI
import random
import Massage



class TweetTimer:
    # EVENTTWEETCODE01 = 매 시간 자동으로 하는 혼잣말
    # EVENTTWEETCODE02 = 매 시간 랜덤한 특정상대를 대상으로 하는 말
    # fllower = 권한이 수락된 팔로워들 목록을 보관하는 배열
    # eventManager = 조건이 맞을때 이벤트를 추가해줄 eventManager
    def __init__(self,api,timeSec,eventManager,fllower):
        self.api = api
        self.timeSec = timeSec
        self.eventManager = eventManager
        self.fllower = fllower
        self.Task()

    def Task(self):
        self.startTimerEvent()
        threading.Timer(self.timeSec,self.Task).start()

    def startTimerEvent(self):
        r=random.randrange(0, 2)
        #r==0
        #TODO
        if(r==0):
            # 50퍼센트의 확률로 혼잣말
            # 봇한테 EVENTTWEETCODE01 로 말을 걸면 EVENTTWEETCODE01 에 맞는 혼잣말 대사를 매칭해서 말한다.
            botTweeterAPI.sendBotAndTweetRespone(self.api, "EVENTTWEETCODE01")
        # 1. 랜덤 상대 골라내기 , 2. 골라낸 상대에게 보고싶다고 말할지 질문을 할지 랜덤고르기 ,
        else:
            # 50퍼센트의 확률로 랜덤상대한테 말걸기
            screen_name = random.choice(self.fllower)
            time_msg = Massage.createEventMessage(screen_name,"EVENTTWEETCODE02")
            botTweeterAPI.sendBotAndTweetRespone(self.api, "EVENTTWEETCODE02",time_msg)
            #addEvent(self,screen_name, event_code, value=None):
            #상대한테 말을 걸고 이벤트 추가하기
            #self.eventManager.addEvent()

        