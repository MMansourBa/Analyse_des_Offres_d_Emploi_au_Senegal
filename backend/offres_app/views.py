import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
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

# ── KPIs globaux ──
@api_view(['GET'])
def stats(request):
    total = Offre.objects.count()
    ville_leader = Offre.objects.values('ville').order_by('-ville').first()
    secteur_dominant = (Offre.objects.exclude(secteur='Autre')
                        .values('secteur').order_by('-secteur').first())
    return Response({
        'total_offres': total,
        'ville_leader': ville_leader['ville'] if ville_leader else None,
        'secteur_dominant': secteur_dominant['secteur'] if secteur_dominant else None,
    })

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
    from django.db.models import Count
    data = (Offre.objects.exclude(secteur='Autre')
            .values('secteur')
            .annotate(count=Count('id'))
            .order_by('-count'))
    return Response(list(data))

# ── Offres par ville ──
@api_view(['GET'])
def villes(request):
    from django.db.models import Count
    data = (Offre.objects.values('ville')
            .annotate(count=Count('id'))
            .order_by('-count')[:10])
    return Response(list(data))

# ── Évolution mensuelle ──
@api_view(['GET'])
def evolution(request):
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    data = (Offre.objects.filter(date_publication__isnull=False)
            .annotate(mois=TruncMonth('date_publication'))
            .values('mois')
            .annotate(count=Count('id'))
            .order_by('mois'))
    result = [{'mois': str(d['mois'])[:7], 'count': d['count']} for d in data]
    return Response(result)

# ── Répartition par contrat ──
@api_view(['GET'])
def contrats(request):
    from django.db.models import Count
    data = (Offre.objects.exclude(type_contrat='Non précisé')
            .values('type_contrat')
            .annotate(count=Count('id'))
            .order_by('-count'))
    return Response(list(data))