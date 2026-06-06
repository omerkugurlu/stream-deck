# 🎛️ Ömer Stream Deck v4.5 (ESP8266 Mini Makro Pad)

Bu proje, bir **ESP8266 (NodeMCU)** Wi-Fi modülünü/mikrokontrolcüsünü donanımsal bir makro klavyeye dönüştüren ve **CustomTkinter** ile yazılmış modern bir Python arayüzü üzerinden bilgisayarınızı kontrol etmenizi sağlayan tam katmanlı (Full-Stack) bir Stream Deck alternatifidir.

Sistem, fiziksel butonlara basıldığında Seri Port (`Serial COM`) üzerinden bilgisayara sinyal gönderir. Python arka plan programı bu sinyalleri yakalayarak **Medya Kontrolü**, **OBS Studio Yönetimi**, **Uygulama Çalıştırma** veya **Web Sitesi Açma** gibi önceden tanımladığınız görevleri tetikler.

---

## 📸 Ekran Görüntüleri

### Ana Kontrol Paneli
![Ana Ekran](https://i.ibb.co/kg1F3Kkm/image.png)
*Modern CustomTkinter arayüzü ile 4 farklı tuşun atamasını anlık olarak görün, düzenleyin ve yönetin.*

---

## ✨ Öne Çıkan Özellikler

* **🎨 Modern UI/UX:** Tamamen karanlık mod (Dark Mode) uyumlu, şık ve minimalist CustomTkinter tasarımı.
* **⚡ Gelişmiş Donanım Kararlılığı:** ESP8266 üzerinde `INPUT_PULLUP` dirençleri kullanılarak harici dirence ihtiyaç duymayan, stabil buton okuma algoritması.
* **🛡️ Çift Basım (Debounce) Koruması:** Butona basılı tutulduğunda bilgisayara yüzlerce kez komut gitmesini engelleyen akıllı `while` kilidi.
* **🎥 Akıllı OBS Entegrasyonu:** OBS kapalı olsa bile uygulamanın çökmesini engelleyen özel WebSocket timeout koruması.
* **📌 Sistem Tepsisi (Tray Icon):** Sağ üstteki kapatma tuşuna basıldığında arka planda (`pystray`) gizlenerek çalışmaya devam etme yeteneği.
* **💾 Kalıcı Hafıza:** Tüm ayarlar anında `deck_v3_ayarlar.json` dosyasına kaydedilir ve uygulama açılışında otomatik yüklenir.

---

## 🛠️ Adım Adım Kurulum Kılavuzu

### 1. Donanım ve Bağlantı Şeması

Butonlarınızı ESP8266 (NodeMCU) kartınıza bağlarken aşağıdaki pin eşleşmelerini referans almalısınız. `INPUT_PULLUP` modu kullanıldığı için butonların bir bacağını belirtilen pine, diğer bacağını ise kart üzerindeki **GND** pinine bağlamanız yeterlidir (Ekstra direnç gerekmez).

* **Buton 1** ➡️ Pin `D5` (GPIO 14)
* **Buton 2** ➡️ Pin `D6` (GPIO 12)
* **Buton 3** ➡️ Pin `D7` (GPIO 13)
* **Buton 4** ➡️ Pin `D1` (GPIO 5) *(D8 yerine açılış güvenliği için D1 tercih edilmiştir)*

---

### 2. ESP8266 Kodunun Yüklenmesi

Aşağıdaki kodu **Arduino IDE** programını açarak ESP8266 kartınıza yükleyin. Yükleme yapmadan önce Araçlar menüsünden doğru portu ve kart modelinizi (NodeMCU 1.0) seçtiğinizden emin olun.

```cpp
// ESP8266 Modern Makro Pad - 4 Tuş Final Kod

const int tuslar[] = {14, 12, 13, 5}; // D5, D6, D7, D1 pinleri
const int tusSayisi = 4;

void setup() {
  Serial.begin(115200); // Python ile aynı baud rate olmalı
  
  for (int i = 0; i < tusSayisi; i++) {
    pinMode(tuslar[i], INPUT_PULLUP); // Dahili pull-up aktif
  }
  
  // Seri port temizliği
  Serial.println("");
  Serial.println("SISTEM_HAZIR");
}

void loop() {
  for (int i = 0; i < tusSayisi; i++) {
    if (digitalRead(tuslar[i]) == LOW) { // Butona basıldıysa
      // Python'ın anlayacağı formatta sinyal gönder (Örn: TUS_1)
      Serial.print("TUS_");
      Serial.println(i + 1); 
      
      delay(200); // Hızlı basım ve ark bastırma gecikmesi
      
      // Tuş bırakılana kadar burada bekle (Sonsuz döngü koruması)
      while(digitalRead(tuslar[i]) == LOW);
    }
  }
}
