import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from offres_app.models import Offre
from datetime import datetime

class Command(BaseCommand):
    help = 'Importer les offres depuis le CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv(settings.CSV_FILE, encoding='utf-8-sig')
        Offre.objects.all().delete()
        count = 0
        for _, row in df.iterrows():
            try:
                date = pd.to_datetime(row.get('Date de publication'), errors='coerce')
                Offre.objects.create(
                    intitule=row.get('Intitulé du poste', ''),
                    entreprise=row.get('Entreprise', ''),
                    ville=row.get('Ville', ''),
                    type_contrat=row.get('Type de contrat', ''),
                    date_publication=date.date() if pd.notna(date) else None,
                    competences=row.get('Compétences demandées', ''),
                    secteur=row.get('Secteur', 'Autre'),
                )
                count += 1
            except Exception as e:
                continue
        self.stdout.write(f'✅ {count} offres importées !')