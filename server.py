import socket
import threading
import pickle

groups = {}

class Group:
	def __init__(self,admin,client):
		self.admin = admin
		self.clients = {}
		self.offlineMessages = {}
		self.allMembers = set()
		self.onlineMembers = set()
		self.joinRequests = set()

		self.clients[admin] = client
		self.allMembers.add(admin)
		self.onlineMembers.add(admin)

def pyconChat(client):
	while True:
		msg = client.recv(1024).decode("utf-8")
		if msg == "/viewRequests":
			client.send(b"/viewRequests")
			username = client.recv(1024).decode("utf-8")
			client.send(b"/sendGroupname")
			groupname = client.recv(1024).decode("utf-8")
			client.send(pickle.dumps(groups[groupname].joinRequests))

if __name__ == "__main__":
	ip = '127.0.0.1'
	port = 8000
	listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listenSocket.bind((ip,port))
	listenSocket.listen(10)
	print("PyconChat Server running")
	while True:
		client,_ = listenSocket.accept()
		username = client.recv(1024).decode("utf-8")
		client.send(b"/sendGroupname")
		groupname = client.recv(1024).decode("utf-8")
		if groupname in groups:
			if username in groups[groupname].allMembers:
				groups[groupname].onlineMembers.add(username)
				threading.Thread(target=pyconChat, args=(client,)).start()
				client.send(b"/ready")
			else:
				groups[groupname].joinRequests.add(username)
				client.send(b"/wait")
		else:
			groups[groupname] = Group(username,client)
			threading.Thread(target=pyconChat, args=(client,)).start()
			client.send(b"/adminReady")
			print("New group:",groupname,"| Admin:",username)