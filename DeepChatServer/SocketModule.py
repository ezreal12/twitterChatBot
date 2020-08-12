import socket
# 통신 정보 설정
# 빈값을 넣으면 IP 상관없이 모든 인터페이스와 연결
IP = ''
PORT = 3000
SIZE = 1024
ADDR = (IP, PORT)
TIMEOUT_SEC = 15
RETRY_LIMIT = 2


# 답장 보내기
def sendReply(client_socket, reple):
    retryCnt = 0
    client_socket.settimeout(TIMEOUT_SEC)

    while retryCnt < RETRY_LIMIT:
        try:
            client_socket.sendall(reple.encode())  # 클라이언트에게 응답
            client_socket.close()  # 클라이언트 소켓 종료
            return 
        except BaseException as e:
            print("sendReply ERROR --- !!!")
            print(e)
            retryCnt = retryCnt + 1
    # 메시지를 성공적으로 보내지 못해도 리트라이가 끝나면 소켓 닫기
    client_socket.close()

# 챗봇 채팅에 준비한 사전데이터 chatData
def openSocketServer(model):
    # 서버 소켓 설정
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(ADDR)  # 주소 바인딩
        server_socket.listen()  # 클라이언트의 요청을 받을 준비

        # 무한루프 진입
        while True:
            client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
            msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
            # -- 주의 !! 클라이언트 쪽에선 반드시 메시지를 encode 해서 보내고 서버쪽에선 반드시 decode 해서읽는다.
            # 이는 서버가 클라이언트한테 답장을 보낼때도 동일하다.
            msg = msg.decode()
            print("[{}] message : {}".format(client_addr, msg))  # 클라이언트가 보낸 메시지 출력

            reple = model.getReply(msg)

            if(reple==None):
                reple="None"

            sendReply(client_socket,reple)
