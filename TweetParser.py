def encodeTweetData(data):
    try:
        data = data.encode('utf-8')
        data = data.decode('unicode_escape')
    except:
        return "Err"

    return data

# 프로토콜에 쓰여진대로 봇의 특수문자를 처리하기위한 함수
# 트윗 조작 후 처리 프로토콜 : 트위터의 조작 후 처리 보고를 표현하는 프로토콜
# 예 (안화 봇) : 트윗 CODET01 처리 완료 했다. -> 트윗 삭제 처리 완료 했다.
# CODES01 = (
# CODES02 = )
# CODET01 = 삭제 (트윗 조작 후 처리 프로토콜)
def parseBotScriptProtocol(data):
    data = data.replace("CODES01","(")
    data = data.replace("CODES02",")")
    data = data.replace("CODET01", "삭제")
    return data
# 사용자가 봇한테 건네는 메시지를 먼저 가져와서
# 트위터에 사용하는 특수 기능을 요구하는 내용인지 확인함
# 특수기능을 요구하는 내용이면 해당 코드를 리턴하고 아니면 null 리턴
# 특수기능의 처리 혹은 null 일때 처리는 호출부에서 알아서 할것
# CODET01 = 최근 트윗 제거
# CODET02 = 관리자가 아닌데 명령해서 거절트윗
def parseUserMsgForTweet(msg):
    # 트윗 보낸자가 관리자가 아닐경우 명령어 인식을 할수없다.
    removeCode1 = "트윗"
    removeCode2 = "지워"
    if removeCode1 in msg.text :
        if removeCode2 in msg.text:
            #트윗 / 지워가 다 있을경우 삭제 명령으로 취급
            # 관리자면 명령수행코드 리턴 아니면 거절코드 리턴
            if msg.isAdmin:
                return "CODET01"
            else:
                return "CODET02"
    return "null"
def parseTweetData(data,id):
    arr = data.split(',')
    formatId = '"' + id + '"'
    for i in arr:
        #print(i)
        arr2 = i.split(':')
        #['{"created_at"', '"Thu Sep 26 04', '53', '06 +0000 2019"']
        #['"text"', '"테스트하다 하루종일 다가갯다"']
        
        #print (arr2[0]+ ':' + arr2[1]) 내용 출력해서 보고싶으면 주석해제

        if arr2[0]==formatId:
            serchData = arr2[1]
            # 문자열 데이터에 들어있을 쌍따옴표 제거
            serchData = serchData.replace('"',"")
            # 문자열 데이터의 개행문자를 띄어쓰기 문자로 치환
            serchData = serchData.replace('\n', " ")
            return serchData

    return "null"

if __name__ == '__main__':

    data = '{"created_at":"Thu Sep 26 04:53:06 +0000 2019","id":1177083652120825856,"id_str":"1177083652120825856","text":"\ud14c\uc2a4\ud2b8\ud558\ub2e4 \ud558\ub8e8\uc885\uc77c \ub2e4\uac00\uac2f\ub2e4","source":"\u003ca href=\"https:\/\/mobile.twitter.com\" rel=\"nofollow\"\u003eTwitter Web App\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":937835196568571904,"id_str":"937835196568571904","name":"\uc2dc\uc6b0\ucd08\ub144\uc0dd","screen_name":"Cyphers_SiuKim","location":null,"url":null,"description":"\uc0ac\uc774\ud37c\uc988 \ub2c9\ub124\uc784 \uc2dc\uc6b0\ucd08\ub144\uc0dd 53\uae09 \uc131\uc778\ub0a8\uc131\n\ub9c8\ube44\ub178\uae30 \uacc4\uc815 @Mabinogi_SiuKim","translator_type":"none","protected":false,"verified":false,"followers_count":23,"friends_count":110,"listed_count":0,"favourites_count":6310,"statuses_count":9599,"created_at":"Tue Dec 05 00:05:09 +0000 2017","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"F5F8FA","profile_background_image_url":"","profile_background_image_url_https":"","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/1176355093391663105\/NvyK8Qdl_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/1176355093391663105\/NvyK8Qdl_normal.jpg","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"ko","timestamp_ms":"1569473586479"}"'


    result = parseTweetData(data,"text")

    print ("--------------------- result !! = {}".format(result))







