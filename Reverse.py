s = "Hello world"
result = ""

# By using join method 
for ch in s: 
    result = result.join(ch)+result
    
print(result)
