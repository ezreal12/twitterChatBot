# Simple chat client to communicate with chat script server
# Not very efficient, since it uses a thread per socket model,
# If servicing a large number of clients, twisted may be a better fit

from optparse import OptionParser
import socket
import sys
import tweepy
import TweetParser

# 트윗 전송하기 msg = 트윗에 담을 메시지
#msg = 트윗관련 정보
# 리턴으로 봇의 응답을 담음
# 1. 메시지가 null이 아닌지 검사한다.
# 2. 메시지가 null이 아니면 botTweeterAPI를 통해 소켓 통신으로 봇 서버에 메시지를 전달한다.
# 3. 전달한 메시지의 대한 답장을 가져온다.
# 4. 가져온 답장을 트위터에 그대로 적는다.
#+ 트윗을 보낸 사람의 ID 정보가 있으면 앞에 태그해서 트위터에 적는다. ex) @screen_name 트윗내용
# 스케쥴러 등에 의해 호출됬는데 태그할 대상이 따로없는경우(혼잣말인경우) msg가 None이다
# msg가 있는경우 => 태그를 받을 대상이 있다는것.
# (중요) eventManager 가 있는경우 => (반드시) 유저가 이벤트가 없는 상태에서 말을해 이벤트가 발생할 가능성이 있는대화인경우.
# 봇한테 보내는 메시지를 msg.text로 찾으려고 들지말것.
def sendBotAndTweetRespone(api,text,msg=None,eventManager=None):
    if text != "null":
        # 주의 : 임시로 포트번호 1023으로 바꿨음
        result = sendAndReceiveChatScriptMsg("Siu", "Sensiki", text, '127.0.0.1', 1023)
        # 이벤트 매니저가 파서에서 쓰이는 이유 : 봇이 뱉어낸 이벤트코드의 처리를 위해.
        if(msg!=None and eventManager!=None):
            result = TweetParser.parseBotScriptProtocol(result,name=msg.name,eventManager=eventManager,screen_name=msg.screen_name)
        elif(msg!=None):
            result = TweetParser.parseBotScriptProtocol(result, name=msg.name)
        else:
            result = TweetParser.parseBotScriptProtocol(result)

        print("send = {}".format(text))
        print("result = {}".format(result))
        # + 트윗을 보낸 사람의 ID 정보가 있으면 앞에 태그해서 트위터에 적는다.
        if (msg!=None):
            result="@"+msg.screen_name+" "+result
        updateStatusOnWrapper(api,result)
        return result
    else:
        print("---------------------!! Error !! text is NULL -------------------")
        return "null"


# isRespone : 트윗을 지우고 답장 트윗을 보낼지 말지에 대한 설정 True이면 삭제 후 보고트윗을 보냄
# 에러로 인한 처리가 아닌 사용자 명령으로 삭제처리를 했을때 주로 보고함
def removeAllTweet(api,isRespone=False,msg=None):
    for status in tweepy.Cursor(api.user_timeline).items():
        try:
            api.destroy_status(status.id)
            # isRespone이 True일시 삭제 완료 텍스트를 봇한테 받아와서 트윗작성함
            if isRespone:
                # 봇한테 CODET01로 말을 걸면 CODET01에 맞는 대사를 매칭해서 말한다.
                if(msg!=None):
                    sendBotAndTweetRespone(api, "CODET01",msg)
                else :
                    sendBotAndTweetRespone(api, "CODET01")
        except:
            pass

# 트윗 전송시 사용하는 Wrapper 함수
# 모든 트윗 전송시에는 반드시 이 함수를 거칠것 (디버깅 편의 및 버그방지)
# 트윗 전송 및 에러처리 까지만 할것
# text = 트윗으로 작성할 메시지
def updateStatusOnWrapper(api,text):
    try:
        api.update_status(text)
    # code 170 : Missing required parameter: status 에러가 아직 미해결
    except tweepy.TweepError as error:
        if error.api_code == 187:
            removeAllTweet(api)
            updateStatusOnWrapper(api,text)
            print(error)
        else:
            updateStatusOnWrapper(api, error)
            print("updateStatusOnWrapper tweepy.TweepError : ")
            print(error)
    except Exception as e:
        print("---------------------!! Error !! -------------------")
        print(e)

def sendAndReceiveChatScriptMsg(userName,botName,msgText, server='127.0.0.1', port=1024, timeout=10):
    msg = u'%s\u0000%s\u0000%s\u0000' % (userName, botName, msgText)
    msg = str.encode(msg)
    resp = sendAndReceiveChatScript(msg, server=server, port=port)
    errText = "null"

    if resp is None:
        print("-- ! Error communicating with Chat Server !--")
        return errText
    else:
        return resp


def sendAndReceiveChatScript(msgToSend, server='127.0.0.1', port=1024, timeout=10):
    try:
        # Connect, send, receive and close socket. Connections are not persistent
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)  # timeout in secs
        s.connect((server, port))
        s.sendall(msgToSend)
        msg = ''
        while True:
            chunk = s.recv(1024)
            if chunk == b'':
                break
            msg = msg + chunk.decode("utf-8")
        s.close()
        return msg
    except:
        return None


if __name__ == '__main__':
    server = "127.0.0.1"
    port = 1024
    botname = ""

    # Setup the command line arguments.
    optp = OptionParser()

    # user name to login to chat script as
    optp.add_option("-u", dest="user", help="user id, required")
    # botname
    optp.add_option("-b", dest="botname", help="which bot to talk to, if not specified, will use default bot")
    # server
    optp.add_option("-s", dest="server", help="chat server host name (default is " + str(server) + ")")
    # port
    optp.add_option("-p", dest="port", help="chat server listen port (default is " + str(port) + ")")

    opts, args = optp.parse_args()

    if opts.user is None:
        optp.print_help()
        sys.exit(1)
    user = opts.user

    if opts.botname is not None:
        botname = opts.botname

    if opts.server is not None:
        server = opts.server

    if opts.port is not None:
        port = int(opts.port)

    print("Hi " + user + ", enter ':quit' to end this session")

    while True:
        s = input("[" + user + "]" + ">: ").lower().strip()
        if s == ':quit':
            break

        # Ensure empty strings are padded with atleast one space before sending to the
        # server, as per the required protocol
        if s == "":
            s = " "
        # Send this to the server and print the response
        # Put in null terminations as required
        msg = u'%s\u0000%s\u0000%s\u0000' % (user, botname, s)
        msg = str.encode(msg)
        resp = sendAndReceiveChatScript(msg, server=server, port=port)
        if resp is None:
            print("Error communicating with Chat Server")
            break  # Stop on any error
        else:
            print("[Bot]: " + resp)
