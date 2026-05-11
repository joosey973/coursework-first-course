def kanon_polinom(x, y):
    A = create_matrix(x=x)
    detA = find_determinante(A)
    revA = find_reversed_matrix(A, detA)
    if revA is None:
        return

    C = []
    for i in range(len(revA)):
        summa = 0
        for j in range(len(revA)):
            summa += revA[i][j] * y[j]
        C.append(summa)
    
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
    print(f'P{len(C) - 1}(x)={polinom}')


def find_minor(matrix, row, col):
    matrix = [cop[:] for cop in matrix]
    del matrix[row]
    for i in range(len(matrix)):
        matrix[i] = matrix[i][:col] + matrix[i][col + 1:]
    return matrix
    

def find_determinante(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    summa = 0
    for j in range(len(matrix)):
        summa += matrix[0][j] * (-1) ** j * find_determinante(find_minor(matrix, 0, j))
    return summa


def find_reversed_matrix(matrix, det=None):
    if det is None:
        det = find_determinante(matrix)

    if det == 0:
        return

    arr = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix)):
            alg_dop = (-1) ** (i + j) * find_determinante(find_minor(matrix, i, j))
            temp.append(alg_dop)
        arr.append(temp)
    rev_arr = list(map(lambda x: [i / det for i in x], zip(*arr)))
    return rev_arr


def matrix_multiplication(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result
    

def create_matrix(n=None, *coefs, x=None):
    if coefs:
        matrix = [[0 for j in range(n + 1)] for i in range(n + 1)]
        A, C, B, F = coefs[0]
        matrix[0][0] = -C[0]
        count = 0
        for i in range(1, n):
            matrix[i][count] = A[i]
            matrix[i][count + 1] = -C[i]
            matrix[i][count + 2] = B[i]
            count += 1
        matrix[-1][-1] = -C[-1]
    else:
        matrix = []
        for i in range(len(x)):
            temp = []
            for j in range(len(x)):
                temp.append(x[i] ** j)
            matrix.append(temp)
        return matrix
    return matrix


def matrix_method(x, h, n):
    matrix = create_matrix(n, get_coefs(x, h, n), x=None)
    result_matrix = matrix_multiplication(find_reversed_matrix(matrix), [[i] for i in get_coefs(x, h, n)[-1]])
    result_matrix = [i[0] for i in result_matrix]
    return result_matrix


def get_p(x):
    return [-val for val in x]


def get_q(x):
    return [2 for i in range(len(x))]


def get_r(x):
    return [val ** 2 for val in x]


def get_coefs(x, h, n):
    p = get_p(x)
    q = get_q(x)
    r = get_r(x)
    A = [0 for _ in range(len(x))]
    C = [0 for _ in range(len(x))]
    B = [0 for _ in range(len(x))]
    F = [0 for _ in range(len(x))]
    F[0], F[-1] = y_0, y_k
    C[0], C[-1] = -1, -1

    for i in range(1, n):
        A[i] = 1 - p[i] * h / 2
        C[i] = 2 - q[i] * h ** 2
        B[i] = 1 + p[i] * h / 2
        F[i] = r[i] * h ** 2
    
    return A, C, B, F


def progonka_method(x, h, n):
    alpha = [0 for i in range(n + 1)]
    beta = [0 for i in range(n + 1)]
    A, C, B, F = get_coefs(x, h, n)
    alpha[0], beta[0] = B[0] / C[0], -F[0] / C[0]
    for i in range(1, n + 1):
        alpha[i] = B[i] / (C[i] - alpha[i - 1] * A[i])
        beta[i] = (beta[i - 1] * A[i] - F[i]) / (C[i] - alpha[i - 1] * A[i])
    y = [0 for i in range(len(x))]
    y[-1] = beta[-1]
    for i in range(n - 1, -1, -1):
        y[i] = alpha[i] * y[i + 1] + beta[i]
    return y


def show_table(x, y_prog, y_matr):
    print("┌──────────┬─────────────┬────────────┐")
    print("│    x     │  Матричный  │  Прогонка  │")
    print("├──────────┼─────────────┼────────────┤")
    
    def fmt(val):
        return f"{val:^10.6f}"
    
    for i in range(len(x)):
        x_str = f"{x[i]:^10.6f}" if isinstance(x[i], (int, float)) else f"{str(x[i]):^10}"
        y_prog_str = fmt(y_prog[i])
        y_matr_str = fmt(y_matr[i])
        print(f"│{x_str}│{y_prog_str}   │{y_matr_str}  │")
    
    print("└──────────┴─────────────┴────────────┘")


def mkr(x_0, x_k, y_0, y_k, n=8):
    h = (x_k - x_0) / n
    x = [x_0]
    for i in range(1, n + 1):
        x.append(x_0 + i * h)
    y_prog = progonka_method(x, h, n)
    y_matr = matrix_method(x, h, n)
    show_table(x, y_prog, y_matr)
    kanon_polinom(x, y_prog)



x_0, x_k = 0, 2
y_0, y_k = 1, 4
mkr(x_0, x_k, y_0, y_k)