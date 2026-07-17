import platform
import subprocess
import sys
from pathlib import Path

def install_autostart():
    system = platform.system()
    if system == "Linux":
        _install_linux()
    elif system == "Windows":
        _install_windows()
    else:
        print(f"Autostart belum didukung untuk OS: {system}")

def _install_linux():
    unit_dir = Path.home() / ".config/systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    unit_file = unit_dir / "chansecurity.service"

    unit_file.write_text(f"""[Unit]
Description=ChanSecurity Monitoring Daemon

[Service]
ExecStart={sys.executable} -m chansecurity.daemon
Restart=no

[Install]
WantedBy=default.target
""")
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    subprocess.run(["systemctl", "--user", "enable", "--now", "chansecurity.service"], check=False)
    print("Autostart terpasang lewat systemd --user.")

def _install_windows():
    startup_dir = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    bat_path = startup_dir / "chansecurity.bat"
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    bat_path.write_text(f'start "" "{pythonw}" -m chansecurity.daemon\n')
    print("Autostart terpasang di folder Startup Windows.")
