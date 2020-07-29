from sys import argv
import simplex

def main():
    
    new_file = open(argv[1], "r")
    model, n_rows, n_cols = simplex.read_model(new_file)
    c, A, b, non_basic, basic = simplex.create_model(model, n_rows, n_cols)

    # _xB, _basic, _non_basic = simplex.solve_auxiliary_lp(A, b)

    if (b < 0).any():
        print("\nThere are negative elements in the b vector.\nI'm sorry, I can't solve this yet :-(\n")
        return

    # check = simplex.check_feasibility(A, b)
    # print(check) 
    # if check is False:
    #     A, b, c, basic, non_basic = simplex.create_auxiliary(A, b)
    #     z, w, xB, basic, status = simplex.solve(A, b, c, basic, non_basic) 

    z, w, xB, basic, status = simplex.solve(A, b, c, basic, non_basic)
    print("obj:", z)
    print("basic variables", basic, "with values:", xB)
    print("status:", status)

if __name__ == "__main__":
    main()
