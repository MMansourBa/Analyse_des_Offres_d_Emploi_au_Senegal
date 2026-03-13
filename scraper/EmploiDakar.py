import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.makedirs("data/raw", exist_ok=True)

WAIT_TIMEOUT      = 20
MAX_RETRIES_OFFRE = 2

# ──────────────────────────────────────────────────────
# FONCTION — Créer un nouveau driver Chrome
# ──────────────────────────────────────────────────────
def creer_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

driver = creer_driver()
data   = []
links  = []

# ──────────────────────────────────────────────────────
# ÉTAPE 1 — Récupérer les liens
# ──────────────────────────────────────────────────────
for page in range(1, 21):
    url = f"https://www.emploidakar.com/offres-demploi-au-senegal/page/{page}/"
    print(f"Page {page}/20...")

    try:
        driver.get(url)
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.job_listing"))
        )
        jobs = driver.find_elements(By.CSS_SELECTOR, "li.job_listing")

        for job in jobs:
            try:
                link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                links.append(link)
            except:
                pass

        print(f"  {len(links)} liens récupérés jusqu'ici")

    except Exception as e:
        print(f"  Erreur page {page} : {e}")
        continue

print(f"\nTotal liens : {len(links)}")

# ──────────────────────────────────────────────────────
# FONCTION — Scraper une offre avec relance + restart Chrome
# ──────────────────────────────────────────────────────
def scraper_offre(link, driver):
    for tentative in range(1, MAX_RETRIES_OFFRE + 1):
        try:
            driver.get(link)
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            time.sleep(2)

            try:
                title = driver.find_element(By.CSS_SELECTOR, "h1").text
            except:
                title = "Non précisé"

            try:
                company = driver.find_element(By.CSS_SELECTOR, ".company strong").text
            except:
                company = "Non précisé"

            try:
                location = driver.find_element(By.CSS_SELECTOR, ".location").text
            except:
                location = "Non précisé"

            try:
                date = driver.find_element(By.CSS_SELECTOR, "time").text
            except:
                date = "Non précisé"

            try:
                job_type = driver.find_element(By.CSS_SELECTOR, "li.job-type").text
            except:
                job_type = "Non précisé"

            try:
                skills_elements = driver.find_elements(
                    By.CSS_SELECTOR, "div.job_description ul li"
                )
                skills = [s.text for s in skills_elements if s.text.strip()]
                competences = " | ".join(skills) if skills else "Non précisé"
            except:
                competences = "Non précisé"

            return driver, {
                "Intitulé du poste":     title,
                "Entreprise":            company,
                "Ville":                 location,
                "Type de contrat":       job_type,
                "Date de publication":   date,
                "Compétences demandées": competences,
            }

        except Exception as e:
            print(f"  Tentative {tentative}/{MAX_RETRIES_OFFRE} échouée : {e}")

            # Si Chrome est mort le relancer
            if "invalid session id" in str(e):
                print(" Chrome crash détecté → Relancement...")
                try:
                    driver.quit()
                except:
                    pass
                time.sleep(3)
                driver = creer_driver()

            if tentative < MAX_RETRIES_OFFRE:
                time.sleep(3)
            else:
                print(f"  Offre abandonnée : {link}")
                return driver, None

# ──────────────────────────────────────────────────────
# ÉTAPE 2 — Scraper les offres avec sauvegarde progressive
# ──────────────────────────────────────────────────────
for i, link in enumerate(links):
    print(f"🔍 Offre {i+1}/{len(links)}")
    driver, offre = scraper_offre(link, driver)

    if offre:
        data.append(offre)

    # Sauvegarde progressive toutes les 50 offres
    if (i + 1) % 50 == 0:
        df_temp = pd.DataFrame(data)
        df_temp.to_csv("data/raw/offres_emploi_raw.csv", index=False, encoding="utf-8-sig")
        print(f" Sauvegarde progressive : {len(df_temp)} offres")

    time.sleep(1)

try:
    driver.quit()
except:
    pass

# ──────────────────────────────────────────────────────
# ÉTAPE 3 — Sauvegarder
# ──────────────────────────────────────────────────────
df = pd.DataFrame(data)
print(f"\nTotal offres scrapées : {len(df)}")

file_path = "data/raw/offres_emploi_raw.csv"
if os.path.exists(file_path):
    os.remove(file_path)

df.to_csv(file_path, index=False, encoding="utf-8-sig")
df.to_json(
    "data/raw/offres_emploi_raw.json",
    orient="records",
    force_ascii=False
)

print("Fichiers sauvegardés dans data/raw/")