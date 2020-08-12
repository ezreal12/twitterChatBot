import socket
import sys

HOST, PORT = "localhost", 3000
message = "돈이 없어"
# 소켓을 생성 (SOCK_STREAM 은 TCP 소켓을 의미)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # 서버에 연결하고 데이터를 전송
    sock.connect((HOST, PORT))
    #sbuff = bytes(message, encoding='utf-8')
    #sock.send(sbuff)  # 메시지 송신 print('송신 {0}'.format(message))
    sock.sendall(message.encode())
    # 데이터를 수신하고 소켓 연결을 닫음
    received = sock.recv(1024)
    received = received.decode()
finally:
    sock.close()

print ("Sent: {}".format(message))
print ("Received: {}".format(received))







