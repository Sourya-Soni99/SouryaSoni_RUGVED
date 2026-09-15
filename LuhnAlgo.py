def isValid(number):
    digits = [int(d) for d in str(number) if d.isdigit()]
    s = 0
    rev = digits[::-1]
    for idx, digit in enumerate(rev):
        if idx % 2 == 1:
            doubled = digit * 2
            s += doubled - 9 if doubled > 9 else doubled
        else:
            s += digit
    return s % 10 == 0

num = input("Enter credit card number: ")
if isValid(num):
    print("Valid Credit Card Number.")
else:
    print("Invalid Credit Card Number.")