def divStr(s, n):
    if len(s) % n != 0:
        raise ValueError(
            f"Error: String length ({len(s)}) is not divisible by {n}."
        )
    parts = [s[i : i + n] for i in range(0, len(s), n)]
    first_part = parts[0]
    if not all(part == first_part for part in parts):
        raise ValueError("Error: Sequences in divided parts are not identical.")
    return parts

str = input("Enter string: ")
l = int(input("Enter part length (n): "))

try:
    result = divStr(str, l)
    print("Output:", ", ".join(f'"{p}"' for p in result))
except ValueError as e:
    print(e)