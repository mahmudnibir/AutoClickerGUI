import os
import threading
import time
import json
import sys
import tempfile
import pyautogui
from pyautogui import ImageNotFoundException
import keyboard
import customtkinter as ctk
from tkinter import filedialog, messagebox, Listbox, END, SINGLE, Spinbox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import winsound
import pystray
from pystray import MenuItem as item
from io import BytesIO

# === MAX SPEED CONFIG ===
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

class AutoClickerApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Auto Clicker Pro")
        self.root.geometry("700x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # State
        self.image_paths = []
        self.running = False
        self.click_thread = None
        self.cycle_count = 0
        self.tray_icon = None

        # Layout
        self.control_frame = ctk.CTkFrame(self.root)
        self.control_frame.pack(fill="x", pady=5, padx=5)
        self.list_frame = ctk.CTkFrame(self.root)
        self.list_frame.pack(fill="both", expand=True, pady=5, padx=5)
        self.settings_frame = ctk.CTkFrame(self.root)
        self.settings_frame.pack(fill="x", pady=5, padx=5)
        self.log_frame = ctk.CTkFrame(self.root)
        self.log_frame.pack(fill="both", expand=True, pady=5, padx=5)

        # Controls: Upload, Save, Load, Start, Stop
        self.upload_btn = ctk.CTkButton(self.control_frame, text="Upload Images", command=self.upload_images)
        self.upload_btn.pack(side="left", padx=5)
        self.save_btn = ctk.CTkButton(self.control_frame, text="Save Profile", command=self.save_profile)
        self.save_btn.pack(side="left", padx=5)
        self.load_btn = ctk.CTkButton(self.control_frame, text="Load Profile", command=self.load_profile)
        self.load_btn.pack(side="left", padx=5)
        self.start_btn = ctk.CTkButton(self.control_frame, text="▶️ Start (F3)", fg_color="#32CD32", command=self.toggle_clicking)
        self.start_btn.pack(side="right", padx=5)
        self.stop_btn = ctk.CTkButton(self.control_frame, text="⏹️ Stop", fg_color="#DC143C", command=self.stop_clicking, state="disabled")
        self.stop_btn.pack(side="right", padx=5)

        # Listbox for reorder
        self.listbox = Listbox(self.list_frame, selectmode=SINGLE)
        self.listbox.pack(fill="both", expand=True, side="left", padx=5)
        self.listbox.bind('<Button-1>', self.on_list_click)
        self.listbox.bind('<B1-Motion>', self.on_list_drag)
        self._drag_data = {"x":0, "y":0, "item":None}
        self.scrollbar = ctk.CTkScrollbar(self.list_frame, command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Settings: confidence, clicks per image, max loops, delays, theme
        ctk.CTkLabel(self.settings_frame, text="Confidence").pack(anchor="w", padx=5)
        self.confidence = ctk.CTkSlider(self.settings_frame, from_=0.5, to=0.99, number_of_steps=49)
        self.confidence.set(0.8)
        self.confidence.pack(fill="x", padx=5)

        ctk.CTkLabel(self.settings_frame, text="Clicks per Image").pack(anchor="w", padx=5)
        # Using native Spinbox due to CTkSpinbox unavailability
        self.click_count = Spinbox(self.settings_frame, from_=1, to=10, width=5)
        self.click_count.pack(anchor="w", padx=5)

        ctk.CTkLabel(self.settings_frame, text="Max Loops (0=infinite)").pack(anchor="w", padx=5)
        self.loop_count = ctk.CTkEntry(self.settings_frame, placeholder_text="0")
        self.loop_count.pack(fill="x", padx=5)

        ctk.CTkLabel(self.settings_frame, text="Search Delay").pack(anchor="w", padx=5)
        self.search_delay = ctk.CTkEntry(self.settings_frame, placeholder_text="0.005")
        self.search_delay.pack(fill="x", padx=5)

        ctk.CTkLabel(self.settings_frame, text="Cycle Delay").pack(anchor="w", padx=5)
        self.cycle_delay = ctk.CTkEntry(self.settings_frame, placeholder_text="0")
        self.cycle_delay.pack(fill="x", padx=5)

        self.theme_switch = ctk.CTkSwitch(self.settings_frame, text="Light Theme", command=self.toggle_theme)
        self.theme_switch.pack(pady=5)

        self.progress_label = ctk.CTkLabel(self.settings_frame, text="Cycles: 0")
        self.progress_label.pack(anchor="e", padx=5)

        # Log panel
        self.log_text = ScrolledText(self.log_frame, state='disabled', height=8)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.export_btn = ctk.CTkButton(self.log_frame, text="Export Log", command=self.export_log)
        self.export_btn.pack(pady=5)

        # Hotkey
        keyboard.add_hotkey("F3", self.toggle_clicking)

        # System tray
        self.setup_tray()

        self.root.mainloop()

    # Drag & drop
    def on_list_click(self, event):
        idx = self.listbox.nearest(event.y)
        self._drag_data["item"] = idx

    def on_list_drag(self, event):
        i = self.listbox.nearest(event.y)
        j = self._drag_data["item"]
        if i != j:
            self.image_paths[j], self.image_paths[i] = self.image_paths[i], self.image_paths[j]
            self.refresh_list()
            self._drag_data["item"] = i

    def upload_images(self):
        files = filedialog.askopenfilenames(title="Select button images",
                                            filetypes=[('Image Files','*.png;*.jpg;*.jpeg')])
        if files:
            self.image_paths = list(files)
            self.refresh_list()
            self.log(f"Loaded {len(files)} images")

    def refresh_list(self):
        self.listbox.delete(0, END)
        for p in self.image_paths:
            self.listbox.insert(END, os.path.basename(p))

    def save_profile(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON','*.json')])
        if path:
            data = {
                'images': self.image_paths,
                'confidence': self.confidence.get(),
                'click_count': int(self.click_count.get()),
                'loop_count': int(self.loop_count.get() or 0),
                'search_delay': float(self.search_delay.get() or 0),
                'cycle_delay': float(self.cycle_delay.get() or 0),
                'theme': ctk.get_appearance_mode()
            }
            with open(path,'w') as f: json.dump(data,f)
            self.log(f"Profile saved to {path}")

    def load_profile(self):
        path = filedialog.askopenfilename(filetypes=[('JSON','*.json')])
        if path:
            with open(path) as f: data = json.load(f)
            self.image_paths = data.get('images', [])
            self.confidence.set(data.get('confidence',0.8))
            self.click_count.delete(0, 'end'); self.click_count.insert(0, str(data.get('click_count',1)))
            self.loop_count.delete(0, 'end'); self.loop_count.insert(0, str(data.get('loop_count',0)))
            self.search_delay.delete(0, 'end'); self.search_delay.insert(0, str(data.get('search_delay',0.005)))
            self.cycle_delay.delete(0, 'end'); self.cycle_delay.insert(0, str(data.get('cycle_delay',0)))
            mode = data.get('theme','dark'); ctk.set_appearance_mode(mode)
            self.theme_switch.select() if mode=='light' else self.theme_switch.deselect()
            self.refresh_list()
            self.log(f"Profile loaded from {path}")

    def toggle_theme(self):
        mode = 'light' if self.theme_switch.get() else 'dark'
        ctk.set_appearance_mode(mode)

    def toggle_clicking(self):
        if self.running: self.stop_clicking()
        else: self.start_clicking()

    def start_clicking(self):
        if not self.image_paths:
            messagebox.showwarning("Warning","No images loaded!")
            return
        self.running = True
        self.start_btn.configure(state='disabled'); self.stop_btn.configure(state='normal')
        self.cycle_count = 0; self.progress_label.configure(text="Cycles: 0")
        self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
        self.click_thread.start()
        self.log("Started clicking")

    def stop_clicking(self):
        self.running = False
        self.start_btn.configure(state='normal'); self.stop_btn.configure(state='disabled')
        self.log("Stopped clicking")

    def _click_loop(self):
        max_loops = int(self.loop_count.get() or 0)
        while self.running and (max_loops==0 or self.cycle_count<max_loops):
            for img in self.image_paths:
                if not self.running: break
                loc=None
                while self.running and loc is None:
                    try: loc = pyautogui.locateCenterOnScreen(img, confidence=self.confidence.get(), grayscale=True)
                    except ImageNotFoundException: loc=None
                    if loc is None: time.sleep(float(self.search_delay.get() or 0))
                if not self.running: break
                for _ in range(int(self.click_count.get())): pyautogui.click(loc)
                self.log(f"Clicked {os.path.basename(img)} @ {loc}")
                    # Refresh the tab after each cycle
            pyautogui.hotkey("ctrl", "r")  # or use pyautogui.press("f5")
            self.log("Browser refreshed")
            self.cycle_count +=1
            self.progress_label.configure(text=f"Cycles: {self.cycle_count}")
          #   winsound.Beep(1000, 100)
            time.sleep(float(self.cycle_delay.get() or 0))
        self.stop_clicking()

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log_text.configure(state='normal')
        self.log_text.insert(END,f"[{ts}] {msg}\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(END)

    def export_log(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text','*.txt')])
        if path:
            with open(path,'w') as f: f.write(self.log_text.get('1.0', END))
            messagebox.showinfo("Export","Log exported to " + path)

    def setup_tray(self):
          
          icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

          if not os.path.exists(icon_path):
               icon_path = os.path.join(tempfile.gettempdir(), "icon.ico")
               if not os.path.exists(icon_path):
                    # Create a temporary icon file if it doesn't exist
                    with open(icon_path, 'wb') as f:
                         img = Image.new('RGB', (16, 16), color='blue')
                         img.save(f, format='ICO')

          img = Image.open(icon_path)

          self.tray_icon = pystray.Icon('auto_clicker', img, 'AutoClicker', menu=pystray.Menu(
               item('Show', lambda: self.root.deiconify()),
               item('Start/Stop', lambda: self.toggle_clicking()),
               item('Exit', lambda: self.exit_app())
          ))

          self.root.bind('<Unmap>', self.minimize_to_tray)
     

    def minimize_to_tray(self, event):
        if self.root.state()=='iconic':
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            self.root.withdraw()

    def on_close(self): self.exit_app()
    def exit_app(self):
        try: self.tray_icon.stop()
        except: pass
        self.running=False
        self.root.destroy()
        sys.exit()

if __name__ == '__main__':
    AutoClickerApp()
