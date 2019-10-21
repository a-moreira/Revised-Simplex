import numpy as np

def read_model(arq):
    model = np.loadtxt(arq)

    return model


def main():
    arq = open("teste.txt", "r")
    lines_list = arq.readlines()
    n_cols, n_rows = (int(val) for val in lines_list[0].split())
    model = [[int(val) for val in line.split()] for line in lines_list[1:]]

    n_var = n_cols + n_rows
    c = np.asarray(model[0])
    A = np.transpose(model[1:])
    b = A[-1]
    A = np.delete(A, -1, 0)
    N = A
    B = np.identity(n_rows)
    cN = c
    cB = np.zeros(n_cols)
    A = np.vstack([A, B])
    # indexes of the basic and non basic variables
    non_basic_variables = [i for i in range(n_cols)]
    basic_variables = [i+n_cols for i in range(n_rows)]


    minimum = float('-inf')


    while minimum < 0:

        b_ = np.linalg.solve(np.linalg.inv(B), b)
        z = np.dot(cB, b_)

        w = np.dot(cB, np.linalg.inv(B))
        z_non_basic = []
        for j in range(len(non_basic_variables)):
            z_non_basic.append(np.dot(w, N[j]))

        min_non_basic = []
        for i in range(len(non_basic_variables)):
            aux = z_non_basic[i] - cN[i]
            min_non_basic.append(aux)


        minimum = min(min_non_basic)
        entering_var = min_non_basic.index(minimum)
        y = np.linalg.solve(np.linalg.inv(B), N[entering_var])

        if (y <= 0).all():
            print("ilimitada")

        ratio_test = []
        for i in range(len(basic_variables)):
            ratio_test.append(b[i] / y[i])

        leaving_var = n_rows + ratio_test.index(min(ratio_test))
        basic_variables.remove(leaving_var)
        basic_variables.append(entering_var)
        non_basic_variables.remove(entering_var)
        non_basic_variables.append(leaving_var)


        # manter a matriz original intacta para comparação
        # acho que vai ser melhor do que usar dict
        # B = np.delete(B, leaving_var)
        # N = np.delete(N, entering_var)

        print(B)
        print(N)


    if minimum >= 0:
        print("otima")







if __name__ == "__main__":
    main()
