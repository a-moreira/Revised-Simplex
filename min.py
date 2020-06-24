import numpy as np
from sys import argv

# aux = float("inf")

def read_model(test_file):
    lines_list = test_file.readlines()
    n_rows, n_cols = (int(val) for val in lines_list[0].split())
    model = [[int(val) for val in line.split()] for line in lines_list[1:]]

    return model, n_rows, n_cols

def create_model(model, n_rows, n_cols):
    c = np.asarray(model[0])
    A = np.asarray(model[1:])
    b = A[:, -1]
    A = np.delete(A, -1 , 1)
    Id = np.identity(n_rows)
    c = np.append(c, np.zeros(n_rows))
    A = np.append(A, Id, axis=1)
    # m = min(n_cols, n_rows)
    # n = max(n_cols, n_rows)
    non_basic = [i for i in range(n_cols)]
    basic = [i + n_cols for i in range(n_rows)]

    return c, A, b, non_basic, basic

def step_one(A, b, c, basic, non_basic):
    xB = np.linalg.solve(A[:, basic], b)
    z = np.dot(c[tuple([basic])], xB)

    return xB, z

def step_two(A, b, c, basic, non_basic, xB):
    aux = -1.0 * float("inf")
    idx = -1
    w = np.linalg.solve(np.transpose(A[:, basic]), c[tuple([basic])])
    for j in non_basic:
        price = np.dot(w, A[:, j]) - c[j]
        if price > aux:
            idx = j
            aux = price

    return w, aux, idx

def step_three(A, idx, basic):
    y = np.linalg.solve(A[:, basic], A[:, idx])
    
    return y

def step_four(A, b, y, basic):
    aux = float("inf")
    for i in range(len(basic)):
        if y[i] > 0:
            ratio = b[i] / y[i]
            if ratio < aux:
                aux = ratio
                idx = i
    leaving_var = basic[idx]

    return leaving_var

def solve(A, b, c, basic, non_basic):
    while True:
        print("A", A)
        print("b", b)
        print("c", c)
        print("basic", basic)
        print("non_basic", non_basic)
        xB, z = step_one(A, b, c, basic, non_basic)
        w, aux, idx = step_two(A, b, c, basic, non_basic, xB)
        print("w", w)
        print("aux", aux)
        print("idx", idx)
        if aux <= 0:
            status = "optimal"
            break
        else:
            aux = float("inf")
        
        y = step_three(A, idx, basic)
        print ("y", y)
        
        if (y <= 0).all():
            status = "unlimited"
            break
        
        leaving_var = step_four(A, b, y, basic)
        print("leaving_var", leaving_var)

        non_basic.remove(idx)
        basic.append(idx)
        basic.remove(leaving_var)
        non_basic.append(leaving_var)
        basic.sort()
        non_basic.sort()

        
    return z, w, status

def main():
    test_file = open(argv[1], "r")
    model, n_rows, n_cols = read_model(test_file)
    c, A, b, non_basic, basic = create_model(model, n_rows, n_cols)
    z, w, status = solve(A, b, c, basic, non_basic)
    print("z", z)
    print("w", w)
    print("status", status)

if __name__ == "__main__":
    main()
