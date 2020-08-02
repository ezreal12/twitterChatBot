import threading
import TraceDataManager
#일정 시간마다 Tmp 파일들을 읽어들여 tmp가 아닌 json 파일로 바꿔주는 스케쥴러
# 1. 일정 시간이 된다.
# 2. tmp파일들을 전부 1개씩 읽는다.
# 3. tmp 파일에서 읽어온 word들중 cnt가 가장 높은거 5개만 가져온다.
# 4. 가져온 5개의 word를 tmp가 아닌 진짜 screen_name.json에 저장한다.
class Timer:
    def __init__(self,timeSec):
        # Tmp 전환은 스케쥴러의 두번째부터 실행가능하게끔
        # 즉 서버 켜지자마자 tmp 갱신하는짓은 안하게끔
        # isFirst는 최초실행시까지 True였다가 
        self.isFirst = True
        self.timeSec = timeSec
        self.Task()

    def Task(self):
        # 일정 시간마다 실행하고 싶은 내용을 아래 넣을것
        # 일정 시간마다 tmp 파일 체크해서 word의 json 파일로 바꿔주기
        # 두번째 실행부터 tmp 갱신
        print("-- checkTmpFiles Timer!!")
        if(self.isFirst==True):
            self.isFirst=False
        else:
            TraceDataManager.checkTmpFiles()
            
        threading.Timer(self.timeSec, self.Task).start()
        
        
