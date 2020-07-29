import MeCab
mecabTagger = MeCab.Tagger()
# text를 입력받고 형태소 분석한 뒤 문자 배열로 리턴하기
def parseToArrStr(text):
    node = mecabTagger.parseToNode(text)
    result = []
    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        if (hinshi != "BOS/EOS"):
            result.append(word)
        # print(word+": "+hinshi)
        node = node.next
    return result


# text를 입력받고 형태소 분석한 뒤 문자 배열로 리턴하기
# 형태소중에 "명사"만 리턴함 (NNP,NNG)
# 청량리역: NNP 진심: NNG
# textLimit = 해당 변수값 이하의 길이를 가진 word는 입력받지 않음.
# 즉, textLimit가 1이면 한글자짜리 word는 기록하지않음.
def parseToArrStrNN(text,textLimit=1):
    node = mecabTagger.parseToNode(text)
    result = []
    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        if (hinshi != "BOS/EOS"):
            if(hinshi == "NNP" or hinshi == "NNG"):
                if(len(word)>textLimit):
                    result.append(word)
        # print(word+": "+hinshi)
        node = node.next
    return result