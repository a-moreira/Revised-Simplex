import numpy as np


def read_model(arq):
    lines_list = arq.readlines()
    n_rows, n_cols = (int(val) for val in lines_list[0].split())
    model = [[int(val) for val in line.split()] for line in lines_list[1:]]

    return model, n_cols, n_rows


def create_model(model, n_cols, n_rows):
    # n_var = n_cols + n_rows
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
    b_ = np.linalg.solve(A[:, basic], b)
    z = np.dot(c[[basic]], b_)

    return b_, z


def step_two(A, b, c, basic, non_basic, b_, minimum):
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
    # print(y)
    # y_ = np.zeros(np.shape(A)[1])
    # y_[basic] = y
    # print(y_)
    # return y_
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


def main():
    minimum = float('inf')
    minimum_2 = float('inf')
    arq = open("teste.txt", "r")
    model, n_cols, n_rows = read_model(arq)
    c, A, b, non_basic, basic = create_model(model, n_cols, n_rows)
    # mantemos a matriz A original para comparacao
    # np.where((A == (2,3)).all(axis=1))
    print(c)
    print(A)
    print(b)
    print(basic)
    print(non_basic)

    while True:
        b_, z = step_one(A, b, c, basic, non_basic)
        print(b_)
        print(z)
        # idx eh eh o index da variavel que entra na base
        w, minimum, idx = step_two(A, b, c, basic, non_basic, b_, minimum)
        print(w)
        print(minimum)
        print(idx)
        if minimum >= 0:
            certificado = "otima"
            break
        else:
            minimum = float('inf')
        y = step_three(A, idx, basic)

        if (y <= 0).all():
            certificado = "ilimitada"
            break

        leaving_var = step_four(A, b, y, basic, minimum_2)

        non_basic.remove(idx)
        basic.append(idx)
        basic.remove(leaving_var)
        non_basic.append(leaving_var)
        basic.sort()
        non_basic.sort()
        print(basic)
        print(non_basic)

    print(certificado)


if __name__ == "__main__":
    main()
