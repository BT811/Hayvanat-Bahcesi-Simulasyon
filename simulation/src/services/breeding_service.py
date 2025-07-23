import random
from config import BREEDING_RANGE,BREEDING_ENABLED

from services.animal_factory import AnimalFactory

class BreedingService:
    def __init__(self):
        pass
    
    def can_breed(self, animal1, animal2):
        if not animal1.is_alive or not animal2.is_alive:
            return False
        
        if animal1 == animal2:
            return False
        
        # Çifleşme kurallarını kontrol et
        animal_type = animal1.animal_type.value
        if animal_type not in BREEDING_ENABLED:
            return False
        
        # Cinsiyet ve cins uyumu kontrolü
        return animal1.can_breed_with(animal2)
    
    def is_in_breeding_range(self, animal1, animal2):
        distance = animal1.distance_to(animal2)
        return distance <= BREEDING_RANGE
    
    def attempt_breeding(self, animal1, animal2):
        if (self.can_breed(animal1, animal2) and 
            self.is_in_breeding_range(animal1, animal2)):
            
            offspring = AnimalFactory.create_offspring(animal1, animal2)
            return offspring
        return None
    
    def find_breeding_pairs(self, animals):
        breeding_pairs = []
        alive_animals = [animal for animal in animals if animal.is_alive]
        used_animals = set()
        
        for i, animal1 in enumerate(alive_animals):
            if animal1 in used_animals:
                continue
                
            for j, animal2 in enumerate(alive_animals[i+1:], i+1):
                if animal2 in used_animals:
                    continue
                    
                if (self.can_breed(animal1, animal2) and 
                    self.is_in_breeding_range(animal1, animal2)):
                    breeding_pairs.append((animal1, animal2))
                    used_animals.add(animal1)
                    used_animals.add(animal2)
                    break  
        
        return breeding_pairs
    
    def process_all_breeding(self, animals):
        """Yeni doğumları işleme al"""
        breeding_pairs = self.find_breeding_pairs(animals)
        new_animals = []
        
        for animal1, animal2 in breeding_pairs:
            offspring = self.attempt_breeding(animal1, animal2)
            if offspring:
                new_animals.append(offspring)
        
        return new_animals
    
    def get_breeding_statistics(self, animals):
        breeding_pairs = self.find_breeding_pairs(animals)
        stats = {}
        
        for animal1, animal2 in breeding_pairs:
            animal_type = animal1.animal_type.value
            if animal_type not in stats:
                stats[animal_type] = 0
            stats[animal_type] += 1
        
        return stats