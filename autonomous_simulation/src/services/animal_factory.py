import random
from models.animals import Sheep, Wolf, Cow, Chicken, Lion, Hunter, Gender
from config.settings import FIELD_WIDTH, FIELD_HEIGHT
from config.animal_config import INITIAL_ANIMALS

class AnimalFactory:
    """Hayvan oluşturma - Thread safe"""
    
    
    @staticmethod
    def create_random_position():
        """Rastgele oluşturulmuş pozisyon üret"""
        x = random.randint(0, FIELD_WIDTH - 1)
        y = random.randint(0, FIELD_HEIGHT - 1)
        return x, y
    
    @staticmethod
    def create_sheep(gender):
        x, y = AnimalFactory.create_random_position()
        return Sheep(x, y, gender)
    
    @staticmethod
    def create_wolf(gender):
        x, y = AnimalFactory.create_random_position()
        return Wolf(x, y, gender)
    
    @staticmethod
    def create_cow(gender):
        x, y = AnimalFactory.create_random_position()
        return Cow(x, y, gender)
    
    @staticmethod
    def create_chicken(gender):
        x, y = AnimalFactory.create_random_position()
        return Chicken(x, y, gender)
    
    @staticmethod
    def create_lion(gender):
        x, y = AnimalFactory.create_random_position()
        return Lion(x, y, gender)
    
    @staticmethod
    def create_hunter():
        x, y = AnimalFactory.create_random_position()
        return Hunter(x, y)
    
    @staticmethod
    def create_initial_animals():
        """Başlangıç hayvanlarını oluştur"""
        animals = []
        
        # Koyunları oluştur
        for _ in range(INITIAL_ANIMALS['sheep']['male']):
            animals.append(AnimalFactory.create_sheep(Gender.MALE))
        for _ in range(INITIAL_ANIMALS['sheep']['female']):
            animals.append(AnimalFactory.create_sheep(Gender.FEMALE))
        
        # İnekleri oluştur
        for _ in range(INITIAL_ANIMALS['cow']['male']):
            animals.append(AnimalFactory.create_cow(Gender.MALE))
        for _ in range(INITIAL_ANIMALS['cow']['female']):
            animals.append(AnimalFactory.create_cow(Gender.FEMALE))
        
        # Tavukları oluştur
        for _ in range(INITIAL_ANIMALS['chicken']['male']):
            animals.append(AnimalFactory.create_chicken(Gender.MALE))
        for _ in range(INITIAL_ANIMALS['chicken']['female']):
            animals.append(AnimalFactory.create_chicken(Gender.FEMALE))

        # Kurtları oluştur
        for _ in range(INITIAL_ANIMALS['wolf']['male']):
            animals.append(AnimalFactory.create_wolf(Gender.MALE))
        for _ in range(INITIAL_ANIMALS['wolf']['female']):
            animals.append(AnimalFactory.create_wolf(Gender.FEMALE))
        
        # Aslanları oluştur
        for _ in range(INITIAL_ANIMALS['lion']['male']):
            animals.append(AnimalFactory.create_lion(Gender.MALE))
        for _ in range(INITIAL_ANIMALS['lion']['female']):
            animals.append(AnimalFactory.create_lion(Gender.FEMALE))
        
        # Avcıyı oluştur
        for _ in range(INITIAL_ANIMALS['hunter']['male']):
            animals.append(AnimalFactory.create_hunter())
        
        return animals
    
    @staticmethod
    def create_offspring(parent1, parent2):
        """İki ebeveynden yavru oluştur"""
        # Rastgele cinsiyet seç
        gender = random.choice([Gender.MALE, Gender.FEMALE])
        
        # Yavruların pozisyonu ebeveynlerin ortalaması
        avg_x = (parent1.x + parent2.x) // 2
        avg_y = (parent1.y + parent2.y) // 2
        
        # Parent'ın create_offspring metodunu kullan
        return parent1.create_offspring(avg_x, avg_y, gender)