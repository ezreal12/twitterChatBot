# 이벤트 1개의 자료구조 클래스


class Event:
    # (@닉네임,CODERE_1,값)
    def __init__(self,screen_name,event_code,value=None):
        #@닉네임
        self.screen_name=screen_name
        #이벤트 코드 (CODERE_1 등)
        self.event_code=event_code
        # 이벤트 값 주의: None일수있음
        if(value!=None):
            self.value=value