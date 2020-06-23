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
    msg.id = id;
    msg.screen_name = screenName;
    msg.text = text;
    msg.name = name;
    return msg
