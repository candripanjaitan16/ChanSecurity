# ChanSecurity v1

**ChanSecurity** adalah solusi monitoring infrastruktur server proaktif 24/7 yang dirancang untuk menjaga keberlangsungan operasional bisnis digital. Alat ini bekerja di latar belakang untuk mendeteksi anomali performa secara *real-time*, memitigasi ancaman siber sejak dini, dan mengirimkan notifikasi instan langsung ke Gmail Anda ketika sistem mendeteksi adanya masalah.

---

## 🚀 Fitur Utama (Version 1)

Pada versi perdana (v1), ChanSecurity fokus pada tiga fondasi utama kesehatan dan keamanan server:

* **CPU Real-Time Scanning:** Memantau penggunaan prosesor untuk mendeteksi *overload* sistem, aktivitas *malware*, atau indikasi *cryptojacking*.
* **RAM Leak Detection:** Mendeteksi kebocoran memori (*memory leaks*) pada aplikasi perusahaan dan memantau proses mencurigakan di dalam memori.
* **Network Anomaly Monitor:** Mengawasi lalu lintas jaringan untuk mendeteksi lonjakan *traffic* tidak wajar (gejala DDoS) atau indikasi pencurian data (*data exfiltration*).
* **Gmail Alert System:** Sistem peringatan dini otomatis yang mengirimkan email darurat secara instan jika parameter server melewati batas aman (*threshold*).
* **Hybrid GUI/CLI Ecosystem:** Kontrol penuh via Terminal untuk stabilitas *background service*, dikombinasikan dengan Jendela Dashboard grafis interaktif untuk visualisasi data historis.

---

## 🛠️ Langkah Instalasi

Anda dapat memasang ChanSecurity langsung dari repositori GitHub menggunakan `pip`:

```bash
pip install git+https://github.com/username/chansecurity.git
```

---

## 🎛️ Panduan Perintah CLI

Setelah instalasi selesai, Anda dapat mengelola layanan ChanSecurity menggunakan perintah-perintah berikut di Terminal (Linux) atau Command Prompt (Windows):

### 1. Inisialisasi & Aktivasi Layanan
Perintah ini digunakan untuk mengaktifkan agen pemantau. Sistem akan meminta konfirmasi `yes/no` untuk mendaftarkan ChanSecurity sebagai *Background Service* (*Daemon* di Linux / *Windows Service* di Windows) agar tetap aktif 24/7 meskipun server di-*restart*.
```bash
chansecurity run
```

### 2. Membuka Dashboard Grafis
Perintah untuk memunculkan jendela aplikasi (GUI Window). Di sini Anda bisa melihat grafik balok performa dinamis yang bisa di-*scroll* dan interaktif (berubah otomatis saat kartu CPU/RAM/Network di-klik).
```bash
chansecurity window
```
> 💡 *Catatan: Menutup jendela GUI ini tidak akan menghentikan proses pemantauan 24/7 di latar belakang.*

### 3. Memeriksa Status Agen
Perintah cepat untuk memastikan apakah agen pemantau ChanSecurity di latar belakang sedang berjalan aktif (`active`) atau berhenti (`stopped`).
```bash
chansecurity status
```

### 4. Menghentikan Layanan Total
Perintah untuk mematikan seluruh aktivitas pemantauan dan menghapus *background service* secara bersih dari sistem operasi server.
```bash
chansecurity stop
```

---

## 📋 Persyaratan Sistem
* Python 3.8 atau versi di atasnya
* Akses Administrator/Root (diperlukan untuk mendaftarkan *Background Service* 24/7 di sistem operasi)