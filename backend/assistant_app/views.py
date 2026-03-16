import anthropic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from offres_app.models import Offre
from django.db.models import Count

@api_view(['POST'])
def chat(request):
    question = request.data.get('message', '')
    if not question:
        return Response({'error': 'Message requis'}, status=400)

    # Contexte des données
    total = Offre.objects.count()
    ville_leader = Offre.objects.values('ville').annotate(c=Count('id')).order_by('-c').first()
    secteur_top = (Offre.objects.exclude(secteur='Autre')
                   .values('secteur').annotate(c=Count('id')).order_by('-c').first())

    contexte = f"""
    Tu es un assistant expert du marché de l'emploi au Sénégal.
    Voici les données actuelles :
    - Total offres : {total}
    - Ville avec le plus d'offres : {ville_leader['ville'] if ville_leader else 'N/A'}
    - Secteur dominant : {secteur_top['secteur'] if secteur_top else 'N/A'}
    Réponds en français de manière concise et utile.
    """

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=contexte,
        messages=[{"role": "user", "content": question}]
    )
    return Response({'response': message.content[0].text})