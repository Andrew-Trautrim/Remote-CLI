import socket
import threading

# an empty list to store connections
connections = []

# client handling thread function
def handle_connection(conn, addr):
    while True: 
        global connections
        
        # prints out what the client sends, maximum of 1024 bytes
        data = conn.recv(1024)
        print "Recieved from %s:%d: %s" % (addr[0], addr[1], data)
        
        # sends a packet (acknowledgement) back to conected user
        conn.send(bytes("ACK\n"))
        
        if not data:
            connections.remove(conn)
            conn.close()
            break

bind_ip = socket.gethostbyname(socket.gethostname())
bind_port = 80

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

# socket listens to incoming connections
# limit of 5, additional connections refused
server.listen(5)

print "Listening on %s:%d..." % (bind_ip, bind_port)
    
while True:
    
    conn, addr = server.accept()
    
    # starts the client thread to handle incoming data
    connection_thread = threading.Thread(target=handle_connection, args=(conn, addr))
    
    # the program will be able to exit regardless if any threads are still running
    connection_thread.daemon = True
    
    connection_thread.start()
    connections.append(conn)