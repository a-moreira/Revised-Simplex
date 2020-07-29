import numpy as np

def read_model(test_file):
    lines_list = test_file.readlines()
    n_rows, n_cols = (int(val) for val in lines_list[0].split())
    model = [[float(val) for val in line.split()] for line in lines_list[1:]]

    return model, n_rows, n_cols

def create_model(model, n_rows, n_cols):
    c = np.asarray(model[0])
    A = np.asarray(model[1:])
    b = A[:, -1]
    A = np.delete(A, -1 , 1)
    Id = np.identity(n_rows)
    c = np.append(c, np.zeros(n_rows))
    A = np.append(A, Id, axis=1)
    non_basic = [i for i in range(n_cols)]
    basic = [i + n_cols for i in range(n_rows)]

    return c, A, b, non_basic, basic

def step_one(A, b, c, basic, non_basic):
    xB = np.linalg.solve(A[:, basic], b)
    z = np.dot(c[tuple([basic])], xB)

    return xB, z

def step_two(A, b, c, basic, non_basic, xB):
    aux = float("inf")
    idx = -1
    w = np.linalg.solve(np.transpose(A[:, basic]), c[tuple([basic])]) # transposed because wB = c = B^T w^T
    for j in non_basic:
        price = np.dot(w, A[:, j]) - c[j]
        if price < aux:
            idx = j
            aux = price

    return w, aux, idx

def step_three(A, idx, basic):
    y = np.linalg.solve(A[:, basic], A[:, idx])
    
    return y

def step_four(A, b, y, basic, xB):
    aux = float("inf")
    for i in range(len(basic)):
        if y[i] > 0:
            ratio = xB[i] / y[i]
            if ratio < aux:
                aux = ratio
                idx = i
    leaving_var = basic[idx]
    return leaving_var

def solve(A, b, c, basic, non_basic):
    while True:
        # print("basic", basic)
        # print("non_basic", non_basic)
        xB, z = step_one(A, b, c, basic, non_basic)
        w, aux, idx = step_two(A, b, c, basic, non_basic, xB)
        # print("w", w)
        # print("aux", aux)
        # print("idx", idx)
        # print("z", z) 
        if aux >= 0:
            status = "optimal"
            break
        else:
            aux = float("inf")
        
        y = step_three(A, idx, basic)
        # print ("y", y)
        
        if (y <= 0).all():
            status = "unbounded"
            break
        
        # print("basic", basic) 
        leaving_var = step_four(A, b, y, basic, xB)
        # print("leaving_var", leaving_var)

        non_basic.remove(idx)
        basic.append(idx)
        basic.remove(leaving_var)
        non_basic.append(leaving_var)
        basic.sort()
        non_basic.sort()
        
    return z, w, xB, basic, status

# TODO

#def check_feasibility(A, b):
#    n_rows, n_cols = A.shape
#    if (b < 0).any():
#        negative_idx = np.where(b < 0)
#        negative_idx = [i for i in negative_idx[0]]
#        A = -1.0*A[negative_idx]
#        b = -1.0*b[negative_idx]
#        A = np.append(A, np.identity(n_rows), axis=1)
#        check = False
#    else:
#        check = True
#    return check
#
#def create_auxiliary(A, b):
#    new_A = A
#    new_b = b
#    n_rows, n_cols = A.shape
#    new_c = np.zeros(n_cols + 2*n_rows)
#    new_c[n_cols + n_rows : ] = -1
#    Id = np.identity(n_rows)
#    new_A = np.append(new_A, Id, axis=1)
#    new_non_basic = [i for i in range(n_cols)]
#    new_basic = [i + n_cols for i in range(n_rows)] 
#
#    return new_A, new_b, new_c, new_basic, new_non_basic
