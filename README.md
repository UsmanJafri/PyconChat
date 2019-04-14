PyConChat
============================
***Py**thon **Con**sole **Chat** - A Python chat application featuring group conversations, file sharing and offline messaging.*

<img src="/sample.png">

## Requirements

1. Python 3

## Instructions (Client)

1. Open a terminal window in the directory containing *client.py* and run the following command:
> python client.py localhost 8000
2. Replace `localhost` with your IP and `8000` with a TCP port number of your choice.
3. A prompt to enter a username will appear. Enter a username and press enter.
4. Next, a prompt to enter a group name will appear. Enter a group name and press enter.
5. If a group with the specified name does not exist, a new group is automatically created with the current user as admin. Otherwise, a join request is sent to the current group admin.
6. Type anything to send a message or use the following commands:

| Command | Behaviour |
|---|---|
| /1 | View pending join requests** |
| /2 | Approve pending join requests** |
| /3 | Disconnect |
| /4 | View all group members |
| /5 | View online group members |
| /6 | Transfer adminship** |
| /7 | View group admin |
| /8 | Kick member** |
| /9 | Send a file to group |
** = Admin only action

## Instructions (Server)

1. Open a terminal window in the directory containing *server.py* and run the following command:
> python server.py localhost 8000
2. Replace `localhost` with your IP and `8000` with a TCP port number of your choice.
3. The server console will display logs for:
	1. New group creation
	2. User connection
	3. User disconnection
	4. User kick
	5. Admin transfer
	6. Join request
	7. Join request approval
	8. File transfer

## Features

- File sharing
- View online group members
- View all group members
- Transfer admin privilege
- Kick members
- View group admin
- If a user enters a group name which does not exist, a new group with the user as admin is automatically created.

## Upcoming
1. Offline Messages
2. Password authentication
