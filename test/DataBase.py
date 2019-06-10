# Library designed to handle csv files in memory

import csv


def generate_excel(file):
    big_matrix = []
    with open(file, encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            big_matrix.append(row)
    return big_matrix


def write_to_excel(file, lista):
    with open(file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(lista)
    csvFile.close()


def projection(cols, big_matrix):
    proj = []
    for i in big_matrix:
        subproj = []
        for j in cols:
            subproj.append(i[j])
        proj.append(subproj)
    return proj


def selection(col, funct, big_matrix):
    select = []
    for i in big_matrix:
        if (funct(i[col])):
            select.append(i)
    return select


def transform(col, funct, big_matrix):
    trans = []
    for i in big_matrix:
        i[col] = funct(i[col])
        trans.append(i)
    return trans


def transformCols(listCols, resultCol, funct, big_matrix):
    trans = []
    for i in big_matrix:
        input = []
        for elem in listCols:
            input.append(i[elem])
        input = tuple(input)
        i[resultCol] = funct(*input)
        trans.append(i)
    return trans


def groupBy(listKeys, listAppliedFunc, listFuncAggreg, big_matrix, returnsort=False):
    dict = {}
    for i in big_matrix:
        keys = []
        for l in listKeys:
            keys.append(i[l])
        T = tuple(keys)
        values = []
        for l in listAppliedFunc:
            values.append(i[l])
        if not T in dict:
            dict[T] = []
        dict[T].append(values)

    items = dict.items()

    if returnsort:
        items = sorted(items, key=lambda x: x[0])

    gby = []
    for key, values in items:
        idx = 0
        cols = list(key)
        for func in listFuncAggreg:
            input = []
            for v in values:
                input.append(v[idx])
            idx += 1
            cols.append(func(*tuple(input)))
        gby.append(cols)
    return gby


def matrixToArray(big_matrix):
    ret = []
    for i in big_matrix:
        ret.append(i[0])
    return ret


def sumA(*input):  # A stands for Aggregation
    suma = 0
    for i in input:
        suma += i
    return suma


def minA(*input):
    if len(input) == 0: return None
    mini = input[0]
    for i in input:
        mini = min(mini, i)
    return mini


def maxA(*input):
    if len(input) == 0: return None
    maxi = input[0]
    for i in input:
        maxi = max(maxi, i)
    return maxi


def countA(*input):
    return len(input)


# MAIN FUNCTION
if __name__ == "__main__":
    bigmtx = [
        [1, 2, 3, 4, 5, 6],
        [10, 20, 30, 40, 50, 60],
        [100, 200, 300, 400, 500, 600],
        [1, 2, 3, 40, 50, 60],
        [1, 2, 3, 400, 500, 600],
    ]


    def suma(*input):
        suma = 0
        for i in input:
            suma += i
        return suma


    def count(*input):
        print(input)
        return len(input)


    print(groupBy([0, 1, 2], [3, 4, 5], [suma, suma, count], bigmtx))

    bigmtx = [
        ['ENTREGA', 1],
        ['RECOLLIDA', 1],
        ['ENTREGA', 1],
        ['ENTREGA', 1],
        ['ENTREGA', 1],
        ['AENTREGA', 1],
        ['ENTREGA', 1],
        ['RECOLLIDA', 1],
        ['DUAL', 1],
    ]

    print(groupBy([0], [1], [count], bigmtx, True))
