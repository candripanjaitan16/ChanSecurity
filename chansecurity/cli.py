import argparse
import subprocess
import sys
import os
import signal
import time

from . import state
from .autostart import install_autostart

def cmd_run(args):
    if state.is_daemon_alive():
        print("ChanSecurity sudah jalan di background.")
    else:
        answer = input("Aktifkan ChanSecurity otomatis nyala tiap boot/login? [Y/n]: ").strip().lower()
        if answer in ("", "y", "yes"):
            install_autostart()

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

def main():
    parser = argparse.ArgumentParser(prog="chansecurity")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("run").set_defaults(func=cmd_run)
    sub.add_parser("window").set_defaults(func=cmd_window)
    sub.add_parser("stop").set_defaults(func=cmd_stop)
    sub.add_parser("status").set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
