def outer():
    def inner():
        return "I am inside!!"
    return inner()


my_var = outer
print(my_var())

###############################################################

def outer1():
    def inner1():
        return "I am inside!!"
    return inner1

my_var2 = outer1()
print(my_var2())

#############################################################333

def my_decorator(func):
    def wrapper():
        print("Something before the function")
        func()
        print("Something after the function")
    return wrapper

def say_hello():
    print("Hello!")

# Decorate the function
decorated_hello = my_decorator(say_hello)
decorated_hello()

# Output:
# Something before the function
# Hello!
# Something after the function

##############################################################3

def my_decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

@my_decorator  # This is equivalent to: say_hello = my_decorator(say_hello)
def say_hello():
    print("Hello!")

# print(say_hello) # <function my_decorator.<locals>.wrapper at 0x7708e7415c60>
say_hello()

####################################################

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

print(add(5, 3))
print(add) # <function my_decorator.<locals>.wrapper at 0x7a74de915c60>

"""
THE FUNCTION WHICH IS BEING DECORATED WHICH WHEN CALLED ACTUALLY CALLS THE WRAPPER FUNCTION INSIDE THE DECORATOR
"""

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print("started")
        result = func(*args, **kwargs)
        print("started result")
        end = time.time()
        print("ended result")
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    print("going to sleep")
    time.sleep(1)
    print("sleep done")
    return "Done!"

print(slow_function())  # Output: slow_function took 1.0001 seconds

"""
started
going to sleep
sleep done
started result
ended result
slow_function took 1.0002 seconds
Done!
"""
