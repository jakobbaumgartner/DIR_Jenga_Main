# python server.py
# python client.py

import socket


class Server:

    def __init__(self, addr='localhost', port=5000):
        self.addr = addr
        self.port = port
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('*** SERVER POSTAVLJEN ***')

    def povezi(self):
        self.serv.bind((self.addr, self.port))
        self.serv.listen(5)

    def poslji(self, sporocilo):
        conn, addr = self.serv.accept()
        print('--- log: nova komunikacija')
        conn.send(bytes(sporocilo, 'utf-8'))

    def poslusaj(self):
        conn, addr = self.serv.accept()
        while True:
            from_client = ''
            data = conn.recv(4096)
            if not data:
                print('***ni sporocila gosta***')
                break
            data = data.decode('utf-8')
            from_client += data
            print('Sporočilo gosta:    ', from_client)

    def ustavi(self):
        conn, addr = self.serv.accept()
        self.conn.close()
        print('*** SERVER USTAVLJEN ***')


class Gost:

    def __init__(self, addr='localhost', port=5000):
        self.addr = addr
        self.port = port
        self.gost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gost.connect((self.addr, self.port))
        print('*** GOST POVEZAN ***')

    def poslji(self, msg):
        self.gost.send(bytes(msg, 'utf-8'))

    def poslusaj(self):
        from_server = self.gost.recv(4096)
        from_server = from_server.decode('utf-8')
        print('Prejeto sporocilo:   ', from_server)
    
    def ustavi(self):
        self.gost.close()
