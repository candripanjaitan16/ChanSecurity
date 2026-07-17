import signal
import sys
import time

from .components.cpu import get_cpu_usage
from .components.ram import get_ram_usage
from .components.network import get_network_usage
from . import state

HISTORY_LEN = 20
running = True

def handle_stop(signum, frame):
    global running
    running = False

def main():
    signal.signal(signal.SIGTERM, handle_stop)
    signal.signal(signal.SIGINT, handle_stop)
    state.write_pid()

    history = {"CPU": [0] * HISTORY_LEN, "RAM": [0] * HISTORY_LEN, "NETWORK": [0] * HISTORY_LEN}

    while running:
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        net = get_network_usage()

        for key, val in [("CPU", cpu), ("RAM", ram), ("NETWORK", net)]:
            history[key].append(val)
            history[key].pop(0)

        state.write_state({
            "cpu": cpu,
            "ram": ram,
            "net": net,
            "history": history,
            "timestamp": time.strftime("%H:%M:%S"),
        })
        time.sleep(1)

    state.clear_pid()
    sys.exit(0)

if __name__ == "__main__":
    main()
