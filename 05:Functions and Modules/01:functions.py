# a,b,c = 4,2,1
# a1,b1,c1 = 6,4,2


# def avrage(a,b,c):
#     avg= (a+b+c) / 3.0
#     return avg



# o1 = avrage(a,b,c)
# o2 = avrage(a1,b1,c1)

# print(o1,o2,)

# print(type(avrage))


# def sum_all(*args):
#     return sum(args)



# print(sum_all(1,2,4))


def greeting(greating,*names):
    for name in names:
        print(f"{greating},{name}")



greeting("hello","osama","mohsen","zharaa")