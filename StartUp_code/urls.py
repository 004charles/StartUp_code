from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('StartUp_Code_Impact/', include('core.urls')),
]
