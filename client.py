import socket
import sys

def main():
	if len(sys.argv) < 3:
		print("USAGE: python client.py <Server IP> <Server Port>")
		print("EXAMPLE: python client.py localhost 8000")
		return

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect((sys.argv[1], int(sys.argv[2])))
	
	print("Welcome to PyconChat!")
	username = input("Please enter your username: ")
	groupname = input("Please enter the name of the group: ")
	password = input("Please enter your password: ")

	server.sendall(bytes(username, "utf-8"))
	server.recv(1024)
	server.sendall(bytes(groupname, "utf-8"))
	server.recv(1024)
	server.sendall(bytes(password, "utf-8"))
	message = server.recv(1024).decode("utf-8")
	print(message)
	server.close()

if __name__ == "__main__":
	main()