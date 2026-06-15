s = "Hi Every One I am Tanishka Soni"

str1 = s.lower()

dicti = {}

for char in str1:
    if(char not in dicti):
        dicti[char] = 1
        
    else :
        dicti[char] += 1
    
print(dicti)