from django.urls import path
from . import views

urlpatterns = [
    path('offres/', views.OffreListView.as_view(), name='offres-list'),
    path('offres/<int:pk>/', views.OffreDetailView.as_view(), name='offres-detail'),
    path('stats/', views.stats, name='stats'),
    path('competences/', views.competences, name='competences'),
    path('secteurs/', views.secteurs, name='secteurs'),
    path('villes/', views.villes, name='villes'),
    path('evolution/', views.evolution, name='evolution'),
    path('contrats/', views.contrats, name='contrats'),
]