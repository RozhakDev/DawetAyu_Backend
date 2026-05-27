# AyuPay Backend

AyuPay merupakan backend API untuk sistem pemesanan dan pembayaran digital Dawet Ayu khas Banjarnegara. Sistem ini dibangun untuk membantu digitalisasi UMKM melalui pengelolaan produk, transaksi, pembayaran online, dan administrasi berbasis web dalam satu arsitektur terpusat.

Backend menggunakan Django REST Framework sebagai pusat business logic dan komunikasi data antara aplikasi mobile Flutter dengan sistem administrasi. Selain menangani autentikasi dan transaksi, backend juga mengelola integrasi payment gateway *Paymenku* serta webhook pembayaran otomatis.

## Fitur Utama

- **Admin Dashboard:** Dashboard administrasi menggunakan Django Unfold untuk pengelolaan data, transaksi, dan monitoring sistem.
- **Authentication API:** Sistem autentikasi berbasis JWT untuk login, register, dan pengelolaan akses pengguna.
- **Product & Order Management:** Pengelolaan produk, kategori, checkout, dan pemrosesan pesanan customer melalui REST API.
- **Payment Gateway Integration:** Integrasi Paymenku untuk transaksi pembayaran digital beserta webhook validasi otomatis.

## Teknologi

- Django
- Django REST Framework
- Django Unfold
- JWT Authentication
- SQLite / MySQL
- Paymenku Payment Gateway
- Swagger OpenAPI

## Instalasi

1. Clone repository
   
   ```bash
   git clone https://github.com/RozhakDev/AyuPay_Backend.git
   cd AyuPay_Backend
   ```

2. Setup environment
   
   ```bash
   python -m venv venv
   source venv/bin/activate
   cp .env.example .env
   ```

3. Install dependency
   
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan server
   
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Dokumentasi

Swagger OpenAPI tersedia pada endpoint berikut:

```text
http://127.0.0.1:8000/api/v1/docs/
```

Panel administrasi Django tersedia pada:

```text
http://127.0.0.1:8000/admin/
```

## Catatan

> Sistem dirancang menggunakan arsitektur client-server sederhana dengan pendekatan REST API berbasis JSON. Backend dioptimalkan untuk deployment ringan seperti shared hosting berbasis WSGI tanpa penggunaan service realtime tambahan seperti WebSocket, Redis, atau message broker agar tetap sederhana, ringan, dan mudah dikembangkan.

## Lisensi

Project ini menggunakan lisensi MIT. Silakan lihat file `LICENSE` untuk informasi lebih lanjut.