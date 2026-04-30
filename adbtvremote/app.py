import subprocess
import threading
import sys
import shutil
import logging
import customtkinter as ctk
import tkinter as tk # For Pydroid3



ADB_PATH = "adb"
LOG_FILE = "remote.log"
LOG_LEVEL = logging.DEBUG

def has_adb():
    return shutil.which(ADB_PATH) is not None

USE_ADB_SHELL = not has_adb()

AdbDeviceTcp = None
if USE_ADB_SHELL:
    try:
        from adb_shell.adb_device import AdbDeviceTcp
        from adb_shell.auth.sign_pythonrsa import PythonRSASigner
    except ImportError:
        USE_ADB_SHELL = False

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.debug(f"has_adb={has_adb()}")
logging.debug(f"USE_ADB_SHELL={USE_ADB_SHELL}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RemoteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.adb_device = None
        
        self.title("Android TV Remote")
        self.geometry("250x600")
        self.minsize(250, 600)

        self.connected_ip = None

        # ---------- TOP BAR ----------
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)

        self.ip_entry = ctk.CTkEntry(self.top_frame, placeholder_text="192.168.1.145:5555")
        self.ip_entry.pack(side="left", expand=True, fill="x", padx=(0,10))

        self.connect_btn = ctk.CTkButton(self.top_frame, text="Connect", width=100, command=self.toggle_connection)
        self.connect_btn.pack(side="right")

        self.status_label = ctk.CTkLabel(self, text="Status: Disconnected")
        self.status_label.pack(pady=5)

        # ---------- SCROLL AREA ----------
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=2)
        self.container.grid_rowconfigure(1, weight=0)
        self.container.grid_rowconfigure(2, weight=0)
        self.container.grid_rowconfigure(3, weight=0)
        self.container.grid_rowconfigure(4, weight=0)
        
        self.build_remote()
        self.bind_keys()
        self.after(0, self.center_window)
        
    def center_window(self):
        w = 360
        h = 600

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        offset_y = 40
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2) - offset_y
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ---------- UI ----------
    def build_remote(self):
        frame = ctk.CTkFrame(self.container)
        frame.grid(row=0, column=0, sticky="n", pady=10)
        frame.grid_anchor("center")

        for i in range(3):
            frame.grid_columnconfigure(i, weight=1, uniform="dpad")
            frame.grid_rowconfigure(i, weight=1, uniform="dpad")

        self.btn(frame, "▲", "KEYCODE_DPAD_UP", 0, 1)
        self.btn(frame, "◀", "KEYCODE_DPAD_LEFT", 1, 0)
        self.btn(frame, "OK", "KEYCODE_DPAD_CENTER", 1, 1)
        self.btn(frame, "▶", "KEYCODE_DPAD_RIGHT", 1, 2)
        self.btn(frame, "▼", "KEYCODE_DPAD_DOWN", 2, 1)

        bottom = ctk.CTkFrame(self.container)
        bottom.grid(row=1, column=0, sticky="ew", pady=10)

        for i in range(3):
            bottom.grid_columnconfigure(i, weight=1)

        self.btn(bottom, "Home", "KEYCODE_HOME", 0, 0)
        self.btn(bottom, "Back", "KEYCODE_BACK", 0, 1)
        self.btn(bottom, "Menu", "KEYCODE_MENU", 0, 2)

        vol = ctk.CTkFrame(self.container)
        vol.grid(row=2, column=0, sticky="ew", pady=10)

        for i in range(3):
            vol.grid_columnconfigure(i, weight=1)


        self.btn(vol, "Vol-", "KEYCODE_VOLUME_DOWN", 0, 0)
        self.btn(vol, "Vol+", "KEYCODE_VOLUME_UP", 0, 1)
        self.btn(vol, "Mute", "KEYCODE_VOLUME_MUTE", 0, 2)

        self.power_btn = ctk.CTkButton(self.container, text="Power", fg_color="red",
                                       command=lambda: self.send_key("KEYCODE_POWER"))
        self.power_btn.grid(row=3, column=0, pady=10, sticky="ew")

        self.text_modal_btn = ctk.CTkButton(self.container, text="Send Text", command=self.open_text_modal)
        self.text_modal_btn.grid(row=4, column=0, pady=10, sticky="ew")

    def btn(self, parent, text, key, r, c):
        b = ctk.CTkButton(
            parent,
            text=text,
            height=60,  # más consistente
            corner_radius=12,
            command=lambda k=key: self.send_key(k)
        )
        b.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

    # ---------- Modal ----------
    def open_text_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Send Text")
        modal.update_idletasks()

        w = 300
        h = 150

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()

        x = parent_x + (parent_w // 2) - (w // 2)
        y = parent_y + (parent_h // 2) - (h // 2)

        modal.geometry(f"{w}x{h}+{x}+{y}")
        
        modal.grab_set()

        entry = ctk.CTkEntry(modal, placeholder_text="Type text...")
        entry.pack(pady=20, padx=20, fill="x")
        modal.lift()
        modal.focus_force()
        modal.after(50, lambda: entry.focus_set())

        def send():
            text = entry.get()
            if text:
                safe_text = text.replace(" ", "%s")
                logging.debug(f"Sending text: {text}")
                if USE_ADB_SHELL and self.adb_device:
                    threading.Thread(
                        target=lambda: self.adb_device.shell(f'input text "{text}"'),
                        daemon=True
                    ).start()
                else:
                    self.run_adb_async(["shell", "input", "text", safe_text])
                modal.destroy()

        ctk.CTkButton(modal, text="Send", command=send).pack(pady=10)
        modal.bind("<Return>", lambda e: send())
        modal.bind("<Escape>", lambda e: modal.destroy())

    # ---------- ADB ----------
    def run_adb_async(self, args, callback=None):
        def task():
            logging.debug(f"ADB call: {args}")
            try:
                kwargs = {
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                    "text": True
                }

                if sys.platform == "win32":
                    kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

                result = subprocess.run([ADB_PATH] + args, **kwargs)

                logging.debug(f"ADB stdout: {result.stdout.strip()}")
                logging.debug(f"ADB stderr: {result.stderr.strip()}")

                if callback:
                    self.after(0, lambda: callback(result))

            except Exception:
                logging.exception("ADB exception")
                if callback:
                    self.after(0, lambda: callback(None))

        threading.Thread(target=task, daemon=True).start()

    def toggle_connection(self):
        if self.connected_ip:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        ip = self.ip_entry.get().strip()
        self.status_label.configure(text="Status: Connecting...")

        if USE_ADB_SHELL:
            def task():
                try:
                    parts = ip.split(":")

                    host = parts[0]
                    port = int(parts[1]) if len(parts) > 1 else 5555
                    port = int(port)

                    device = AdbDeviceTcp(host, port, default_transport_timeout_s=9)

                    device.connect()

                    self.adb_device = device

                    self.after(0, lambda: self._on_connected(ip))
                except Exception:
                    logging.exception("ADB-SHELL connect error")
                    self.after(0, lambda: self.status_label.configure(text="Status: Failed"))

            threading.Thread(target=task, daemon=True).start()

        else:
            def cb(result):
                if not result:
                    self.status_label.configure(text="Status: Error")
                    return

                out = (result.stdout + result.stderr).lower()

                if "connected" in out or "already connected" in out:
                    self._on_connected(ip)
                else:
                    self.status_label.configure(text="Status: Failed")

            self.run_adb_async(["connect", ip], callback=cb)

    def disconnect(self):
        if USE_ADB_SHELL:
            self.adb_device = None
            self.connected_ip = None
            self.status_label.configure(text="Status: Disconnected")
            self.connect_btn.configure(text="Connect")
            self.ip_entry.pack(side="left", expand=True, fill="x", padx=(0,10))
        else:
            ip = self.connected_ip
            self.status_label.configure(text="Status: Disconnecting...")

            def cb(_):
                self.connected_ip = None
                self.status_label.configure(text="Status: Disconnected")
                self.connect_btn.configure(text="Connect")
                self.ip_entry.pack(side="left", expand=True, fill="x", padx=(0,10))

            self.run_adb_async(["disconnect", ip], callback=cb)
        
    def _on_connected(self, ip):
        self.connected_ip = ip
        self.status_label.configure(text=f"Connected: {ip}")
        self.connect_btn.configure(text="Disconnect")
        self.ip_entry.pack_forget()
    
    def send_key(self, keycode):
        if not self.connected_ip:
            return

        if USE_ADB_SHELL and self.adb_device:
            def task():
                try:
                    self.adb_device.shell(f"input keyevent {keycode}")
                except Exception:
                    logging.exception("ADB-SHELL key error")

            threading.Thread(target=task, daemon=True).start()

        else:
            self.run_adb_async(["shell", "input", "keyevent", keycode])

    # ---------- Keyboard ----------
    def bind_keys(self):
        self.bind("<Up>", lambda e: self.send_key("KEYCODE_DPAD_UP"))
        self.bind("<Down>", lambda e: self.send_key("KEYCODE_DPAD_DOWN"))
        self.bind("<Left>", lambda e: self.send_key("KEYCODE_DPAD_LEFT"))
        self.bind("<Right>", lambda e: self.send_key("KEYCODE_DPAD_RIGHT"))
        self.bind("<Return>", lambda e: self.send_key("KEYCODE_DPAD_CENTER"))
        self.bind("<BackSpace>", lambda e: self.send_key("KEYCODE_BACK"))
        self.bind("<Escape>", lambda e: self.send_key("KEYCODE_HOME"))


def main():
    logging.info("Starting app")
    app = RemoteApp()
    app.mainloop()

if __name__ == "__main__":
    main()
