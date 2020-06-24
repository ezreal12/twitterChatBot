import JsonTest

# follower.txt에 저장된 팔로우들 목록을 list로 읽어들여서 리턴함.
# 팔로워 1명의 형식은 @ 없이 이름만 있어야함 @Sensiki(X) Sensiki(O) 이렇게 한줄
def initFllowers():
    f = open('follower.txt', 'r',encoding='UTF8')
    l = f.readlines()
    f.close()
    return l

# follower.txt에 저장된 팔로우들 목록을 list로 읽어들여서 리턴함.
# 팔로워 1명의 형식은 @ 없이 이름만 있어야함 @Sensiki(X) Sensiki(O) 이렇게 한줄
def parseText(name):
    f = open(name, 'rt', encoding='UTF8')
    result =[]
    l = f.readlines()
    for d in l:
        result.append(d.replace('\n',''))
    f.close()
    return result

#checkFllower("Dev_test_siuKim")
list = parseText("char.txt")
print(list)

list = JsonTest.listParseToJson(list)
list["옌"]=9
list["유"]=25
list["안토네와"]=50
list["시호인"]=77
list["랜스"]=41
name="chat.json"
JsonTest.saveJson(list,name)
data=JsonTest.jsonPrintTest(name)
print("루안 옌 : {}".format(data["루안 옌"]))
print("루안 유 : {}".format(data["루안 유"]))
print("샤오옌 : {}".format(data["샤오옌"]))
print("앙투아네트: {}".format(data["앙투아네트"]))
print("시호인 린 : {}".format(data["시호인 린"]))
print("란스 : {}".format(data["란스"]))