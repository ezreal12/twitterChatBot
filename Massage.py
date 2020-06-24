import TweetParser

class Massage:
    id=0
    name=None
    screen_name=None
    text=None
    isAdmin=False
    # 호감도
    HP=0
    # 첫번째 스크립트를 봤는가?
    isFirstScript = False
    # 두번째 스크립트를 봤는가?
    isSecondScript=False

# 트위터에서 받아온 data를 기반으로 메시지 객체 만들어내기
def parseMassage(data):
    text = TweetParser.parseTweetData(data, "text")
    # 해시태그는 지워줌.
    # 이 해시태그는 botTweeterClient의 메인함수에서도 똑같이 적용해줘야함.
    text = text.replace("#CODE_NUM_1000","")
    screenName = TweetParser.parseTweetData(data, "screen_name")
    id = TweetParser.parseTweetData(data, "id")
    name = TweetParser.parseTweetData(data, "name")
    # 주의 : 트위터 기호같은게 닉네임, 텍스트에 포함될수있음으로
    # 트위터 기호와 호환되는 utf-16으로 인코딩
    name = name.encode('utf-16','surrogatepass').decode('utf-16')
    text = text.encode('utf-16','surrogatepass').decode('utf-16')
    
    msg = Massage()
    msg.id = id
    msg.screen_name = screenName
    msg.text = text
    msg.name = name
    return msg


# screen_name과 코드를 입력받고 해당 코드와 screen_name으로 된 가짜 Message 객체를 만들어냄
# Message를 "어떤 사람이 봇한테 한 말과 그 정보를 담는 객체"로 인식할것
# 그렇다면 여기서 만드는 Message는 스케쥴러가 봇한테 보내는 메시지가 되는것.
def createEventMessage(id,screen_name,name,code):
    msg = Massage()
    msg.id=id
    msg.screen_name = screen_name
    msg.text=code
    msg.name=name
    return msg