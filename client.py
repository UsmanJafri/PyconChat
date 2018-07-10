import socket
import threading
import pickle

state = {}

def serverListen(serverSocket):
	while True:
		msg = serverSocket.recv(1024).decode("utf-8")
		if msg == "/viewRequests":
			serverSocket.send(bytes(state["username"],"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(state["groupname"],"utf-8"))
			response = serverSocket.recv(1024).decode("utf-8")
			if response == "/sendingData":
				serverSocket.send(b"/readyForData")
				data = pickle.loads(serverSocket.recv(1024))
				if data == set():
					print("No pending requests.")
				else:
					print("Pending Requests:")
					for element in data:
						print(element)
			else:
				print(response)
		elif msg == "/approveRequest":
			serverSocket.send(bytes(state["username"],"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(state["groupname"],"utf-8"))
			response = serverSocket.recv(1024).decode("utf-8")
			if response == "/proceed":
				state["inputMessage"] = False
				print("Please enter the username to approve: ")
				with state["inputCondition"]:
					state["inputCondition"].wait()
				state["inputMessage"] = True
				serverSocket.send(bytes(state["userInput"],"utf-8"))
				print(serverSocket.recv(1024).decode("utf-8"))
			else:
				print(response)
		elif msg == "/disconnect":
			serverSocket.send(bytes(state["username"],"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(state["groupname"],"utf-8"))
			state["alive"] = False
			break
		elif msg == "/messageSend":
			serverSocket.send(bytes(state["username"],"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(state["groupname"],"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(state["userInput"],"utf-8"))
			state["sendMessageLock"].release()
		else:
			print(msg)

def userInput(serverSocket):
	while True:
		state["sendMessageLock"].acquire()
		state["userInput"] = input()
		state["sendMessageLock"].release()
		with state["inputCondition"]:
			state["inputCondition"].notify()
		if state["userInput"] == "/1":
			serverSocket.send(b"/viewRequests")
		elif state["userInput"] == "/2":
			serverSocket.send(b"/approveRequest")
		elif state["userInput"] == "/3":
			serverSocket.send(b"/disconnect")
			break
		elif state["inputMessage"]:
			state["sendMessageLock"].acquire()
			serverSocket.send(b"/messageSend")

def waitUserInput(serverSocket):
	while not state["alive"]:
		state["userInput"] = input()
		if state["userInput"] == "/3" and not state["alive"]:
			serverSocket.send(b"/waitDisconnect")
			break
		elif state["userInput"] == "/2":
			break

def waitServerListen(serverSocket):
	while not state["alive"]:
		msg = serverSocket.recv(1024).decode("utf-8")
		if msg == "/accepted":
			state["alive"] = True
			print("Your join request has been approved. Press any key to begin chatting.")
			break
		elif msg == "/waitDisconnect":
			serverSocket.send(bytes(state["username"],"utf-8"))
			serverSocket.recv(1024)
			serverSocket.send(bytes(state["groupname"],"utf-8"))
			state["joinDisconnect"] = True
			break

if __name__ == "__main__":
	ip = '127.0.0.1'
	port = 8000
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.connect((ip,port))
	state["inputCondition"] = threading.Condition()
	state["sendMessageLock"] = threading.Lock()
	state["username"] = input("Welcome to PyconChat! Please enter your username: ")
	state["groupname"] = input("Please enter the name of the group: ")
	state["alive"] = False
	state["joinDisconnect"] = False
	state["inputMessage"] = True
	serverSocket.send(bytes(state["username"],"utf-8"))
	serverSocket.recv(1024)
	serverSocket.send(bytes(state["groupname"],"utf-8"))
	response = serverSocket.recv(1024).decode("utf-8")
	if response == "/adminReady":
		print("You have created the group",state["groupname"],"and are now an admin.")
		state["alive"] = True
	elif response == "/ready":
		print("You have joined the group",state["groupname"])
		state["alive"] = True
	elif response == "/wait":
		print("Your request to join the group is pending admin approval.")
	waitUserInputThread = threading.Thread(target=waitUserInput,args=(serverSocket,))
	waitServerListenThread = threading.Thread(target=waitServerListen,args=(serverSocket,))
	userInputThread = threading.Thread(target=userInput,args=(serverSocket,))
	serverListenThread = threading.Thread(target=serverListen,args=(serverSocket,))
	waitUserInputThread.start()
	waitServerListenThread.start()
	while True:
		if state["alive"] or state["joinDisconnect"]:
			break
	if state["alive"]:
		waitUserInputThread.join()
		waitServerListenThread.join()
		userInputThread.start()
		serverListenThread.start()
	while True:
		if state["joinDisconnect"]:
			serverSocket.shutdown(socket.SHUT_RDWR)
			serverSocket.close()
			waitUserInputThread.join()
			waitServerListenThread.join()
			print("Disconnected from PyconChat.")
			break
		elif not state["alive"]:
			serverSocket.shutdown(socket.SHUT_RDWR)
			serverSocket.close()
			userInputThread.join()
			serverListenThread.join()
			print("Disconnected from PyconChat.")
			break