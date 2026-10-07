import math
from requests import get



num = math.remainder(5,2)

print(num)



def rd():
    global num
    num = num *2 
    return num


print(rd())


