# without recursion Find a facorial 
def fact(a):
    facto = 1
    while(a != 0):
        facto *= a 
        a -= 1
    print(facto)
    
b = int(input("Enter number "))
fact(b)

    
#recursion 
"""def fact(num):
    if(num == 1):
        return 1
    else:
        return num * fact(num - 1)
    
b = int(input("Enter number "))    #479001600
print(fact(b))
    """