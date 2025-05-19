import os
import sys
import locale

try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    print("Locale sistem varsayılanına ayarlanamadı, 'C' locale deneniyor.")
    try:
        locale.setlocale(locale.LC_ALL, "C")
    except locale.Error:
        print("Locale 'C' olarak da ayarlanamadı. Varsayılan locale kullanılacak.")
        pass

import pyaudio
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
# keyboard kütüphanesi artık kullanılmıyor.
import json

class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.gain = 1.0
        self.distortion = 1.0
        self.clipping = 1.0
        self.effects_enabled = False
        self.latest_amplitude = 0.0

    def get_device_list(self, device_type):
        devices = []
        seen_devices = set()
        
        host_api_count = self.p.get_host_api_count()
        host_api_details = {}
        for i in range(host_api_count):
            try:
                info = self.p.get_host_api_info_by_index(i)
                host_api_details[i] = info['name']
            except Exception as e:
                print(f"Host API {i} bilgisi alınamadı: {e}")
                host_api_details[i] = "Unknown API"

        for i in range(self.p.get_device_count()):
            try:
                dev_info = self.p.get_device_info_by_index(i)
                host_api_index = dev_info['hostApi']
                host_api_name = host_api_details.get(host_api_index, "Unknown API")
                
                device_name = dev_info['name']
                device_key = (device_name, host_api_name, dev_info['maxInputChannels'], dev_info['maxOutputChannels'])
                
                if device_key in seen_devices:
                    continue
                seen_devices.add(device_key)
                
                if device_type == 'input' and dev_info['maxInputChannels'] > 0:
                    devices.append(f"{i}: {device_name} ({host_api_name})")
                elif device_type == 'output' and dev_info['maxOutputChannels'] > 0:
                    devices.append(f"{i}: {device_name} ({host_api_name})")
            except Exception as e:
                print(f"Aygıt {i} bilgisi alınamadı: {e}")
        return devices
    
    def process_audio(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        if self.effects_enabled:
            audio_data = audio_data * (self.gain ** 2)
            audio_data = np.tanh(audio_data * self.distortion)
            audio_data = np.tanh(audio_data * 1.5)
            audio_data = np.clip(audio_data, -self.clipping, self.clipping)
        self.latest_amplitude = np.max(np.abs(audio_data)) if audio_data.size > 0 else 0.0
        return (audio_data.tobytes(), pyaudio.paContinue)

    def start_stream(self, input_device_index, output_device_index):
        if self.stream is not None:
            self.stop_stream()
        try:
            self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                output=True,
                input_device_index=input_device_index,
                output_device_index=output_device_index,
                stream_callback=self.process_audio,
                frames_per_buffer=1024
            )
            self.stream.start_stream()
            print(f"Stream başlatıldı: Giriş IDX {input_device_index}, Çıkış IDX {output_device_index}")
        except Exception as e:
            self.stream = None
            raise e

    def stop_stream(self):
        if self.stream is not None:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                print(f"Stream durdurulurken/kapatılırken hata: {e}")
            finally:
                self.stream = None
                print("Stream durduruldu.")

    def cleanup(self):
        self.stop_stream()
        if self.p:
            try:
                self.p.terminate()
                self.p = None
                print("PyAudio sonlandırıldı.")
            except Exception as e:
                print(f"PyAudio sonlandırılırken hata: {e}")

class AudioEffectGUI:
    def __init__(self):
        self.config_file = "audio_config.json"
        self.device_file = "device_selection.json"
        self.load_config()
        self.profile_settings = self.config.get("presets", {
            "Normal": {"gain": 1.0, "distortion": 1.0, "clipping": 1.0},
            "Boost": {"gain": 5.0, "distortion": 5.0, "clipping": 0.8},
            "Extreme": {"gain": 10.0, "distortion": 10.0, "clipping": 0.5}
        })
        self.night_mode = self.config.get("night_mode", False)
        self.theme_name = "darkly" if self.night_mode else "flatly"
        self.root = ttk.Window(themename=self.theme_name)
        self.root.title("RAGE MIC!")
        self.root.geometry("800x900")
        
        self.icon = None
        try:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(base_path, "icon.png")
            if os.path.exists(icon_path):
                self.icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(False, self.icon)
            else:
                print(f"İkon dosyası bulunamadı: {icon_path}")
        except Exception as e:
            print(f"İkon yüklenemedi: {e}")

        self.processor = AudioProcessor()
        # Kısayol güncellendi (macOS için Command tuşu ile)
        self.toggle_key_display = "⌘⇧R"  # Butonda ve metinlerde gösterilecek (Cmd+Shift+R)
        self.toggle_key_bind = "<Command-Shift-R>" # Tkinter bind için

        self.setup_ui()
        self.load_device_selection()
        self.setup_hotkey()
        self.update_volume_meter()

        last_preset = self.config.get("last_preset")
        if last_preset and last_preset in self.profile_settings:
            self.profile_var.set(last_preset)
            self.apply_profile()
        elif list(self.profile_settings.keys()):
             self.profile_var.set(list(self.profile_settings.keys())[0])
             self.apply_profile()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Config dosyası JSON okuma hatası: {e}. Varsayılan config kullanılacak.")
                self.config = {}
            except Exception as e:
                print(f"Config dosyası yükleme hatası: {e}")
                self.config = {}
        else:
            self.config = {}

    def save_config(self):
        self.config["presets"] = self.profile_settings
        self.config["night_mode"] = self.night_mode
        if hasattr(self, 'profile_var'):
             self.config["last_preset"] = self.profile_var.get()
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Config dosyası kaydetme hatası: {e}")

    def load_device_selection(self):
        if os.path.exists(self.device_file):
            try:
                with open(self.device_file, "r") as f:
                    device_config = json.load(f)
                    input_device_str = device_config.get("input_device", "")
                    output_device_str = device_config.get("output_device", "")
                    
                    input_list = self.processor.get_device_list('input')
                    output_list = self.processor.get_device_list('output')

                    if input_list:
                        self.input_device_combo['values'] = input_list
                        if input_device_str in input_list:
                            self.input_device_var.set(input_device_str)
                        else:
                            self.input_device_var.set(input_list[0])
                    else:
                        self.input_device_combo['values'] = []
                        self.input_device_var.set("")

                    if output_list:
                        self.output_device_combo['values'] = output_list
                        if output_device_str in output_list:
                            self.output_device_var.set(output_device_str)
                        else:
                            self.output_device_var.set(output_list[0])
                    else:
                        self.output_device_combo['values'] = []
                        self.output_device_var.set("")

            except json.JSONDecodeError as e:
                print(f"Cihaz seçim dosyası JSON okuma hatası: {e}")
            except Exception as e:
                print(f"Cihaz seçim yükleme hatası: {e}")
        else:
            input_list = self.processor.get_device_list('input')
            output_list = self.processor.get_device_list('output')
            if input_list:
                self.input_device_combo['values'] = input_list
                self.input_device_var.set(input_list[0])
            if output_list:
                self.output_device_combo['values'] = output_list
                self.output_device_var.set(output_list[0])

    def save_device_selection(self):
        device_config = {
            "input_device": self.input_device_var.get(),
            "output_device": self.output_device_var.get()
        }
        try:
            with open(self.device_file, "w") as f:
                json.dump(device_config, f, indent=4)
        except Exception as e:
            print(f"Cihaz seçim dosyası kaydetme hatası: {e}")

    def on_closing(self):
        print("Kapatılıyor...")
        self.save_config()
        self.save_device_selection()
        self.processor.cleanup()
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.destroy()

    def update_ui_mode(self):
        self.theme_name = "darkly" if self.night_mode else "flatly"
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.style.theme_use(self.theme_name)
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                 self.canvas.config(bg= "gray10" if self.night_mode else "whitesmoke")

    def toggle_ui_mode(self):
        self.night_mode = not self.night_mode
        self.update_ui_mode()

    def add_new_preset(self):
        preset_win = ttk.Toplevel(self.root)
        preset_win.title("Yeni Preset Ekle")
        preset_win.geometry("300x370")
        preset_win.resizable(False, False)
        if self.icon:
            try:
                preset_win.iconphoto(False, self.icon)
            except Exception as e:
                print(f"Preset penceresi için ikon yüklenemedi: {e}")
        
        ttk.Label(preset_win, text="Preset Adı:").pack(pady=5)
        preset_name_entry = ttk.Entry(preset_win)
        preset_name_entry.pack(pady=5, padx=10, fill="x")
        
        ttk.Label(preset_win, text="Gain (0-20):").pack(pady=5)
        gain_entry = ttk.Entry(preset_win)
        gain_entry.pack(pady=5, padx=10, fill="x")
        
        ttk.Label(preset_win, text="Distorsiyon (1-50):").pack(pady=5)
        distortion_entry = ttk.Entry(preset_win)
        distortion_entry.pack(pady=5, padx=10, fill="x")
        
        ttk.Label(preset_win, text="Klip Seviyesi (0.01-1.0):").pack(pady=5)
        clipping_entry = ttk.Entry(preset_win)
        clipping_entry.pack(pady=5, padx=10, fill="x")
        
        def save_preset():
            name = preset_name_entry.get().strip()
            try:
                gain = max(0.0, min(20.0, float(gain_entry.get())))
                distortion = max(1.0, min(50.0, float(distortion_entry.get())))
                clipping = max(0.01, min(1.0, float(clipping_entry.get())))
            except ValueError:
                ttk.Messagebox.show_error("Hata", "Lütfen geçerli sayısal değerler girin!", parent=preset_win)
                return
            if not name:
                ttk.Messagebox.show_error("Hata", "Preset adı boş olamaz!", parent=preset_win)
                return
            if name in self.profile_settings:
                 if not ttk.Messagebox.askyesno("Onay", f"'{name}' adlı preset zaten mevcut. Üzerine yazılsın mı?", parent=preset_win):
                    return

            self.profile_settings[name] = {"gain": gain, "distortion": distortion, "clipping": clipping}
            self.profile_combo['values'] = list(self.profile_settings.keys())
            self.profile_var.set(name)
            self.apply_profile()
            preset_win.destroy()
        
        ttk.Button(preset_win, text="Kaydet", command=save_preset, style="success.TButton").pack(pady=10, padx=10, fill="x")
        
        preset_win.transient(self.root)
        preset_win.grab_set()
        self.root.wait_window(preset_win)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        device_frame = ttk.Labelframe(main_frame, text="Ses Aygıtları")
        device_frame.pack(padx=5, pady=5, fill="x")
        ttk.Label(device_frame, text="Mikrofon:").pack(pady=2)
        self.input_device_var = tk.StringVar()
        self.input_device_combo = ttk.Combobox(device_frame, textvariable=self.input_device_var, state="readonly", width=60)
        self.input_device_combo.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(device_frame, text="Çıkış:").pack(pady=2)
        self.output_device_var = tk.StringVar()
        self.output_device_combo = ttk.Combobox(device_frame, textvariable=self.output_device_var, state="readonly", width=60)
        self.output_device_combo.pack(padx=5, pady=5, fill="x")

        profile_frame = ttk.Labelframe(main_frame, text="Profil Seçimi")
        profile_frame.pack(padx=5, pady=5, fill="x")
        ttk.Label(profile_frame, text="Ön ayarlar:").pack(pady=2)
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.profile_var, state="readonly")
        self.profile_combo['values'] = list(self.profile_settings.keys())
        if list(self.profile_settings.keys()):
            self.profile_combo.current(0)
        self.profile_combo.pack(padx=5, pady=5, fill="x")
        self.profile_combo.bind("<<ComboboxSelected>>", self.apply_profile)
        
        ttk.Button(profile_frame, text="Yeni Preset Ekle", command=self.add_new_preset).pack(pady=5, fill="x")
        
        ttk.Button(main_frame, text="UI Modunu Değiştir (Sabah/Akşam)", command=self.toggle_ui_mode).pack(padx=5, pady=5, fill="x")

        effects_frame = ttk.Labelframe(main_frame, text="Efekt Ayarları")
        effects_frame.pack(padx=5, pady=5, fill="x")
        
        gain_label_frame = ttk.Frame(effects_frame)
        gain_label_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(gain_label_frame, text="Ses seviyesi (Gain):").pack(side="left")
        self.gain_value_label = ttk.Label(gain_label_frame, text=f"{self.profile_settings.get(self.profile_var.get(), {}).get('gain', 1.0):.1f}")
        self.gain_value_label.pack(side="right")
        self.gain_scale = ttk.Scale(effects_frame, from_=0, to=20, orient="horizontal", command=self.update_gain)
        self.gain_scale.set(self.profile_settings.get(self.profile_var.get(), {}).get("gain", 1.0))
        self.gain_scale.pack(fill="x", padx=5, pady=5)
        
        distortion_label_frame = ttk.Frame(effects_frame)
        distortion_label_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(distortion_label_frame, text="Distorsiyon:").pack(side="left")
        self.distortion_value_label = ttk.Label(distortion_label_frame, text=f"{self.profile_settings.get(self.profile_var.get(), {}).get('distortion', 1.0):.1f}")
        self.distortion_value_label.pack(side="right")
        self.distortion_scale = ttk.Scale(effects_frame, from_=1, to=50, orient="horizontal", command=self.update_distortion)
        self.distortion_scale.set(self.profile_settings.get(self.profile_var.get(), {}).get("distortion", 1.0))
        self.distortion_scale.pack(fill="x", padx=5, pady=5)

        clipping_label_frame = ttk.Frame(effects_frame)
        clipping_label_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(clipping_label_frame, text="Klip seviyesi:").pack(side="left")
        self.clipping_value_label = ttk.Label(clipping_label_frame, text=f"{self.profile_settings.get(self.profile_var.get(), {}).get('clipping', 1.0):.2f}")
        self.clipping_value_label.pack(side="right")
        self.clipping_scale = ttk.Scale(effects_frame, from_=0.01, to=1.0, orient="horizontal", command=self.update_clipping)
        self.clipping_scale.set(self.profile_settings.get(self.profile_var.get(), {}).get("clipping", 1.0))
        self.clipping_scale.pack(fill="x", padx=5, pady=5)

        meter_frame = ttk.Labelframe(main_frame, text="Ses Seviyesi Göstergesi")
        meter_frame.pack(padx=5, pady=5, fill="both", expand=True)
        self.canvas = tk.Canvas(meter_frame, bg= "gray10" if self.night_mode else "whitesmoke" , height=100, highlightthickness=0)
        self.canvas.pack(padx=5, pady=5, fill="x", expand=True)
        self.meter_rect = self.canvas.create_rectangle(0, 0, 0, 100, fill="green", outline="")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(padx=5, pady=5, fill="x", side="bottom")
        self.toggle_button_text = f"Efektleri Aç/Kapa ({self.toggle_key_display})" 
        self.toggle_button = ttk.Button(button_frame, text=self.toggle_button_text, command=self.toggle_processing_button_action)
        self.toggle_button.pack(pady=5, fill="x")
        self.stop_button = ttk.Button(button_frame, text="Stream Durdur", command=self.stop_processing)
        self.stop_button.pack(pady=5, fill="x")
        self.info_button = ttk.Button(button_frame, text="Yardım & Bilgi", command=self.show_info)
        self.info_button.pack(pady=5, fill="x")
        self.credits_button = ttk.Button(button_frame, text="Geliştiriciler", command=self.show_credits) 
        self.credits_button.pack(pady=5, fill="x")
        self.status_label = ttk.Label(main_frame, text="Durum: Efektler Kapalı", anchor="center")
        self.status_label.pack(pady=10, fill="x", side="bottom")

    def apply_profile(self, event=None):
        profile = self.profile_var.get()
        settings = self.profile_settings.get(profile)
        if settings:
            new_gain = settings.get("gain", 1.0)
            new_distortion = settings.get("distortion", 1.0)
            new_clipping = settings.get("clipping", 1.0)

            self.gain_scale.set(new_gain)
            self.distortion_scale.set(new_distortion)
            self.clipping_scale.set(new_clipping)
            
            if hasattr(self, 'gain_value_label'): self.gain_value_label.config(text=f"{new_gain:.1f}")
            if hasattr(self, 'distortion_value_label'): self.distortion_value_label.config(text=f"{new_distortion:.1f}")
            if hasattr(self, 'clipping_value_label'): self.clipping_value_label.config(text=f"{new_clipping:.2f}")

            self.processor.gain = float(new_gain)
            self.processor.distortion = float(new_distortion)
            self.processor.clipping = float(new_clipping)

    def setup_hotkey(self):
        self.root.bind(self.toggle_key_bind, self.toggle_processing_hotkey_action)
        print(f"'{self.toggle_key_display}' ({self.toggle_key_bind}) kısayolu uygulama penceresine atandı.")

    def show_info(self):
        info_win = ttk.Toplevel(self.root)
        info_win.title("Yardım & Bilgi")
        info_win.geometry("600x450")
        info_win.resizable(False, False)
        if self.icon:
            try:
                info_win.iconphoto(False, self.icon)
            except Exception as e:
                print(f"Bilgi penceresi için ikon yüklenemedi: {e}")
        
        info_text_content = f"""
        Rage Mic Kullanım Kılavuzu ve Sorun Giderme

        Temel Kullanım:
        1. Mikrofon ve Çıkış aygıtlarınızı seçin.
        2. Bir efekt profili seçin veya ayarları manuel olarak yapın.
        3. "Efektleri Aç/Kapa ({self.toggle_key_display})" butonuna tıklayarak veya uygulama 
           penceresi odaktayken {self.toggle_key_display} tuşlarına basarak efektleri 
           aktif/deaktif edin.
        4. Ses seviyesi göstergesinden mikrofonunuzun ses düzeyini takip edin.

        Sorun Giderme:
        - Ses Gelmiyor/Efektler Çalışmıyor:
            - Doğru mikrofon ve çıkış aygıtlarının seçili olduğundan emin olun.
            - macOS kullanıyorsanız: Sistem Ayarları > Gizlilik ve Güvenlik > Mikrofon
              bölümünden uygulamanın (Rage Mic.app veya python) mikrofon
              erişim izni olduğundan emin olun.
            - "Stream Durdur" butonuna basıp tekrar "Efektleri Aç/Kapa" ile
              başlatmayı deneyin.
        - Kısayol Tuşu ({self.toggle_key_display}) Çalışmıyor:
            - Kısayol, uygulama penceresi aktif (odakta) olduğunda çalışır.
              Farklı bir pencere seçiliyken global olarak çalışmaz.
        - "CABLE Input/Output" gibi sanal ses aygıtları kullanıyorsanız, 
          bu aygıtların sisteminizde doğru şekilde kurulduğundan ve 
          çalıştığından emin olun.

        Katkıda bulunanlar hakkında bilgi için "Geliştiriciler" bölümüne bakınız.
        """
        
        text_container_frame = ttk.Frame(info_win, padding=10)
        text_container_frame.pack(expand=True, fill="both")

        text_widget = tk.Text(text_container_frame, wrap="word", relief="flat", height=15, borderwidth=0)
        text_widget.insert("1.0", info_text_content)
        
        try:
            bg_color = self.root.style.colors.get('bg') 
        except: # Stil veya renkler yoksa varsayılan
            bg_color = "SystemButtonFace" 
        text_widget.config(state="disabled", background=bg_color)

        text_scroll = ttk.Scrollbar(text_container_frame, orient="vertical", command=text_widget.yview, bootstyle="round")
        text_widget['yscrollcommand'] = text_scroll.set

        text_scroll.pack(side="right", fill="y", padx=(0,5))
        text_widget.pack(side="left", expand=True, fill="both")
        
        button_container = ttk.Frame(info_win, padding=(0,0,0,10))
        button_container.pack(fill="x")
        close_button = ttk.Button(button_container, text="Kapat", command=info_win.destroy)
        close_button.pack()

        info_win.transient(self.root)
        info_win.grab_set()
        self.root.wait_window(info_win)

    def show_credits(self):
        credits_win = ttk.Toplevel(self.root)
        credits_win.title("Geliştiriciler")
        credits_win.geometry("400x270")
        credits_win.resizable(False, False)
        if self.icon:
            try:
                credits_win.iconphoto(False, self.icon)
            except Exception as e:
                print(f"Geliştiriciler penceresi için ikon yüklenemedi: {e}")

        credits_text_content = """Rage Mic - Katkıda Bulunanlar

İlk Versiyon: Goblinhan Yıkan
2. Versiyon: Bay Eggex
macOS'e Uyarlayan: Atilla Yalın Öksüz

Bu uygulama, açık kaynaklı çeşitli Python
kütüphanelerinden faydalanılarak geliştirilmiştir.
"""
        content_frame = ttk.Frame(credits_win, padding=20)
        content_frame.pack(expand=True, fill="both")

        credits_label = ttk.Label(content_frame, text=credits_text_content, justify="center")
        credits_label.pack(expand=True, pady=10)

        close_button_frame = ttk.Frame(content_frame)
        close_button_frame.pack(fill="x", pady=(10,0))
        close_button = ttk.Button(close_button_frame, text="Kapat", command=credits_win.destroy)
        close_button.pack()

        credits_win.transient(self.root)
        credits_win.grab_set()
        self.root.wait_window(credits_win)

    def _update_button_and_status(self):
        if self.processor.effects_enabled:
            self.status_label.config(text="Durum: Efektler Açık")
            self.toggle_button.config(text=f"Efektleri Kapat ({self.toggle_key_display})")
        else:
            self.status_label.config(text="Durum: Efektler Kapalı")
            self.toggle_button.config(text=f"Efektleri Aç ({self.toggle_key_display})")

    def toggle_processing_shared_logic(self):
        if not self.input_device_var.get() or not self.output_device_var.get():
            self.status_label.config(text="Hata: Giriş veya çıkış aygıtı seçilmemiş!")
            ttk.Messagebox.showerror("Aygıt Hatası", "Lütfen bir giriş ve çıkış aygıtı seçin.", parent=self.root)
            return False

        if self.processor.stream is None or not self.processor.stream.is_active():
            try:
                input_device_str = self.input_device_var.get()
                input_idx = int(input_device_str.split(':')[0])
                output_device_str = self.output_device_var.get()
                output_idx = int(output_device_str.split(':')[0])
            except (ValueError, IndexError) as e:
                self.status_label.config(text=f"Hata: Geçersiz aygıt formatı ({str(e)})")
                return False
            try:
                self.processor.start_stream(input_idx, output_idx)
                self.processor.effects_enabled = True
            except Exception as err:
                self.status_label.config(text=f"Stream başlatma hatası: {str(err)}")
                ttk.Messagebox.showerror("Stream Hatası", f"Stream başlatılamadı:\n{err}", parent=self.root)
                self.processor.effects_enabled = False
                return False
        else:
            self.processor.effects_enabled = not self.processor.effects_enabled
        
        self._update_button_and_status()
        return True

    def toggle_processing_button_action(self):
        self.toggle_processing_shared_logic()

    def toggle_processing_hotkey_action(self, event=None):
        print(f"'{self.toggle_key_display}' kısayoluna basıldı.")
        self.toggle_processing_shared_logic()

    def stop_processing(self):
        self.processor.stop_stream()
        self.processor.effects_enabled = False
        self._update_button_and_status()
        self.status_label.config(text="Durum: Stream Durduruldu")

    def update_gain(self, value_str):
        value = float(value_str)
        self.processor.gain = value
        if hasattr(self, 'gain_value_label'): self.gain_value_label.config(text=f"{value:.1f}")

    def update_distortion(self, value_str):
        value = float(value_str)
        self.processor.distortion = value
        if hasattr(self, 'distortion_value_label'): self.distortion_value_label.config(text=f"{value:.1f}")

    def update_clipping(self, value_str):
        value = float(value_str)
        self.processor.clipping = value
        if hasattr(self, 'clipping_value_label'): self.clipping_value_label.config(text=f"{value:.2f}")

    def update_volume_meter(self):
        if not (hasattr(self, 'root') and self.root.winfo_exists()):
            return

        amp = self.processor.latest_amplitude
        
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            self.root.after(50, self.update_volume_meter)
            return

        meter_width = int(canvas_width * amp)
        meter_width = max(0, min(canvas_width, meter_width))
        
        self.canvas.coords(self.meter_rect, 0, 0, meter_width, self.canvas.winfo_height())
        
        color = "green"
        if amp > 0.7: color = "red"
        elif amp > 0.3: color = "yellow"
        self.canvas.itemconfig(self.meter_rect, fill=color)
        
        self.root.after(50, self.update_volume_meter)

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Kullanıcı tarafından kesildi.")
        finally:
            self.on_closing()

if __name__ == "__main__":
    try:
        app = AudioEffectGUI()
        app.run()
    except Exception as e:
        print(f"Uygulama başlatılamadı. Hata: {e}")
        import traceback
        traceback.print_exc()
        input("Çıkmak için ENTER tuşuna basın...")