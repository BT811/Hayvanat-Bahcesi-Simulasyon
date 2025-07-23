import threading
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
        self.lock = threading.Lock()
    
        self.last_breed_time = 0  
    
   
    
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def move(self, field_width, field_height):
        """Hareket metodu"""
        if not self.is_alive:
            return
        
        with self.lock:
            # Kendi hızı kadar rastgele hareket
            remaining_speed = self.speed
            
            # X yönünde hareket
            dx = random.randint(-remaining_speed, remaining_speed)
            remaining_speed -= abs(dx)
            
            # Y yönünde hareket (kalan hızla)
            dy = random.choice([-remaining_speed, remaining_speed])
            
            # Yeni pozisyon hesapla
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Sınır kontrolü ve Sekme
            if new_x < 0:
                new_x = abs(new_x)  
            elif new_x >= field_width:
                new_x = field_width - 1 - (new_x - field_width + 1)
            
            if new_y < 0:
                new_y = abs(new_y)  
            elif new_y >= field_height:
                new_y = field_height - 1 - (new_y - field_height + 1)

            
            # Final sınır kontrolü
            self.x = new_x
            self.y = new_y
            
    
    def die(self):
        
        with self.lock:
            if self.is_alive: 
                self.is_alive = False
    
    def _mark_dead(self):
        """Lock var ise, sadece iç kullanım için"""
        self.is_alive = False
    
    @abstractmethod
    def can_hunt(self, target):
        """Avlanabilirlik metodu"""
        pass
    
    @abstractmethod
    def can_breed_with(self, other):
        """Üreme uyumluluğunu tanımlar"""
        pass
    
    @abstractmethod
    def create_offspring(self, x, y, gender):
        
        pass
    
    def __str__(self):
        status = "alive" if self.is_alive else "dead"
        return f"{self.animal_type.value}({self.gender.value}) at ({self.x}, {self.y}) - {status}"