import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Offre
from .serializers import OffreSerializer, OffreListSerializer
from django.conf import settings

# ── Liste paginée des offres ──
class OffreListView(generics.ListAPIView):
    queryset = Offre.objects.all()
    serializer_class = OffreListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ville', 'type_contrat', 'secteur']
    search_fields = ['intitule', 'entreprise', 'competences']
    ordering_fields = ['date_publication']

# ── Détail d'une offre ──
class OffreDetailView(generics.RetrieveAPIView):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer

# ── KPIs globaux (adapté pour le frontend) ──
@api_view(['GET'])
def stats_globales(request):  # Renommé pour correspondre à l'appel frontend
    total = Offre.objects.count()
    
    # Secteur dominant
    secteur_dominant = Offre.objects.values('secteur').annotate(
        count=Count('id')
    ).exclude(secteur__isnull=True).exclude(secteur='').order_by('-count').first()
    
    # Ville top
    ville_top = Offre.objects.values('ville').annotate(
        count=Count('id')
    ).exclude(ville__isnull=True).exclude(ville='').order_by('-count').first()
    
    # Compétences les plus demandées (à partir du CSV)
    df = pd.read_csv(settings.CSV_FILE, encoding='utf-8-sig')
    COMPETENCES = {
        'Excel': ['excel'], 'Python': ['python'], 'SQL': ['sql'],
        'Communication': ['communication'], 'Management': ['management'],
        'Comptabilité': ['comptabilité'], 'Finance': ['finance'],
        'Marketing': ['marketing'], 'Vente': ['vente'],
        'Anglais': ['anglais'], 'Logistique': ['logistique'],
        'Informatique': ['informatique'], 'SAP': ['sap'],
        'Gestion de projet': ['gestion de projet'],
        'Service client': ['service client'],
    }
    
    top_competences = []
    for label, kws in COMPETENCES.items():
        count = df['Compétences demandées'].dropna().str.lower().apply(
            lambda x: any(kw in x for kw in kws)
        ).sum()
        if count > 0:
            top_competences.append({'nom': label, 'count': int(count)})
    
    top_competences = sorted(top_competences, key=lambda x: x['count'], reverse=True)[:10]
    
    # Croissance mensuelle (simplifiée pour l'instant)
    croissance_mensuelle = 0
    
    # Contrat dominant
    contrat_dominant = Offre.objects.values('type_contrat').annotate(
        count=Count('id')
    ).exclude(type_contrat__isnull=True).exclude(type_contrat='').order_by('-count').first()
    
    return Response({
        'total_offres': total,
        'secteur_dominant': secteur_dominant,
        'ville_top': ville_top,
        'croissance_mensuelle': croissance_mensuelle,
        'contrat_dominant': contrat_dominant,
        'top_competences': top_competences,
    })

# ── Top entreprises (nouvel endpoint) ──
@api_view(['GET'])
def top_entreprises(request):
    entreprises = Offre.objects.values('entreprise').annotate(
        count=Count('id')
    ).exclude(entreprise__isnull=True).exclude(entreprise='').order_by('-count')[:10]
    
    return Response(list(entreprises))

# ── Top compétences ──
@api_view(['GET'])
def competences(request):
    df = pd.read_csv(settings.CSV_FILE, encoding='utf-8-sig')
    COMPETENCES = {
        'Excel': ['excel'], 'Python': ['python'], 'SQL': ['sql'],
        'Communication': ['communication'], 'Management': ['management'],
        'Comptabilité': ['comptabilité'], 'Finance': ['finance'],
        'Marketing': ['marketing'], 'Vente': ['vente'],
        'Anglais': ['anglais'], 'Logistique': ['logistique'],
        'Informatique': ['informatique'], 'SAP': ['sap'],
        'Gestion de projet': ['gestion de projet'],
        'Service client': ['service client'],
    }
    result = []
    for label, kws in COMPETENCES.items():
        count = df['Compétences demandées'].dropna().str.lower().apply(
            lambda x: any(kw in x for kw in kws)
        ).sum()
        result.append({'competence': label, 'count': int(count)})
    result = sorted(result, key=lambda x: x['count'], reverse=True)[:10]
    return Response(result)

# ── Offres par secteur ──
@api_view(['GET'])
def secteurs(request):
    data = (Offre.objects.exclude(secteur='Autre')
            .values('secteur')
            .annotate(count=Count('id'))
            .order_by('-count'))
    return Response(list(data))

# ── Offres par ville ──
@api_view(['GET'])
def villes(request):
    data = (Offre.objects.values('ville')
            .annotate(count=Count('id'))
            .order_by('-count')[:10])
    return Response(list(data))

# ── Évolution mensuelle ──
@api_view(['GET'])
def evolution(request):
    data = (Offre.objects.filter(date_publication__isnull=False)
            .annotate(mois=TruncMonth('date_publication'))
            .values('mois')
            .annotate(count=Count('id'))
            .order_by('mois'))
    result = [{'mois': str(d['mois'])[:7], 'offres': d['count']} for d in data]  # 'offres' au lieu de 'count'
    return Response(result)

# ── Répartition par contrat ──
@api_view(['GET'])
def contrats(request):
    data = (Offre.objects.exclude(type_contrat='Non précisé')
            .values('type_contrat')
            .annotate(count=Count('id'))
            .order_by('-count'))
    return Response(list(data))