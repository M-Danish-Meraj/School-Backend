import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f-g(+qh+a5fn0b#gmd2)szqs)%4%++jln0!54t+vi8px061o2)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

# Sabko allow kar rahe hain taake Vercel pe koi rok tok na ho
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party libraries
    'rest_framework',
    'corsheaders',

    # Your Apps
    'accounts',  
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ==========================================
# 🔥 DATABASE SETUP (FIXED)
# Humne SQLite ko hata diya hai aur Hardcoded Neon Link laga diya hai.
# ==========================================

MY_DB_LINK = "postgresql://neondb_owner:npg_uJ2RyMzCLo4B@ep-lively-sun-ah9ffw9h-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

DATABASES = {
    'default': dj_database_url.parse(MY_DB_LINK)
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================
# 📂 STATIC FILES (Vercel Requirement)
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# ==========================================
# 🌐 CORS & SECURITY SETTINGS
# ==========================================
CORS_ALLOW_ALL_ORIGINS = False # Set to True agar frontend connect na ho
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://school-backend-woad-three.vercel.app", # Aapka Vercel Domain add kiya hai
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://school-backend-woad-three.vercel.app", # Aapka Vercel Domain add kiya hai
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

SESSION_COOKIE_SECURE = False  
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'