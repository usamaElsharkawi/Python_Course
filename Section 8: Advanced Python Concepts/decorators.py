

def decorator(func):
    def wrapper(a):
        # do some logic befor calling the passed func
        print("We are about execute the func")
        func(a)
        # do some loginc after calling the passed func
        print("we have executed the func")
    return wrapper


@decorator
def say_hello(a):
    print(f"Hello {a}")


say_hello("usama")








