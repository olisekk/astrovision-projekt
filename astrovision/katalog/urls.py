from django.urls import path
from . import views

app_name = 'katalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('objekty/', views.objekty_seznam, name='objekty_seznam'),
    path('objekty/<int:pk>/', views.objekt_detail, name='objekt_detail'),
    path('pozorovateny/', views.pozorovateny_seznam, name='pozorovateny_seznam'),
    path('pozorovateny/<int:pk>/', views.pozorovatelna_detail, name='pozorovatelna_detail'),
]
