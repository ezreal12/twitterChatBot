import json

from collections import OrderedDict


def saveJson(data,fileName):
    with open(fileName, 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t")

def listParseToJson(list):
    data = OrderedDict()
    i=0
    for l in list:
        i=i+1
        data[l]=i
    return data

def jsonPrintTest(fileName):
    with open(fileName, 'r') as f:
        json_data = json.load(f)
    print(json_data)
    return json_data


if __name__ == '__main__':
    data = '{"created_at":"Thu Sep 26 04:53:06 +0000 2019","id":1177083652120825856,"id_str":"1177083652120825856","text":"\ud14c\uc2a4\ud2b8\ud558\ub2e4 \ud558\ub8e8\uc885\uc77c \ub2e4\uac00\uac2f\ub2e4","source":"\u003ca href=\"https:\/\/mobile.twitter.com\" rel=\"nofollow\"\u003eTwitter Web App\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":937835196568571904,"id_str":"937835196568571904","name":"\uc2dc\uc6b0\ucd08\ub144\uc0dd","screen_name":"Cyphers_SiuKim","location":null,"url":null,"description":"\uc0ac\uc774\ud37c\uc988 \ub2c9\ub124\uc784 \uc2dc\uc6b0\ucd08\ub144\uc0dd 53\uae09 \uc131\uc778\ub0a8\uc131\n\ub9c8\ube44\ub178\uae30 \uacc4\uc815 @Mabinogi_SiuKim","translator_type":"none","protected":false,"verified":false,"followers_count":23,"friends_count":110,"listed_count":0,"favourites_count":6310,"statuses_count":9599,"created_at":"Tue Dec 05 00:05:09 +0000 2017","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"F5F8FA","profile_background_image_url":"","profile_background_image_url_https":"","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/1176355093391663105\/NvyK8Qdl_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/1176355093391663105\/NvyK8Qdl_normal.jpg","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"ko","timestamp_ms":"1569473586479"}'
    result = json.loads(data)
    print(data)

else:
    file_data = OrderedDict()
    file_data["name"] = "COMPUTER"
    file_data["language"] = "kor"
    file_data["words"] = {'ram': '램', 'process': '프로세스', 'processor': '프로세서', 'CPU': '씨피유'}
    file_data["number"] = 4

    print(json.dumps(file_data, ensure_ascii=False, indent="\t"))

    # json 파일로 저장

    with open('test.json', 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, indent="\t")

    # 저장한 파일 출력하기

    with open('test.json', 'r') as f:
        json_data = json.load(f)

    print(json_data)

