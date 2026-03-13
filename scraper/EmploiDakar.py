from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

# Créer le dossier
os.makedirs("data/raw", exist_ok=True)

driver = webdriver.Chrome()

data = []
links = []

# -------------------------
# 1. récupérer les liens
# -------------------------

for page in range(1,20):

    url = f"https://www.emploidakar.com/offres-demploi-au-senegal/page/{page}/"
    print(f"Récupération page {page}")

    driver.get(url)

    WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,"li.job_listing"))
    )

    jobs = driver.find_elements(By.CSS_SELECTOR,"li.job_listing")

    for job in jobs:
        try:
            link = job.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
            links.append(link)
        except:
            pass

print("Total liens récupérés :",len(links))

# -------------------------
# 2. scraper chaque offre
# -------------------------

for link in links:

    try:

        driver.get(link)

        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"div.single_job_listing"))
        )

        try:
            title = driver.find_element(By.CSS_SELECTOR,"h1").text
        except:
            title = "Non précisé"

        try:
            company = driver.find_element(By.CSS_SELECTOR,".company strong").text
        except:
            company = "Non précisé"

        try:
            location = driver.find_element(By.CSS_SELECTOR,".location").text
        except:
            location = "Non précisé"

        try:
            date = driver.find_element(By.CSS_SELECTOR,"time").text
        except:
            date = "Non précisé"

        try:
            job_type = driver.find_element(By.CSS_SELECTOR,"li.job-type").text
        except:
            job_type = "Non précisé"

        # -------------------------
        # compétences
        # -------------------------

        try:
            skills_elements = driver.find_elements(By.CSS_SELECTOR,"div.job_description ul li")

            skills = [s.text for s in skills_elements]

            if len(skills) > 0:
                competences = " | ".join(skills)
            else:
                competences = "Non précisé"

        except:
            competences = "Non précisé"

        data.append({
            "Intitulé du poste": title,
            "Entreprise": company,
            "Ville": location,
            "Type de contrat": job_type,
            "Date de publication": date,
            "Compétences demandées": competences
        })

    except:
        print("Erreur sur :",link)

driver.quit()

# -------------------------
# DataFrame
# -------------------------

df = pd.DataFrame(data)

print(df.head())
print("\nTotal offres :",len(df))

# -------------------------
# sauvegarde
# -------------------------

file_path = "data/raw/offres_emploi_raw.csv"

if os.path.exists(file_path):
    os.remove(file_path)

df.to_csv(file_path,index=False,encoding="utf-8-sig")

df.to_json(
    "data/raw/offres_emploi_raw.json",
    orient="records",
    force_ascii=False
)

print("Fichiers sauvegardés dans data/raw/")