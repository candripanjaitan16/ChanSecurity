import psutil

def get_ram_usage():
    return psutil.virtual_memory().percent
