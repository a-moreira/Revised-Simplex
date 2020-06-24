# Two-Phase Revised Simplex

### Details 
Adaptation of the Revised Simplex Algorithm described in `Linear Programming and Network Flows 4th edition, by Bazaraa, Jarvis and Sherali`.


Additionally:
* The Two-Phase Method to provide a starting basic feasible solution for the original problem.
* Certificates of optimality, infeasibility and unboundedness
* The canonical LP form as input 


## Linear Programming
We wish to maximize a linear function subject to a set of linear constraints:
##### The canonical form
```                                                                                               
max   c'x                                           // c' is the transposed vector of costs,
s.t.                                                // x is the vector of decision variables,     
     Ax <= b                                        // A is the constraint matrix,
      x >= 0                                        // b is a constant vector
```

### Examples
##### Input
```
tests/test_1.txt

3 3                                           // number of constraints & variables
2 4 8                                         // 2x1 + x2 + x3 objective function
1 0 0 1                                       // 1x1 + 0x2 + 0x3 <= 1 constraint 1
0 1 0 1                                       // 0x1 + x2 + 0x3 <= 1 constraint 2
0 0 1 1                                       // 0x1 + 0x2 + x3 <= 1 constraint 3
```
##### Run
```
$ python3 simplex.py tests/test_1.txt
```

##### Output
```
optimal                                                         // status
14.0                                                            // objective function value
1.0 1.0 1.0 0.0 0.0 0.0                                         // certificate vector
2.0 4.0 8.0                                                     // decision vector  
```


#### License
This project is a free software licensed under GNU General Public License v2.0 or later.

