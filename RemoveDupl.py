# Remove duplicates from a list 

num = [1,2,3,1,2]
List = []
"""
# Use List comprehension 
[List.append(n) for n in num if n not in List]
print(List )"""

#
for n in num: 
    if n not in List:
        List.append(n)
    else:
        n += 1
        
print(List)


