#Find a second largest number in a list 
num = [-23, 0, 45, 90, 1, 2]

Largest = max(num)
secLar = max(filter(lambda x : x != Largest, num))

print(secLar)