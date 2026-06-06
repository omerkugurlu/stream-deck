# 🎛️ Ömer Stream Deck v4.5 (Mini Makro Klavye)

CustomTkinter arayüzü ile güçlendirilmiş, donanımsal mini klavyenizi (Arduino, Raspberry Pi Pico vb.) tamamen özelleştirilebilir bir **Stream Deck** kontrol merkezine dönüştüren modern bir Python uygulamasıdır.

Bu proje; seri port üzerinden gelen donanım sinyallerini yakalar ve bilgisayarınızda **Medya Kontrolü**, **OBS Studio Yönetimi**, **Uygulama Çalıştırma** veya **Web Sitesi Açma** gibi dinamik görevleri tetikler.

---

## 📸 Ekran Görüntüleri

### Ana Kontrol Paneli
![Ana Ekran]([yazilim_arayuzu.png](https://i.ibb.co/kg1F3Kkm/image.png))
*Modern CustomTkinter arayüzü ile 4 farklı tuşu anlık olarak takip edin ve yönetin.*

---

## ✨ Öne Çıkan Özellikler

* **🎨 Modern UI:** Tamamen karanlık mod (Dark Mode) uyumlu, şık ve minimalist tasarım.
* **⚡ Kesintisiz Seri Port Dinleme:** Arka planda donanımınızı kesintisiz dinleyen asenkron `threading` yapısı.
* **🎥 Akıllı OBS Entegrasyonu:** OBS kapalı olsa bile uygulamanın çökmesini engelleyen özel timeout koruması.
* **📌 Sistem Tepsisi (Tray Icon):** Uygulamayı kapattığınızda tamamen kapanmaz, arka planda küçülerek çalışmaya devam eder.
* **💾 Kalıcı Hafıza:** Tüm ayarlar anında `deck_v3_ayarlar.json` dosyasına kaydedilir.

---

## 🛠️ Donanım Bağlantısı Nasıl Yapılır?

Fiziksel butonlarınızı Arduino veya benzeri bir karta aşağıdaki şemaya uygun olarak bağlamanız gerekir. Kartınız, butona basıldığında bilgisayara seri port üzerinden `TUS_1`, `TUS_2`, `TUS_3`, `TUS_4` metinlerini göndermelidir.

![Donanım Şeması](arduino_sema.png)

---

## 🚀 Adım Adım Kurulum Kılavuzu

### 1. Gereksinimlerin Yüklenmesi
Bilgisayarınızda Python 3.x kurulu olduğundan emin olun. Ardından terminal veya komut satırını açarak aşağıdaki komutla gerekli tüm kütüphaneleri tek seferde yükleyin:

```bash
pip install customtkinter pyserial pyautogui obsws-python pillow pystray
