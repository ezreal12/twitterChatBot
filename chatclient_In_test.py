# Simple chat client to communicate with chat script server
# Not very efficient, since it uses a thread per socket model,
# If servicing a large number of clients, twisted may be a better fit


import socket

import TweetParser

def sendAndReceiveChatScript(msgToSend, server='127.0.0.1', port=1023, timeout=10):
    try:
        # Connect, send, receive and close socket. Connections are not persistent
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)  # timeout in secs
        s.connect((server, port))
        s.sendall(msgToSend)
        msg = ''
        while True:
            chunk = s.recv(1024)
            if chunk == b'':
                break
            msg = msg + chunk.decode("utf-8")
        s.close()
        return msg
    except:
        return None


if __name__ == '__main__':
    server = "127.0.0.1"
    port = 1023
    botname = "Zepi"
    user ='Siu'


    print("Hi " + user + ", enter ':quit' to end this session")

    while True:
        s = input("[" + user + "]" + ">: ").lower().strip()
        if s == ':quit':
            break

        # Ensure empty strings are padded with atleast one space before sending to the
        # server, as per the required protocol
        if s == "":
            s = " "
        # Send this to the server and print the response
        # Put in null terminations as required
        #s = TweetParser.encodeTweetData(s)
        print ("s = {}".format(s))
        msg = u'%s\u0000%s\u0000%s\u0000' % (user, botname, s)
        msg = str.encode(msg)
        resp = sendAndReceiveChatScript(msg, server=server, port=port)
        if resp is None:
            print("Error communicating with Chat Server")
            break  # Stop on any error
        else:
            title = "[{}] : ".format(botname)
            print(title + resp)
