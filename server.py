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

	def disconnect(self,username):
		self.onlineMembers.remove(username)
		del self.clients[username]
	
	def connect(self,username,client):
		self.onlineMembers.add(username)
		self.clients[username] = client

def pyconChat(client):
	while True:
		msg = client.recv(1024).decode("utf-8")
		if msg == "/viewRequests":
			client.send(b"/viewRequests")
			username = client.recv(1024).decode("utf-8")
			client.send(b"/sendGroupname")
			groupname = client.recv(1024).decode("utf-8")
			if username == groups[groupname].admin:
				client.send(b"/sendingData")
				client.recv(1024)
				client.send(pickle.dumps(groups[groupname].joinRequests))
			else:
				client.send(b"You're not an admin.")
		elif msg == "/approveRequest":
			client.send(b"/approveRequest")
			username = client.recv(1024).decode("utf-8")
			client.send(b"/sendGroupname")
			groupname = client.recv(1024).decode("utf-8")
			if username == groups[groupname].admin:
				client.send(b"/proceed")
				username = client.recv(1024).decode("utf-8")
				if username in groups[groupname].joinRequests:
					groups[groupname].joinRequests.remove(username)
					groups[groupname].allMembers.add(username)
					print("Member Approved:",username,"| Group:",groupname)
					client.send(b"User has been added to the group.")
				else:
					client.send(b"The user has not requested to join.")
			else:
				client.send(b"You're not an admin.")
		elif msg == "/disconnect":
			client.send(b"/disconnect")
			username = client.recv(1024).decode("utf-8")
			client.send(b"/sendGroupname")
			groupname = client.recv(1024).decode("utf-8")
			groups[groupname].disconnect(username)

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
				groups[groupname].connect(username,client)
				threading.Thread(target=pyconChat, args=(client,)).start()
				client.send(b"/ready")
				print("User Connected:",username,"| Group:",groupname)
			else:
				groups[groupname].joinRequests.add(username)
				client.send(b"/wait")
				print("Join Request:",username,"| Group:",groupname)
		else:
			groups[groupname] = Group(username,client)
			threading.Thread(target=pyconChat, args=(client,)).start()
			client.send(b"/adminReady")
			print("New Group:",groupname,"| Admin:",username)