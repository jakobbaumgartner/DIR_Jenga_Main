import socket               

def startSocket (server_ip, port):
    
    # starts socket and sets connection

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.connect((server_ip, port))

    return s