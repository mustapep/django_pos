"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.accounts import views as va



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', va.Login.as_view()),
    path('logout/', va.LogoutView.as_view()),
    path('login/process', va.LoginProcess.as_view()),
    path('admin_landingpage', va.AdminLandingPageView.as_view()),
    path('register/', va.RegisterView.as_view()),
    path('register/save', va.RegisterSaveView.as_view()),

    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('items/', include('apps.items.urls', namespace='items')),
    path('transactions/', include('apps.transactions.urls', namespace='transaction')),
    path('testing/', include('testing.urls', namespace='testing'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
