def selectSort(s):
    s = s.lower() 
    arr = list(s)
    n = len(arr)
    for i in range(n):
        p = i
        for j in range(i + 1, n):
            if arr[j] < arr[p]:
                p = j
        arr[i], arr[p] = arr[p], arr[i]
    return "".join(arr)

s = input("Enter a string to sort: ")
print(f"Sorted String: {selectSort(s)}")