class Dog:
    species = 'Mammal'
    danger_lvl = 10

    def __init__(self, name, weight, age, color):
        self.name = name
        self.weight = weight
        self.age = age
        self.color = color

    def print_name(self):
        print(self.name)

    def print_weigth(self):
        print(self.weight)

    def print_age(self):
        print(self.age)

    def get_color(self):
        return self.color

kelly = Dog('kelly', 26, 11, 'Black And White')
topsie = Dog('Topsie', 7.2, 3, 'Brown And White')
emma = Dog('Emma', 30, 12, 'Black And White')

dogs = []
dogs.append(kelly)
dogs.append(topsie)
dogs.append(emma)

for i in range(3):
    print(dogs[i].name)
