import threading
import botTweeterAPI

class TweetTimer:
    def __init__(self,api,timeSec):
        self.api = api
        self.timeSec = timeSec
        self.keyword = "EVENTTWEETCODE01"
        #print("트윗 타이머 시작 keyword = {}".format(self.keyword))
        self.Task()

    def Task(self):
        #print ("트윗 타이머 동작중 keyword = {}".format(self.keyword))
        self.sendMsg()
        threading.Timer(self.timeSec,self.Task).start()

    def sendMsg(self):
        # 봇한테 EVENTTWEETCODE01 로 말을 걸면 EVENTTWEETCODE01 에 맞는 대사를 매칭해서 말한다.
        botTweeterAPI.sendBotAndTweetRespone(self.api,self.keyword)