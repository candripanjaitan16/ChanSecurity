import platform
import subprocess
import sys
from pathlib import Path

def install_shortcut():
    system = platform.system()
    if system == "Linux":
        _install_linux()
    elif system == "Windows":
        _install_windows()

def _icon_path():
    icon_dir = Path(__file__).parent / "assets"
    ico = icon_dir / "icon.ico"
    png = icon_dir / "icon.png"
    if png.exists():
        return png
    if ico.exists():
        return ico
    return None

def _install_linux():
    apps_dir = Path.home() / ".local/share/applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    desktop_file = apps_dir / "chansecurity.desktop"
    icon = _icon_path()

    desktop_file.write_text(f"""[Desktop Entry]
Type=Application
Name=ChanSecurity
Comment=Monitoring CPU, RAM, dan Network secara real-time
Exec={sys.executable} -m chansecurity.cli open
Icon={icon if icon else "utilities-system-monitor"}
Terminal=false
Categories=System;Monitor;
""")
    desktop_file.chmod(0o755)
    print("Shortcut ChanSecurity ditambahkan ke menu aplikasi.")

def _install_windows():
    start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
    shortcut_path = start_menu / "ChanSecurity.lnk"
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    icon = _icon_path()
    icon_line = f'$s.IconLocation = "{icon}"' if icon else ""

    ps_script = f"""
$w = New-Object -ComObject WScript.Shell
$s = $w.CreateShortcut("{shortcut_path}")
$s.TargetPath = "{pythonw}"
$s.Arguments = "-m chansecurity.cli open"
{icon_line}
$s.Save()
"""
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=False, capture_output=True)
        print("Shortcut ChanSecurity ditambahkan ke Start Menu.")
    except FileNotFoundError:
        print("Tidak bisa membuat shortcut otomatis di Windows.")