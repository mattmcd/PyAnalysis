# Fizz Buzz example 

# Simple version with nested if statements
def fizzbuzz(x):
    if (x % 3 == 0) and (x % 5 == 0):
        return "FizzBuzz"
    else:
        if x % 3 == 0:
            return "Fizz"
        else:
            if x % 5 ==0:
                return "Buzz"
            else:
                return x
    
#  Generic version: define a set of predicate functions 
p1 = lambda(x): x % 3 == 0
p2 = lambda(x): x % 5 == 0
p3 = lambda(x): p1(x) and p2(x)

# Create mapping from predicate function to action
fbLst = [(p3, "FizzBuzz"), (p1, "Fizz"), (p2, "Buzz")]

# Generic fizz buzz creator. 
def mkFizzBuzz(lst):
    lc = lst[:] # Copy input list
    # Helper function
    def aux(x):
        for el in lc:
            if el[0](x):
                return el[1]
        return x 
    return aux

fizzbuzz2 = mkFizzBuzz(fbLst)