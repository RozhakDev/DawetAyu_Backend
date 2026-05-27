import json
from django.db.models import Sum
from django.utils import timezone
from users.models import CustomUser
from orders.models import Order

def dashboard_callback(request, context):
    """
    Menyusun ringkasan metrik performa untuk dashboard admin.

    Menghitung jumlah pengguna, status pesanan, total omzet, serta merangkum
    data grafik pendapatan harian selama seminggu terakhir.

    Args:
        request (Request): Objek request dari halaman dashboard admin.
        context (dict): Context data bawaan dari panel admin Unfold.

    Returns:
        dict: Data context yang telah diperbarui dengan KPI dan informasi grafik.
    """
    total_users = CustomUser.objects.filter(role='customer').count()
    pending_orders = Order.objects.filter(order_status='pending').count()
    completed_orders = Order.objects.filter(order_status='completed').count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_price'))['total'] or 0

    days = []
    revenues = []
    today = timezone.now().date()
    for i in range(6, -1, -1):
        d = today - timezone.timedelta(days=i)
        daily_revenue = Order.objects.filter(
            payment_status='paid', 
            created_at__date=d
        ).aggregate(total=Sum('total_price'))['total'] or 0
        days.append(d.strftime('%d %b'))
        revenues.append(int(daily_revenue))
        
    chart_data = json.dumps({
        "labels": days,
        "datasets": [
            {
                "label": "Pendapatan Harian (Rp)",
                "data": revenues,
                "borderColor": "#4F8A5B",
                "backgroundColor": "rgba(79, 138, 91, 0.2)",
                "fill": True,
                "tension": 0.4
            }
        ]
    })

    context.update({
        "kpis": [
            {
                "title": "Total Pelanggan",
                "metric": f"{total_users}",
            },
            {
                "title": "Pesanan Menunggu",
                "metric": f"{pending_orders}",
            },
            {
                "title": "Pesanan Selesai",
                "metric": f"{completed_orders}",
            },
            {
                "title": "Total Pendapatan",
                "metric": f"Rp {total_revenue:,.0f}".replace(",", "."),
            },
        ],
        "chart_data": chart_data
    })
    return context