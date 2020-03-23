"""app8 URL Configuration

"""
from django.urls import path
from store import views
from store.views import filter

urlpatterns = [
    path('', views.home, name='home'),
    path('resultats', views.resultats, name='resultats'),
    path('filter', views.filter, name='filter'),
    path('rating', views.rating, name='rating'),
    path('resultats/<int:page>/', views.resultats, name='resultats'),
    path('filter/<int:page>/', views.filter, name='filter'),
    path('aliment', views.aliment, name='aliment'),
    path('aliment/<int:fav>/<int:prod>/', views.save_aliment, name='save_aliment'),
    path('detail_favori/<int:pk>', views.detail_favori, name='detail_favori'),
    path('aliment_delete/<int:pk>', views.aliment_delete, name='aliment_delete'),
    path('mentions_legales', views.mention, name='mention'),
]
