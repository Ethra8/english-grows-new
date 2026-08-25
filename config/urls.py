
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from profiles import views as profile_views

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    
    path('admin/', admin.site.urls),
    path("accounts/redirect/", profile_views.login_redirect, name="login_redirect"),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),
    path('courses/', include('courses.urls')),
    path('', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)