class HuntingService:
    def __init__(self):
        pass
    
    def is_in_hunt_range(self, hunter, target):
        distance = hunter.distance_to(target)
        return distance <= hunter.hunt_range
    
    def attempt_hunt(self, hunter, target):
        if (hunter.can_hunt(target) and  
            self.is_in_hunt_range(hunter, target)):
            target.die()
            return True
        return False
    
    def process_all_hunting_with_details(self, animals):
        """Avlanma işlemini tüm hayvanlar için gerçekleştirir"""
        hunters = [animal for animal in animals if animal.hunt_range > 0 and animal.is_alive]
        hunted_animals = []
        
        for hunter in hunters:
            for target in animals:
                if self.attempt_hunt(hunter, target):
                    hunted_animals.append(target)
                    break  
        
        return hunted_animals