import socket, pickle
import threading 
import pyaudio
import sys
import numpy as np
import wave
import struct
import time

global radioStation
global tcp
global udp
global finish

HOST = '127.0.0.1'      # Endereco IP do Servidor
PORT = 54321             # Porta que o Servidor está


finish = False

radioStation = []
radioStation.append(0)
radioStation.append(0)
radioStation.append(0)
radioStation[0] = []
radioStation[1] = []
radioStation[2] = []


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

	
def isAlive(conn):
	try:
		if not conn:
			return False
		else:
			return True
	except Exception:
		return False

def removeClient(host, port,connection):
	for p in range(len(radioStation)):
		if (host,port,connection) in radioStation[p]:
			radioStation[p].remove((host,port,connection))

def finishConnections():
	radioStation[0] = []
	radioStation[1] = []
	radioStation[2] = []


def radioStart(file, radio, stream):
		client =('',0)
		portUdpClient = 0
		connection = socket
		chunk = 16
		while True:
			try:
				wf = wave.open(file, 'rb')
				
				data = wf.readframes(chunk)

				while data != b'': 
					if finish:
						break
					for p in range(len(radioStation[radio-1])):
						port = radioStation[radio-1][p][1]
						host = radioStation[radio-1][p][0][0]

						client = radioStation[radio-1][p][0]
						portUdpClient = port
						connection = radioStation[radio-1][p][2]

						if port != 0:
							udp.sendto(data,(host,port))

					stream.write(data)
					data = wf.readframes(chunk)

				for p in range(len(radioStation[radio-1])):
						port = radioStation[radio-1][p][1]
						conn = radioStation[radio-1][p][2]

						client = radioStation[radio-1][p][0]
						portUdpClient = port
						connection = conn

						if port != 0:
							conn.send(str("Announce").encode())
			except ConnectionAbortedError:
				removeClient(client[0],portUdpClient,connection)
			except ConnectionResetError:
				removeClient(client[0],portUdpClient,connection)
			except OSError:
				removeClient(client[0],portUdpClient,connection)
		stream.close()
	

def newConnectionStart(client, connection):
	handShakeOk = False
	portUdpClient = 0

	while True:
		try:
			msg = connection.recv(1024).decode()

			if ":" in msg:
				msg =msg.split(":")
				if not msg[0] or msg[0].lower() == 'exit':
					break
				elif msg[0].lower() == "hello" and not handShakeOk:
					print(msg)
					portUdpClient = int(msg[1])
					answer = "\n\n|         Set your station:     |\n|1 = The Rising Fighting Spirit |\n|2 = Top 5 Segundos             |\n|3 = A historia do mamute       |"
					connection.send(str(answer).encode())
					handShakeOk = True

				elif msg[0].lower() == "setstation" and handShakeOk:
					if int(msg[1]) > 0 and int(msg[1]) < 4:
						removeClient(client,portUdpClient,connection)
						posRadio = int(msg[1])-1
						radioStation[posRadio].append((client,portUdpClient,connection)) 
						connection.send(str("Announce").encode())
					else:
						connection.send(str("InvalidCommand").encode())
						break

				else:
					connection.send(str("InvalidCommand").encode())
					break
			else:
				connection.send(str("InvalidCommand").encode())
				break

			msg = 0
		except ConnectionAbortedError:
			break
		except ConnectionResetError:
			break

	finishClient(client,portUdpClient,connection)

def finishClient(client,portUdpClient,connection):
	
	removeClient(client,portUdpClient,connection)
	connection.close()
	print('Finalizando conexão do cliente', client)

def command():
	while True:
		command = input()
		if command == "p":
			for p in range(len(radioStation)):
				print()
				print("Radio:. "+str(p+1))
				for x in range(len(radioStation[p])):
					print(radioStation[p][x][0])
		if command == "q":
			for i in range(len(radioStation)):
				for p in range(len(radioStation[i])):
					port = radioStation[i][p][1]
					conn = radioStation[i][p][2]
					if port != 0:
						conn.send(str("finish").encode())
			finishConnections()
			finish = True



print('\nEstação de radio iniciado no IP', HOST, 'na porta', PORT)

p = pyaudio.PyAudio()

stream = [p.open(format = 8,
		    channels = 2 ,
		    rate = 44100,
		    output = True) for i in range(3)]

threading.Thread(target=radioStart,args=("radio1.wav", 1, stream[0],)).start()
threading.Thread(target=radioStart,args=("radio2.wav", 2, stream[1], )).start()
threading.Thread(target=radioStart,args=("radio3.wav", 3, stream[2], )).start()
threading.Thread(target=command).start()

tcp.bind((HOST, PORT))
tcp.listen(10)


while True:
	if finish:
		break
	connection, client = tcp.accept()
	threading.Thread(target=newConnectionStart,args=(client, connection, )).start()	
	print('\nConexão realizada por:', client)
	


print("Sistema Finalizando")
sys.exit(0)







	

		    
		    
	