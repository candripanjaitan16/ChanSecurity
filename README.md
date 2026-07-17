<p align="center">
  <img src="docs/images/logo.png" width="280" alt="ChanSecurity Logo">
</p>

# ChanSecurity v1

**ChanSecurity** adalah solusi monitoring infrastruktur server proaktif 24/7 yang dirancang untuk menjaga keberlangsungan operasional bisnis digital. Alat ini bekerja di latar belakang untuk mendeteksi anomali performa secara *real-time*, memitigasi ancaman siber sejak dini.

---

## 🚀 Fitur Utama (Version 1)

Pada versi perdana (v1), ChanSecurity fokus pada tiga fondasi utama kesehatan dan keamanan server:

* **CPU Real-Time Scanning** — Memantau penggunaan prosesor untuk mendeteksi *overload* sistem, aktivitas *malware*, atau indikasi *cryptojacking*.
* **RAM Leak Detection** — Mendeteksi kebocoran memori (*memory leaks*) pada aplikasi perusahaan dan memantau proses mencurigakan di dalam memori.
* **Network Anomaly Monitor** — Mengawasi lalu lintas jaringan untuk mendeteksi lonjakan *traffic* tidak wajar (gejala DDoS) atau indikasi pencurian data (*data exfiltration*).
* **Hybrid GUI/CLI Ecosystem** — Kontrol penuh via Terminal untuk stabilitas *background service*, dikombinasikan dengan Jendela Dashboard grafis interaktif untuk visualisasi data historis.
* **Persistent Background Service** — Sekali diaktifkan, agen pemantau tetap berjalan 24/7 meskipun jendela dashboard ditutup atau server di-*restart*.

---

## 🛠️ Langkah Instalasi

Pasang ChanSecurity langsung dari repositori GitHub menggunakan `pip`:

```bash
pip install git+https://github.com/candripanjaitan16/chansecurity.git --no-build-isolation
```

> 💡 **Kenapa perlu `--no-build-isolation`?**
> Secara default, `pip` membangun paket di dalam *sandbox* terisolasi dan mengunduh `setuptools` versi terbaru untuk membaca konfigurasi project. Pada sejumlah environment, proses ini gagal mengenali metadata project sehingga paket terpasang sebagai `UNKNOWN` alih-alih `chansecurity`. Flag ini memaksa `pip` memakai `setuptools` yang sudah terpasang di sistem, yang terbukti lebih stabil untuk instalasi ini.

**Prasyarat sebelum instalasi:**
```bash
pip install --upgrade setuptools
```

---

## 🎛️ Panduan Perintah CLI

Setelah instalasi selesai, kelola layanan ChanSecurity menggunakan perintah berikut di Terminal (Linux) atau Command Prompt (Windows):

### 1. Inisialisasi & Aktivasi Layanan
Mengaktifkan agen pemantau. Sistem akan meminta konfirmasi `[Y/n]` untuk mendaftarkan ChanSecurity sebagai *background service* (*systemd* di Linux / *Startup* di Windows) agar tetap aktif 24/7 meskipun perangkat di-*restart*. Dashboard langsung terbuka setelah agen aktif.
```bash
chansecurity run
```

### 2. Membuka Dashboard Grafis
Memunculkan kembali jendela dashboard tanpa mengganggu agen yang sedang berjalan. Grafik balok performa berubah otomatis saat kartu CPU/RAM/Network diklik.
```bash
chansecurity window
```
> Menutup jendela ini **tidak** menghentikan pemantauan 24/7 di latar belakang.

### 3. Memeriksa Status Agen
Memastikan apakah agen pemantau sedang `AKTIF` atau `MATI`.
```bash
chansecurity status
```

### 4. Menghentikan Layanan
Mematikan proses pemantauan di latar belakang secara bersih.
```bash
chansecurity stop
```

---

## 📋 Persyaratan Sistem

* Python 3.8 atau versi di atasnya
* `pip` dan `setuptools` versi terbaru
* Linux (systemd) atau Windows untuk fitur *autostart*

---

## 🧩 Struktur Project

```
chansecurity/
├── pyproject.toml
├── README.md
└── chansecurity/
    ├── cli.py             # entry point: run, window, stop, status
    ├── daemon.py          # proses background, menulis state tiap detik
    ├── gui.py             # dashboard tkinter, membaca state
    ├── state.py           # penyimpanan state & PID (JSON)
    ├── autostart.py       # pendaftaran service systemd / Windows Startup
    └── components/
        ├── cpu.py
        ├── ram.py
        └── network.py
```