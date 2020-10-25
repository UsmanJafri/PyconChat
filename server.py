import socket
import sys

def handshake(client, groups):
	username = client.recv(1024).decode("utf-8")
	client.sendall(b"/sendGroupname")
	groupname = client.recv(1024).decode("utf-8")
	client.sendall(b"/sendPassword")
	password = client.recv(1024).decode("utf-8")

	if groupname in groups:
		if username in groups[groupname]["admins"]:
			if password == groups[groupname]["admins"][username]["password"]:
				client.sendall(b"Admin logged in successfully.")
			else:
				client.sendall(b"Incorrect password.")
		elif username in groups[groupname]["users"]:
			if password == groups[groupname]["users"][username]["password"]:
				client.sendall(b"User logged in successfully.")
			else:
				client.sendall(b"Incorrect password.")
		else:
			groups[groupname]["requests"][username] = { "password" : password}
			client.sendall(bytes("You are not a member of the group " + groupname + ". A request join request has been added, please wait for the admin's approval.", "utf-8"))
	else:
		groups[groupname] = { "admins" : {}, "users" : {}, "requests" : {}}
		groups[groupname]["admins"][username] = { "password" : password}
		client.sendall(bytes("New group " + groupname + " created. You are now an admin.", "utf-8"))

def main():
	if len(sys.argv) < 3:
		print("USAGE: python server.py <IP> <Port>")
		print("EXAMPLE: python server.py localhost 8000")
		return

	groups = {}
	listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listenSocket.bind((sys.argv[1], int(sys.argv[2])))
	listenSocket.listen(5)
	print("PyconChat Server running")

	while True:
		client, _ = listenSocket.accept()

		handshake(client, groups)
		

	client.close()
	listenSocket.close()

if __name__ == "__main__":
	main()