import zmq
import sys
from collections import namedtuple

def numeroworkers(socket,identity):
    socket.send_multipart([identity,b'numeroWorkers', b'preguntando'])
    sender, msg , operacion = socket.recv_multipart()
    return operacion

def workersid(socket,identity):
    socket.send_multipart([identity,b'workersId', b'preguntando'])
    sender, msg , operacion = socket.recv_multipart()
    return operacion.decode('utf8').split(',')

def multiplicacionParalela(socket,identity,matrizA,matrizB):
    print('sera que funcion')
    workersidwwww = workersid(socket,identity)
    numeroWorkers5 = int(numeroworkers(socket,identity))
    nFilas = len(matrizA)/numeroWorkers5
    filas_extra = len(matrizA)%numeroWorkers5

    for x in workersidwwww:
        socket.send_multipart(x.encode('utf8'),str(nFilas).encode('utf8'),b'matrizA')
        nFilas = nFilas + nFilas
        print(x)
    if filas_extra !=0:
        socket.send_multipart(workersidwwww[0].encode('utf8'),str(nFilas).encode('utf8'),b'matrizA')



def main():
    identity = b'a1'
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
            if(op=='multparalela'):
                pass
            else:
                socket.send_multipart([bytes(dest, 'ascii'), bytes(msg, 'ascii'), bytes(op, 'ascii')])


if __name__ == '__main__':
    main()
