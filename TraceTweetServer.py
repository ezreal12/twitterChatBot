from __future__ import absolute_import, print_function
from tweepy import OAuthHandler, Stream, StreamListener
import TweetParser
import tweepy
import time
import TraceDataManager
import TmPJsonTimer
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="C7LW1zGfBPdBEPuMZI8skPwKB"
consumer_secret="il2tiXlSztxy1Wyogx22eMIIr1ci8DTncHZEUQlVZgoUKP4K1n"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1104054737324859392-zXRx7ak34w4FuHILaBoJQ5YLEDzsTi"
access_token_secret="Km90CJMsp8NPaVnw2ecAKTlPywLtARC9HuYkr1fMpnV71"
follwers=['1263315003370688513','937835196568571904']

global api

# 입력받은 id_str을 확인해서 팔로워면 True 아니면 False 리턴
def isFollwerId(id_str):
    for f in follwers:
        if(f==id_str):
            return True
    return False

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    #RT 데이터
    #"text":"RT @dominika_walker: Now I’ve seen everything - two b...
    #1287760944148312065 : null -> 리트윗 해제시 id는 같은데 text가 null로 나옴
    # id를 확인해서 id가 다르면 RT임
    def on_data(self, data):
        data = TweetParser.encodeTweetData(data)
        data = data.encode('utf-16', 'surrogatepass').decode('utf-16')
        if data == "Err":
            print("------------------------ERROR on_data -------------------")
        elif api:
            parseText = TweetParser.parseTweetData(data, "text")
            screen_name = TweetParser.parseTweetData(data, "screen_name")
            id_str = TweetParser.parseTweetData(data, "id_str")

            # text 안에 RT와 골뱅이@가 포함된경우 리트윗으로간주하고 집계하지않음
            # 여기까지 온 리트윗의경우 팔로워가 자기자신의 트윗을 리트윗 혹은 다른 팔로워의 트윗을 리트윗했을 가능성이 크다.
            if(parseText.find("RT")>=0 and parseText.find("@")>=0):
                print("is RT" + id_str + " : " + parseText)
                return True
            # 모종의 이유로 text가 없거나 파싱하지 못한경우
            if(parseText=="null"):
                print("TEXT NULL!!!" + id_str)
                return True

            TraceDataManager.saveTweetTmp(parseText,screen_name)

        return True

    def on_error(self, status):
        print(status)

    def on_limit(self, status):
        #print("Rate Limit Exceeded, Sleep for 15 Mins")
        #time.sleep(15 * 60)
        # 예제에서는 15분을 권하지만 대충 2분만
        print("Rate Limit Exceeded, Sleep for 2 Mins")
        time.sleep(2 * 60)
        return True

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # 초단위 / 1*60*60 = 1시간
    timer = TmPJsonTimer.Timer(2*60*60)

    print("auth SET")
    stream = Stream(auth, l)
    print("Stream SET")
    stream.filter(follow=follwers)
    print("stream filter")