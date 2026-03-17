# offres_app/views.py
import pandas as pd
import json
from datetime import datetime, timedelta
from collections import Counter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.conf import settings
from .models import Offre
from .serializers import OffreSerializer, OffreListSerializer

# ============================================
# CONFIGURATION DE PAGINATION
# ============================================
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# ============================================
# ENDPOINTS POUR LES OFFRES
# ============================================

class OffreListView(generics.ListAPIView):
    """
    GET /api/offres/
    Liste paginée des offres avec filtres
    """
    queryset = Offre.objects.all()
    serializer_class = OffreListSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'ville': ['exact', 'icontains'],
        'type_contrat': ['exact'],
        'secteur': ['exact', 'icontains'],
        'date_publication': ['gte', 'lte', 'year', 'month'],
    }
    search_fields = ['intitule', 'entreprise', 'competences', 'description']
    ordering_fields = ['date_publication', 'entreprise', 'ville']
    ordering = ['-date_publication']


class OffreDetailView(generics.RetrieveAPIView):
    """
    GET /api/offres/{id}/
    Détail complet d'une offre
    """
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer


# ============================================
# ENDPOINTS STATISTIQUES
# ============================================

@api_view(['GET'])
def stats_globales(request):
    """
    GET /api/stats/
    KPIs globaux du marché de l'emploi
    """
    total = Offre.objects.count()
    
    # Secteur dominant
    secteur_dominant = Offre.objects.values('secteur').annotate(
        count=Count('id')
    ).exclude(secteur__isnull=True).exclude(secteur='').order_by('-count').first()
    
    # Ville leader
    ville_top = Offre.objects.values('ville').annotate(
        count=Count('id')
    ).exclude(ville__isnull=True).exclude(ville='').order_by('-count').first()
    
    # Contrat dominant
    contrat_dominant = Offre.objects.values('type_contrat').annotate(
        count=Count('id')
    ).exclude(type_contrat__isnull=True).exclude(type_contrat='').order_by('-count').first()
    
    # Top compétences (depuis le champ competences)
    competences_counts = {}
    for offre in Offre.objects.exclude(competences__isnull=True).exclude(competences=''):
        if offre.competences:
            # Nettoyer et séparer les compétences
            skills = [s.strip() for s in offre.competences.replace('[', '').replace(']', '').replace("'", "").split(',')]
            for skill in skills:
                if skill and len(skill) > 2:  # Ignorer les chaînes trop courtes
                    competences_counts[skill] = competences_counts.get(skill, 0) + 1
    
    top_competences = sorted(competences_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Croissance mensuelle
    maintenant = datetime.now().date()
    mois_dernier = maintenant - timedelta(days=30)
    mois_precedent = mois_dernier - timedelta(days=30)
    
    offres_mois_dernier = Offre.objects.filter(date_publication__gte=mois_dernier).count()
    offres_mois_precedent = Offre.objects.filter(
        date_publication__gte=mois_precedent,
        date_publication__lt=mois_dernier
    ).count()
    
    croissance = 0
    if offres_mois_precedent > 0:
        croissance = ((offres_mois_dernier - offres_mois_precedent) / offres_mois_precedent) * 100
    
    return Response({
        'total_offres': total,
        'secteur_dominant': secteur_dominant,
        'ville_top': ville_top,
        'croissance_mensuelle': round(croissance, 2),
        'contrat_dominant': contrat_dominant,
        'top_competences': [{'nom': k, 'count': v} for k, v in top_competences],
    })


@api_view(['GET'])
def top_competences(request):
    """
    GET /api/competences/
    Top 10 des compétences les plus demandées
    """
    limit = int(request.GET.get('limit', 10))
    
    # Méthode 1: Depuis le champ competences
    competences_counts = {}
    for offre in Offre.objects.exclude(competences__isnull=True).exclude(competences=''):
        if offre.competences:
            skills = [s.strip() for s in offre.competences.replace('[', '').replace(']', '').replace("'", "").split(',')]
            for skill in skills:
                if skill and len(skill) > 2:
                    competences_counts[skill] = competences_counts.get(skill, 0) + 1
    
    top = sorted(competences_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    # Méthode 2: Depuis le CSV pour les compétences structurées
    df = pd.read_csv(settings.CSV_FILE, encoding='utf-8-sig')
    competences_structurees = {
        'Informatique': df['Comp_informatique'].sum() if 'Comp_informatique' in df.columns else 0,
        'Réseau': df['Comp_réseau'].sum() if 'Comp_réseau' in df.columns else 0,
        'Sécurité': df['Comp_sécurité'].sum() if 'Comp_sécurité' in df.columns else 0,
        'Communication': df['Comp_communication'].sum() if 'Comp_communication' in df.columns else 0,
        'Gestion': df['Comp_gestion'].sum() if 'Comp_gestion' in df.columns else 0,
        'Comptabilité': df['Comp_comptabilité'].sum() if 'Comp_comptabilité' in df.columns else 0,
        'Marketing': df['Comp_marketing'].sum() if 'Comp_marketing' in df.columns else 0,
        'Logistique': df['Comp_logistique'].sum() if 'Comp_logistique' in df.columns else 0,
        'Anglais': df['Comp_anglais'].sum() if 'Comp_anglais' in df.columns else 0,
        'Français': df['Comp_francais'].sum() if 'Comp_francais' in df.columns else 0,
    }
    
    structurees_top = sorted(competences_structurees.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    return Response({
        'competences_libres': [{'nom': k, 'count': v} for k, v in top],
        'competences_structurees': [{'nom': k, 'count': int(v)} for k, v in structurees_top],
    })


@api_view(['GET'])
def top_entreprises(request):
    """
    GET /api/entreprises/top/
    Top entreprises qui recrutent le plus
    """
    limit = int(request.GET.get('limit', 10))
    
    entreprises = Offre.objects.values('entreprise').annotate(
        count=Count('id')
    ).exclude(
        entreprise__isnull=True
    ).exclude(
        entreprise=''
    ).order_by('-count')[:limit]
    
    return Response(list(entreprises))


@api_view(['GET'])
def offres_par_secteur(request):
    """
    GET /api/secteurs/
    Répartition des offres par secteur d'activité
    """
    secteurs = Offre.objects.values('secteur').annotate(
        count=Count('id')
    ).exclude(
        secteur__isnull=True
    ).exclude(
        secteur=''
    ).exclude(
        secteur='Autre'
    ).order_by('-count')
    
    return Response(list(secteurs))


@api_view(['GET'])
def offres_par_ville(request):
    """
    GET /api/villes/
    Répartition des offres par ville
    """
    limit = int(request.GET.get('limit', 20))
    
    villes = Offre.objects.values('ville').annotate(
        count=Count('id')
    ).exclude(
        ville__isnull=True
    ).exclude(
        ville=''
    ).order_by('-count')[:limit]
    
    return Response(list(villes))


@api_view(['GET'])
def evolution_mensuelle(request):
    """
    GET /api/evolution/
    Évolution mensuelle du nombre d'offres
    """
    months = int(request.GET.get('months', 12))
    
    # Date limite
    date_limite = datetime.now().date() - timedelta(days=30 * months)
    
    evolution = Offre.objects.filter(
        date_publication__isnull=False,
        date_publication__gte=date_limite
    ).annotate(
        mois=TruncMonth('date_publication')
    ).values('mois').annotate(
        count=Count('id')
    ).order_by('mois')
    
    result = []
    for item in evolution:
        if item['mois']:
            result.append({
                'mois': item['mois'].strftime('%Y-%m'),
                'offres': item['count']
            })
    
    return Response(result)


@api_view(['GET'])
def repartition_contrats(request):
    """
    GET /api/contrats/
    Répartition des offres par type de contrat
    """
    contrats = Offre.objects.values('type_contrat').annotate(
        count=Count('id')
    ).exclude(
        type_contrat__isnull=True
    ).exclude(
        type_contrat=''
    ).exclude(
        type_contrat='Non précisé'
    ).order_by('-count')
    
    return Response(list(contrats))


# ============================================
# ENDPOINTS POUR L'ASSISTANT IA
# ============================================

@api_view(['POST'])
def chat_assistant(request):
    """
    POST /api/chat/
    Assistant IA pour répondre aux questions sur les offres
    """
    try:
        # Vérifier si la requête a un corps
        if not request.body:
            return Response(
                {'error': 'Corps de la requête vide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les données JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response(
                {'error': 'Format JSON invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = data.get('message', '').strip()
        
        if not message:
            return Response(
                {'error': 'Message requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Analyser la question
        response = analyser_question(message)
        
        return Response({'response': response})
        
    except Exception as e:
        print(f"Erreur dans chat_assistant: {str(e)}")  # Pour le debug
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def analyser_question(message):
    """Analyse la question et génère une réponse basée sur les données réelles"""
    
    message = message.lower()
    
    # Statistiques de base
    total_offres = Offre.objects.count()
    
    # ============================================
    # QUESTIONS SUR LES SECTEURS
    # ============================================
    if any(word in message for word in ['secteur', 'domaine', 'filière', 'branche']):
        # Top secteurs
        secteurs = Offre.objects.values('secteur').annotate(
            count=Count('id')
        ).exclude(
            secteur__isnull=True
        ).exclude(
            secteur=''
        ).exclude(
            secteur='Autre'
        ).order_by('-count')[:5]
        
        if 'plus' in message or 'top' in message or 'leader' in message or 'principal' in message:
            if secteurs:
                top = secteurs[0]
                return f"Le secteur qui recrute le plus actuellement est **{top['secteur']}** avec {top['count']} offres d'emploi."
        
        if 'moins' in message:
            if len(secteurs) > 0:
                bottom = secteurs[-1]
                return f"Parmi les secteurs actifs, **{bottom['secteur']}** a le moins d'offres avec {bottom['count']} offres."
        
        # Réponse générale sur les secteurs
        response = "📊 **Secteurs qui recrutent le plus :**\n\n"
        for i, s in enumerate(secteurs, 1):
            pourcentage = (s['count'] / total_offres * 100) if total_offres > 0 else 0
            response += f"{i}. **{s['secteur']}** : {s['count']} offres ({pourcentage:.1f}%)\n"
        
        response += f"\n💰 Total des offres analysées : {total_offres}"
        return response
    
    # ============================================
    # QUESTIONS SUR LES COMPÉTENCES
    # ============================================
    elif any(word in message for word in ['compétence', 'skill', 'savoir', 'connaître', 'maîtrise']):
        
        # Compétences pour une ville spécifique
        villes = ['dakar', 'thies', 'thiès', 'saint-louis', 'ziguinchor', 'kaolack']
        ville_specifique = None
        for v in villes:
            if v in message:
                ville_specifique = v
                break
        
        if ville_specifique:
            # Compétences dans une ville spécifique
            offres_ville = Offre.objects.filter(ville__icontains=ville_specifique)
            
            if offres_ville.count() == 0:
                return f"Je n'ai pas trouvé d'offres pour {ville_specifique.title()}."
            
            # Extraire les compétences
            competences = Counter()
            for offre in offres_ville:
                if offre.competences:
                    # Nettoyer la chaîne de compétences
                    skills = offre.competences.replace('[', '').replace(']', '').replace("'", "").split(',')
                    for skill in skills:
                        skill = skill.strip()
                        if skill and len(skill) > 2:
                            competences[skill] += 1
            
            if competences:
                top = competences.most_common(5)
                response = f"🎯 **Top 5 des compétences demandées à {ville_specifique.title()} :**\n\n"
                for comp, count in top:
                    pourcentage = (count / offres_ville.count() * 100)
                    response += f"• **{comp}** : {count} offres ({pourcentage:.1f}% des offres)\n"
                return response
        
        # Compétences globales
        competences = Counter()
        for offre in Offre.objects.exclude(competences__isnull=True).exclude(competences=''):
            if offre.competences:
                skills = offre.competences.replace('[', '').replace(']', '').replace("'", "").split(',')
                for skill in skills:
                    skill = skill.strip()
                    if skill and len(skill) > 2:
                        competences[skill] += 1
        
        if competences:
            top = competences.most_common(10)
            response = "🔧 **Top 10 des compétences les plus demandées :**\n\n"
            for comp, count in top[:5]:  # Top 5 pour la réponse
                pourcentage = (count / total_offres * 100)
                response += f"• **{comp}** : {count} offres ({pourcentage:.1f}%)\n"
            
            response += "\n💡 Les compétences techniques les plus recherchées sont en informatique, gestion de projet et communication."
            return response
        
        return "Je n'ai pas encore assez de données sur les compétences."
    
    # ============================================
    # QUESTIONS SUR LES VILLES
    # ============================================
    elif any(word in message for word in ['ville', 'dakar', 'thies', 'thiès', 'région', 'localisation', 'où']):
        
        # Top villes
        villes = Offre.objects.values('ville').annotate(
            count=Count('id')
        ).exclude(
            ville__isnull=True
        ).exclude(
            ville=''
        ).order_by('-count')[:5]
        
        if 'plus' in message or 'top' in message or 'leader' in message:
            if villes:
                top = villes[0]
                pourcentage = (top['count'] / total_offres * 100)
                return f"🏙️ **{top['ville']}** est la ville qui offre le plus d'opportunités avec {top['count']} offres ({pourcentage:.1f}% du total)."
        
        response = "📍 **Répartition géographique des offres :**\n\n"
        for v in villes:
            pourcentage = (v['count'] / total_offres * 100)
            response += f"• **{v['ville']}** : {v['count']} offres ({pourcentage:.1f}%)\n"
        
        return response
    
    # ============================================
    # QUESTIONS SUR LES CONTRATS
    # ============================================
    elif any(word in message for word in ['cdi', 'cdd', 'stage', 'contrat', 'freelance']):
        
        # Compter par type de contrat
        contrats = Offre.objects.values('type_contrat').annotate(
            count=Count('id')
        ).exclude(
            type_contrat__isnull=True
        ).exclude(
            type_contrat=''
        ).exclude(
            type_contrat='Non précisé'
        ).order_by('-count')
        
        if 'cdi' in message:
            cdi = next((c for c in contrats if 'cdi' in c['type_contrat'].lower()), None)
            if cdi:
                return f"📄 Il y a actuellement **{cdi['count']} offres en CDI** au Sénégal."
        
        elif 'cdd' in message:
            cdd = next((c for c in contrats if 'cdd' in c['type_contrat'].lower()), None)
            if cdd:
                return f"📅 Il y a actuellement **{cdd['count']} offres en CDD** au Sénégal."
        
        elif 'stage' in message:
            stage = next((c for c in contrats if 'stage' in c['type_contrat'].lower()), None)
            if stage:
                return f"🎓 Il y a actuellement **{stage['count']} offres de stage** au Sénégal."
        
        # Réponse générale
        response = "📋 **Répartition par type de contrat :**\n\n"
        for c in contrats:
            pourcentage = (c['count'] / total_offres * 100)
            response += f"• **{c['type_contrat']}** : {c['count']} offres ({pourcentage:.1f}%)\n"
        
        return response
    
    # ============================================
    # QUESTIONS SUR LES ENTREPRISES
    # ============================================
    elif any(word in message for word in ['entreprise', 'société', 'boîte', 'employeur', 'recruteur']):
        
        entreprises = Offre.objects.values('entreprise').annotate(
            count=Count('id')
        ).exclude(
            entreprise__isnull=True
        ).exclude(
            entreprise=''
        ).order_by('-count')[:5]
        
        if entreprises:
            response = "🏢 **Top entreprises qui recrutent :**\n\n"
            for e in entreprises:
                response += f"• **{e['entreprise']}** : {e['count']} offres\n"
            
            return response
    
    # ============================================
    # QUESTIONS SUR LES QUANTITÉS
    # ============================================
    elif any(word in message for word in ['combien', 'total', 'nombre', 'statistique']):
        
        # Compter les offres récentes (30 derniers jours)
        date_limite = datetime.now().date() - timedelta(days=30)
        offres_recentes = Offre.objects.filter(date_publication__gte=date_limite).count()
        
        return (
            f"📊 **Statistiques globales :**\n\n"
            f"• Total d'offres : **{total_offres}**\n"
            f"• Offres des 30 derniers jours : **{offres_recentes}**\n"
            f"• Secteur principal : **{get_top_secteur()}**\n"
            f"• Ville principale : **{get_top_ville()}**\n"
            f"• Contrat principal : **{get_top_contrat()}**"
        )
    
    # ============================================
    # QUESTIONS SUR LES TENDANCES
    # ============================================
    elif any(word in message for word in ['tendance', 'évolution', 'progression', 'augmentation']):
        
        # Calculer l'évolution
        maintenant = datetime.now().date()
        mois_dernier = maintenant - timedelta(days=30)
        mois_precedent = mois_dernier - timedelta(days=30)
        
        offres_mois_dernier = Offre.objects.filter(date_publication__gte=mois_dernier).count()
        offres_mois_precedent = Offre.objects.filter(
            date_publication__gte=mois_precedent,
            date_publication__lt=mois_dernier
        ).count()
        
        if offres_mois_precedent > 0:
            variation = ((offres_mois_dernier - offres_mois_precedent) / offres_mois_precedent) * 100
            if variation > 0:
                return f"📈 Le marché est en hausse : **+{variation:.1f}%** d'offres par rapport au mois dernier."
            elif variation < 0:
                return f"📉 Le marché est en baisse : **{variation:.1f}%** d'offres par rapport au mois dernier."
            else:
                return "📊 Le marché est stable, le nombre d'offres est similaire au mois dernier."
    
    # ============================================
    # MESSAGE D'ACCUEIL / AIDE
    # ============================================
    elif any(word in message for word in ['bonjour', 'salut', 'hello', 'aide', 'help']):
        return (
            "👋 **Bonjour ! Je suis votre assistant Emploi Sénégal.**\n\n"
            "Je peux vous aider à analyser le marché de l'emploi. Posez-moi des questions comme :\n\n"
            "• 🔍 \"Quel secteur recrute le plus ?\"\n"
            "• 🎯 \"Top compétences à Dakar\"\n"
            "• 📍 \"Villes avec le plus d'offres\"\n"
            "• 📄 \"Combien d'offres CDI ?\"\n"
            "• 🏢 \"Entreprises qui recrutent\"\n"
            "• 📊 \"Statistiques globales\"\n"
            "• 📈 \"Tendance du marché\"\n\n"
            "Que souhaitez-vous savoir ?"
        )
    
    # ============================================
    # RÉPONSE PAR DÉFAUT
    # ============================================
    else:
        return (
            "🤖 Je n'ai pas bien compris votre question. Voici ce que je peux faire :\n\n"
            "• **Secteurs** : 'Quel secteur recrute le plus ?'\n"
            "• **Compétences** : 'Compétences demandées à Dakar'\n"
            "• **Villes** : 'Top villes pour l'emploi'\n"
            "• **Contrats** : 'Nombre d'offres CDI'\n"
            "• **Entreprises** : 'Entreprises qui recrutent'\n"
            "• **Statistiques** : 'Statistiques globales'\n\n"
            "Essayez de reformuler votre question !"
        )


def get_top_secteur():
    """Fonction utilitaire pour obtenir le top secteur"""
    top = Offre.objects.values('secteur').annotate(
        count=Count('id')
    ).exclude(secteur__isnull=True).exclude(secteur='').order_by('-count').first()
    return top['secteur'] if top else "Non déterminé"


def get_top_ville():
    """Fonction utilitaire pour obtenir la top ville"""
    top = Offre.objects.values('ville').annotate(
        count=Count('id')
    ).exclude(ville__isnull=True).exclude(ville='').order_by('-count').first()
    return top['ville'] if top else "Non déterminé"


def get_top_contrat():
    """Fonction utilitaire pour obtenir le top contrat"""
    top = Offre.objects.values('type_contrat').annotate(
        count=Count('id')
    ).exclude(type_contrat__isnull=True).exclude(type_contrat='').order_by('-count').first()
    return top['type_contrat'] if top else "Non déterminé"


# ============================================
# ENDPOINT POUR LE SCRAPING (OPTIONNEL)
# ============================================

@api_view(['POST'])
def lancer_scraping(request):
    """
    POST /api/scrape/
    Lancer le scraping des offres (nécessite une clé API)
    """
    # Vérification d'authentification simple
    api_key = request.headers.get('X-API-Key')
    
    if api_key != settings.SCRAPING_API_KEY:
        return Response(
            {'error': 'Non autorisé'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        # Importer et lancer le scraper
        from scrapers.scraper_manager import run_all_scrapers
        
        result = run_all_scrapers()
        
        return Response({
            'status': 'success',
            'message': 'Scraping terminé',
            'result': result
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================
# ENDPOINTS DE FILTRES (pour les menus déroulants)
# ============================================

@api_view(['GET'])
def filtres_disponibles(request):
    """
    GET /api/filtres/
    Retourne toutes les valeurs disponibles pour les filtres
    """
    villes = Offre.objects.values_list('ville', flat=True).distinct().exclude(ville='').exclude(ville__isnull=True)
    secteurs = Offre.objects.values_list('secteur', flat=True).distinct().exclude(secteur='').exclude(secteur__isnull=True)
    contrats = Offre.objects.values_list('type_contrat', flat=True).distinct().exclude(type_contrat='').exclude(type_contrat__isnull=True)
    
    return Response({
        'villes': sorted(list(set([v for v in villes if v]))),
        'secteurs': sorted(list(set([s for s in secteurs if s]))),
        'contrats': sorted(list(set([c for c in contrats if c]))),
    })