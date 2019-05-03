import zmq
import random
import itertools



X = [
    [12,7,3,2,3],
    [4,5,6,2,3],
    [7,8,9,3,5],
    [1,3,4,5,7],
    [3,7,8,2,1]]
# 3x4 matrix
Y = [
    [5,8,1,4,5],
    [6,7,3,6,7],
    [4,5,1,8,9],
    [2,3,4,5,6],
    [8,6,9,0,2]
    ]
# result is 3x4
result = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
         ]
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
    print(matrizA)


def setmatrizfile(matrizA):
    filas = len(matrizA)
    columnas = len(matrizA[0])
    with open('matrizB'+str(filas)+'X'+str(columnas)+'.txt', 'w') as file:
        for x in matrizA:
            file.write(str(x)+'\n')

def leermatrizcompleta(nombre):
    with open(nombre,'r') as file:
        texto = itertools.islice(file, 0, 5)
        for linea in texto:
            print(linea)
    


def multmatrices(matrizA,matrizB,matrizR):
# iterate through rows of X
    for i in range(len(matrizA)):
        print(i)
        print('-----------')
       # iterate through columns of Y
        for j in range(len(matrizB[0])):
           # iterate through rows of Y
            for k in range(len(matrizB)):
                matrizR[i][j] += X[i][k] * Y[k][j]

    for r in matrizR:
       print(r)

#multmatrices(X,Y,result)
#leermatrizcompleta('matriz5X5.txt')
#setmatrizfile(crearMatrizNXN(5,5))
