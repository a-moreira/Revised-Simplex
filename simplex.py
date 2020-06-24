import numpy as np
from sys import argv

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
    print(A)
    print(c)
    print(b)
    print(non_basic)
    print(basic)

    return c, A, b, non_basic, basic


def step_one(A, b, c, basic, non_basic):
    xB = np.linalg.solve(A[:, basic], b)
    z = np.dot(c[tuple([basic])], xB)

    return xB, z


def step_two(A, b, c, basic, non_basic, xB, minimum):
    w = np.linalg.solve(np.transpose(A[:, basic]), c[tuple([basic])])
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


def step_four(A, b, y, basic, minimum_2, xB):
    for i in range(len(basic)):
        if y[i] > 0:
            aux = xB[i] / y[i]
            if aux < minimum_2:
                minimum_2 = aux
                idx = i

    leaving_var = basic[idx]
    return leaving_var


def solve(c, A, b, non_basic, basic, minimum, minimum_2):

    while True:
        xB, z = step_one(A, b, c, basic, non_basic)

        print("xB", xB)
        print("z", z)

        # idx is the index of the variable entering the base
        # w is the certificate
        w, minimum, idx = step_two(A, b, c, basic, non_basic, xB, minimum)

        print("w", w)
        print("idx", idx)

        if minimum >= 0:
            status = "optimal"
            break
        else:
            minimum = float('inf')
        y = step_three(A, idx, basic)

        print("y", y)

        if (y <= 0).all():
            status = "unlimited"
            break

        leaving_var = step_four(A, b, y, basic, minimum_2, xB)
        print("leaving", leaving_var)
        print("basis", basic)

        non_basic.remove(idx)
        basic.append(idx)
        basic.remove(leaving_var)
        non_basic.append(leaving_var)
        basic.sort()
        non_basic.sort()

        print("z", z)

    return z, w, status, xB


def main():
    minimum = float('inf')
    minimum_2 = float('inf')
    arq = open(argv[1], "r")
    model, n_cols, n_rows = read_model(arq)
    c, A, b, non_basic, basic = create_model(model, n_cols, n_rows)
    first_basic = basic

    # here we build and auxiliary problem to check feasibility
    # if the objective value is 0, continue
    # else, the original LP is infeasible
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
        non_basic2 = [i for i in range(n_cols + n_rows)]
        basic2 = [i+n_rows+n_cols for i in range(n_rows)]
        z, w, status, xB = solve(c2, A2, b2, non_basic2, basic2, minimum, minimum_2)

        # if the auxiliary problem has objective < 0, it's over
        # our original problem is infeasible
        if z < 0:
            status = "infeasible"

        # if the auxiliary problem has objective >=0, we solve the
        # original problem with this base
        else:
            z, w, status, xB = solve(c, A, b, non_basic, basic, minimum, minimum_2)

    else:
        z, w, status, xB = solve(c, A, b, non_basic, basic, minimum, minimum_2)

    solution = [0. for i in range(n_cols + n_rows)]
    solution = {key: value for (key, value) in zip(basic, xB)}

    x = [0. for i in range(n_rows+n_cols)]

    for key in solution:
        x[key] = solution[key]

    # x = x[:n_cols]

    if status == "unlimited":
        w = np.zeros(n_cols+n_rows)
        aux = np.where((A[1:] < 0).all(axis=0))
        w[aux[0][0]] = 1
        aux2 = A[:, aux[0][0]]
        w[first_basic] = -1.0*aux2

    w = w.tolist()

    if status == "optimal":
        print(status)
        print(z)
        print(*x)
        print(*w)
    elif status == "unlimited":
        print(status)
        print(*x)
        print(*w)
    elif status == "infeasible":
        print(status)
        u = [-1.0*v for v in w]
        print(*u)



if __name__ == "__main__":
    main()
