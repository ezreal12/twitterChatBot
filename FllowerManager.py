# follower.txt에 저장된 팔로우들 목록을 list로 읽어들여서 리턴함.
# 팔로워 1명의 형식은 @ 없이 이름만 있어야함 @Sensiki(X) Sensiki(O) 이렇게 한줄
def initFllowers():
    f = open('follower.txt', 'r')
    result =[]
    l = f.readlines()
    for d in l:
        result.append(d.replace('\n',''))
    f.close()
    return result
