<p align="center">
  <img src="docs/images/logo.png" width="280" alt="ChanSecurity Logo">
</p>

# ChanSecurity v1

**ChanSecurity** adalah solusi monitoring infrastruktur server proaktif 24/7 yang dirancang untuk menjaga keberlangsungan operasional bisnis digital. Alat ini bekerja di latar belakang untuk mendeteksi anomali performa secara *real-time*, memitigasi ancaman siber sejak dini, dan mengirim peringatan otomatis ke email saat kondisi kritis terjadi.

---

## 🚀 Fitur Utama (Version 1)

* **CPU Real-Time Scanning** — Memantau penggunaan prosesor untuk mendeteksi *overload* sistem, aktivitas *malware*, atau indikasi *cryptojacking*.
* **RAM Leak Detection** — Mendeteksi kebocoran memori (*memory leaks*) pada aplikasi perusahaan dan memantau proses mencurigakan di dalam memori.
* **Network Anomaly Monitor** — Mengawasi lalu lintas jaringan untuk mendeteksi lonjakan *traffic* tidak wajar (gejala DDoS) atau indikasi pencurian data (*data exfiltration*).
* **Hybrid GUI/CLI Ecosystem** — Kontrol penuh via Terminal untuk stabilitas *background service*, dikombinasikan dengan Jendela Dashboard grafis interaktif untuk visualisasi data historis.
* **Persistent Background Service** — Sekali diaktifkan, agen pemantau tetap berjalan 24/7 meskipun jendela dashboard ditutup atau perangkat di-*restart*.
* **App Shortcut** — Muncul sebagai aplikasi di menu sistem (Linux/Windows) lengkap dengan icon, tinggal diklik tanpa perlu buka terminal.
* **Notifikasi Email Bertingkat** — Mengirim peringatan otomatis ke Gmail saat CPU/RAM/Network melewati ambang batas, dengan aturan *sustain duration* dan *cooldown* berbeda per tingkat keparahan agar tidak membanjiri inbox.
* **Email Tujuan Terkunci** — Email penerima notifikasi diatur sekali lewat dashboard, lalu otomatis terkunci demi konsistensi konfigurasi.

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
Mengaktifkan agen pemantau. Sistem akan meminta konfirmasi `[Y/n]` untuk mendaftarkan ChanSecurity sebagai *background service* (*systemd* di Linux / *Startup* di Windows) agar tetap aktif 24/7 meskipun perangkat di-*restart*. Shortcut aplikasi juga otomatis ditambahkan ke menu sistem, dan dashboard langsung terbuka.
```bash
chansecurity run
```

### 2. Membuka Dashboard Grafis
Memunculkan kembali jendela dashboard tanpa mengganggu agen yang sedang berjalan.
```bash
chansecurity window
```
> Menutup jendela ini **tidak** menghentikan pemantauan 24/7 di latar belakang.

### 3. Membuka via Shortcut Aplikasi
Dipanggil otomatis saat shortcut di menu aplikasi diklik. Menyalakan daemon secara diam-diam jika belum aktif, lalu langsung membuka dashboard — tanpa pertanyaan interaktif apa pun.
```bash
chansecurity open
```

### 4. Konfigurasi Notifikasi Email
Mengatur kredensial pengirim (Gmail + App Password) dan email tujuan notifikasi.
```bash
chansecurity config
```
> Gmail mewajibkan **App Password** (bukan password akun biasa) untuk pengiriman otomatis. Aktifkan 2-Step Verification di akun Google, lalu buat App Password lewat [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

Aturan notifikasi berlaku untuk CPU, RAM, dan Network:

| Ambang Batas | Durasi Bertahan | Frekuensi Maksimal |
|---|---|---|
| ≥ 80% | 50 detik | 1x per 1 jam |
| ≥ 90% | 50 detik | 1x per 15 menit |
| ≥ 100% | 50 detik | 1x per 10 menit |

### 5. Memeriksa Status Agen
Memastikan apakah agen pemantau sedang `AKTIF` atau `MATI`.
```bash
chansecurity status
```

### 6. Menghentikan Layanan
Mematikan proses pemantauan di latar belakang secara bersih.
```bash
chansecurity stop
```

### 7. Membuka Kunci Email Notifikasi (Admin)
Email tujuan yang sudah diatur lewat dashboard akan otomatis terkunci. Gunakan perintah ini untuk membuka kunci dan mengatur ulang.
```bash
chansecurity reset-email
```

---

## 📧 Notifikasi Email via Dashboard

Kotak input email di bagian bawah dashboard digunakan untuk mengatur **email tujuan** notifikasi. Setelah diisi dan disimpan, kotak tersebut otomatis terkunci (*read-only*) untuk menjaga konsistensi konfigurasi. Kredensial pengirim (Gmail + App Password) diatur terpisah lewat `chansecurity config` demi keamanan.

> ⚠️ Kredensial disimpan secara lokal di `~/.chansecurity/config.json` pada perangkat masing-masing pengguna, tidak dikirim ke server mana pun.

---

## 📋 Persyaratan Sistem

* Python 3.8 atau versi di atasnya
* `pip` dan `setuptools` versi terbaru
* Linux (systemd) atau Windows untuk fitur *autostart* dan shortcut aplikasi
* Akun Gmail dengan 2-Step Verification aktif, untuk fitur notifikasi email

---

## 🎨 Kustomisasi Icon

Icon aplikasi dan shortcut menggunakan file berikut di `chansecurity/assets/`:
* `icon.png` — icon utama (Linux/Mac, digunakan juga untuk shortcut menu)
* `icon.ico` — icon untuk title bar dan shortcut Windows

---

## 🧩 Struktur Project

```
chansecurity/
├── pyproject.toml
├── README.md
└── chansecurity/
    ├── cli.py             # entry point: run, window, open, stop, status, config, reset-email
    ├── daemon.py          # proses background, menulis state & mengecek threshold notifikasi tiap detik
    ├── gui.py             # dashboard tkinter, membaca state, input email notifikasi
    ├── state.py           # penyimpanan state & PID (JSON)
    ├── config.py          # penyimpanan kredensial email & aturan tier notifikasi
    ├── notifier.py        # pengiriman email via SMTP Gmail dengan logika tier & cooldown
    ├── autostart.py       # pendaftaran service systemd / Windows Startup
    ├── shortcut.py        # pembuatan shortcut aplikasi di menu sistem
    ├── assets/
    │   ├── icon.png
    │   └── icon.ico
    └── components/
        ├── cpu.py
        ├── ram.py
        └── network.py
```