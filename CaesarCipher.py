def ccEncrypt(text, shift):
    encrypted = []
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            encChar = chr((ord(char) - base + shift) % 26 + base)
            encrypted.append(encChar)
        else:
            encrypted.append(char)
    return "".join(encrypted)

txtt = input("Enter text to encrypt: ")
shiftt = int(input("Enter shift amount (integer): "))

print(f"Encrypted Text: {ccEncrypt(txtt, shiftt)}")