import argparse
import subprocess
import sys
import os
import signal
import time
import getpass

from . import state
from . import config as config_module
from .autostart import install_autostart
from .shortcut import install_shortcut

def cmd_run(args):
    if state.is_daemon_alive():
        print("ChanSecurity sudah jalan di background.")
    else:
        answer = input("Aktifkan ChanSecurity otomatis nyala tiap boot/login? [Y/n]: ").strip().lower()
        if answer in ("", "y", "yes"):
            install_autostart()

        install_shortcut()

        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        else:
            kwargs["start_new_session"] = True

        subprocess.Popen([sys.executable, "-m", "chansecurity.daemon"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs)
        time.sleep(0.5)
        print("Daemon ChanSecurity nyala di background.")

    cmd_window(args)

def cmd_window(args):
    if not state.is_daemon_alive():
        print("Daemon belum jalan. Jalankan 'chansecurity run' dulu.")
        return
    from .gui import launch
    launch()

def cmd_open(args):
    if not state.is_daemon_alive():
        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        else:
            kwargs["start_new_session"] = True
        subprocess.Popen([sys.executable, "-m", "chansecurity.daemon"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs)
        time.sleep(0.5)
    from .gui import launch
    launch()

def cmd_stop(args):
    pid = state.read_pid()
    if pid is None or not state.is_daemon_alive():
        print("ChanSecurity tidak sedang jalan.")
        return
    os.kill(pid, signal.SIGTERM)
    state.clear_pid()
    print("ChanSecurity dihentikan.")

def cmd_status(args):
    print("Status: AKTIF" if state.is_daemon_alive() else "Status: MATI")

def cmd_config(args):
    cfg = config_module.load_config()

    print("Setup notifikasi email ChanSecurity")
    print("Kosongkan input untuk tetap pakai nilai lama.\n")

    gmail = input(f"Alamat Gmail pengirim [{cfg['gmail_address']}]: ").strip()
    if gmail:
        cfg["gmail_address"] = gmail

    app_password = getpass.getpass("Gmail App Password (16 karakter, kosongkan jika tidak diubah): ").strip()
    if app_password:
        cfg["gmail_app_password"] = app_password

    email_to = input(f"Kirim notifikasi ke email [{cfg['email_to']}]: ").strip()
    if email_to:
        cfg["email_to"] = email_to

    print("\nAturan notifikasi (tetap, berlaku untuk CPU/RAM/NETWORK):")
    print("  >= 80% selama 50 detik -> maksimal 1x per jam")
    print("  >= 90% selama 50 detik -> maksimal 1x per 15 menit")
    print("  >= 100% selama 50 detik -> maksimal 1x per 10 menit")

    config_module.save_config(cfg)
    print("\nKonfigurasi tersimpan.")
    if not config_module.is_configured(cfg):
        print("Peringatan: email pengirim, app password, atau email tujuan masih kosong. Notifikasi belum aktif.")

def cmd_reset_email(args):
    cfg = config_module.load_config()
    cfg["email_to"] = ""
    cfg["email_locked"] = False
    config_module.save_config(cfg)
    print("Kunci email notifikasi dibuka. Silakan atur ulang lewat dashboard.")

def main():
    parser = argparse.ArgumentParser(prog="chansecurity")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("run").set_defaults(func=cmd_run)
    sub.add_parser("window").set_defaults(func=cmd_window)
    sub.add_parser("open").set_defaults(func=cmd_open)
    sub.add_parser("stop").set_defaults(func=cmd_stop)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("config").set_defaults(func=cmd_config)
    sub.add_parser("reset-email").set_defaults(func=cmd_reset_email)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()