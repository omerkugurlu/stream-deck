# 🚀 Handheld Controller & System Manager (Steam Deck & Switch)

[![GitHub license](https://img.shields.io/github/license/mashape/apistore.svg?style=flat-flat)]()
[![Platform Support](https://img.shields.io/badge/platform-Steam%20Deck%20%7C%20Nintendo%20Switch-critical.svg)]()

Bu proje, **Steam Deck** ve **Nintendo Switch** gibi taşınabilir oyun konsollarının **donanım entegrasyonunu**, **özelleştirilmiş kontrolcü haritalamalarını** ve **sistem optimizasyonlarını** tek bir çatı altında toplayan açık kaynaklı bir platformdur. 

Cihazlar arası **senkronizasyon**, **cross-platform API iletişimleri** ve **gelişmiş taşınabilir oyun deneyimi** sunmayı hedefler.

---

## 📌 Öne Çıkan Özellikler

* **🎮 Gelişmiş Kontrolcü Eşleştirme:** Steam Deck ve Switch buton konfigürasyonlarını **dinamik olarak algılama** ve yeniden haritalandırma.
* **🔌 IoT ve Donanım Entegrasyonu:** Taşınabilir konsollar ile harici donanımların/sensörlerin iletişim kurmasını sağlayan **düşük gecikmeli protokoller**.
* **📊 Sistem İzleme & Optimizasyon:** Cihazların **batarya durumu**, **sıcaklık değerleri** ve **performans profillerini** anlık olarak takip etme.
* **🌐 Cross-Platform Mimari:** Hem Linux tabanlı (SteamOS) hem de özel kütüphanelerle entegre çalışabilen **modüler kod yapısı**.

---

## 🛠️ Kullanılan Teknolojiler

Projenin altyapısı yüksek performans, esneklik ve hızlı veri işleme odaklı teknolojilerle geliştirilmiştir:

| Katman | Teknoloji / Kütüphane | Görevi |
| :--- | :--- | :--- |
| **Backend & Mantık** | Python / C++ | **Donanım seviyesinde iletişim** ve veri işleme |
| **Arayüz & Mobil** | React Native / Flutter | **Çoklu platform desteği** ve kullanıcı paneli |
| **Gömülü Sistemler** | Arduino / ESP8266 (C++) | Harici donanım kontrolü ve **NFC/RFID tetikleyicileri** |
| **Veri İletişimi** | P2P / REST API | Cihazlar arası **senkronizasyon ve hızlı veri aktarımı** |

---

## 📁 Proje Yapısı

```text
├── config/               # Cihaz bazlı (Deck/Switch) konfigürasyon dosyaları
├── docs/                 # Teknik dokümantasyon ve şemalar
├── docs/                 # Teknik dokümantasyon ve şemalar
└── README.md             # Proje ana tanıtım belgesi
