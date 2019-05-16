import socket, pickle
import threading 
import pyaudio
import sys
import numpy as np
import wave
import struct
from random import randint
 
HOST = '127.0.0.1'      # Endereco IP do Servidor
PORTtcp = 54321             # Porta que o Servidor está
 
def finishConnection():
	udp.close()
	tcp.close()
	sys.exit(0)

def newSocketUDP(PORTudp):
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	udp.bind((HOST,PORTudp)) 
	return udp

def newSocketTCP(PORTtcp):
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp.connect((HOST, PORTtcp))
	return tcp

def playMusic(udp):
	try:
		while True:
			p = pyaudio.PyAudio()
			stream = p.open( 
			    format = 8,
			    channels = 2 ,
			    rate = 44100,
			    output = True)

			byteMusic = udp.recv(1024)
			if not byteMusic:
				continue

			while byteMusic != b'':
				stream.write(byteMusic)
				byteMusic = udp.recv(1024)

			stream.close()
			p.terminate()
	except ConnectionAbortedError:
		print("Erro de conexão")
		finishConnection()
	except ConnectionResetError:
		print("Erro de conexão")
		finishConnection()
	except OSError:
		finishConnection()	


print('|-------------- INSTRUÇÕES ----------------|')
print('|- Para qualquer comando digite o comando -|')
print('|------- e o valor separados por ":" ------|')
print('|------------------------------------------|')

command = input()

if ":" in command:
	if command.split(":")[0].lower() == "hello":
		port = int(command.split(":")[1])
		udp = newSocketUDP(port)
		tcp = newSocketTCP(PORTtcp)
		threading.Thread(target=playMusic,args=(udp, )).start()
		tcp.send(str(command).encode())
		try:
			while command.lower() != "exit":
		 		
	 			answer = tcp.recv(1024).decode()
	 			if answer == "finish":
	 				break
	 			
	 			print(answer)
	 			if answer == "InvalidCommand":
	 				break
	 			command = input()
	 			tcp.send(str(command).encode())


			finishConnection()
		
		except ConnectionAbortedError:
			finishConnection()
		except ConnectionResetError:
			finishConnection()
		except OSError:
			finishConnection()	
	 			
	else:
		print("InvalidCommand")
		sys.exit(0)
else:
	print("InvalidCommand")
	sys.exit(0)



