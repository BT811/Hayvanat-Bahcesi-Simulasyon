from config import FIELD_WIDTH, FIELD_HEIGHT

class MovementService:
    def __init__(self):
        pass
    
    def move_animal(self, animal):
        if animal.is_alive:
            animal.move(FIELD_WIDTH, FIELD_HEIGHT)
    
    def move_all_animals(self, animals):
        for animal in animals:
            if animal.is_alive:
                self.move_animal(animal)