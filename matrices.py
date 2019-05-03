import zmq
import random
import itertools
import json
import numpy

def crearMatrizNXN(nx,ny):
    fila = []
    columna =[]
    for i in range(nx):
        for j in range(ny):
            number  = random.randrange(0,9)
            columna.append(number)
        fila.append(columna)
        columna =[]
    return fila

def impmatriz(matrizA):
    for r in matrizA:
       print(r) 



def setmatrizfile(matrizA):
    filas = len(matrizA)
    columnas = len(matrizA[0])
    with open('matrizB'+str(filas)+'X'+str(columnas)+'.txt', 'w') as file:
        for x in matrizA:
            file.write(str(x)+'\n')

def leermatrizrangos(nombre,rangoA,rangoB):
    matrizR = []
    with open(nombre,'r') as file:
        texto = itertools.islice(file, rangoA, rangoB)
        for linea in texto:
            a = json.loads(linea)
            matrizR.append(a)
    return matrizR


def multmatrices(matrizA,matrizB):
    matrizR = numpy.zeros((len(matrizA),len(matrizB[0])))
    for i in range(len(matrizA)):
       # iterate through columns of Y
        for j in range(len(matrizB[0])):
           # iterate through rows of Y
            for k in range(len(matrizB)):
                matrizR[i][j] += matrizA[i][k] * matrizB[k][j]
    return matrizR

#multmatrices(X,Y)
a = leermatrizrangos('matrizA5X5.txt',0,5)
b = leermatrizrangos('matrizB5X5.txt',0,5)
impmatriz(multmatrices(a,b))
print(multmatrices(a,b)[0][2])
#setmatrizfile(crearMatrizNXN(5,5))
