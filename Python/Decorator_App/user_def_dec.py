def user_dec(func):
    print("Enter Decorator")
    def wrapper(*args,**kwargs):
        return func(*args,**kwargs)
    return wrapper


@user_dec
def add_num(a,b):
    return a+b

print(add_num(a=1,b=2))


