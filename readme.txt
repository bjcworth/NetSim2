Supporting Documentation								              10/4/13
Brandon Charlesworth
bjcworth@bu.edu
U20809812

Part 1)

echoserver-simple.py
------------------------------
A simple echo server to connect to our client. Allows user to specify port to host connection to locally. Specifies a size of 1024 to indicate that how much of a client message will be handled at a given time. Backlog indicates how many connections we will handle at a given time. Initializes a socket, binds to the port specified, and listens to backlog number of connections. Loops continuously, waiting to accept a connection on the port from the client. If data received, echo it back and close the connection.

Instructions:
chmod +x echoserver-simple.py
./echoserver-simply.py <port #>

Echoclient-simple.py
------------------------------
A simple echo client which takes a host as the first argument, allowing the user to specify to use a local host or connect to a remote IP. The second argument allows for port specification as well. A socket is created to allow the client to connect to the port specified. Since this is a simple program, we only send a small string after successful socket connection. After the data is echoed, we close the socket and print what was received.
Instructions:
chmod +x echoclient-simple.py
./echoclient-simple.py localhost <port #>


Part 2)

For part 2, I implemented more advanced versions of the simple server and client modules I created for part 1. These programs compile with the same arguments and take the same cmd line parameters. Please refer to the commenting in the files themselves for more detail on how they interoperate.
