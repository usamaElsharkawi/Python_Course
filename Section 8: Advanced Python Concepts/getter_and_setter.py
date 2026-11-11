class Employee:
    def __init__(self,name):
        self.name = name
    @property
    def first_name(self):
        l = self.name.split(" ")
        return l[0]

    @first_name.setter
    def first_name(self,first):
        l = self.name.split(" ")
        newName = f"{first} {l[1]}"
        self.name = newName



e = Employee("usama mohamed")
print(e.first_name)
e.first_name = "mohsen"

print(e.name)
