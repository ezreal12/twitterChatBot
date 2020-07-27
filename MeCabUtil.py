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
def parseToArrStrNN(text):
    node = mecabTagger.parseToNode(text)
    result = []
    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        if (hinshi != "BOS/EOS"):
            if(hinshi == "NNP" or hinshi == "NNG"):
                result.append(word)
        # print(word+": "+hinshi)
        node = node.next
    return result