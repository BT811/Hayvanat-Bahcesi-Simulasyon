# Hayvanat Bahçesi Simülasyonu - Staj Vaka Çalışması

Bu repository, DIATICS "Uzun Dönem Stajyer" pozisyonu için hazırlanan vaka çalışmasını ve çözümünü içermektedir.

Probleme yönelik, iki ayrı çözüm geliştirilmiştir. Bu yaklaşımlar, bir problemi hem basit ve anlaşılır yollarla çözebileceğimi, hem de daha karmaşık ve gerçekçi senaryolar için modern programlama tekniklerini etkin bir şekilde kullanabildiğimi göstermeyi amaçlamaktadır. Mimari yapısı değişime açık şekilde tasarlanmıştır.

- **Proje Sahibi:** Berk Türk   
- **İletişim:** B.Trk1@hotmail.com

---


### Problem Çözüm Yaklaşımı 

Problem, bir ekosistemdeki canlıların hareket, avlanma ve üreme gibi temel davranışlarını modelleyen bir simülasyon olarak ele alınmıştır. Bu doğrultuda iki farklı çözüm mimarisi tasarlanmıştır:

1.  **Sıralı Yaklaşım (`simulation` klasöründe):**
    *   **Mantık:** Simülasyon, merkezi bir döngü tarafından yönetilir. Her adımda (iterasyonda), tüm canlıların hareket, üreme ve avlanma eylemleri sırayla ve merkezi servisler (`HuntingService`, `BreedingService`,`MovementService`) tarafından kontrol edilir.
    *   **Avantajları:** Kodun akışını takip etmek ve anlamak daha kolaydır. Deterministik yapısı sayesinde test edilmesi ve hata ayıklaması daha basittir.
    *   **Dezavantajları:** Gerçek dünyadaki canlıların "eş zamanlı" ve "özerk" doğasını tam olarak yansıtmaz. Tüm mantık tek bir ana iş parçacığında (main thread) çalışır.

2.  **Eş Zamanlı ve Özerk Yaklaşım (`autonomous_simulation` klasöründe):**
    *   **Mantık:** Simülasyondaki her bir canlı, kendi yaşam döngüsünü yöneten bağımsız bir iş parçacığı (thread) olarak modellenmiştir. Canlılar, merkezi bir kontrole ihtiyaç duymadan, kendi başlarına hareket eder, çevrelerini gözlemler, avlanır ve çiftleşirler.
    *   **Avantajları:** Gerçek hayata çok daha yakın, dinamik ve özerk bir simülasyon sunar. Her canlının bağımsız bir varlık olduğu fikrini yansıtır. Thread yönetimi, `lock` mekanizmaları gibi ileri seviye programlama yetkinliklerini sergileme fırsatı sunar.
    *   **Dezavantajları:** Paylaşılan kaynaklara (canlı listesi vb.) erişim nedeniyle "race condition" ve "deadlock" gibi riskler barındırır ve bu risklerin yönetilmesi gerekir. Bu da kodun karmaşıklığını artırır.

### Algoritma Yaklaşımı

*   **Hareket:** Canlılar, kendilerine atanan hız birimi kadar rastgele hareket eder. Simülasyon alanının dışına çıkmamaları için konumları sürekli kontrol edilir ve sınırlara ulaştıklarında geri dönerler.
*   **Mesafe Hesaplama:** İki canlı arasındaki mesafe, standart Öklid formülü kullanılarak hesaplanır.
*   **Avlanma:**
    *   **Sıralı Yaklaşımda:** Merkezi `HuntingService`, her iterasyonda tüm avcıları ve potansiyel avları kontrol ederek avlanma girişimlerini gerçekleştirir.
    *   **Eş Zamanlı Yaklaşımda:** Her avcı canlı, kendi thread'i içinde periyodik olarak etrafını tarar. Menzili içindeki uygun bir avı tespit ettiğinde, avın durumunu değiştirmeden önce o kaynağa erişimi bir `lock` mekanizması ile kilitleyerek thread-safe bir şekilde avlanma işlemini gerçekleştirir.
*   **Üreme:**
    *   **Sıralı Yaklaşımda:** Merkezi `BreedingService`, uygun çiftleri (aynı tür, farklı cinsiyet, yakın mesafe) bularak yeni yavrular oluşturur ve simülasyona ekler.
    *   **Eş Zamanlı Yaklaşımda:** Her canlı, kendi thread'i içinde periyodik olarak uygun bir eş arar. Potansiyel bir eş bulunduğunda, "deadlock" riskini önlemek için her iki canlının `lock`'ları belirli bir sırada (ID'ye göre) alınır ve yeni bir yavru (ve yeni bir thread) oluşturulur. İki canlının aynı anda birbirini bularak çift yavru oluşturması gibi bir durumunu engellemek için, üreme gerçekleştikten sonra her iki ebeveyn de geçici bir "bekleme süresine" (cooldown) alınır ve bu süre boyunca tekrar üreyemezler.

### Kodlama Pratikleri 

*   **Nesne Yönelimli Programlama (OOP):** `BaseAnimal` gibi soyut sınıflar ve bu sınıflardan türetilen alt sınıflar (`Wolf`, `Sheep` vb.) kullanılarak kalıtım (inheritance) ve çok biçimlilik (polymorphism) prensipleri etkin bir şekilde uygulanmıştır.
*   **SOLID Prensipleri:** Sorumluluklar `SimulationService`, `HuntingService`, `BreedingService`, `AnimalFactory` gibi farklı sınıflara ve modüllere ayrılarak Tek Sorumluluk Prensibi'ne (Single Responsibility Principle) uyulmuştur.
*   **Konfigürasyon Yönetimi:** Simülasyon parametreleri (saha boyutu, canlı sayıları, hızlar vb.) kodun içindeki "sihirli sayılar" (magic numbers) yerine `config` paketindeki dosyalara taşınarak kodun esnekliği ve yönetilebilirliği artırılmıştır.
*   **Thread Güvenliği (Eş Zamanlı Yaklaşımda):** Paylaşılan kaynaklara (canlı listesi, simülasyon durumu) erişim, `threading.Lock` kullanılarak senkronize edilmiş ve "race condition" gibi çoklu iş parçacığı problemlerinin önüne geçilmiştir.

### Dökümantasyon 

*   Bu `README.md` dosyası, projenin genel yapısını, yaklaşımları ve tasarım kararlarını açıklayarak dökümantasyonun temelini oluşturur.
*   Kod içerisinde, karmaşık veya önemli mantık bloklarını açıklamak için yorum satırları kullanılmıştır.
*   Sınıf, metot ve değişken isimlendirmeleri, kodun kendi kendini belgelemesi (self-documenting code) amacıyla açık ve anlaşılır bir şekilde yapılmıştır.

---

## Projeler Nasıl Çalıştırılır?

Her iki projenin de kendi klasöründe bir `run_simulation.py` dosyası bulunmaktadır.

**Gereksinimler:**
*   Python 3.x

**Çalıştırma Adımları:**

```bash
# 1. Sıralı Yaklaşımı Çalıştırmak İçin:
cd simulation
python run_simulation.py

# 2. Eş Zamanlı ve Özerk Yaklaşımı Çalıştırmak İçin:
cd autonomous-simulation
python run_simulation.py
```

Simülasyon tamamlandığında, 1000 birim hareket sonundaki canlı sayıları konsola yazdırılacaktır.
