import numpy as np

def find_minor(matrix, row, col):
    matrix = [cop[:] for cop in matrix]
    del matrix[row]
    for i in range(len(matrix)):
        matrix[i] = matrix[i][:col] + matrix[i][col + 1:]
    return matrix


def find_determinante(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    summa = 0
    for j in range(len(matrix)):
        summa += matrix[0][j] * (-1) ** j * find_determinante(find_minor(matrix, 0, j))
    return summa


def find_reversed_matrix(matrix, det=None):
    if det is None:
        det = find_determinante(matrix)
    arr = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix)):
            alg_dop = (-1) ** (i + j) * find_determinante(find_minor(matrix, i, j))
            temp.append(alg_dop)
        arr.append(temp)

    rev_arr = list(map(lambda x: [i / det for i in x], zip(*arr)))
    return rev_arr


def create_matrix(x, y=None):
    matrix = []
    if y is None:
        for i in range(len(x)):
            temp = []
            for j in range(len(x)):
                temp.append(x[i] ** j)
            matrix.append(temp)
    return matrix

def build_polinom_and_table(x, C):
    terms = []
    for i in range(len(x) - 1, -1, -1):
        coeff = round(C[i], 3)
        if coeff != 0:
            if i == 0:
                terms.append(f'{coeff}')
            elif i == 1:
                terms.append(f'{coeff}*x')
            else:
                terms.append(f'{coeff}*x^{i}')
    
    polinom = ' + '.join(terms).replace(' + -', ' - ')
    print(f'Полином: P(x) = {polinom}')
    print('\n' + '┌' + '─' * 10 + '┬' + '─' * 15 + '┐')
    print(f'│{"x":^10}│{"P5(x)":^15}│')
    print('├' + '─' * 10 + '┼' + '─' * 15 + '┤')
    
    start, stop = -1, 2.5
    dots = int((stop - start) / 0.25) + 1
    for xi in np.linspace(start, stop, dots):
        p_value = 0
        for i, coeff in enumerate(C):
            p_value += coeff * (xi ** i)
        print(f'│{xi:^10.2f}│{p_value:^15.3f}│')
    
    print('└' + '─' * 10 + '┴' + '─' * 15 + '┘')


def kanon_polinom(x, y):
    print('Канонический полином:')
    A = create_matrix(x)
    detA = find_determinante(A)
    revA = find_reversed_matrix(A, detA)
    C = []
    for i in range(len(revA)):
        summa = 0
        for j in range(len(revA)):
            summa += revA[i][j] * y[j]
        C.append(summa)
    build_polinom_and_table(x, C)


def kramer_polinom(x, y):
    print('Полином через метод Крамера:')
    A = create_matrix(x)
    detA = find_determinante(A)
    determinates = []
    for i in range(len(A)):
        matrix = [el[:] for el in A]
        for j in range(len(A)):
            matrix[j][i] = y[j]
        determinates.append(find_determinante(matrix))
    C = [det / detA for det in determinates]
    build_polinom_and_table(x, C)


def lagrange_polinom(x, y):
    def lagrange_basis(x, y, i, x_val):
        li = 1
        for j in range(len(x)):
            if j != i:
                li *= (x_val - x[j]) / (x[i] - x[j])
        return li

    def interpolate(x, y, x_val):
        result = 0
        for i in range(len(x)):
            result += y[i] * lagrange_basis(x, y, i, x_val)
        return result

    print('Полином Лагранжа:')
    print('\n' + '┌' + '─' * 10 + '┬' + '─' * 15 + '┐')
    print(f'│{"x":^10}│{"L(x)":^15}│')
    print('├' + '─' * 10 + '┼' + '─' * 15 + '┤')

    start, stop = min(x), max(x)
    dots = int((stop - start) / 0.25) + 1
    for xi in np.linspace(start, stop, dots):
        l_value = interpolate(x, y, xi)
        print(f'│{xi:^10.2f}│{l_value:^15.3f}│')
    
    print('└' + '─' * 10 + '┴' + '─' * 15 + '┘')


def newton_polinom(x, y):
    final_differencies = []
    for i in range(len(y) - 1):
        temp_diff = []
        for j in range(1, len(final_differencies[i - 1] if final_differencies else y)):
            if final_differencies:
                temp_diff.append(final_differencies[i - 1][j] - final_differencies[i - 1][j - 1])
            else:
                temp_diff.append(y[j] - y[j - 1])
        final_differencies.append(temp_diff)
    h = x[1] - x[0]
    final_differencies.insert(0, y[0])
    indexies_list = []
    total_k = 1
    for i in range(len(y)):
        if i == 0:
            indexies_list.append(y[0])
        else:
            indexies_list.append(final_differencies[i][0] / (total_k * h ** i))
            total_k *= (i + 1)
    
    final_x = 2.8
    while round(x[-1], 3) != final_x:
        x.append(x[-1] + 0.1)
    p_x = []
    for i in range(len(x)):
        N_sum = indexies_list[0]
        for j in range(1, len(indexies_list)):
            total = 1
            counter = 0
            for _ in range(j):
                total *= x[i] - x[counter]
                counter += 1
            N_sum += total * indexies_list[j]
        p_x.append(N_sum)
    
    print('Полином Ньютона:')
    print('\n' + '┌' + '─' * 10 + '┬' + '─' * 15 + '┐')
    print(f'│{"x":^10}│{"L(x)":^15}│')
    print('├' + '─' * 10 + '┼' + '─' * 15 + '┤')

    for i in range(len(x)):
        print(f'│{x[i]:^10.2f}│{p_x[i]:^15.3f}│')
    
    print('└' + '─' * 10 + '┴' + '─' * 15 + '┘')


x = [-1, -0.5, 0, 0.5, 1, 1.5]
y = [0, 2, -1.5, -4, 3, 7]
kanon_polinom(x, y)
kramer_polinom(x, y)
lagrange_polinom(x, y)
newton_polinom(x, y)
