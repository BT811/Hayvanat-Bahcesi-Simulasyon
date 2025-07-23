from .base_animal import BaseAnimal, Gender, AnimalType
from config import HUNT_RANGES, ANIMAL_SPEEDS

class Sheep(BaseAnimal):
    def __init__(self, x, y, gender):
        super().__init__(x, y, gender, AnimalType.SHEEP, speed=ANIMAL_SPEEDS['sheep'] )
    
    def can_hunt(self, target):
        return False  
    
    def can_breed_with(self, other):
        return (isinstance(other, Sheep) and 
                other.gender != self.gender and 
                other.is_alive and self.is_alive)

class Wolf(BaseAnimal):
    def __init__(self, x, y, gender):
        super().__init__(x, y, gender, AnimalType.WOLF, speed=ANIMAL_SPEEDS['wolf'], hunt_range=HUNT_RANGES['wolf'])
    
    def can_hunt(self, target):
        return isinstance(target, (Sheep, Chicken)) and target.is_alive  
    
    def can_breed_with(self, other):
        return (isinstance(other, Wolf) and 
                other.gender != self.gender and 
                other.is_alive and self.is_alive)

class Cow(BaseAnimal):
    def __init__(self, x, y, gender):
        super().__init__(x, y, gender, AnimalType.COW, speed=ANIMAL_SPEEDS['cow'])
    
    def can_hunt(self, target):
        return False  
    
    def can_breed_with(self, other):
        return (isinstance(other, Cow) and 
                other.gender != self.gender and 
                other.is_alive and self.is_alive)

class Chicken(BaseAnimal):
    def __init__(self, x, y, gender):
        super().__init__(x, y, gender, AnimalType.CHICKEN, speed=ANIMAL_SPEEDS['chicken'])
    
    def can_hunt(self, target):
        return False 
    
    def can_breed_with(self, other):
        return (isinstance(other, Chicken) and 
                other.gender != self.gender and 
                other.is_alive and self.is_alive)

class Lion(BaseAnimal):
    def __init__(self, x, y, gender):
        super().__init__(x, y, gender, AnimalType.LION, speed=ANIMAL_SPEEDS['lion'], hunt_range=HUNT_RANGES['lion'])
    
    def can_hunt(self, target):
        return isinstance(target, (Cow, Sheep)) and target.is_alive
    
    def can_breed_with(self, other):
        return (isinstance(other, Lion) and 
                other.gender != self.gender and 
                other.is_alive and self.is_alive)

class Hunter(BaseAnimal):
    def __init__(self, x, y):
        super().__init__(x, y, Gender.MALE, AnimalType.HUNTER, speed=ANIMAL_SPEEDS['hunter'], hunt_range=HUNT_RANGES['hunter'])

    def can_hunt(self, target):
        return target.is_alive and not isinstance(target, Hunter)
    
    def can_breed_with(self, other):
        return False  