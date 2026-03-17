# offres_app/management/commands/import_csv.py
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from offres_app.models import Offre

class Command(BaseCommand):
    help = 'Importe les offres depuis le CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin vers le fichier CSV')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.stdout.write(f"Importation depuis {csv_file}...")
        
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0
            
            # Afficher les noms des colonnes pour vérification
            self.stdout.write(f"Colonnes trouvées: {reader.fieldnames}")
            
            for row in reader:
                try:
                    # Récupérer le secteur depuis le CSV
                    secteur_csv = row.get('secteur', '').strip()
                    
                    # Si le secteur est vide ou 'Non précisé', essayer de le déduire
                    if not secteur_csv or secteur_csv == 'Non précisé':
                        secteur = self.deduire_secteur(row)
                    else:
                        secteur = secteur_csv
                    
                    # Créer l'offre
                    offre, created = Offre.objects.update_or_create(
                        intitule=row.get('Intitulé du poste', '')[:500],
                        entreprise=row.get('Entreprise', '')[:300],
                        defaults={
                            'ville': row.get('Ville', '')[:100],
                            'type_contrat': self.normaliser_contrat(row.get('Type de contrat', '')),
                            'date_publication': None,  # À gérer séparément
                            'competences': row.get('Compétences demandées', '')[:1000],
                            'secteur': secteur[:100] if secteur else 'Autre',
                        }
                    )
                    
                    if created:
                        count += 1
                        if count % 100 == 0:
                            self.stdout.write(f"  {count} offres importées...")
                            
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur ligne {count}: {e}"))
            
            self.stdout.write(self.style.SUCCESS(f"✅ {count} offres importées avec succès!"))
    
    def normaliser_contrat(self, contrat):
        if not contrat:
            return 'Non précisé'
        
        contrat = str(contrat).upper()
        if 'CDI' in contrat:
            return 'CDI'
        elif 'CDD' in contrat:
            return 'CDD'
        elif 'STAGE' in contrat or 'INTERN' in contrat:
            return 'Stage'
        elif 'FREELANCE' in contrat:
            return 'Freelance'
        else:
            return 'Autre'
    
    def deduire_secteur(self, row):
        """Déduire le secteur à partir de l'intitulé et des compétences"""
        intitule = str(row.get('Intitulé du poste', '')).lower()
        competences = str(row.get('Compétences demandées', '')).lower()
        texte = intitule + ' ' + competences
        
        # Dictionnaire de mots-clés par secteur
        secteurs_mots = {
            'Informatique': ['developpeur', 'dev', 'programmeur', 'informaticien', 'it', 'data', 'python', 'java', 'sql', 'réseau', 'informatique'],
            'Commercial': ['commercial', 'vente', 'business', 'marketing', 'client', 'chargé', 'account', 'sales'],
            'Logistique': ['logistique', 'transport', 'approvisionnement', 'chaine', 'livraison', 'stock'],
            'RH': ['rh', 'ressources', 'recrutement', 'formation', 'social', 'paie'],
            'Finance': ['finance', 'comptable', 'comptabilité', 'banque', 'audit', 'contrôle de gestion'],
            'Administration': ['administratif', 'assistant', 'secrétaire', 'gestion', 'accueil'],
            'Santé': ['santé', 'medical', 'infirmier', 'docteur', 'hopital', 'clinique'],
            'Education': ['éducation', 'enseignement', 'professeur', 'formateur', 'école'],
        }
        
        for secteur, mots in secteurs_mots.items():
            for mot in mots:
                if mot in texte:
                    return secteur
        
        return 'Autre'