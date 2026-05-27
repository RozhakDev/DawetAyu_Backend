import requests
import hmac
import hashlib
from django.conf import settings
from rest_framework.exceptions import APIException

class PaymenkuService:
    def __init__(self):
        self.base_url = settings.PAYMENKU_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {settings.PAYMENKU_API_KEY}',
            'Content-Type': 'application/json'
        }

    def _handle_response(self, response):
        try:
            data = response.json()
            if response.status_code not in [200, 201] or data.get('status') != 'success':
                raise APIException(f"Paymenku Error: {data.get('message', 'Unknown error')}")
            return data.get('data')
        except ValueError:
            raise APIException("Invalid JSON response from Paymenku")
    
    def get_payment_channels(self):
        url = f"{self.base_url}/payment-channels"
        response = requests.get(url, headers=self.headers, timeout=30)
        return self._handle_response(response)
    
    def create_transaction(self, order, channel_code, return_url):
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
        url = f"{self.base_url}/check-status/{trx_id}"
        response = requests.get(url, headers=self.headers, timeout=30)
        return self._handle_response(response)

    @staticmethod
    def verify_webhook_signature(signature, timestamp, raw_body):
        secret = bytes(settings.PAYMENKU_WEBHOOK_SECRET, 'utf-8')
        message = bytes(f"{timestamp}.{raw_body}", 'utf-8')

        generated_signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(generated_signature, signature)