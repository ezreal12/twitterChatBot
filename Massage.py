import TweetParser

class Massage:
    id=0
    name=None
    screen_name=None
    text=None
    isAdmin=False

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
