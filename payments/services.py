import requests
import hmac
import hashlib
from django.conf import settings
from rest_framework.exceptions import APIException

class PaymenkuService:
    """
    Layanan integrasi API Payment Gateway Paymenku.

    Menghubungkan backend sistem dengan gateway eksternal untuk sinkronisasi daftar
    saluran bayar, pembuatan tautan transaksi, dan pengecekan status transaksi.
    """
    def __init__(self):
        """
        Inisialisasi awal properti API Paymenku.

        Memuat basis alamat URL server dan menyusun header otorisasi Bearer Token.
        """
        self.base_url = settings.PAYMENKU_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {settings.PAYMENKU_API_KEY}',
            'Content-Type': 'application/json'
        }

    def _handle_response(self, response):
        """
        Menangani parsing respons server Paymenku secara seragam.

        Args:
            response (Response): Objek HTTP response hasil request.

        Returns:
            dict: Data payload utama yang dikembalikan Paymenku.

        Raises:
            APIException: Jika respons status gagal atau format respons rusak.
        """
        try:
            data = response.json()
            if response.status_code not in [200, 201] or data.get('status') != 'success':
                raise APIException(f"Paymenku Error: {data.get('message', 'Unknown error')}")
            return data.get('data')
        except ValueError:
            raise APIException("Invalid JSON response from Paymenku")
    
    def get_payment_channels(self):
        """
        Mengambil daftar channel pembayaran yang didukung.

        Returns:
            list: Daftar metode pembayaran aktif (seperti VA, QRIS, dll).
        """
        url = f"{self.base_url}/payment-channels"
        response = requests.get(url, headers=self.headers, timeout=30)
        return self._handle_response(response)
    
    def create_transaction(self, order, channel_code, return_url):
        """
        Membuat invoice transaksi pembayaran baru di server Paymenku.

        Args:
            order (Order): Objek model pesanan terkait.
            channel_code (str): Kode metode pembayaran yang dipilih.
            return_url (str): URL tujuan pengalihan setelah pembayaran sukses.

        Returns:
            dict: Data transaksi (trx_id, status, pay_url) dari Paymenku.
        """
        url = f"{self.base_url}/transaction/create"
        payload = {
            "channel_code": channel_code,
            "amount": int(order.total_price),
            "reference_id": f"ORD-{order.id}",
            "customer_name": order.user.name,
            "customer_email": order.user.email,
            "return_url": return_url
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        return self._handle_response(response)

    def check_status(self, trx_id):
        """
        Memeriksa status pembayaran dari suatu ID transaksi.

        Args:
            trx_id (str): ID transaksi unik di Paymenku.

        Returns:
            dict: Data status detail terkini dari transaksi tersebut.
        """
        url = f"{self.base_url}/check-status/{trx_id}"
        response = requests.get(url, headers=self.headers, timeout=30)
        return self._handle_response(response)

    @staticmethod
    def verify_webhook_signature(signature, timestamp, raw_body):
        """
        Memverifikasi keaslian signature notifikasi webhook dari Paymenku.

        Args:
            signature (str): Signature rahasia dari header request.
            timestamp (str): Timestamp pengiriman dari header request.
            raw_body (str): Body mentah data request webhook.

        Returns:
            bool: Mengembalikan True jika signature cocok dan valid.
        """
        secret = bytes(settings.PAYMENKU_WEBHOOK_SECRET, 'utf-8')
        message = bytes(f"{timestamp}.{raw_body}", 'utf-8')

        generated_signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(generated_signature, signature)