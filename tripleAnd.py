def triple_and(a, b, c):
    return bool(a and b and c)

v1 = input("Enter first boolean (True/False): ").strip().lower() == "true"
v2 = input("Enter second boolean (True/False): ").strip().lower() == "true"
v3 = input("Enter third boolean (True/False): ").strip().lower() == "true"

print(f"Result: {triple_and(v1, v2, v3)}")