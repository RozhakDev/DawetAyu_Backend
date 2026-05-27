import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

PAYMENKU_API_KEY = env('PAYMENKU_API_KEY')
PAYMENKU_BASE_URL = env('PAYMENKU_BASE_URL', default='https://paymenku.com/api/v1')
PAYMENKU_WEBHOOK_SECRET = env('PAYMENKU_WEBHOOK_SECRET', default='')

FRONTEND_RETURN_URL = env('FRONTEND_RETURN_URL', default=f'http://localhost:3000/success')

INSTALLED_APPS = [
    "unfold",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    # Third Party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular', # Dokumentasi API
    
    # Local Apps
    'core',
    'users',
    'orders',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'users.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'id' # Bahasa Indonesia
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AyuPay API - Dawet Ayu Banjarnegara',
    'DESCRIPTION': (
        'Dokumentasi resmi REST API untuk platform pemesanan dan pembayaran digital AyuPay.'
        'Sistem ini mengintegrasikan aplikasi mobile (Flutter) dengan backend '
        'untuk melayani pemesanan minuman tradisional khas Banjarnegara secara modern.\n\n'
        '**Autentikasi:** API ini menggunakan otorisasi berbasis JSON Web Token (JWT). '
        'Gunakan format `Bearer <token>` pada header permintaan untuk mengakses endpoint privat.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'TAGS': [
        {'name': 'Autentikasi', 'description': 'Manajemen registrasi, login, dan logout pengguna.'},
        {'name': 'Katalog Dawet Ayu', 'description': 'Melihat daftar kategori dan produk Dawet Ayu.'},
        {'name': 'Manajemen Pesanan', 'description': 'Pembuatan pesanan (checkout) dan riwayat transaksi.'},
        {'name': 'Pembayaran Digital', 'description': 'Integrasi payment gateway (Paymenku) dan webhook callback.'},
        {'name': 'Profil Pengguna', 'description': 'Pengelolaan informasi akun pengguna.'},
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayRequestDuration': True,
        'persistAuthorization': True,
        'filter': True,
    },
}

UNFOLD = {
    "SITE_TITLE": "AyuPay Admin",
    "SITE_HEADER": "AyuPay - Dawet Ayu",
    "SITE_SYMBOL": "storefront",
    "COLORS": {
        "primary": {
            "50": "#edf5ef",
            "100": "#d3e7d8",
            "200": "#acd2b7",
            "300": "#7ab68d",
            "400": "#5a9e68",
            "500": "#4F8A5B",
            "600": "#3d7c4a",
            "700": "#2f6339",
            "800": "#264f2e",
            "900": "#203f26",
            "950": "#0e1d11",
        },
    },
    "DASHBOARD_CALLBACK": "core.admin_dashboard.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Toko Dawet Ayu"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dasbor Utama"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Katalog"),
                "separator": True,
                "items": [
                    {
                        "title": _("Kategori"),
                        "icon": "category",
                        "link": reverse_lazy("admin:core_category_changelist"),
                    },
                    {
                        "title": _("Produk"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:core_product_changelist"),
                    },
                ],
            },
            {
                "title": _("Transaksi & Keuangan"),
                "separator": True,
                "items": [
                    {
                        "title": _("Pesanan (Orders)"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": _("Pembayaran"),
                        "icon": "payments",
                        "link": reverse_lazy("admin:payments_payment_changelist"),
                    },
                ],
            },
            {
                "title": _("Manajemen Sistem"),
                "separator": True,
                "items": [
                    {
                        "title": _("Pengguna & Admin"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_customuser_changelist"),
                    },
                ],
            },
        ],
    },
}

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}] - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}