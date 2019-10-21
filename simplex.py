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
    c = np.append(cN, cB)
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
        entering_var_index = min_non_basic.index(minimum)
        y = np.linalg.solve(np.linalg.inv(B), N[entering_var_index])

        if (y <= 0).all():
            print("ilimitada")

        ratio_test = []

        for i in range(len(basic_variables)):
            ratio_test.append(b[i] / y[i])

        leaving_var_index = n_rows + ratio_test.index(min(ratio_test))
        basic_variables.remove(leaving_var_index)
        basic_variables.append(entering_var_index)
        non_basic_variables.remove(entering_var_index)
        non_basic_variables.append(leaving_var_index)

        leaving_var = A[leaving_var_index]
        entering_var = A[entering_var_index]
        leaving_var_cost = c[leaving_var_index]
        entering_var_cost = c[entering_var_index]

        # atualizamos B, N, cB e cN
        # essa forma esta deletando todas as ocorrencias
        # talvez seja melhor usar o indice ou um for loop
        B = np.vstack([B, entering_var])
        N = np.vstack([N, leaving_var])

        B = np.delete(B, np.where((leaving_var == B).all(1)), 0)
        N = np.delete(N, np.where((entering_var == N).all(1)), 0)
        print(cB)
        print(cN)
        """
        for i in cB:
            if i == leaving_var_cost:
                cB = np.delete(cB, leaving_var_cost.index())
                break

        for i in cN:
            if  i == entering_var_cost:
                cN = np.delete(cN, leaving_var_cost.index())
                break

        """
        # cB = cB[(leaving_var_cost != cB)]
        # cN = cN[(entering_var_cost != cN)]
        print(np.where(leaving_var_cost == cB)[0][0])
        cB = np.delete(cB, np.where(leaving_var_cost == cB)[0][0])
        cN = np.delete(cN, np.where(entering_var_cost == cN)[0][0])
        cB = np.append(cB, entering_var_cost)
        cN = np.append(cN, leaving_var_cost)

        print(cB)
        # print(B)
        print(cN)
        # print(N)

    if minimum >= 0:
        print("otima")







if __name__ == "__main__":
    main()

