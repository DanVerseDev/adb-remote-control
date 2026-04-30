# Android TV Remote 📺

A lightweight Python remote control for Android TV using ADB over network.  
Works on desktop and mobile (Pydroid3).

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-PC%20%7C%20Android-green)
![ADB](https://img.shields.io/badge/ADB-Network-orange)
![PyPI](https://img.shields.io/badge/PyPI-adbtvremote-blue)

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

- Python 3.8+
- ADB installed and accessible in PATH

## ⚡ Quick Start

### Option 1: Install with pipx (Recommended)

```bash
pipx install adbtvremote
adbtvremote
```

> **Why pipx?** Keeps the app isolated in its own virtual environment, avoiding dependency conflicts with other Python projects.

### Option 2: Install with pip

```bash
pip install adbtvremote
adbtvremote
```

### Option 3: Run from source

```bash
git clone https://github.com/DanVerseDev/android-tv-remote.git
cd android-tv-remote
pip install -r requirements.txt
python main.py
```

### Pydroid3 (Android)

1. Install the package via pip in Pydroid3:

```bash
pip install adbtvremote
```

2. Create a new Python script (e.g., `run.py`) with the following content:

```python
from adbtvremote import app
import tkinter
app.main()
```

3. Run the script in Pydroid3.

> **Note:** Make sure `customtkinter` is installed and the ADB binary is available on your Android device (manual setup may be required).

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

After installation, simply run:

```bash
adbtvremote
```

Or if running from source:

```bash
python main.py
```

### Connect

- Enter IP: `192.168.x.x:####`
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

- Uses `adb shell input keyevent` for buttons
- Uses `adb shell input text` for text input
- Runs ADB commands in background threads
- Logs all activity for debugging to `remote.log`

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
- Text input replaces spaces with `%s` (ADB limitation)

## 🐞 Logging

All ADB calls and errors are logged in `remote.log`

## 📄 License
MIT License - Copyright (c) 2026 Daniel Martí

---
Built with ❤️ by [Daniel Martí](https://gravatar.com/danversedev) aka [DanVerse](https://github.com/DanVerseDev)
