import socket
import threading

def serverListen(serverSocket):
	pass

def userInput(serverSocket):
	username = input("Welcome to PyconChat! Please enter your username: ")
	groupname = input("Please enter the name of the group: ")
	serverSocket.send(b"/register")
	serverSocket.recv(1024)
	serverSocket.send(bytes(username,"utf-8"))
	serverSocket.recv(1024)
	serverSocket.send(bytes(groupname,"utf-8"))

if __name__ == "__main__":
	ip = '127.0.0.1'
	port = 8000
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.connect((ip,port))
	serverListenThread = threading.Thread(target=serverListen,args=(serverSocket,))
	userInputThread = threading.Thread(target=userInput,args=(serverSocket,))
	serverListenThread.start()
	userInputThread.start()