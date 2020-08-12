# 채팅할때 필요한 데이터를 미리 set 해놓고 보관하는 클래스
class ChatData:
    def __init__(self,tok_path,model,vocab,tok,kogptqa,sent_tokens):
        self.tok_path=tok_path
        self.model = model
        self.vocab = vocab
        self.tok = tok
        self.kogptqa = kogptqa
        self.sent_tokens = sent_tokens
