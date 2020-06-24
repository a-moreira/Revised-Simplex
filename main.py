from sys import argv
import simplex

def main():
    new_file = open(argv[1], "r")
    model, n_rows, n_cols = simplex.read_model(new_file)
    c, A, b, non_basic, basic = simplex.create_model(model, n_rows, n_cols)
    z, w, xB, basic, status = simplex.solve(A, b, c, basic, non_basic)
    print("obj:", z)
    # print("solution variables", basic)
    # print("their values:", xB)
    print("solution", xB)
    print("status:", status)

if __name__ == "__main__":
    main()
