import sys
import os
    
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.simulation_service import SimulationService
from config.settings import MOVEMENT_STEPS

def main():
    print("=== Hayvanat Bahçesi Simülasyonu ===")
    
    
    try:
        # Oluştur ve başlat simülasyonu
        simulation = SimulationService()
        simulation.initialize_simulation()
        
        
        simulation.run_simulation(max_movement_units=MOVEMENT_STEPS)

        # Final istatistikleri yazdır
        stats = simulation.get_simulation_statistics()
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()