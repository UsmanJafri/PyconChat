# PyconChat 
**Py**thon **Con**sole **Chat** - A Python chat application featuring group conversations, file sharing and offline messaging.
### Requirements
1. Python 3
### Instructions (Server)
1. Open **server.py**, change the **ip** in line 94 and **port** in line 95 as needed.
2. Open **client.py**, change the **ip** in line 99 and **port** in line 100 as needed.
3. Open a Terminal window in the directory containing server.py and run:
> python3 server.py
### Instructions (Client)
1. Open a Terminal window in the directory containing client.py and run:
> python3 client.py
2. Enter your username in the prompt and press Enter.
3. Enter your groupname in the prompt and Enter.
4. If a group with the entered groupname did not exist, a group with you as the admin is created and you are ready to chat!
5. Otherwise, the admin of the chosen group is notified about your join request. Once your join request is approved, you will be asked to press any key to confirm and then you may begin chatting.
### Features
- File sharing
- View online group members
- View all group members
- Transfer admin privilege
- Kick members
- View group admin
- If a user enters a group name which does not exist, a new group with the user as admin is automatically created.

#### Upcoming
1. Improvements to user input handling to negate the chance of a user's message being treated as a system protocol message.
2. Offline Messages
3. Password authentication
