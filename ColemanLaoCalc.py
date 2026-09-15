def CL_index(text):
    letters = sum(c.isalpha() for c in text)
    words = len(text.split())
    sentences = text.count(".") + text.count("!") + text.count("?")
    if words == 0:
        return "Before Grade 1"
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    if index >= 16:
        return "Grade 16+"
    elif index < 1:
        return "Before Grade 1"
    else:
        return f"Grade {index}"

text = input("Enter paragraph/text: ")
print("Calculated Grade Level:", CL_index(text))