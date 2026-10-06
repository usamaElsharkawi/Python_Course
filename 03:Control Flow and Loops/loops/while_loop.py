
# i = 1

# while i < 6:
#     print(i)
#     i = i + 1


# input validation

while True:
    age = input("Enter age (or 'q' to quit): ")
    if age == 'q':
        break
    if not age.isdigit():
        print("Please Enter a Numper")
        continue
    age = int(age)
    if age < 0 or age > 150:
        print("Unrealistic Number")
        continue
    print("valid age:",age)
    break
