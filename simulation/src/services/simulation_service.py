from config import MOVEMENT_STEPS, FIELD_WIDTH, FIELD_HEIGHT, INITIAL_ANIMALS

from services.animal_factory import AnimalFactory
from services.hunting_service import HuntingService
from services.breeding_service import BreedingService
from services.movement_service import MovementService

class SimulationService:
    def __init__(self):
        self.animals = []
        self.hunting_service = HuntingService()
        self.breeding_service = BreedingService()
        self.movement_service = MovementService()
        self.step_count = 0
        self.total_movement_units = 0  # Toplam hareket birimi sayacı
        
        # Detaylı istatistik takibi
        self.initial_counts = {}  # Başlangıç sayıları
        self.birth_counts = {}    # Doğum sayıları
        self.hunt_deaths = {}     # Av nedeniyle ölümler
    
    def initialize_simulation(self):
        print("Simulasyon başlatılıyor...")
        self.animals = AnimalFactory.create_initial_animals()
        print(f" {len(self.animals)}  hayvan oluşturuldu.")
        
        # Başlangıç sayılarını kaydet
        self._record_initial_counts()
        self.print_animal_count()
    
    def _record_initial_counts(self):
        from collections import defaultdict
        counts = defaultdict(int)
        
        for animal in self.animals:
            animal_type = animal.animal_type.value
            counts[animal_type] += 1
        
        self.initial_counts = dict(counts)
        
        # Doğum ve av ölümleri için başlangıç sayıları
        for animal_type in self.initial_counts.keys():
            self.birth_counts[animal_type] = 0
            self.hunt_deaths[animal_type] = 0
    
    
    
    def run_simulation(self, max_movement_units=MOVEMENT_STEPS):
        print(f"Toplam {max_movement_units} hareket birimine kadar simülasyon çalıştırılıyor...")
        
        while self.total_movement_units < max_movement_units:
            try:
                # Her adımda sadece bir hayvan hareket etsin
                alive_animals = [a for a in self.animals if a.is_alive]
                if not alive_animals:
                    print("Hayatta kalan hayvan kalmadı")
                    break
                
                # Sırayla hayvanları hareket ettir
                for animal in alive_animals:
                    if self.total_movement_units >= max_movement_units:
                        break
                    
                    # Hayvanı hareket ettir
                    self.movement_service.move_animal(animal)
                    self.total_movement_units += animal.speed
                    
                    # İlerleme
                    if self.total_movement_units % 100 == 0 or self.total_movement_units >= max_movement_units:
                        print(f"Hareket: {self.total_movement_units}/{max_movement_units}")

                # Çiftleşme kontrolü (her hayvanın hareketinden sonra)
                new_animals = self.breeding_service.process_all_breeding(self.animals)
                if new_animals:
                    # Yeni doğan hayvanları kaydet
                    for baby in new_animals:
                        animal_type = baby.animal_type.value
                        if animal_type not in self.birth_counts:
                            self.birth_counts[animal_type] = 0
                        self.birth_counts[animal_type] += 1
                    
                    self.animals.extend(new_animals)
                    print(f"Doğum: {len(new_animals)} yeni hayvan")

                # Av kontrolü (her tam turdan sonra)
                hunted_animals = self.hunting_service.process_all_hunting_with_details(self.animals)
                if hunted_animals:
                    # Avlanan hayvanları kaydet
                    for hunted_animal in hunted_animals:
                        animal_type = hunted_animal.animal_type.value
                        if animal_type not in self.hunt_deaths:
                            self.hunt_deaths[animal_type] = 0
                        
                        self.hunt_deaths[animal_type] += 1


                    print(f"Avlandı: {len(hunted_animals)} hayvan")

                self.step_count += 1
                
                # Safety check
                alive_count = len([a for a in self.animals if a.is_alive])
                if alive_count < 2:
                    print(f"Simülasyon erken sona erdi - sadece {alive_count} hayvan kaldı")
                    break
                    
            except Exception as e:
                print(f"Hata {self.step_count}: {e}")
                break

        print("Simülasyon tamamlandı!")
        self.print_final_results()
    
    def print_animal_count(self):
        from collections import defaultdict
        
        counts = defaultdict(lambda: {'male': 0, 'female': 0, 'total': 0})
        
        for animal in self.animals:
            if animal.is_alive:
                animal_type = animal.animal_type.value
                gender = animal.gender.value
                counts[animal_type][gender] += 1
                counts[animal_type]['total'] += 1

        print("\n=== Güncel Hayvan Sayısı ===")
        for animal_type, count_data in counts.items():
            print(f"{animal_type.capitalize()}: {count_data['total']} "
                  f"(Erkek: {count_data['male']}, Dişi: {count_data['female']})")
        print("==========================\n")
    
    def print_final_results(self):
        """Final simulasyon Sonuçlarını yazdırır"""
        print("\n" + "="*50)
        print("Simulasyon sonuçları")
        print("="*50)
        print(f"Toplam adım: {self.step_count}")
        print(f"Toplam hareket birimleri: {self.total_movement_units}")

        # Detaylı istatistik tablosu
        self.print_detailed_statistics_table()
        
        total_alive = len([a for a in self.animals if a.is_alive])
        total_created = len(self.animals)

        print(f"\nTOPLAM ÖZET:")
        print(f"Simülasyon sırasında oluşturulan toplam hayvan: {total_created}")
        print(f"Hayatta kalan hayvanlar: {total_alive}")
        print(f"Ölen hayvanlar: {total_created - total_alive}")
        print("="*50)
    
    def print_detailed_statistics_table(self):
        print("\n" + "="*84)
        print("                    DETAYLI HAYVAN İSTATİSTİKLERİ")
        print("="*84)
        print("Hayvan Türü  Başlangıç  Doğan   Avlanma Ölümü  Mevcut")
        print("-"*84)
        
        current_counts = {}
        for animal in self.animals:
            if animal.is_alive:
                animal_type = animal.animal_type.value
                current_counts[animal_type] = current_counts.get(animal_type, 0) + 1
        
        all_types = set(self.initial_counts.keys()) | set(current_counts.keys())
        
        for animal_type in sorted(all_types):
            initial = self.initial_counts.get(animal_type, 0)
            born = self.birth_counts.get(animal_type, 0)
            hunt_deaths = self.hunt_deaths.get(animal_type, 0)
            current = current_counts.get(animal_type, 0)
            
            print(f"{animal_type.capitalize():<12} {initial:<8} {born:<6} {hunt_deaths:<12} {current}")
        
        print("="*84)
    
    def get_simulation_statistics(self):
        stats = {
            'adım': self.step_count,
            'toplam_hareket_birimi': self.total_movement_units,
            'toplam_hayvan': len(self.animals),
            'hayatta_kalan_hayvan': len([a for a in self.animals if a.is_alive]),
            'ölen_hayvan': len([a for a in self.animals if not a.is_alive])
        }
        return stats