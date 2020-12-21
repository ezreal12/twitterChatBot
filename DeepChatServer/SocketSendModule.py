import socket

HOST, PORT = "13.125.213.62", 9082
BUF_SIZE = 1024
TIMEOUT_SEC = 15
RETRY_LIMIT = 2
# 메시지 보내고 답신 받아오기
def sendMessage(text):
    retryCnt = 0
    # 소켓을 생성 (SOCK_STREAM 은 TCP 소켓을 의미)
    while retryCnt<RETRY_LIMIT:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_SEC)
        try:
            # 서버에 연결하고 데이터를 전송
            sock.connect((HOST, PORT))
            sock.sendall(text.encode())
            # 데이터를 수신하고 소켓 연결을 닫음
            received = sock.recv(BUF_SIZE)
            received = received.decode()
            sock.close()
            return received
        except BaseException as e:
            print("Socket SEND ERROR -- !!!!")
            print(e)
            sock.close()
            retryCnt=retryCnt+1
    return None


if __name__ == "__main__":
    text = "밖에 공사하는게 너무 시끄러워"
    #text = '\n\n응!'
    msg = sendMessage(text)
    print(msg)