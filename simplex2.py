import numpy as np


def read_model(arq):
    lines_list = arq.readlines()
    n_cols, n_rows = (int(val) for val in lines_list[0].split())
    model = [[int(val) for val in line.split()]
             for line in lines_list[1:]]

    return model, n_cols, n_rows


def create_model(model, n_cols, n_rows):
    n_var = n_cols + n_rows
    c = np.asarray(model[0])
    A = np.transpose(model[1:])
    b = A[-1]
    A = np.delete(A, -1, 0)
    N = A
    B = np.identity(n_rows)
    cN = c
    cB = np.zeros(n_cols)
    c = np.append(cN, cB)
    A = np.vstack([A, B])
    non_basic_variables = [i for i in range(n_cols)]
    basic_variables = [i + n_cols for i in range(n_rows)]

    return A, B, N, b, c, cB, cN, basic_variables, non_basic_variables


def step_one(B, b, cB):
    BT = np.transpose(B)
    b_ = np.linalg.solve(BT, b)
    z = np.dot(cB, b_)

    return b_, z, BT

def step_two(B, cB, N, BT):
    w = np.dot(cB, np.linalg.inv(BT))
    # z_non_basic = [np.dot(w, N(j)) for j in range(N.shape[0])]
    keys = []
    values = []
    for j in range(N.shape[0]):
        values.append(np.dot(w, N[j]))
        keys.append(tuple(N[j]))

    z_non_basic = dict(zip(keys, values))
    print(z_non_basic)

    return w, z_non_basic

def main():
    minimum = float('-inf')
    arq = open("teste.txt", "r")
    model, n_cols, n_rows = read_model(arq)
    A, B, N, b, c, cB, cN, basic_variables, non_basic_variables = create_model(model, n_cols, n_rows)

    # mantemos a matriz A original para comparacao
    # np.where((A == (2,3)).all(axis=1))

    while minimum < 0:
        b_, z, BT = step_one(B, b, cB)
        w, z_non_basic = step_two(B, cB, N, BT)
        break


if __name__ == "__main__":
    main()
