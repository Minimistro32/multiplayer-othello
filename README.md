# Overview

This is a multiplayer implementation of the popular board game Othello. There is a board class that handles the game logic. There is a server and client file that handles the networking logic required for multiplayer. 

I wanted to write this program in order to implement what I've learned about the OSI model and computer networking in general. I knew I was capable of making an Othello CLI and wanted to extend that functionality while simultaneously expanding my understanding of networking with practical experience.


[Software Demo Video](https://youtu.be/N5STa4AcGIA)

# Network Communication

The networking architecture in use here is client-server.

Packets are sent using the TCP on port 61235.

The message format is different depending on the direction of communication between client and server. Messages from the client are integers. Because we are using TCP the first message is the row and the second is column. Messages from the server are a utf-8 string that can be printed to display the board.

# Development Environment

I used VS Code and the terminal for development.

The language was Python3. I used several libraries including socket, selectors, and types. These libraries allowed me to implement networking and handle multiple connections.

# Useful Websites

* [Computer Networking in 100 Seconds](https://www.youtube.com/watch?v=keeqnciDVOo)
* [Crash Course Computer Science #28-30](https://www.youtube.com/watch?v=3QhU9jd03a0&list=PL8dPuuaLjXtNlUrzyH5r6jN9ulIgZBpdo&index=29)
* [Socket Programming in Python (Guide)](https://realpython.com/python-sockets)
* [Online Multiplayer Game With Python](https://www.youtube.com/watch?v=-3B1v-K1oXE)

# Future Work

* Implement a lobby.
* Prompt the user to play again.
* Handle when players disconnect.
* Provide the ability to save game progress.