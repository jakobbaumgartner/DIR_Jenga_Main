import socket                
  
# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  


length = 75 
height = 15
width = 24.5
width_off = width / 2
height_off = height / 2  

  
# Define the port on which you want to connect 
port = 5000
server_ip = '192.168.125.1'
s.connect((server_ip, port))

# data = s.recv(4096)
# if len(data) > 0:
	# data_str = str(data)
	# print(data_str[2:len(data_str) - 1]) 


# pošlji koordinate v ks stolpa v rapid:
def send_coords():
	
	start_point = []
	end_point = []
	while True:
		row = int(input('enter row: '))
		s.send(bytes(str(row), 'utf-8'))
		col = int(input('enter block: '))
		s.send(bytes(str(col), 'utf-8'))
  		
  		

		data = s.recv(4096)
		if (len(data) > 0): 
			data_str = str(data)
			print(data_str[2:len(data_str) - 1])


send_coords()
      


