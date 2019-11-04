import numpy as np
import fileinput

def read_model(arq):
    lines_list = arq.readlines()
    n_rows, n_cols = (int(val) for val in lines_list[0].split())
    model = [[int(val) for val in line.split()] for line in lines_list[1:]]

    return model, n_cols, n_rows


def create_model(model, n_cols, n_rows):
    c = np.asarray(model[0])
    A = np.asarray(model[1:])
    b = A[:, -1]
    A = np.delete(A, -1, 1)
    Id = np.identity(n_rows)
    c = np.append(c, np.zeros(n_rows))
    A = np.append(A, Id, axis=1)
    non_basic = [i for i in range(n_cols)]
    basic = [i + n_cols for i in range(n_rows)]

    return c, A, b, non_basic, basic


def step_one(A, b, c, basic, non_basic):
    xB = np.linalg.solve(A[:, basic], b)
    z = np.dot(c[[basic]], xB)

    return xB, z


def step_two(A, b, c, basic, non_basic, xB, minimum):
    w = np.linalg.solve(np.transpose(A[:, basic]), c[[basic]])
    idx = -1
    for j in non_basic:
        aux = np.dot(w, A[:, j]) - c[j]
        if aux < minimum:
            idx = j
            minimum = aux

    return w, minimum, idx


def step_three(A, idx, basic):
    y = np.linalg.solve(A[:, basic], A[:, idx])

    return y


def step_four(A, b, y, basic, minimum_2):
    for i in range(len(basic)):
        if y[i] > 0:
            aux = b[i] / y[i]
            if aux < minimum_2:
                minimum_2 = aux
                idx = i

    leaving_var = basic[idx]
    return leaving_var


def solve(c, A, b, non_basic, basic, minimum, minimum_2):

    while True:
        xB, z = step_one(A, b, c, basic, non_basic)
        # print(basic)
        # print(non_basic)
        # print('xB:', xB)
        # print('z:', z)
        # idx eh o index da variavel que entra na base
        w, minimum, idx = step_two(A, b, c, basic, non_basic, xB, minimum)
        # w eh o certificado
        # print('w:', w)
        # print('minimum:', minimum)
        # print('idx:', idx)
        if minimum >= 0:
            status = "otima"
            break
        else:
            minimum = float('inf')
        y = step_three(A, idx, basic)

        if (y <= 0).all():
            status = "ilimitada"
            break

        leaving_var = step_four(A, b, y, basic, minimum_2)

        non_basic.remove(idx)
        basic.append(idx)
        basic.remove(leaving_var)
        non_basic.append(leaving_var)
        basic.sort()
        non_basic.sort()
        # print('basic:', basic)
        # print('non_basic:', non_basic)

    return z, w, status, xB


def main():
    minimum = float('inf')
    minimum_2 = float('inf')
    arq = open("teste.txt", "r")
    model, n_cols, n_rows = read_model(arq)
    c, A, b, non_basic, basic = create_model(model, n_cols, n_rows)
    first_basic = basic
    first_n_basic = non_basic
    # aqui criamos uma PL auxiliar
    # SE OBJ = 0, CONTINUO NORMALMENTE
    # SE OBJ != 0, PL ORIGINAL EH INVIAVEL
    if (b < 0).any():
        negative_idx = np.where(b < 0)
        negative_idx = [i for i in negative_idx[0]]
        c2 = np.zeros(n_cols + 2*n_rows)
        c2[n_cols + n_rows:] = -1
        A2 = A
        b2 = b
        A2[negative_idx] = -1.0*A2[negative_idx]
        b2[negative_idx] = -1.0*b2[negative_idx]
        A2 = np.append(A2, np.identity(n_rows), axis=1)
        # for i in range(A2.shape[0]):
        #   c2 = np.add(c2, A2[i])
        non_basic2 = [i for i in range(n_cols + n_rows)]
        basic2 = [i+n_rows+n_cols for i in range(n_rows)]
        z, w, status, xB = solve(c2, A2, b2, non_basic2, basic2, minimum, minimum_2)

        # se a PL auxiliar tem obj < 0, acabou
        if z < 0:
            status = 'inviavel'

        # se nao, rodamos o simplex
        else:
            z, w, status, xB = solve(c, A, b, non_basic, basic, minimum, minimum_2)

    else:
        z, w, status, xB = solve(c, A, b, non_basic, basic, minimum, minimum_2)



    solucao = [0. for i in range(n_cols + n_rows)]
    solucao = {key:value for (key,value) in zip(basic, xB)}


    x = [0. for i in range(n_rows+n_cols)]

    for key in solucao:
        x[key] = solucao[key]

    if status == 'ilimitada':
        w = A[, np.where((A < 0).all())]

    w = w.tolist()
    if status == 'otima':
        print(status)
        print(z)
        print(*x)
        print(*w)
    elif status == 'ilimitada':
        print(status)
        print(*x)
        print(*w)
    elif status == 'inviavel':
        print(status)
        print(*w)


if __name__ == "__main__":
    main()
