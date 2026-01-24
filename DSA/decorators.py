# def outer():
#     def inner():
#         return "I am inside!!"
#     return inner()
#
#
# my_var = outer
# print(my_var())

###############################################################

# def outer1():
#     def inner1():
#         return "I am inside!!"
#     return inner1
#
# my_var2 = outer1()
# print(my_var2())

#############################################################333

# def my_decorator(func):
#     def wrapper():
#         print("Something before the function")
#         func()
#         print("Something after the function")
#     return wrapper
#
# def say_hello():
#     print("Hello!")
#
# # Decorate the function
# decorated_hello = my_decorator(say_hello)
# decorated_hello()
#
# # Output:
# # Something before the function
# # Hello!
# # Something after the function

##############################################################3

# def my_decorator(func):
#     def wrapper():
#         print("Before function")
#         func()
#         print("After function")
#     return wrapper
#
# @my_decorator  # This is equivalent to: say_hello = my_decorator(say_hello)
# def say_hello():
#     print("Hello!")
#
# # print(say_hello) # <function my_decorator.<locals>.wrapper at 0x7708e7415c60>
# say_hello()

####################################################





