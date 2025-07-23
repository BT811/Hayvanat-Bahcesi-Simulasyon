import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.simulation_service import SimulationService
from config.settings import MOVEMENT_STEPS

def main():
    """Özerk hayvan davranışlı simülasyon"""
    print("� === ÖZERK HAYVAN DAVRANIŞLI SİMÜLASYON ===")
    
    try:
        # Simülasyon oluştur ve başlat
        simulation = SimulationService()
        simulation.initialize_simulation()
        
        # Özerk davranış simülasyonunu çalıştır
        simulation.run_simulation(max_movement_units=MOVEMENT_STEPS)
        
        
    except KeyboardInterrupt:
        print("\n⚠️  Kullanıcı simülasyonu durdurdu")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
