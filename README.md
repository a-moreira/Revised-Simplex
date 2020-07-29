# Simplex

A simple implementation of the Simplex algorithm adapted from `Linear Programming and Network Flows 4th edition, by Bazaraa, Jarvis and Sherali`


## Linear Programming
We wish to maximize a linear function subject to a set of linear constraints in the form:
```                                                                                               
max   c'x                                           // c' is the transposed vector of costs,
s.t.                                                // x is the vector of decision variables,     
     Ax <= b                                        // A is the constraint matrix,
      x >= 0                                        // b is a non-negative constant vector
```

### Examples
##### Input
```
tests/test_1.txt

3 3                                           // number of constraints & variables
2 4 8                                         // 2x1 + x2 + x3, objective function
1 0 0 1                                       // 1x1 + 0x2 + 0x3 <= 1, constraint 1
0 1 0 1                                       // 0x1 + x2 + 0x3 <= 1, constraint 2
0 0 1 1                                       // 0x1 + 0x2 + x3 <= 1, constraint 3
```
##### Run
```
$ python3 main.py tests/test_1.txt
```

##### Output
```
optimal                                                         // status
14.0                                                            // objective function value
2.0 4.0 8.0                                                     // decision vector  
```

#### Disclaimer
This implementation serves an educational purpose and it's not optimized for huge instances. It can probably find your solution, but it might take forever. This version is not prepared to deal with degeneracy either.

#### License
This project is free software licensed under GNU General Public License v2.0 or later.
