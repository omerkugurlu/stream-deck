import customtkinter as ctk
import serial
import threading
import pyautogui
import os
import json
import webbrowser
import subprocess
import obsws_python as obs
import time
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

AYAR_DOSYASI = "deck_v3_ayarlar.json"

class ActionPicker(ctk.CTkToplevel):
    def __init__(self, parent, tid, current_config, callback):
        super().__init__(parent)
        self.title(f"{tid} Yapılandırma")
        self.geometry("400x500")
        self.callback = callback
        self.tid = tid
        self.lift()
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Bir İşlem Seçin", font=("Roboto", 18, "bold")).pack(pady=10)

        self.tabview = ctk.CTkTabview(self, width=380, height=400)
        self.tabview.pack(padx=10, pady=10)
        
        self.tabview.add("Medya")
        self.tabview.add("OBS")
        self.tabview.add("Sistem")

        medya_buttons = [
            ("Sesi Artır", "volumeup"), ("Sesi Kıs", "volumedown"),
            ("Sustur", "volumemute"), ("Oynat/Duraklat", "playpause"),
            ("Sonraki", "nexttrack"), ("Önceki", "prevtrack")
        ]
        for btn_text, val in medya_buttons:
            ctk.CTkButton(self.tabview.tab("Medya"), text=btn_text, 
                          command=lambda v=val: self.select("Medya", v)).pack(pady=5, fill="x")

        ctk.CTkButton(self.tabview.tab("OBS"), text="Kaydı Başlat/Durdur", fg_color="red",
                      command=lambda: self.select("OBS Kayıt/Yayın", "kayit")).pack(pady=5, fill="x")
        ctk.CTkButton(self.tabview.tab("OBS"), text="Yayını Başlat/Durdur", fg_color="purple",
                      command=lambda: self.select("OBS Kayıt/Yayın", "yayin")).pack(pady=5, fill="x")
        
        self.scene_entry = ctk.CTkEntry(self.tabview.tab("OBS"), placeholder_text="Sahne Adı Yazın...")
        self.scene_entry.pack(pady=10, fill="x")
        ctk.CTkButton(self.tabview.tab("OBS"), text="Sahneye Geç", 
                      command=lambda: self.select("OBS Sahne", self.scene_entry.get())).pack(pady=5, fill="x")

        self.cmd_entry = ctk.CTkEntry(self.tabview.tab("Sistem"), placeholder_text="Dosya Yolu veya URL...")
        self.cmd_entry.pack(pady=10, fill="x")
        ctk.CTkButton(self.tabview.tab("Sistem"), text="Uygulama/Dosya Ata", 
                      command=lambda: self.select("Uygulama", self.cmd_entry.get())).pack(pady=5, fill="x")
        ctk.CTkButton(self.tabview.tab("Sistem"), text="Web Sitesi Ata", 
                      command=lambda: self.select("Web Sitesi", self.cmd_entry.get())).pack(pady=5, fill="x")

    def select(self, mod, deger):
        self.callback(self.tid, mod, deger)
        self.destroy()

class ProDeckV3(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ömer Stream Deck v4.5")
        self.geometry("600x700")

        self.tus_ayarlari = self.ayarlari_yukle()
        self.obs_client = None
        
        # OBS Bağlantısı - Çökmeyi Engelleyen Blok
        threading.Thread(target=self.connect_obs, daemon=True).start()

        self.create_main_ui()
        self.protocol('WM_DELETE_WINDOW', self.hide_window)
        
        self.running = True
        threading.Thread(target=self.listen_serial, daemon=True).start()
        self.create_tray_icon()

    def connect_obs(self):
        """OBS açık değilse programın çökmesini engeller."""
        try:
            # timeout=3 ekleyerek bağlanamazsa hızlıca vazgeçmesini sağlıyoruz
            self.obs_client = obs.ReqClient(host='localhost', port=4455, password='', timeout=3)
            print("OBS Bağlantısı Başarılı.")
        except Exception:
            self.obs_client = None
            print("OBS kapalı veya WebSocket devre dışı. OBS özellikleri çalışmayacak.")

    def ayarlari_yukle(self):
        if os.path.exists(AYAR_DOSYASI):
            with open(AYAR_DOSYASI, "r", encoding="utf-8") as f: return json.load(f)
        return {f"TUS_{i}": {"mod": "Kısayol", "deger": "none", "etiket": f"Tuş {i}"} for i in range(1, 5)}

    def ayarlari_kaydet(self):
        with open(AYAR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(self.tus_ayarlari, f, ensure_ascii=False, indent=4)

    def create_main_ui(self):
        ctk.CTkLabel(self, text="STREAM DECK PRO", font=("Roboto", 24, "bold")).pack(pady=20)
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.button_widgets = {}
        for i in range(1, 5):
            tid = f"TUS_{i}"
            btn_frame = ctk.CTkFrame(self.container, border_width=2)
            btn_frame.pack(fill="x", pady=10, padx=10)

            lbl = ctk.CTkLabel(btn_frame, text=f"BUTON {i}", font=("Roboto", 14, "bold"))
            lbl.pack(side="left", padx=20)

            info_text = f"{self.tus_ayarlari[tid]['mod']}: {self.tus_ayarlari[tid]['deger']}"
            info_lbl = ctk.CTkLabel(btn_frame, text=info_text, text_color="gray")
            info_lbl.pack(side="left", padx=10)
            self.button_widgets[tid] = info_lbl

            edit_btn = ctk.CTkButton(btn_frame, text="⚙ Yapılandır", width=100,
                                     command=lambda t=tid: self.open_picker(t))
            edit_btn.pack(side="right", padx=10, pady=10)

    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), (31, 83, 141))
        d = ImageDraw.Draw(image)
        d.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
        menu = (item('Göster', self.show_window), item('Çıkış', self.quit_app))
        self.tray_icon = pystray.Icon("ÖmerDeck", image, "Ömer Stream Deck", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_window(self): self.withdraw()
    def show_window(self): self.after(0, self.deiconify)
    def quit_app(self):
        self.running = False
        self.tray_icon.stop()
        self.destroy()

    def open_picker(self, tid):
        ActionPicker(self, tid, self.tus_ayarlari[tid], self.apply_setting)

    def apply_setting(self, tid, mod, deger):
        self.tus_ayarlari[tid]["mod"] = mod
        self.tus_ayarlari[tid]["deger"] = deger
        self.button_widgets[tid].configure(text=f"{mod}: {deger}")
        self.ayarlari_kaydet()

    def listen_serial(self):
        while self.running:
            try:
                # Portu kontrol etmeyi unutma!
                ser = serial.Serial('COM3', 115200, timeout=0.01)
                while self.running:
                    if ser.in_waiting > 0:
                        raw = ser.readline().decode('utf-8', errors='ignore').strip()
                        if raw in self.tus_ayarlari: self.execute(raw)
            except: time.sleep(1)

    def execute(self, tid):
        config = self.tus_ayarlari[tid]
        mod, val = config["mod"], config["deger"]
        
        if mod == "Medya":
            pyautogui.press(val)
        elif mod == "OBS Sahne":
            if self.obs_client: 
                try: self.obs_client.set_current_program_scene(val)
                except: self.obs_client = None # Bağlantı koptuysa sıfırla
        elif mod == "OBS Kayıt/Yayın":
            if self.obs_client:
                try:
                    if val == "kayit": self.obs_client.toggle_record()
                    else: self.obs_client.toggle_stream()
                except: self.obs_client = None
        elif mod == "Web Sitesi": webbrowser.open(val)
        elif mod == "Uygulama":
            if val and val != "none": os.startfile(val)

if __name__ == "__main__":
    app = ProDeckV3()
    app.mainloop()