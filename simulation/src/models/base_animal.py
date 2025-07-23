import random
from abc import ABC, abstractmethod
from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class AnimalType(Enum):
    SHEEP = "sheep"
    WOLF = "wolf"
    COW = "cow"
    CHICKEN = "chicken"
    LION = "lion"
    HUNTER = "hunter"

class BaseAnimal(ABC):
    def __init__(self, x, y, gender, animal_type, speed, hunt_range=0):
        self.x = x
        self.y = y
        self.gender = gender
        self.animal_type = animal_type
        self.speed = speed
        self.hunt_range = hunt_range
        self.is_alive = True
    
    @abstractmethod
    def can_hunt(self, target):
        pass
    
    @abstractmethod
    def can_breed_with(self, other):
        pass
    
    def move(self, field_width, field_height):
        """Hareket Özelliği ve Sınırdan Sekme Algoritması"""
        if not self.is_alive:
            return
        remaining_speed = self.speed
        dx = random.randint(-remaining_speed, remaining_speed)
        
        remaining_speed -= abs(dx)
        dy = random.choice([-remaining_speed, remaining_speed])

        # Yeni pozisyon
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Sınır Kontrolü ve Sekme
        if new_x < 0:
            new_x = abs(new_x) 
        elif new_x >= field_width:
            new_x = field_width - 1 - (new_x - field_width + 1)
        
        if new_y < 0:
            new_y = abs(new_y)  
        elif new_y >= field_height:
            new_y = field_height - 1 - (new_y - field_height + 1)
        
        # Sınır Kontrolü ve Sekme
        self.x = max(0, min(field_width - 1, new_x))
        self.y = max(0, min(field_height - 1, new_y))
        

    

    def distance_to(self, other):
        """Mesafe Hesaplama"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def die(self):
        """Ölüm metodu"""
        self.is_alive = False
    
    def __str__(self):
        return f"{self.animal_type.value}({self.gender.value}) at ({self.x}, {self.y})"