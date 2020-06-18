# Two-Phase Revised Simplex

### Details 
Adaptation of the Revised Simplex Algorithm as described in `Linear Programming and Network Flows 4th edition, by Bazaraa, Jarvis and Sherali`.


Additional features:
* The Two-Phase Method to provide a starting basic feasible solution for the original problem.
* Certificates of optimality, infeasibility and unboundedness
* The canonical LP form as input 


## Linear Programming
We wish to maximize an affine function subject to a set of linear constraints:
##### The canonical form
```                                                                                               
max   c'x                                                        where c' is the transposed vector of costs,
s.t.                                                                   x is vector of decision variables,     
     Ax <= b                                                           A is the constraint matrix        
      x >= 0                                                           b is constant vector
```

### Examples
##### Input
The tests file format as follows:
```
tests/test_1.txt

3 3                                                                                // number of constraints & variables
2 4 8                                                            2x + 4y + 8z      // objective function
1 0 0 1                                                          1x + 0y + 0z <= 1 // constraint 1
0 1 0 1                                                          0x + 1y + 0z <= 1 // constraint 2
0 0 1 1                                                          0x + 0y + 1z <= 1 // constraint 3
```
Run

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
