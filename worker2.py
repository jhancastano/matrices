import zmq
import sys
from collections import namedtuple

def numeroworkers(socket,identity):
    socket.send_multipart([identity,b'numeroWorkers', b'preguntando'])
    sender, msg , operacion = socket.recv_multipart()
    print('--prueba.----')
    print(operacion)
    print('---fin prueba---')
    return msg

def multiplicacionParalela(socket,identity,matrizA,matrizB):
    print('sera que funcion')
    numeroWorkers5 = numeroworkers(socket,identity)
    numeroFilas = len(matrizA)
    print(numeroWorkers5)
    pass



def main():
    identity = b'b1'
    servidortcp = "tcp://localhost:4444"


    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.identity = identity
    socket.connect(servidortcp)
    

    print("Started client with id {}".format(identity))
    poller = zmq.Poller()
    poller.register(sys.stdin, zmq.POLLIN)
    poller.register(socket, zmq.POLLIN)

    socket.send_multipart([identity,b'registrar', b'registradoWorker'])
    socket.recv_multipart()
    while True:
        socks = dict(poller.poll())
        if socket in socks:
            sender, m , operacion = socket.recv_multipart()
            print("[{}]: {} ----- {}".format(sender, m, operacion))

        elif sys.stdin.fileno() in socks:
            print("?")
            command = input()
            dest, msg, op = command.split(' ', 2)
            if(op=='multiplicacion'):
                multiplicacionParalela(socket,identity,[1,2,3],[2,3,4])
            else:
                socket.send_multipart([bytes(dest, 'ascii'), bytes(msg, 'ascii'), bytes(op, 'ascii')])


if __name__ == '__main__':
    main()
