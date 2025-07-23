import threading
import time
import random
from config import FIELD_WIDTH, FIELD_HEIGHT, BREEDING_RANGE

class AutonomousAnimalService:
    """Her hayvanın özerk davranışını yöneten servis"""
    
    def __init__(self, simulation_service):
        self.simulation_service = simulation_service
        self.running = False
        self.animal_threads = {}
        self.animals = []
        self._lock = threading.Lock()
    
    def start_autonomous_behavior(self, animals):
        """Tüm hayvanlar için özerk davranış thread'lerini başlat"""
        self.running = True
        self.animals = animals
        #  Tüm thread'leri oluştur
        threads_to_start = []
        for animal in animals:
            if animal.is_alive:
                thread = threading.Thread(
                    target=self._autonomous_animal_loop,
                    args=(animal,),
                    name=f"Autonomous-{animal.animal_type.value}-{id(animal)}",
                    daemon=True
                )
                self.animal_threads[id(animal)] = thread
                threads_to_start.append((thread, animal))
        
        print(f"📋 {len(threads_to_start)} thread hazırlandı")
        
        #  Thread'leri Başlat
        print("🎬 Toplu thread başlatma...")
        start_time = time.time()
        
        for thread, animal in threads_to_start:
            thread.start()
        
        end_time = time.time()
        print(f"✅ {len(threads_to_start)} thread {(end_time-start_time)*1000:.1f}ms'de başlatıldı")
        print("🤖 Tüm hayvanlar özerk moda geçti!")
    
    def _autonomous_animal_loop(self, animal):
        """Tek hayvanın özerk davranış döngüsü - Tamamen bağımsız"""
        print(f"🤖 {animal.animal_type.value.capitalize()}-{id(animal)} özerk yaşama başladı!")
        
        while self.running and animal.is_alive:
            try:
                
                animal.move(FIELD_WIDTH, FIELD_HEIGHT)

                # Movement birimini kaydet
                with self._lock:
                    self.simulation_service.total_movement_units += animal.speed
                
                # Avcı hayvanlar için av davranışı
                if  animal.hunt_range > 0:
                    self._autonomous_hunt(animal)
                
                # Çiftleşme davranışı
                self._autonomous_breed(animal)
                
                time.sleep(0.15)
                
            except Exception as e:
                print(f"❌ {animal.animal_type.value} özerk davranış hatası: {e}")
                break
        
        print(f"🔚 {animal.animal_type.value.capitalize()}-{id(animal)} yaşamını tamamladı")
    
    def _autonomous_hunt(self, animal):
        """Tamamen özerk avcılık - sistem durmaz"""
        if not animal.is_alive:
            return
        
        # Animals listesi hızlı kopyalama 
        with self._lock:
            animals = self.simulation_service.animals.copy()
        
        # Lock dışında av analizi
        potential_prey = []
        for target in animals:
            if (target.is_alive and 
                animal.can_hunt(target) and 
                animal.distance_to(target) <= animal.hunt_range):
                potential_prey.append((target, animal.distance_to(target)))
        
        if potential_prey:
            # En yakın avı bul
            closest_prey = min(potential_prey, key=lambda x: x[1])[0]
            
            with closest_prey.lock:
                if closest_prey.is_alive:
                    closest_prey.is_alive = False
                    
                    # Sadece istatistik için minimal global lock
                    with self._lock:
                        animal_type = closest_prey.animal_type.value
                        if animal_type not in self.simulation_service.hunt_deaths:
                            self.simulation_service.hunt_deaths[animal_type] = 0
                        self.simulation_service.hunt_deaths[animal_type] += 1
                    
                    print(f"🎯 {animal.animal_type.value.capitalize()} avladı: {closest_prey.animal_type.value}")
    
    def _autonomous_breed(self, animal):
        """Özerk çiftleşme - hayvan kendi partnerini seçer"""
        if not animal.is_alive:
            return
        
        # Cooldown kontrolü - son çiftleşmeden beri yeterli zaman geçti mi?
        current_time = time.time()
        last_breed = getattr(animal, 'last_breed_time', 0)
        cooldown_period = 3.0  # 3 saniye cooldown
        
        if current_time - last_breed < cooldown_period:
            return  # Henüz cooldown bitmedi
        
        # Animals listesi lock
        with self._lock:
            animals = self.simulation_service.animals.copy()
        
        # partner analizi 
        potential_partners = []
        for partner in animals:
            if (partner != animal and 
                partner.is_alive and 
                animal.can_breed_with(partner) and 
                animal.distance_to(partner) <= BREEDING_RANGE):
                
                # Partner'ın da cooldown'ını kontrol et
                partner_last_breed = getattr(partner, 'last_breed_time', 0)
                if current_time - partner_last_breed >= cooldown_period:
                    potential_partners.append((partner, animal.distance_to(partner)))
        
        if potential_partners:
            # En yakın partneri seç
            closest_partner = min(potential_partners, key=lambda x: x[1])[0]
            
            # ÇİFT LOCK: Her zaman aynı sırada lock al (deadlock önleme)
            animal1_id = id(animal)
            animal2_id = id(closest_partner)
            
            first_animal = animal if animal1_id < animal2_id else closest_partner
            second_animal = closest_partner if animal1_id < animal2_id else animal
            
            with first_animal.lock:
                with second_animal.lock:
                    # Triple-check: Her iki hayvan hala uygun mu ve cooldown bitti mi?
                    current_time_check = time.time()
                    animal_last_breed = getattr(animal, 'last_breed_time', 0)
                    partner_last_breed = getattr(closest_partner, 'last_breed_time', 0)
                    
                    if (animal.is_alive and closest_partner.is_alive and 
                        animal.can_breed_with(closest_partner) and 
                        animal.distance_to(closest_partner) <= BREEDING_RANGE and
                        current_time_check - animal_last_breed >= cooldown_period and
                        current_time_check - partner_last_breed >= cooldown_period):
                        
                        from services.animal_factory import AnimalFactory
                        baby = AnimalFactory.create_offspring(animal, closest_partner)
                        
                        if baby:
                            # Sadece yeni hayvan ekleme ve istatistik için global lock
                            with self._lock:
                                self.simulation_service.animals.append(baby)
                                
                                # Doğum istatistiğini güncelle
                                animal_type = baby.animal_type.value
                                if animal_type not in self.simulation_service.birth_counts:
                                    self.simulation_service.birth_counts[animal_type] = 0
                                self.simulation_service.birth_counts[animal_type] += 1
                            
                            baby_thread = threading.Thread(
                                target=self._autonomous_animal_loop,
                                args=(baby,),
                                name=f"Autonomous-{baby.animal_type.value}-{id(baby)}",
                                daemon=True
                            )
                            
                            # Thread tracking
                            self.animal_threads[id(baby)] = baby_thread
                            baby_thread.start()
                            
                            print(f"💕 Özerk çiftleşme: {animal.animal_type.value.capitalize()} + {closest_partner.animal_type.value.capitalize()} → {baby.animal_type.value.capitalize()} ({baby.gender.value})")
                        
                        # Ebeveynlere cooldown 
                        final_time = time.time()
                        animal.last_breed_time = final_time
                        closest_partner.last_breed_time = final_time
    
    def stop_autonomous_behavior(self):
        with self._lock:
            self.running = False
        
        print("🛑 Tüm özerk davranışlar durduruluyor...")
        
        # Tüm thread'lerin bitmesini bekle
        for thread in self.animal_threads.values():
            if thread.is_alive():
                thread.join(timeout=2.0)
        
        print("✅ Özerk davranışlar durduruldu")
    
    def get_active_threads(self):
        """Aktif thread sayısını döndür"""
        return len([t for t in self.animal_threads.values() if t.is_alive()])
