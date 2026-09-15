def findFirstReapt(arr):
    seen = set()
    p = -1

    for i in range(len(arr) - 1, -1, -1):
        if arr[i] in seen:
            p = i
        else:
            seen.add(arr[i])

    if p != -1:
        return arr[p], p
    return None, -1

arr_str = input("Enter array elements separated by spaces: ")
arr = list(map(int, arr_str.split()))

element, idx = findFirstReapt(arr)
if idx != -1:
    print(f"First repeating element is {element} at index {idx}.")
else:
    print("No repeating elements found.")