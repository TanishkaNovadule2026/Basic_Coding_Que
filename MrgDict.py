#Merge two dictionaries 

dict1 = {1: "emp1", 2: "emps2"}
dict2 = {3: "emp3", 4: "emp4"}

list1 = list(dict1.values())
list2 = list(dict2.values())

NewList = []
for i in list1: 
    NewList.append(i)
for i in list2:
    NewList.append(i)
    
print(NewList)
# dictionary comprehension
result = {NewList: i for i, NewList in enumerate(NewList, start=1)}
print(result)