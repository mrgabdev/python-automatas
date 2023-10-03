# 0 CREAR UNA LISTA : 1, 2, 5, 3, 2, 3, 3, 6, 10, 8, 9
# 1.CONVERTIR LA LISTA EN UN SET PARA ELIMINAR DUPLICADOS
# 2. CALCULAR LA SUMA DE LOS NUMEROS USANDO UNA LISTA
# 3.CALCULAR LA SUMA DE LOS NUMEROS USANDO UN SET
"""4.CREAR UN DICCIONARIO PARA ALMACENAR LAS ESTADISTICAS NUMEROS UNICOS, 
SUMA TOTAL LISTA, SUMA TOTAL SET MAXIMO VALOR, MINIMO VALOR
"""
# 5. IMPRIMIR LAS ESTADISTICAS""


numberList = [1, 2, 5, 3, 2, 3, 3, 6, 10, 8, 9]

uniqueList = set(numberList)

totalSumList = sum(numberList)
totalSumUnique = sum(uniqueList)

maxNumber = max(numberList)
minNumber = min(numberList)

stats = {
    "totalSumList": totalSumList,
    "totalSumSet": totalSumUnique,
    "max": maxNumber,
    "min": minNumber,
}

print(stats)
