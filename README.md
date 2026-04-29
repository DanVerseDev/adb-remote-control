# Android TV Remote 📺

A lightweight Python remote control for Android TV using ADB over network.  
Works on desktop and mobile (Pydroid3).

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-PC%20%7C%20Android-green)
![ADB](https://img.shields.io/badge/ADB-Network-orange)

<img width="301" height="664" alt="screenshot" src="https://github.com/user-attachments/assets/85c94742-4329-4cac-bde3-0e112f880184" />

## ✨ Features

- 📡 ADB over WiFi (no USB required)
- 🎮 Full D-Pad control (navigation + OK)
- 🔊 Volume & Power controls
- 🏠 System buttons (Home, Back, Menu)
- ⌨️ Send text input to the device
- 🧵 Async ADB calls (non-blocking UI)
- 📱 Responsive UI (auto scaling)
- ⌨️ Keyboard shortcuts support
- 📝 Logging system (remote.log)

## 📦 Requirements

- Python 3.x
- ADB installed and accessible in PATH

## ⚡ Quick Start

```bash
pip install customtkinter
python main.py
```

### Python dependencies

```bash
pip install customtkinter
```

### Pydroid3 (Android)

Install:
- customtkinter
- ADB binary (manual setup may be required)

## ⚙️ Setup (ADB over Network)

1. Enable developer options on your Android TV
2. Enable:
   - USB debugging
   - Wireless debugging (if available)

3. Connect once via USB (optional but recommended):

```bash
adb tcpip 5555
```

4. Get device IP and connect:

```bash
adb connect 192.168.x.x:5555
```

## 🚀 Usage

Run the script:

```bash
python main.py
```

### Connect

- Enter IP: 192.168.x.x:####
- Click **Connect**

### Controls

- UI buttons for navigation and system actions
- Keyboard:
  - Arrow keys → Navigation
  - Enter → OK
  - Backspace → Back
  - Escape → Home

### Send Text

- Click **Send Text**
- Input text and send directly to device

## 🧠 How it works

- Uses adb shell input keyevent for buttons
- Uses adb shell input text for text input
- Runs ADB commands in background threads
- Logs all activity for debugging to remote.log

## 📁 Project Structure

```
.
├── main.py
├── remote.log (generated)
└── README.md
```

## ⚠️ Notes

- Device and host must be on the same network
- Some TVs may require pairing for wireless ADB
- Text input replaces spaces with %s (ADB limitation)

## 🐞 Logging

All ADB calls and errors are logged in remote.log

## 📄 License
MIT License - Copyright (c) 2026 Daniel Martí

---
Built with ❤️ by [Daniel Martí](https://gravatar.com/danversedev) aka DanVerse(https://github.com/DanVerseDev).
