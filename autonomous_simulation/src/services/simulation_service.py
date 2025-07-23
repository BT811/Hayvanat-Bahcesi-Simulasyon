import threading
import time
from collections import defaultdict
from config.settings import MOVEMENT_STEPS, FIELD_WIDTH, FIELD_HEIGHT
from services.animal_factory import AnimalFactory
from services.autonomous_service import AutonomousAnimalService

class SimulationService:
    """Ana simülasyon servisi - Özerk hayvan davranışlı"""
    
    def __init__(self):
        self.animals = []
        self.factory = AnimalFactory()
        
        # Özerk davranış servisi
        self.autonomous_service = AutonomousAnimalService(self)
        
        # Thread yönetimi
        self._lock = threading.Lock()
        self._running = False
        
        # İstatistik takibi
        self.step_count = 0
        self.total_movement_units = 0
        self.initial_counts = {}
        self.birth_counts = {}
        self.hunt_deaths = {}
    
    def initialize_simulation(self):
        print("Simülasyon başlatılıyor...")

        with self._lock:
            self.animals = self.factory.create_initial_animals()
            self._record_initial_counts()
            self._running = True
        
        print(f"✅ {len(self.animals)} hayvan oluşturuldu")
        self.print_animal_count()
    
    def _record_initial_counts(self):
        """Başlangıç sayılarını kaydet"""
        counts = defaultdict(int)
        
        for animal in self.animals:
            animal_type = animal.animal_type.value
            counts[animal_type] += 1
        
        self.initial_counts = dict(counts)
        
        # Diğer sayaçları başlat
        for animal_type in self.initial_counts.keys():
            self.birth_counts[animal_type] = 0
            self.hunt_deaths[animal_type] = 0
    
    def run_simulation(self, max_movement_units=MOVEMENT_STEPS):
        print(f"🚀 Simülasyon başlatıldı - Hedef: {max_movement_units} hareket birimi")
        print("🤖 Hayvanlar yaşamaya başlıyor...")
        
        # Özerk davranışları başlat
        self.autonomous_service.start_autonomous_behavior(self.animals)
        
        start_time = time.time()
        
        try:
            while self.total_movement_units < max_movement_units and self._running:
                # İstatistik güncellemesi
                time.sleep(1.0)  # Her 1 saniyede bir kontrol et

                alive_count = len([a for a in self.animals if a.is_alive])
                active_threads = self.autonomous_service.get_active_threads()
                
                # Progress log
                if self.step_count % 10 == 0:
                    print(f"📊 {alive_count} canlı hayvan, {active_threads} aktif thread, "
                          f"{self.total_movement_units}/{max_movement_units} hareket birimi")
                
                self.step_count += 1
                
                # Güvenlik kontrolü
                if alive_count < 2:
                    print("❌ Yetersiz hayvan sayısı - simülasyon durduruluyor")
                    break
                
                
        except KeyboardInterrupt:
            print("\n⚠️  Kullanıcı simülasyonu durdurdu")
        finally:
            # Özerk davranışları durdur
            self.autonomous_service.stop_autonomous_behavior()
            self._running = False
        
        print("✅ Özerk simülasyon tamamlandı!")
        self.print_final_results()
    
    def print_animal_count(self):
        """Mevcut hayvan sayısını yazdır"""
        counts = defaultdict(lambda: {'male': 0, 'female': 0, 'total': 0})
        
        with self._lock:
            for animal in self.animals:
                if animal.is_alive:
                    animal_type = animal.animal_type.value
                    gender = animal.gender.value
                    counts[animal_type][gender] += 1
                    counts[animal_type]['total'] += 1
        
        print("\n" + "="*40)
        print("🐾 MEVCUT HAYVAN SAYILARI")
        print("="*40)
        for animal_type, count_data in counts.items():
            print(f"{animal_type.capitalize()}: {count_data['total']} "
                  f"(Erkek: {count_data['male']}, Dişi: {count_data['female']})")
        print("="*40 + "\n")
    
    def print_final_results(self):
        """Final sonuçları yazdır"""
        print("\n" + "="*60)
        print("🏆 THREAD TABANLI SİMÜLASYON SONUÇLARI")
        print("="*60)
        print(f"📈 Toplam adım: {self.step_count}")
        print(f"🏃 Toplam hareket birimi: {self.total_movement_units}")
        
        # Detaylı istatistik tablosu
        self.print_detailed_statistics_table()
        
        total_alive = len([a for a in self.animals if a.is_alive])
        total_created = len(self.animals)
        initial_total = sum(self.initial_counts.values())  
        born_total = sum(self.birth_counts.values())       
        
        print(f"\n📋 GENEL ÖZET:")
        print(f"Simülasyon {initial_total} hayvan ile başlatıldı")  
        print(f"Toplam doğan hayvan: {born_total}")               
        print(f"Toplam yaratılan hayvan: {total_created}")
        print(f"Hayatta kalan: {total_alive}")
        print(f"Ölen: {total_created - total_alive}")
        print("="*60)
    
    def print_detailed_statistics_table(self):
        """Detaylı istatistik tablosu"""
        print("\n" + "="*84)
        print("                    📊 DETAYLI HAYVAN İSTATİSTİKLERİ")
        print("="*84)
        print("Hayvan Türü  Başlangıç  Doğan   Av Ölümü    Mevcut")
        print("-"*84)
        
        # Mevcut canlı sayıları
        current_counts = {}
        with self._lock:
            for animal in self.animals:
                if animal.is_alive:
                    animal_type = animal.animal_type.value
                    current_counts[animal_type] = current_counts.get(animal_type, 0) + 1
        
        # Her hayvan türü için istatistik yazdır
        all_types = set(self.initial_counts.keys()) | set(current_counts.keys())
        
        for animal_type in sorted(all_types):
            initial = self.initial_counts.get(animal_type, 0)
            born = self.birth_counts.get(animal_type, 0)
            hunt_deaths = self.hunt_deaths.get(animal_type, 0)
            current = current_counts.get(animal_type, 0)
            
            print(f"{animal_type.capitalize():<12} {initial:<11} {born:<7} {hunt_deaths:<11} {current}")
        
        print("="*84)
    
    def stop_simulation(self):
        """Simülasyonu durdur"""
        with self._lock:
            self._running = False
    
    def get_simulation_statistics(self):
        """Simülasyon istatistiklerini al"""
        with self._lock:
            stats = {
                'step_count': self.step_count,
                'total_movement_units': self.total_movement_units,
                'total_animals': len(self.animals),
                'alive_animals': len([a for a in self.animals if a.is_alive]),
                'dead_animals': len([a for a in self.animals if not a.is_alive])
            }
        return stats
