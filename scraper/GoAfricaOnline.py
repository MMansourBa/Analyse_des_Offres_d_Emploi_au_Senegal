import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# ── Configuration ──
os.makedirs("data/raw", exist_ok=True)

MAX_RETRIES = 3
WAIT_RETRY  = 3
PAUSE_PAGE  = 1
PAUSE_OFFRE = 0.5

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BASE_URL = "https://www.goafricaonline.com/sn/emploi"

# ──────────────────────────────────────────────────────
# FONCTION — Récupérer les liens d'une page avec relance
# ──────────────────────────────────────────────────────
def get_links_page(page):
    url = f"{BASE_URL}?page={page}"

    for tentative in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            liens = soup.find_all("a", href=lambda h: h and "/sn/emploi/job-" in h)

            if not liens:
                return []

            page_links = []
            for a in liens:
                href = a["href"]
                if href not in page_links:
                    page_links.append(href)

            return page_links

        except Exception as e:
            print(f"  Tentative {tentative}/{MAX_RETRIES} échouée : {e}")
            if tentative < MAX_RETRIES:
                time.sleep(WAIT_RETRY)
            else:
                print(f"  Page {page} abandonnée après {MAX_RETRIES} tentatives")
                return []

# ──────────────────────────────────────────────────────
# FONCTION — Extraire les détails d'une offre avec relance
# ──────────────────────────────────────────────────────
def extraire_offre(url):
    for tentative in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            # ── Intitulé du poste ──
            try:
                title = soup.find(
                    "div", class_=lambda c: c and "font-black" in c and "text-gray-800" in c
                ).text.strip()
            except:
                title = "Non précisé"

            # ── Entreprise ──
            try:
                entreprise = soup.find(
                    "a", class_=lambda c: c and "font-bold" in c and "text-16/[20px]" in c
                ).text.strip()
            except:
                entreprise = "Non précisé"

            # ── Ville ──
            try:
                ville = "Non précisé"
                for div in soup.find_all(
                    "div", class_=lambda c: c and "font-bold" in c and "text-16/[120%]" in c
                ):
                    if "Adresse du poste" in div.text:
                        parent = div.parent
                        texte = parent.text.strip()
                        ville = texte.replace("Adresse du poste :", "").strip()
                        break
            except:
                ville = "Non précisé"

            # ── Type de contrat ──
            try:
                contrat = "Non précisé"
                titre_div = soup.find(
                    "div", class_=lambda c: c and "font-black" in c and "text-gray-800" in c
                )
                if titre_div:
                    badges_div = titre_div.find_parent("div").find_next_sibling("div")
                    if badges_div:
                        badges = badges_div.find_all(
                            "div", class_=lambda c: c and "bg-gray-100" in c
                        )
                        contrats = [b.text.strip() for b in badges if b.text.strip()]
                        if contrats:
                            contrat = contrats[0]
            except:
                contrat = "Non précisé"

            # ── Date de publication ──
            try:
                date_div = soup.find(
                    "div", class_=lambda c: c and "text-12" in c and "text-gray-650" in c and "font-medium" in c
                )
                date = date_div.text.strip().replace("Posté le", "").strip() if date_div else "Non précisé"
            except:
                date = "Non précisé"

            # ── Compétences demandées ──
            try:
                competences = "Non précisé"
                for div in soup.find_all(
                    "div", class_=lambda c: c and "font-bold" in c and "text-16/[120%]" in c
                ):
                    if "Description du poste" in div.text:
                        parent = div.parent
                        items = parent.find_all("li")
                        if items:
                            competences = " | ".join(
                                [li.text.strip() for li in items if li.text.strip()]
                            )[:300]
                        else:
                            texte = parent.text.replace("Description du poste :", "").strip()
                            competences = texte[:300]
                        break
            except:
                competences = "Non précisé"

            return {
                "Intitulé du poste":     title,
                "Entreprise":            entreprise,
                "Ville":                 ville,
                "Type de contrat":       contrat,
                "Date de publication":   date,
                "Compétences demandées": competences,
            }

        except Exception as e:
            print(f"  Tentative {tentative}/{MAX_RETRIES} échouée : {e}")
            if tentative < MAX_RETRIES:
                time.sleep(WAIT_RETRY)
            else:
                print(f"  Offre abandonnée : {url}")
                return None

# ──────────────────────────────────────────────────────
# ÉTAPE 1 — Récupérer tous les liens
# ──────────────────────────────────────────────────────
links = []

for page in range(1, 132):
    print(f"Page {page}/131...")
    page_links = get_links_page(page)

    if not page_links:
        print(f"  Aucun lien — fin de pagination")
        break

    for link in page_links:
        if link not in links:
            links.append(link)

    print(f"  {len(links)} liens récupérés jusqu'ici")
    time.sleep(PAUSE_PAGE)

print(f"\nTotal liens uniques : {len(links)}")

# ──────────────────────────────────────────────────────
# ÉTAPE 2 — Scraper les détails de chaque offre
# ──────────────────────────────────────────────────────
data  = []
total = len(links)

for i, url in enumerate(links):
    print(f"Offre {i+1}/{total}")

    offre = extraire_offre(url)
    if offre:
        data.append(offre)

    # Sauvegarde progressive toutes les 100 offres
    if (i + 1) % 100 == 0:
        df_temp = pd.DataFrame(data)
        df_temp.to_csv(
            "data/raw/offres_goafricaonline_raw.csv",
            index=False,
            encoding="utf-8-sig"
        )
        print(f"  Sauvegarde progressive : {len(df_temp)} offres")

    time.sleep(PAUSE_OFFRE)

# ──────────────────────────────────────────────────────
# ÉTAPE 3 — Sauvegarder les données finales
# ──────────────────────────────────────────────────────
df = pd.DataFrame(data)

file_path = "data/raw/offres_goafricaonline_raw.csv"
if os.path.exists(file_path):
    os.remove(file_path)

df.to_csv(file_path, index=False, encoding="utf-8-sig")
df.to_json(
    "data/raw/offres_goafricaonline_raw.json",
    orient="records",
    force_ascii=False
)

print(f"\n{len(df)} offres sauvegardées dans data/raw/")