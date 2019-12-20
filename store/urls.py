"""app8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resultats', views.resultats, name='resultats'),
    path('resultats/<int:page>/', views.resultats, name='resultats'),
    path('aliment', views.aliment, name='aliment'),
    path('aliment/<int:fav>/<int:prod>/', views.save_aliment, name='save_aliment'),
    path('detail_favori/<int:pk>', views.detail_favori, name='detail_favori'),
    path('aliment_delete/<int:pk>', views.aliment_delete, name='aliment_delete'),
]
