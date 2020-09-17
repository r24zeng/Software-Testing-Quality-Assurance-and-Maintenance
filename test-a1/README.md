Requirements refer to [ece653-a1.pdf](https://github.com/r24zeng/Software-Testing-Quality-Assurance-and-Maintenance/blob/master/test-a1/ece653-a1.pdf)


# ECE653: Software Testing Quality Assurance and Maintenance
# Assignment 1, Friday, June 7, 2019

+ a `user.yml` file with your UWaterloo user information;
+ a single pdf file called `a1_sub.pdf`, including all text answers;
+ a directory `a1q3` that includes code for Question 3;
+ a directory `wlang` that includes code for Question 4.


### Coding part
+ `./a1q3/coverage_tests.py` is unit test file which achieves node coverage, edge coverage, edge-pair coverage and prime path coverage for **Q3**.

+ `wlang` includes an implementation of a parser and interpreter for the **WHILE** language, coding `./wlang/test_int.py` to achieve `statement coverage` and `branch coverage` for the **Parse**, **Interpreter** and **AST** for **Q4**.


   To compute branch coverage, use the following command:  
   `(venv) $ coverage run --branch -m wlang.test`  
   `(venv) $ coverage html`  
   The result is stored in directory `htmlcov`
   
   
