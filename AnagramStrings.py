def isAnagram(str1, str2):
    s1 = str1.replace(" ", "").lower()
    s2 = str2.replace(" ", "").lower()
    return sorted(s1) == sorted(s2)

s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

if isAnagram(s1, s2):
    print("The strings are anagrams of each other.")
else:
    print("The strings are NOT anagrams.")