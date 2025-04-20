# AutoClickerGUI

![AutoClickerGUI](https://img.shields.io/badge/Built%20With-Python-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

## 🚀 Overview
**AutoClickerGUI** is an advanced Python-based tool that automates mouse clicks on specified images (like UI buttons). Whether you're automating tasks on websites or in apps, this tool gives you full control with a beautiful and intuitive GUI.

---

## 🛠 Features
- Image-based clicking automation
- Drag-and-drop image queue
- Click count, confidence level, and loop settings
- Theme toggle (Light 🌞 / Dark 🌙)
- Save & load profiles
- System tray support
- Hotkey support (F3 to Start/Stop)
- Real-time logging with export option

---

## 📦 Installation

### 🐍 Run Python Script
1. Make sure Python is installed ([Download Python](https://www.python.org/downloads/)).
2. Install dependencies:

```bash
pip install pyautogui pystray keyboard customtkinter pillow
```

3. Run the script:

```bash
python AutoClickerGUI.py
```

---

## 🧠 How It Works

### 🖼 Upload Images
Upload PNG/JPG images of the buttons you want clicked. The tool will scan your screen for them.

### ⚙️ Configure Settings
- **Confidence**: Match accuracy (0.5 to 1.0)
- **Clicks per Image**: Number of clicks per match
- **Max Loops**: 0 = infinite
- **Search Delay**: Time between image searches
- **Cycle Delay**: Time between each loop cycle

### ▶️ Start Clicking
Click **Start** to begin. The tool will loop through images and click them as configured.

### ⏹️ Stop Anytime
Click **Stop** or use the `F3` hotkey.

---

## 🧰 Extra Features

### 🔄 System Tray Support
Minimize to tray with quick options:
- Show app
- Start/Stop
- Exit

> Ensure `icon.ico` is in the root directory.

### 💾 Save/Load Profiles
Save all your configs and uploaded images as a `.json` profile to use later.

### 📋 Logs
Real-time logs help you debug or understand app behavior. Export logs to `.txt` for review.

---

## 🧯 Troubleshooting

### 🔍 Image Not Found?
- Make sure the button image is fully visible on your screen.
- Increase confidence tolerance if needed.

### ❌ Tray Icon Not Showing?
- Ensure `icon.ico` exists.
- If missing, a temporary icon will be generated.

---

## 🙋‍♂️ Need Help?
For questions, custom features, or bugs, feel free to reach out via [GitHub Issues](https://github.com/mahmudnibir/AutoClickerGUI/issues) or contact me directly.

---

## 📄 License
MIT License. Feel free to fork, remix, and build on top of it ✨

---

Made by [Nibir Mahmud](https://github.com/mahmudnibir)
