from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import os

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def lancer_scraping():
    """
    Fonction principale qui lance le scraping
    """
    logger.info(f"Debut du scraping automatique : {datetime.now()}")
    
    try:
        # On appellera le scraper ici quand il sera pret
        logger.info("Scraping en cours...")
        
        # Creer le dossier data/raw s'il n'existe pas
        os.makedirs("data/raw", exist_ok=True)
        
        logger.info(f"Scraping termine avec succes : {datetime.now()}")
        
    except Exception as e:
        logger.error(f"Erreur pendant le scraping : {e}")


def demarrer_scheduler():
    """
    Demarre le planificateur automatique
    """
    scheduler = BlockingScheduler()
    
    # Planification 1 : Tous les jours a 8h00
    scheduler.add_job(
        lancer_scraping,
        CronTrigger(hour=8, minute=0),
        id='scraping_matin',
        name='Scraping automatique matin'
    )
    
    # Planification 2 : Tous les jours a 18h00
    scheduler.add_job(
        lancer_scraping,
        CronTrigger(hour=18, minute=0),
        id='scraping_soir',
        name='Scraping automatique soir'
    )
    
    logger.info("Planificateur demarre !")
    logger.info("Scraping programme a 8h00 et 18h00 tous les jours")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Planificateur arrete.")
        scheduler.shutdown()


if __name__ == "__main__":
    demarrer_scheduler()