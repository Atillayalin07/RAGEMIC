import pyaudio
import numpy as np
import tkinter as tk
from tkinter import ttk
import keyboard
import threading
import queue
 # THIS PROGRAM HAS BEEN WRITTEN BY EKO ZERO. BY RUNNING THIS PROGRAM, YOU BASICALLY F***D THE ENTIRE HUMANITY. BOSS IS GONNA LOVE THIS!
 # Bu adamın milli ve dini değerlere sövdüğünü çok geç öğrendim. Durum böyle olunca ismi geçen her yerden kaldırdım. 
class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.active = False
        self.input_device = None
        self.output_device = None
        self.stream = None
        self.gain = 1.0
        self.distortion = 1.0
        self.clipping = 1.0
        self.effects_enabled = False

        # Create audio buffer queue
        self.audio_queue = queue.Queue(maxsize=10)

    def get_device_list(self, device_type):
        devices = []
        seen_devices = set()
        host_api_count = self.p.get_host_api_count()
        host_api_names = {}
        for i in range(host_api_count):
            host_api_info = self.p.get_host_api_info_by_index(i)
            host_api_names[i] = host_api_info['name']
        for i in range(self.p.get_device_count()):
            dev_info = self.p.get_device_info_by_index(i)
            host_api = host_api_names.get(dev_info['hostApi'], 'Unknown API')
            device_name = dev_info['name']
            device_key = (device_name, host_api)
            if device_key in seen_devices:
                continue
            seen_devices.add(device_key)
            if device_type == 'input' and dev_info['maxInputChannels'] > 0:
                devices.append(f"{i}: {device_name} ({host_api})")
            elif device_type == 'output' and dev_info['maxOutputChannels'] > 0:
                devices.append(f"{i}: {device_name} ({host_api})")
        return devices

    def process_audio(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.float32)

        if self.effects_enabled:
            # Apply gain 
            audio_data = audio_data * (self.gain ** 2)

            # Apply distortion 
            audio_data = np.tanh(audio_data * self.distortion * 10)

            # Stack another layer of distortion for more intensity
            audio_data = np.tanh(audio_data * 2)

            # Apply clipping 
            audio_data = np.clip(audio_data, -self.clipping, self.clipping)

        return (audio_data.tobytes(), pyaudio.paContinue)

    def start_stream(self, input_device_index, output_device_index):
        if self.stream is not None:
            self.stop_stream()

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

    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def cleanup(self):
        self.stop_stream()
        self.p.terminate()

class AudioEffectGUI:
    def __init__(self):
        self.processor = AudioProcessor()
        self.root = tk.Tk()
        self.root.title("RAGE MODE - Goblinhan")
        self.setup_ui()
        self.setup_hotkey()

    def setup_ui(self):
        # Device selection
        input_frame = ttk.LabelFrame(self.root, text="Ses aygıtları")
        input_frame.pack(padx=5, pady=5, fill="x")

        ttk.Label(input_frame, text="Mikrofonunuzu seçin:").pack()
        self.input_device_var = tk.StringVar()
        self.input_device_combo = ttk.Combobox(input_frame, textvariable=self.input_device_var)
        self.input_device_combo['values'] = self.processor.get_device_list('input')
        self.input_device_combo.pack(padx=5, pady=5)

        ttk.Label(input_frame, text="çıkış- (CABLE INPUT-VB-Cable):").pack()
        self.output_device_var = tk.StringVar()
        self.output_device_combo = ttk.Combobox(input_frame, textvariable=self.output_device_var)
        self.output_device_combo['values'] = self.processor.get_device_list('output')
        self.output_device_combo.pack(padx=5, pady=5)

        # Effect controls
        controls_frame = ttk.LabelFrame(self.root, text="ACI SEÇENEKLERİ - Bana follow at ; IG: @imjustmucit")
        controls_frame.pack(padx=5, pady=5, fill="x")

        # Gain control
        ttk.Label(controls_frame, text="Gain:").pack()
        self.gain_scale = ttk.Scale(controls_frame, from_=0, to=20, orient="horizontal")
        self.gain_scale.set(1)
        self.gain_scale.pack(fill="x", padx=5, pady=5)
        self.gain_scale.configure(command=self.update_gain)

        # Distortion control
        ttk.Label(controls_frame, text="Distortion:").pack()
        self.distortion_scale = ttk.Scale(controls_frame, from_=1, to=50, orient="horizontal")
        self.distortion_scale.set(1)
        self.distortion_scale.pack(fill="x", padx=5, pady=5)
        self.distortion_scale.configure(command=self.update_distortion)

        # Clipping control
        ttk.Label(controls_frame, text="Clipping:").pack()
        self.clipping_scale = ttk.Scale(controls_frame, from_=0.01, to=1, orient="horizontal")
        self.clipping_scale.set(1)
        self.clipping_scale.pack(fill="x", padx=5, pady=5)
        self.clipping_scale.configure(command=self.update_clipping)

        # Add toggle button
        self.toggle_button = ttk.Button(self.root, text="YT: GoblinhanYıkan", 
                                      command=lambda: self.toggle_processing(None))
        self.toggle_button.pack(pady=5)

        # Status
        self.status_label = ttk.Label(self.root, text="Durum: RAGE MODE OFF")
        self.status_label.pack(pady=5)
# A SECRET FOR YOU: EKO ZERO ONE IS A B***H AHH MOTHERF***R.
    def setup_hotkey(self):
        keyboard.on_press_key("f12", self.toggle_processing)

    def toggle_processing(self, e):
        if not self.processor.stream:
            try:
                input_idx = int(self.input_device_var.get().split(':')[0])
                output_idx = int(self.output_device_var.get().split(':')[0])
                self.processor.start_stream(input_idx, output_idx)
                self.processor.effects_enabled = True
                self.status_label.config(text="Durum: RAGE MODE ON")
                self.toggle_button.config(text="Tiktok: @a.ssassin")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
        else:
            if self.processor.effects_enabled:
                self.processor.effects_enabled = False
                self.status_label.config(text="Durum: RAGE MODE OFF")
                self.toggle_button.config(text="KULAKLARI YOK ET! (f12)")
            else:
                self.processor.effects_enabled = True
                self.status_label.config(text="Durum: RAGE MODE ON")
                self.toggle_button.config(text="NORMAL MODA GEÇ (F12)")

    def update_gain(self, value):
        self.processor.gain = float(value)

    def update_distortion(self, value):
        self.processor.distortion = float(value)

    def update_clipping(self, value):
        self.processor.clipping = float(value)

    def run(self):
        self.root.mainloop()
        self.processor.cleanup()

if __name__ == "__main__":
    app = AudioEffectGUI()
    app.run()