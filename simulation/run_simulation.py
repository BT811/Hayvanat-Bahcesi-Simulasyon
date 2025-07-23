import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Çalıştır 
if __name__ == "__main__":
    import main  # Özerk hayvan main modülünü import et
    main.main()  # Ana fonksiyonu çağır