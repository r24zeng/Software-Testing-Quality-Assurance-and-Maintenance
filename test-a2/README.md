# ECE653: Software Testing Quality Assurance and Maintenance
# Assignment 2, Friday, July 5, 2019

+ a `user.yml` file with your UWaterloo user information;
+ a single pdf file called `a2_sub.pdf`, including all text answers;
+ a directory `a2q3` that includes code for Question 3;
+ a directory `wlang` that includes code for Question 4.


### Coding part
+ `./a1q3/coverage_tests.py` is unit test file which achieves node coverage, edge coverage, edge-pair coverage and prime path coverage for **Q3**.

+ `wlang` includes an implementation of a parser and interpreter for the **WHILE** language, coding `./wlang/test_int.py` to achieve `statement coverage` and `branch coverage` for the **Parse**, **Interpreter** and **AST** for **Q4**.


   To compute branch coverage, use the following command:  
   `(venv) $ coverage run --branch -m wlang.test`  
   `(venv) $ coverage html`  
   The result is stored in directory `hetmlcov`
   
### More details are in `./ece653-a1.pdf`