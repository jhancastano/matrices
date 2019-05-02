import zmq
import sys
import json



def workers(identidad,lista):
	ident =identidad.decode('utf8')
	if ident in lista:
		print('registrado')
	else:
		lista.append(ident)

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
		if operacion=='nWorkers':
			print('entroaaaaa')
			nWorkers = len(listaworkers)
			msg2 = {'nWorkers':nWorkers}
			msg_json = json.dumps(msg2) 
			socket.send_multipart([destino, sender, msg_json.encode('utf8')])
		if operacion=='workersID':
			msg2 = {'workersID':listaworkers}
			msg_json = json.dumps(msg2) 
			socket.send_multipart([destino, sender, msg_json.encode('utf8')])

			print('entroId')
		else:
			socket.send_multipart([destino, sender, msg])

if __name__ == '__main__':
	main()
