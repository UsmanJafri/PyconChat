import socket
import threading
import pickle

username = ""
groupname = ""

def serverListen(serverSocket):
	while True:
		msg = serverSocket.recv(1024).decode("utf-8")
		print(msg)
		if msg == "/viewRequests":
			serverSocket.send(bytes(username,"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(groupname,"utf-8"))
			print(pickle.loads(serverSocket.recv(1024)))

def userInput(serverSocket):
	while True:
		userInput = input()
		if userInput == "1":
			serverSocket.send(b"/viewRequests")

if __name__ == "__main__":
	ip = '127.0.0.1'
	port = 8000
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.connect((ip,port))
	username = input("Welcome to PyconChat! Please enter your username: ")
	groupname = input("Please enter the name of the group: ")
	userInputThread = threading.Thread(target=userInput,args=(serverSocket,))
	userInputThread.start()
	serverSocket.send(bytes(username,"utf-8"))
	serverSocket.recv(1024)
	serverSocket.send(bytes(groupname,"utf-8"))
	response = serverSocket.recv(1024).decode("utf-8")
	if response == "/adminReady":
		print("You have created the group",groupname,"and are now an admin.")
	elif response == "/ready":
		print("You have joined the group",groupname)
	elif response == "/wait":
		print("Your request to join the group is pending admin approval.")
		serverSocket.recv(1024)
		print("You have joined the group",groupname)
	serverListenThread = threading.Thread(target=serverListen,args=(serverSocket,))
	serverListenThread.start()