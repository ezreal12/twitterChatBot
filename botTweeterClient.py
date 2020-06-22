from __future__ import absolute_import, print_function
from tweepy import OAuthHandler, Stream, StreamListener
import tweepy
import TweetParser
import botTweeterAPI
import TweetTimer
import Massage
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


global api

# CODET01 = 최근 트윗 제거
# CODET02 = 관리자가 아닌데 명령해서 거절트윗
def controlTweet(tweetStatusMsg,screen_name):
    print ("controlTweet -------- tweetStatusMsg = {}".format(tweetStatusMsg))
    if tweetStatusMsg == "CODET02":
        # CODET02 맞는 대사를 매칭해서 말한다.
        botTweeterAPI.sendBotAndTweetRespone(api, "CODET02",screen_name)
    if tweetStatusMsg == "CODET01":
        botTweeterAPI.removeAllTweet(api,True)
        print("removeAllTweet")
        return "remove()"
    return ""
class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    #a = a.decode('cp949').encode('utf-8')
    #line = buf.read_line()
    #next_status_obj = buf.read_len(length)
    #            if self.running and next_status_obj:
    #            self._data(next_status_obj)
    # 데이터는 단순한 문자열이고 파싱이 필요함
    # 파싱  후 text를 뽑아내서 트위터에 써보기
    def on_data(self, data):
        data = TweetParser.encodeTweetData(data)
        if data == "Err":
            print ("------------------------ERROR on_data -------------------")
        elif api:
            # 전달된 데이터를 기반으로 관련 정보(ID,트윗 내용등) 뽑아내기
            msg = Massage.parseMassage(data)
            # 형태소 분석해서 메시지 치환하기
            msg.text=TweetParser.parseFromOkt(msg.text)
            # 관리자외의 사람은 : 명령과 트윗조작 명령을 내릴수없으며 트윗조작명령에 대해선 보고한다.
            # 트윗 보낸자가 관리자가 아닐경우 명령어 인식을 할수없다.
            if admin_screen_name == msg.screen_name:
                msg.isAdmin = True
            # 사용자가 보낸 text에서 트위터 조작에 관한 내용이 있는지 체크
            tweetStatusMsg = TweetParser.parseUserMsgForTweet(msg)

            # 조작에 관한 내용이 아니면 봇한테 전송
            if tweetStatusMsg == "null":
                botTweeterAPI.sendBotAndTweetRespone(api,msg.text,msg.screen_name)
            # 조작에 관한 내용이면 해당 프로세스 실행함
            else:
                controlTweet(tweetStatusMsg,msg.screen_name)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    print("auth SET")
    stream = Stream(auth, l)
    print("Stream SET")
    timer = TweetTimer.TweetTimer(api,600)
    # follow=["950212844385005570"] - 테스트 계정 / 937835196568571904 - 본계
    filtro = ['#CODE_NUM_1000']
    # 팔로우랑 필터가 동시에있으면 필터가안먹음
    stream.filter(track=filtro)
    #stream.filter()
    print("stream filter")
