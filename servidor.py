import zmq
import sys
import json



def workers(identidad,lista):
	if identidad in lista:
		print('registrado')
	else:
		lista.append(identidad)

def main():
	listaworkers = []
	numeroWorkers = 1
	if len(sys.argv) != 1:
		print("Must be called with no arguments")
		exit()

	context = zmq.Context()
	socket = context.socket(zmq.ROUTER)
	socket.bind("tcp://*:4444")

	print("Started server")

	while True:
		sender, destino , msg = socket.recv_multipart()
		mensaje_json = json.loads(msg)
		operacion = mensaje_json['operacion']
		if operacion=='registrar':
			workers(sender,listaworkers)
			print(listaworkers)
		if operacion=='numeroWorkers':
			numeroWorkers = len(listaworkers)
			socket.send_multipart([destino, sender, msg])
		if operacion=='workersId':
			socket.send_multipart([destino, sender, msg])
			print('entroId')
		else:
			socket.send_multipart([destino, sender, msg])

if __name__ == '__main__':
	main()
