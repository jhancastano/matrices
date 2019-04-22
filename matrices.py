import threading



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


def multmatrices(matrizA,matrizB,matrizR):
# iterate through rows of X
    for i in range(len(matrizA)):
       # iterate through columns of Y
       for j in range(len(matrizB[0])):
           # iterate through rows of Y
           for k in range(len(matrizB)):
               matrizR[i][j] += X[i][k] * Y[k][j]

    for r in matrizR:
       print(r)

multmatrices(X,Y,result)