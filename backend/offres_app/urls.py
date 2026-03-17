# offres_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Offres
    path('offres/', views.OffreListView.as_view(), name='offres-list'),
    path('offres/<int:pk>/', views.OffreDetailView.as_view(), name='offres-detail'),
    
    # Statistiques générales
    path('stats/', views.stats_globales, name='stats'),
    path('competences/', views.top_competences, name='competences'),
    path('secteurs/', views.offres_par_secteur, name='secteurs'),
    path('villes/', views.offres_par_ville, name='villes'),
    path('evolution/', views.evolution_mensuelle, name='evolution'),
    path('contrats/', views.repartition_contrats, name='contrats'),
    path('entreprises/top/', views.top_entreprises, name='top-entreprises'),
    
    # Filtres
    path('filtres/', views.filtres_disponibles, name='filtres'),
    
    # Assistant IA
    path('chat/', views.chat_assistant, name='chat'),
    
    # Scraping (protégé)
    path('scrape/', views.lancer_scraping, name='scrape'),
]