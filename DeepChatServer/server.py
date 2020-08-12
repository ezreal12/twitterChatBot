import socketserver
import sys


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("{} wrote:".format(self.client_address[0]))
        print (self.data.decode())
        # 영어의 소문자 데이터를 receive 하면 대문자로 변환해 send
        self.request.sendall(self.data)



if __name__ == "__main__":
    HOST, PORT = "localhost", 3000
    # 서버를 생성합니다. 호스트는 localhost, 포트 번호는 3000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print("waiting for connection...")
    # Ctrl - C 로 종료하기 전까지는 서버는 멈추지 않고 작동
    server.serve_forever()











