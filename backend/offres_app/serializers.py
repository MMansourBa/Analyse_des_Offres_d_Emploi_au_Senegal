from rest_framework import serializers
from .models import Offre

class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = '__all__'

class OffreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['id', 'intitule', 'entreprise', 'ville', 
                  'type_contrat', 'date_publication', 'secteur']