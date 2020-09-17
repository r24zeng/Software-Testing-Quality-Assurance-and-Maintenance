Requirements refer to [a3.pdf](https://github.com/r24zeng/Software-Testing-Quality-Assurance-and-Maintenance/blob/master/test-a3/a3.pdf)

# ECE653: Software Testing Quality Assurance and Maintenance
# Assignment 3, Friday, July 26, 2019

+ a `user.yml` file with your UWaterloo user information;
+ a single pdf file called `a3_sub.pdf`, including all text answers;
+ a directory `dafny` that includes code for Question 2 and 3;
+ a directory `wlang` that includes code for Question 4.


### Coding part
+ Adding **invariants** and **decreases** annotations by **dafny** to verify Q2 and 3 in `./dafny`
+ Extend the symbolic execution engine to a verification engine in `./wlang` and extend `./wlang/est_sym.py` to achieve 100% branch coverage for this imiplementation.  

   To run the test suites using:  
   `(venv) $ python -m wlang.test`  
   To compute branch coverage, use the following command:  
   `(venv) $ coverage run --branch -m wlang.test`  
   `(venv) $ coverage html`  
   The result is stored in directory `htmlcov`
   

