# ECE653: Software Testing Quality Assurance and Maintenance
# Assignment 2, Friday, July 5, 2019

+ a `user.yml` file with your UWaterloo user information;
+ a single pdf file called `a2_sub.pdf`, including all text answers;
+ a directory `a2q3` that includes code for Question 3;
+ a directory `wlang` that includes code for Question 4.


### Coding part
+ Use Z3 Python API to implement a solver for magic square puzzles in `./a2q3/magic_square.py` and its test case in `./a2q3/puzzle_tests.py.`
   Execute the test case in `./a2q3/puzzle_tests.py` using :  
   `python -m a2q3.test`
+ An implementation of symbolic interpreter for the **WHILE** language in `./wlang/sym.py`, extend it to implemnt symbolic execution. And coding test suites `./wlang/test_sym.py` to achieve 100% `branch coverage` for it for **Q4**.

   To run the test suites using:  
   `(venv) $ python -m wlang.test`  
   To compute branch coverage, use the following command:  
   `(venv) $ coverage run --branch -m wlang.test`  
   `(venv) $ coverage html`  
   The result is stored in directory `hetmlcov`
   
### More details are in `./a2.pdf`
