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