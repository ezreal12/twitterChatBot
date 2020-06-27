# 이벤트 1개의 자료구조 클래스


class EventClass:
    # (@닉네임,CODERE_1,값)
    def __init__(self,screen_name,event_code,time,value=None):
        #@닉네임
        self.screen_name=screen_name
        #이벤트 코드 (CODERE_1 등)
        self.event_code=event_code
        # 시간 -> kst 통째로 -> 3시간이 지난 이벤트는 무효가됨.
        self.time = time
        # 이벤트 값 주의: None일수있음
        if(value!=None):
            self.value=value