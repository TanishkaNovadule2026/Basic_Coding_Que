from functools import reduce 

'''import dis 
import keyword
def add(a, b):
    return a * b

print(dis.dis(add))

x = b"hello"
print(x[0])

print(keyword.kwlist)

'''
'''fruits = ["Apple", "Banana"]
print(id(fruits))

x = [1,3,5]
y = [1, 3, 5]

print(x != y)
print(x is y) # It use use memory reference or not 

result = None 
print(result == None)
print (result is None)

print(result is not None)

print(result != None)

'''
"""print(5 | 3) # |, &, ! it use in bitwise operator 
"""

"""def my_funcion(name, /, surname="Hens"):
    print("Hello", name, surname)

my_funcion("Emil")

def my_function(*, name):
  print("Hello", name)"""

"""my_function(1, 2, name = "Emil")"""
"""
def disp_profile(**kwargs):
   for key, value in kwargs.items():
      print(f"{key} : {value} \t", end="\t")
      

disp_profile(name="Emil", age=30, city="Landon")
"""

# Convert String into upper case without upper()

"""def to_upper(s):
    result =""
    for ch in s: 
        if 'a'<= ch <= 'z':
            result += chr(ord(ch) - 32)
        else: 
            result += ch 
    print(result)
to_upper("hello world")"""
 
# Lambda program 
"""to_upper = lambda s : print(s.upper())

to_upper("don't worry be happy you always win ")

square = lambda *x : [print(i**2, end="\t") for i in x]
square(*range(1, 11))
"""
"""
add_y = lambda a, b: a + b + 10

x = int(input("Enter a number : "))
y = int(input("Enter a number : "))

print(add_y(x, y))"""

# Lambda function real use case print in list comprehension 
"""func = [lambda arg = x: arg * 10 for x in range(1, 5)]
for i in func:
    print(i())"""

# map, lis, filter, reduce, zip, enumerate, all, any, sorted, reversed, sum, min, max, abs, round, pow

"""a = [1,23,4,5,6,7,8,4,242,9]
b = ["Alice", "bob"]

print(list(zip(a,b)))
"""
"""map_result = map(lambda x: x/2, a)

print(list(map_result))"""
"""
add = reduce(lambda x, y: x+y, a)

print(add)

for indx, value in enumerate(a):
    print(indx, value)

print(all(x%2 == 0 for x in a))"""


"""s = "Hello World"
vowels = [ch for ch in s if ch.lower() in 'aeiou']

print(vowels)


matrix = [[1,2,3], [4,5,6], [6,4,3]]
flat = [num for i in matrix for num in i]
print(flat)"""


# Remove duplicate elment from list using List comprehension

a = [1,1,2,3,4,2,2,5,6,7,78,10]

res = []
"""[res.append(i) for i in a if i not in res]

print(res)"""

# Using a loop 
"""for i in a:
    if i not in res:
        res.append(i)
print(res)"""

"""Sort a List : sort() -> Original change,
sorted() -> Return a new sorted list (Original unchanges )

Sort by custom key : Sort String by length 
"""

"""words = ["banana", "apple", "kiwi", "mango"]

words.sort(key=len )
print(words)

data = [(1, 'z'), (2, 'a'), (3, 'm')]

data.sort(key=lambda x: x[1])


print(data)
"""

# Decorators : Add extra behavior to a function, without changing the function's code 
# A decorator is a function that takes another function as input and returns a new function.

# @decorator_name 

"""def changecase(func):
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Hello Sally"

print(myfunction())
"""

student = {1: "Alice", "age": 20, "city": "New Delhi"}

"""print(student.get("City"))


for key in student:
    print(key)

for key, value in student.items():
    print(key," : ", value)"""

# Dictionary comprehension 
"""squares = {x: x**2 for x in range(5)}
print(squares)

students = {"Alice": 20, "Bob": 15, "Charlie": 18}

adult = {key: value for key, value in students.items() if value > 18}
print(adult)

"""

# a = int(input("Enter a number : "))
"""try: 
    x = 10/a
    
except Exception as e:
    print(f"{e}")
else: 
    print(f"{x:.2f}")
finally: 
    print("Program finished")"""
 
"""if a <= 0:
    raise ValueError("Input must be a positive and greater than 0")
else:
    print(f"{15/a:.2f}")
"""

# Custom Exception 

"""class AgeError(Exception):
    pass

age = int(input(("Enter your Age :")))

if(age < 0):
    raise AgeError("You are not born now ")
elif age > 150:
    raise AgeError("In kalyug not possible ")
else: 
    print(f"Your age is {age}")"""

"""class Car:
    def __init__(self,  model, year, color):
        self.model = model
        self.year = year
        self.color = color 

    def drive(self):
        print(f"{self.model} jhakaas")

# Object creation 
car1 = Car("Mahindra", 2025, "black")
car2 = Car("Honda", 2026, "Blue")

print(car1.model, end="   ")
print(car2.color)

print("----------------__________Testing _______________------------------" )
car1.drive()

"""

# Polymorphism method overriding same method implementation in different class 

"""class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model 

    def move(self):
        print("Drive ")

class Boad:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model 

    def move(self):
        print("Sail")

class Plane:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model 
    
    def move(self):
        print("Fly!")

# Create a object 
car1 = Car("Ford", "Mustang")
b1 = Boad("Ibiza", "Touring 20")
f1 = Plane("Indigo ", "747")

for x in (car1, b1, f1):
  x.move()

"""
# Operator overloading 
"""class Employee:
    def __init__(self, a):
        self.a = a
    
    def __add__(self, o):
        return self.a + o.a
# Make a object of Employee class 
emp1 = Employee(45)
emp2 = Employee(45)

print(emp1 + emp2)"""

"""class Employee:
    def __init__(self, a):
        self.a = a
    
    def __gt__(self, o):
        return self.a > o.a
# Make a object of Employee class 
emp1 = Employee(25)
emp2 = Employee(30)

if emp1 > emp2:
    print("True ")

else: 
    print("False")"""