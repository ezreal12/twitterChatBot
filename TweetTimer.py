from pytz import timezone
from datetime import datetime

import threading
import botTweeterAPI
import random
import Massage
import TraceDataManager
import tweepy.error

class TweetTimer:
    # EVENTTWEETCODE01 = 매 시간 자동으로 하는 혼잣말
    # EVENTTWEETCODE02 = 매 시간 랜덤한 특정상대를 대상으로 하는 말
    # EVENTTWEETCODE03 = 매 시간 랜덤한 특정상대의 단어장(word json파일)을 뒤져서 해당 단어의 질문이나 말하기
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
        r=random.randrange(0, 4)
        # 한국시간으로 새벽일경우 무조건 혼잣말을 함   즉, r=0
        kst = datetime.now(timezone('Asia/Seoul'))
        if(kst!=None and kst.hour!=None):
            # 새벽 시간은 0시 ~ 7시로 , 혹은 밤 11시(23시)로 한정함
            if(kst.hour<=7 or kst.hour==23):
                print("--- hour limit --")
                r=0

        # r=0. 혼잣말 이벤트
        if(r==0):
            # 봇한테 EVENTTWEETCODE01 로 말을 걸면 EVENTTWEETCODE01 에 맞는 혼잣말 대사를 매칭해서 말한다.
            botTweeterAPI.sendBotAndTweetRespone(self.api, "EVENTTWEETCODE01")
        # r=1. 랜덤 상대 골라내기
        elif(r==1):
            # 팔로워 배열속에서 랜덤한 팔로워 screen_name 뽑아내기
            screen_name = random.choice(self.fllower)
            sendEventCodeForUser("EVENTTWEETCODE02",screen_name,self.api)
        # r=2,3. 2~3 단어 질문하기or 말하기 (정보파일이 없을경우 r=1일때의 처리 하면됨.
        else:
            # 팔로워 배열속에서 랜덤한 팔로워 screen_name 뽑아내기
            screen_name = random.choice(self.fllower)
            # 주의 : 이 타이머에서 이벤트를 생성하는법은 없음. 여기서는 json이 있나 확인만하고 봇한테 코드를 전달한다음
            # 봇이 코드에 맞는 대사를 하면 그 다음에 진짜 처리가 가능함.
            hasJsonFile = TraceDataManager.getWordJsonData(screen_name)
            # Word가 담긴 Json 데이터가 없거나 기타 이유로 못가져오면 그냥 평범하게 말걸기
            if(hasJsonFile==False):
                sendEventCodeForUser("EVENTTWEETCODE02",screen_name,self.api)
            else:
                #주의 : 이 타이머에서 이벤트를 생성하는법은 없음. 여기서는 json이 있나 확인만하고 봇한테 코드를 전달한다음
                #봇이 코드에 맞는 대사를 하면 그 다음에 진짜 처리가 가능함.
                # 랜덤으로 골라낸 screen_name 입력받고 EVENTTWEETCODE03 처리하기
                # EVENTTWEETCODE03 해당 유저의 word 파일 읽어서 랜덤으로 word를 골라낸뒤 질문하거나 말하기
                sendEventCodeForUser("EVENTTWEETCODE03",screen_name, self.api,self.eventManager)

# 랜덤으로 골라낸 유저의 screen_name 입력받고 EVENTTWEETCODE~~~ 처리하기
# 특정시간마다 이벤트 발생시 말을 걸어야할(태그해야할) 상대가 있는 이벤트 처리에 사용
# 말을 걸어야할 유저는 알아서 랜덤으로 뽑아내서 screen_name 가져오고 봇한테 전달할 이벤트 코드 입력하면됨.
# eventManager = "봇이 먼저 말했는데" 그 자체가 이벤트로 추가될 경우 필요함
# 예 : 봇이 모르는 어떤 단어를 질문하고 답변을 기다릴때 이벤트 발생
def sendEventCodeForUser(eventCode,screen_name,api,eventManager=None):
    try:
        # 고른 랜덤상대의 상세한 정보 가져오기
        user = api.get_user(screen_name)
    except tweepy.error.TweepError:
        print("이벤트 에러 발생 !! 해당 유저 정보 없음 : " + screen_name)
        return

    if (user == None):
        print("해당 유저 정보 없음 : "+screen_name)
        return
    # createEventMessage(id,screen_name,name,code):
    time_msg = Massage.createEventMessage(user.id, screen_name, user.name, eventCode)

    # sendBotAndTweetRespone(api,text,msg=None,eventManager=None)
    if(eventManager==None):
        botTweeterAPI.sendBotAndTweetRespone(api, eventCode, time_msg)
    else:
        botTweeterAPI.sendBotAndTweetRespone(api, eventCode,time_msg,eventManager)
