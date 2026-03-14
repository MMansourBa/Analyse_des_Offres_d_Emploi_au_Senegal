import subprocess
import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# ── Configuration ──
PYTHON      = sys.executable
SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))

EMPLOIDAKAR_SCRIPT    = os.path.join(SCRAPER_DIR, "EmploiDakar.py")
GOAFRICAONLINE_SCRIPT = os.path.join(SCRAPER_DIR, "GoAfricaOnline.py")
FUSION_SCRIPT         = os.path.join(SCRAPER_DIR, "fusion.py")
CLEANING_SCRIPT       = os.path.join(SCRAPER_DIR, "cleaning.py")


# FONCTIONS — Lancer les scrapers

def lancer_emploidakar():
    print(" Lancement scraper EmploiDakar...")
    try:
        subprocess.run([PYTHON, EMPLOIDAKAR_SCRIPT], check=True)
        print("EmploiDakar terminé !")
    except Exception as e:
        print(f" Erreur EmploiDakar : {e}")

def lancer_goafricaonline():
    print(" Lancement scraper GoAfricaOnline...")
    try:
        subprocess.run([PYTHON, GOAFRICAONLINE_SCRIPT], check=True)
        print("GoAfricaOnline terminé !")
    except Exception as e:
        print(f" Erreur GoAfricaOnline : {e}")

def lancer_fusion():
    print("Fusion des fichiers CSV...")
    try:
        subprocess.run([PYTHON, FUSION_SCRIPT], check=True)
        print("Fusion terminée !")
    except Exception as e:
        print(f" Erreur fusion : {e}")

def lancer_cleaning():
    print("Nettoyage des données...")
    try:
        subprocess.run([PYTHON, CLEANING_SCRIPT], check=True)
        print("Nettoyage terminé !")
    except Exception as e:
        print(f" Erreur nettoyage : {e}")

def lancer_scraping_complet():
    print("\n" + "="*50)
    print("DÉMARRAGE DU SCRAPING AUTOMATIQUE")
    print("="*50)
    lancer_emploidakar()
    lancer_goafricaonline()
    lancer_fusion()
    lancer_cleaning()
    print("\nSCRAPING COMPLET TERMINÉ !")
    print("="*50 + "\n")


# PLANIFICATION — 8h00 et 18h00 tous les jours

scheduler = BlockingScheduler()

scheduler.add_job(
    lancer_scraping_complet,
    CronTrigger(hour=8, minute=0),
    id="scraping_matin",
    name="Scraping automatique 8h00"
)

scheduler.add_job(
    lancer_scraping_complet,
    CronTrigger(hour=18, minute=0),
    id="scraping_soir",
    name="Scraping automatique 18h00"
)

print("Scheduler démarré !")
print("Scraping planifié à 8h00 et 18h00 tous les jours")
print("   Appuyez sur Ctrl+C pour arrêter\n")

try:
    scheduler.start()
except KeyboardInterrupt:
    print("\nScheduler arrêté")