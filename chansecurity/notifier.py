import smtplib
import time
from email.mime.text import MIMEText

from . import config as config_module

_tier_state = {}
_last_sent = {}

def send_email(cfg, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = cfg["gmail_address"]
    msg["To"] = cfg["email_to"]

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(cfg["gmail_address"], cfg["gmail_app_password"])
        server.sendmail(cfg["gmail_address"], [cfg["email_to"]], msg.as_string())

def _matching_tier(value, tiers):
    matched = None
    for level, sustain, cooldown in tiers:
        if value >= level:
            matched = (level, sustain, cooldown)
    return matched

def check_and_notify(cpu, ram, net):
    cfg = config_module.load_config()
    if not config_module.is_configured(cfg):
        return

    now = time.time()
    metrics = {
        "CPU": (cpu, cfg["tiers"]["cpu"]),
        "RAM": (ram, cfg["tiers"]["ram"]),
        "NETWORK": (net, cfg["tiers"]["network"]),
    }

    for name, (value, tiers) in metrics.items():
        tier = _matching_tier(value, tiers)
        state = _tier_state.setdefault(name, {"level": None, "since": None})

        if tier is None:
            state["level"] = None
            state["since"] = None
            continue

        level, sustain, cooldown = tier

        if state["level"] != level:
            state["level"] = level
            state["since"] = now
            continue

        if now - state["since"] < sustain:
            continue

        last = _last_sent.get((name, level), 0)
        if now - last < cooldown:
            continue

        subject = f"[ChanSecurity] Peringatan {name} {level}%"
        body = (
            f"ChanSecurity mendeteksi penggunaan {name} bertahan di atas {level}% "
            f"selama minimal {sustain} detik.\n\n"
            f"Nilai saat ini: {value}%\n"
            f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        try:
            send_email(cfg, subject, body)
            _last_sent[(name, level)] = now
        except Exception:
            pass