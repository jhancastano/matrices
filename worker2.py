import zmq
import sys
import json
from collections import namedtuple

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
    print('sera que funcion')
    listWorkers = workersID(socket,identity)
    nWorkers = len(listWorkers)
    nFilas = len(matrizA)/nWorkers
    filas_extra = len(matrizA)%nWorkers
    for x in listWorkers:
        socket.send_multipart()
        nFilas = nFilas + nFilas
        print(x)
    if filas_extra !=0:
        socket.send_multipart()



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
