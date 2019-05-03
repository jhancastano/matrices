import zmq
import sys
import json
import numpy
import itertools
import time
from collections import namedtuple

def leermatrizrangos(nombre,rangoA,rangoB):
    matrizR = []
    with open(nombre,'r') as file:
        texto = itertools.islice(file, rangoA, rangoB)
        for linea in texto:
            a = json.loads(linea)
            matrizR.append(a)
    return matrizR

def leermatrizcompleta(nombre):
    matrizR = []
    with open(nombre,'r') as file:
        for linea in file.readlines():
            a = json.loads(linea)
            matrizR.append(a)
    return matrizR

def multiplicar(socket,identity,msg):
    
    mensaje_json = json.loads(msg)
    Inicial = mensaje_json['indiceInicial']
    Final = mensaje_json['indiceFinal']
    matrices = mensaje_json['matrices']
    size = mensaje_json['size']
    matrizA = leermatrizrangos(matrices[0],Inicial,Final)
    matrizB = leermatrizcompleta(matrices[1])
    matrizR = numpy.zeros((len(matrizA),len(matrizB[0])))
    for i in range(len(matrizA)):
        for j in range(len(matrizB[0])):
            for k in range(len(matrizB)):
                matrizR[i][j] += matrizA[i][k] * matrizB[k][j]
    matriz = matrizR.tolist()
    mensaje = {'operacion':'complete','matrizR':matriz,'indiceInicial':Inicial,'indiceFinal':Final,'size':size}
    mensaje_json = json.dumps(mensaje)
    socket.send_multipart([identity,mensaje_json.encode('utf8')])

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

def sendMatrizWorkers(socket,identity,matrizA,matrizB):

    a = leermatrizcompleta(matrizA)
    b = leermatrizcompleta(matrizB)

    listWorkers = workersID(socket,identity)
    nWorkers = len(listWorkers)
    nFilas = int(len(a)/nWorkers)
    filas_extra = len(a)%nWorkers
    indiceInicial = 0
    for x in listWorkers:
        worker = x.encode('utf8')
        mensaje = {'operacion':'multiplicar','indiceInicial':indiceInicial,'indiceFinal':nFilas,'size':len(a),'matrices':[matrizA,matrizB]}
        mensaje_json = json.dumps(mensaje) 
        socket.send_multipart([worker,mensaje_json.encode('utf8')])
        indiceInicial = indiceInicial + nFilas
        nFilas = nFilas + nFilas
    if filas_extra !=0:
        mensaje = {'operacion':'multiplicar','indiceInicial':len(a)-filas_extra,'indiceFinal':len(a),'size':len(a),'matrices':[matrizA,matrizB]}
        mensaje_json = json.dumps(mensaje)
        socket.send_multipart([listWorkers[0].encode('utf8'),mensaje_json.encode('utf8')])
    
def recvMatrizWorkers(socket,identity,msg):
    mensaje_json = json.loads(msg)
    segmento = mensaje_json['matrizR']
    indiceFinal = mensaje_json['indiceFinal']
    size = mensaje_json['size']
    for x in range(int(len(segmento))):
        print(x)
    if(indiceFinal==size):
        return time.time()
    else:
        return -1

def main():
    tiempoInicial = time.time() 
    tiempoFinal = time.time()
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
            mensaje_json = json.loads(msg)
            operacion = mensaje_json['operacion']
            if(operacion=='multiplicar'):
                print('estamos multiplicando')
                multiplicar(socket,sender,msg)
            elif(operacion=='complete'):
                a = recvMatrizWorkers(socket,identity,msg)
                if(a!=-1):
                   tiempoFinal = a
                   print(a-tiempoInicial) 
            else:
                pass
        elif sys.stdin.fileno() in socks:
            print("?")
            command = input()
            op, msg = command.split(' ', 1)
            if(op=='m1'):
                if (msg=='5x5'):
                    a = 'matrizA5X5.txt'
                    b = 'matrizB5X5.txt'
                    tiempoInicial = time.time()
                    print(tiempoInicial)
                    sendMatrizWorkers(socket,identity,a,b)    
                elif(msg=='10x10'):
                    a = 'matrizA10X10.txt'
                    b = 'matrizB10X10.txt'
                    tiempoInicial = time.time()
                    print(tiempoInicial)
                    sendMatrizWorkers(socket,identity,a,b)
                elif(msg=='100x100'):
                    a = 'matrizA100X100.txt'
                    b = 'matrizB100X100.txt'
                    tiempoInicial = time.time()
                    print(tiempoInicial)
                    sendMatrizWorkers(socket,identity,a,b)
                elif(msg=='500x500'):
                    a = 'matrizA1000X1000.txt'
                    b = 'matrizB1000X1000.txt'
                    tiempoInicial = time.time()
                    print(tiempoInicial)
                    sendMatrizWorkers(socket,identity,a,b)
            else:
                socket.send_multipart([identity,mensaje_json.encode('utf8')])


if __name__ == '__main__':
    main()