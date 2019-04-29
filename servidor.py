import zmq
import sys



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
		ident, dest,operacion, msg = socket.recv_multipart()
		print("Message received from {}".format(operacion))
		if operacion==b'registrar':
			workers(ident,listaworkers)
			print(listaworkers)
		if operacion==b'numeroWorkers':
			numeroWorkers = len(listaworkers)
			socket.send_multipart([dest, ident, msg, str(numeroWorkers).encode('utf8')])
		if operacion==b'workersId':
			lista1 = str(listaworkers).lstrip('[')
			lista2 = lista1.rstrip(']')
			socket.send_multipart([dest, ident, msg, lista2.encode('utf8')])
			print('entroId')
		else:
			socket.send_multipart([dest , ident, operacion, msg])

if __name__ == '__main__':
	main()
