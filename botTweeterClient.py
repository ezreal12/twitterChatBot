from __future__ import absolute_import, print_function
from tweepy import OAuthHandler, Stream, StreamListener
from urllib3.exceptions import ProtocolError
import tweepy
import TweetParser
import botTweeterAPI
import TweetTimer
import Massage
import FllowerManager
import EventManager
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="C7LW1zGfBPdBEPuMZI8skPwKB"
consumer_secret="il2tiXlSztxy1Wyogx22eMIIr1ci8DTncHZEUQlVZgoUKP4K1n"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1104054737324859392-zXRx7ak34w4FuHILaBoJQ5YLEDzsTi"
access_token_secret="Km90CJMsp8NPaVnw2ecAKTlPywLtARC9HuYkr1fMpnV71"

#관리자 트위터 ID
admin_screen_name = "Dev_test_siuKim"

## !-- tweepy.error.TweepError: [{'code': 187, 'message': 'Status is a duplicate.'}]
# 위에 대한 대처를 할것 -> 에러 발생시 특정 트윗을 지우던가 싹다 날리던가 하자

# 트위터 API 객체
global api
# 팔로워 목록을 리스트로 보관하는 객체
# FllowerManager에서 반드시 init을 호출해야함
global fllower
# 1개만 존재하는 이벤트 관리자
# 유저의 screen_name으로 이벤트를 관리함.
global eventManager

# 리스트에 screen_name이 등록된 유저만 이용 가능
# 등록된 유저면 True 아닐경우 False 리턴
def checkFllower(screen_name):
    for f in fllower:
        if(f==screen_name):
            return True

    return False
# Message 객체를 입력받아서 해당 객체로 메시지 전달하는 처리하기.
def sendMsg(msg):
    # 형태소 분석해서 메시지 치환하기
    msg.text = TweetParser.parseFromOkt(msg.text)
    # 관리자외의 사람은 : 명령과 트윗조작 명령을 내릴수없으며 트윗조작명령에 대해선 보고한다.
    # 트윗 보낸자가 관리자가 아닐경우 명령어 인식을 할수없다.
    if admin_screen_name == msg.screen_name:
        msg.isAdmin = True
    # 사용자가 보낸 text에서 트위터 조작에 관한 내용이 있는지 체크
    tweetStatusMsg = TweetParser.parseUserMsgForTweet(msg)

    # 조작에 관한 내용이 아니면 봇한테 전송
    if tweetStatusMsg == "null":
        botTweeterAPI.sendBotAndTweetRespone(api, msg.text, msg,eventManager)
    # 조작에 관한 내용이면 해당 프로세스 실행함
    else:
        controlTweet(tweetStatusMsg, msg)

# 스트리밍 시작하기
# 에러 발생시 에러를 무시하고 재시작 시킴
# 주의 startStreaming 다음으로 오는 명령은 실행되지않음.
def startStreaming(stream,filtro):
    while True:
        try:
            stream.filter(track=filtro)
        except ProtocolError:
            # 반복 리스타트 실행시 500에러를 띄우며 기다리는데 이는 HTTP의 500 에러로 추정됨
            # HTTP 500 에러라면 트위터 서버나 트윗피와 관련된 어떤 서버가 터졌을시 이런 에러가 생김
            # 500에러를 리트라이하면서 기다린다면 다시 살아남
            print("------ERROR startStreaming ----")
            print(ProtocolError)
            print("------RESTART startStreaming  ----")
            continue
        except BaseException:
            print("------ERROR startStreaming ----")
            print(BaseException)
            print("------RESTART startStreaming  ----")
            continue

# CODET01 = 최근 트윗 제거
# CODET02 = 관리자가 아닌데 명령해서 거절트윗
def controlTweet(tweetStatusMsg,msg):
    print ("controlTweet -------- tweetStatusMsg = {}".format(tweetStatusMsg))
    if tweetStatusMsg == "CODET02":
        # CODET02 맞는 대사를 매칭해서 말한다.
        botTweeterAPI.sendBotAndTweetRespone(api, "CODET02",msg)
    if tweetStatusMsg == "CODET01":
        botTweeterAPI.removeAllTweet(api,True)
        print("removeAllTweet")
        return "remove()"
    return ""
class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    # 데이터는 단순한 문자열이고 파싱이 필요함
    # 파싱  후 text를 뽑아내서 트위터에 써보기
    # 트윗을 검색했을때 콜백함수 여기가 메인임.
    def on_data(self, data):
        data = TweetParser.encodeTweetData(data)
        if data == "Err":
            print ("------------------------ERROR on_data -------------------")
        elif api:
            # 전달된 데이터를 기반으로 관련 정보(ID,트윗 내용등) 뽑아내기
            msg = Massage.parseMassage(data)
            # 팔로워가 아닌경우 메시지 처리 안함
            if(checkFllower(msg.screen_name)==False):
                print("NOT FLLOWER : "+msg.screen_name)
                return True
            # 해당 사용자가 이벤트 진행중이 아니였으면 대화계속 진행함.
            # 이벤트 진행중이였을때 대화는 EventManager가 알아서함.
            # checkUserEvent 리턴값이 None이면 대화 하던중이였음.
            if(eventManager.checkUserEvent(msg)!=None):
                return True

            sendMsg(msg)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #아래 내용들은 반드시 호출해야함
    fllower = FllowerManager.initFllowers()
    api = tweepy.API(auth)
    eventManager = EventManager.EventManagerCore(api)
    print("auth SET")
    stream = Stream(auth, l)
    print("Stream SET")

    timer = TweetTimer.TweetTimer(api,1*60*60,eventManager,fllower)

    # follow=["950212844385005570"] - 테스트 계정 / 937835196568571904 - 본계
    filtro = ['#CODE_NUM_1000']
    # 팔로우랑 필터가 동시에있으면 필터가안먹음
    # 주의 startStreaming 다음으로 오는 명령은 실행되지않음.
    startStreaming(stream,filtro)
    #stream.filter()
    print("stream filter")
