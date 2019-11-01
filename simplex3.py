import numpy as np


def read_model(arq):
    lines_list = arq.readlines()
    n_cols, n_rows = (int(val) for val in lines_list[0].split())
    model = [[int(val) for val in line.split()] for line in lines_list[1:]]

    return model, n_cols, n_rows




def create_model(model, n_cols, n_rows):
    n_var = n_cols + n_rows
    c = np.asarray(model[0])
    A = np.asarray(model[1:])
    b = A[:,-1]
    A = np.delete(A, -1, 1)
    I = np.identity(n_rows)
    c = np.append(c, np.zeros(n_rows))
    A = np.append(A, I, axis=1)
    non_basic = [i for i in range(n_cols)]
    basic = [i + n_cols for i in range(n_rows)]
    return c, A, b, non_basic, basic

def step_one(A, b):
    b_ = np.linalg.solve()







def main():
    minimum = float('-inf')
    arq = open("teste.txt", "r")
    model, n_cols, n_rows = read_model(arq)
    # A, B, N, b, c, cB, cN, basic_variables, non_basic_variables = create_model(model, n_cols, n_rows)
    c, A, b, non_basic, basic = create_model(model, n_cols, n_rows)
    # mantemos a matriz A original para comparacao
    # np.where((A == (2,3)).all(axis=1))
    print(c)
    print(A)
    print(b)
    print(non_basic)
    print(basic)

    while minimum < 0:
        # b_, z, BT = step_one(B, b, cB)
        # w, z_non_basic = step_two(B, cB, N, BT)
        break


if __name__ == "__main__":
    main()








