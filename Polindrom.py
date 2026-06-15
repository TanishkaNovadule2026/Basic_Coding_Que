s = "Naman"
str1 = s.lower()
s1 = ""
for ch in str1: 
    s1 = s1.join(ch)+s1
    
if(str1 == s1):
    print("Yes it is polindrom")
else:
    print("Not a polindrom")
