from __future__ import absolute_import, print_function
from tweepy import OAuthHandler, Stream, StreamListener
from urllib3.exceptions import ProtocolError
import sys
import TweetParser
import tweepy
import time
import TraceDataManager
import TmPJsonTimer
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="48wXip49Ts8Voe6L1IMizy1ZS"
consumer_secret="rqz8REwXKPUF1KFtWzRFywlpDbFx7HD2PRaZoPPiucFY1c2k3Q"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1104054737324859392-5sUpE6jyoNNOW77fnKQqTP5bscBBtQ"
access_token_secret="zCZbavk6YlerTk449FCJQuORnKyk45jxvT5B4xVGBLZdb"

follwers=[
    '1296394912611540993','937835196568571904','1351746200551124993'
    '1231626376660172800','1365540947484758022','1245140249669328898','1251902603551637505',
    '1312591141208879104','1331283621097848836','1334686745179254784'
]

global api

# 스트리밍 시작하기
# 에러 발생시 에러를 무시하고 재시작 시킴
# 주의 startStreaming 다음으로 오는 명령은 실행되지않음.
def startStreaming(stream):
    while True:
        try:
            stream.filter(follow=follwers)
        except ProtocolError:
            # 반복 리스타트 실행시 500에러를 띄우며 기다리는데 이는 HTTP의 500 에러로 추정됨
            # HTTP 500 에러라면 트위터 서버나 트윗피와 관련된 어떤 서버가 터졌을시 이런 에러가 생김
            # 500에러를 리트라이하면서 기다린다면 다시 살아남
            print("------ERROR ProtocolError Trace Streaming ----")
            print(ProtocolError)
            print("------RESTART ProtocolError Trace Streaming  ----")
            continue
        except KeyboardInterrupt:
            print("------KeyboardInterrupt !! exit ----")
            sys.exit()
            return
        except BaseException:
            print("------ERROR BaseException Trace Streaming ----")
            print(BaseException)
            print("------RESTART BaseException Trace Streaming  ----")
            continue



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
            # "트윗 id의 str"이 아닌 "유저 id의 str"은 2번째에있음.
            id_str = TweetParser.parseTweetData(data, "id_str",2)

            # text 안에 RT와 골뱅이@가 포함된경우 리트윗으로간주하고 집계하지않음
            # 여기까지 온 리트윗의경우 팔로워가 자기자신의 트윗을 리트윗 혹은 다른 팔로워의 트윗을 리트윗했을 가능성이 크다.
            if(parseText.find("RT")>=0 and parseText.find("@")>=0):
                print("is RT" + id_str + " : " + parseText)
                return True
            #답글등으로 인해 "팔로워가 아닌" 답글에 엮인 유저의 데이터도 수집하는것을 방지하기 위하여
            #id_str을 통해 팔로워가 맞는지 검사하고 팔로워가 맞을경우에만 데이터 수집
            if (isFollwerId(id_str) == False):
                print("is NOT FOLLERT " + id_str + " : " + parseText)
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
    timer = TmPJsonTimer.Timer(24*60*60)

    print("auth SET")
    stream = Stream(auth, l)
    print("Stream SET")
    startStreaming(stream)