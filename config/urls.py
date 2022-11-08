"""eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3ODgxNTczLCJqdGkiOiI3ZGFlNmNhODRlZGU0MjBhYjcwZGRiYzgxZGY5N2U3NiIsInVzZXJfaWQiOjF9.8Swsu19DfLF_G8eENHZKORs2tWMgYGZ13BLk33msV1g
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from movies.views import UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('movies.urls')),
    path('auth/', include("dj_rest_auth.urls")),
    path('user/register/', UserView.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    path("auth/token/refresh", TokenRefreshView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
