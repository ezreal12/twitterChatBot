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
    screenName = TweetParser.parseTweetData(data, "screen_name")
    id = TweetParser.parseTweetData(data, "id")
    name = TweetParser.parseTweetData(data, "name")

    msg = Massage()
    msg.id = id;
    msg.screen_name = screenName;
    msg.text = text;
    msg.name = name;
    return msg
