import zmq
import sys
import json
from collections import namedtuple

def multiplicar(socket,identity,matrizA,matrizB,msg):
    matrizR = []
    mensaje_json = json.loads(msg)
    indiceInicial = mensaje_json['indiceInicial']
    indiceFinal = mensaje_json['indiceFinal']
    for i in range(indiceInicial,indiceFinal):
        for j in range(len(matrizB[0])):
            for k in range(len(matrizB)):
                matrizR[i][j] += X[i][k] * Y[k][j]

    mensaje = {'matriz':matrizR,'indiceInicial':indiceInicial,'indiceFinal':indiceFinal}
    mensaje_json = json.loads(mensaje)
    socket.send_multipart(identity,mensaje_json)

def nWorkers(socket,identity):
    msg = {'operacion':'nWorkers'}
    msg_json = json.dumps(msg)
    socket.send_multipart([identity,msg_json.encode('utf8')])
    sender, msg= socket.recv_multipart()
    mensaje_json = json.loads(msg)
    return mensaje_json['nWorkers']

def workersID(socket,identity):
    msg = {'operacion':'workersID'}
    msg_json = json.dumps(msg)
    socket.send_multipart([identity,msg_json.encode('utf8')])
    sender, msg= socket.recv_multipart()
    mensaje_json = json.loads(msg)
    return mensaje_json['workersID']

def multiplicacionParalela(socket,identity,matrizA,matrizB):
    listWorkers = workersID(socket,identity)
    nWorkers = len(listWorkers)
    nFilas = int(len(matrizA)/nWorkers)
    filas_extra = len(matrizA)%nWorkers
    indiceInicial = 0
    for x in listWorkers:
        worker = listWorkers[x].encode('utf8')
        mensaje = {'operacion':'multiplicar','indiceInicial':indiceInicial,'indiceFinal':nFilas}
        mensaje_json = json.dumps(mensaje) 
        socket.send_multipart([worker,mensaje_json])
        nFilas = nFilas + nFilas
        indiceInicial = indiceInicial + nFilas
    if filas_extra !=0:
        mensaje = {'operacion':'multiplicar','indiceInicial':len(matrizA)-filas_extra,'indiceFinal':len(matrizA)}
        mensaje_json = json.dumps(mensaje)
        socket.send_multipart(listWorkers[0].encode('utf8'),mensaje_json)
    sender, msg = socket.recv_multipart()
    mensaje = json.loads(msg)
    while mensaje['indiceFinal']<len(matrizA):
        sender, msg = socket.recv_multipart()
        mensaje = json.loads(msg)


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
    #registrando worker------------ 
    rWorker = {'operacion':'registrar'}
    rWorker_json = json.dumps(rWorker)
    socket.send_multipart([identity,rWorker_json.encode('utf8')])
    #--------------------------------
    
    while True:
        socks = dict(poller.poll())
        mensaje = {'operacion':'sin operacion'}
        mensaje_json = json.dumps(mensaje)

        if socket in socks:
            sender, msg = socket.recv_multipart()
            print(msg)

        elif sys.stdin.fileno() in socks:
            print("?")
            command = input()
            op, msg = command.split(' ', 1)
            if(op=='m'):
                
                print(workersID(socket,identity))
            if(op=='multparalela'):
                pass
            else:

                socket.send_multipart([identity,mensaje_json.encode('utf8')])


if __name__ == '__main__':
    main()