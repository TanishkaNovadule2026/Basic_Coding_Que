# Count vowels 
def countVar(s):
    count = 0
    for ch in s:
        if ch in "aeiouAEIOU":
            count += 1
        else:
            continue
    print(count)

countVar("Hii I Am Intern In Novadule")