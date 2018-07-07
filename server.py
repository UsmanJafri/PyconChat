import socket
import threading

def pyconChat(listenSocket):
	while True:
		client,_ = listenSocket.accept()
		msg = client.recv(1024).decode("utf-8")
		if msg == "/register":
			client.send(b"/sendUsername")
			username = client.recv(1024).decode("utf-8")
			client.send(b"/sendGroupname")
			groupname = client.recv(1024).decode("utf-8")


if __name__ == "__main__":
	ip = '127.0.0.1'
	port = 8000
	listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listenSocket.bind((ip,port))
	listenSocket.listen(10)
	print("PyconChat Server running")
	pyconChatThread = threading.Thread(target=pyconChat, args=(listenSocket,))
	pyconChatThread.start()