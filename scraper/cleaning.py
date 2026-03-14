import pandas as pd
import re
import os

# ── Configuration ──
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE  = os.path.join(BASE_DIR, "data", "raw",     "offres_emploi_senegal_raw.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "cleaned", "offres_emploi_senegal_cleaned.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "data", "cleaned", "offres_emploi_senegal_cleaned.json")

os.makedirs(os.path.join(BASE_DIR, "data", "cleaned"), exist_ok=True)

# ──────────────────────────────────────────────────────
# ÉTAPE 1 — Charger les données
# ──────────────────────────────────────────────────────
df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")
print(f"-- Données chargées : {len(df)} offres")

# ──────────────────────────────────────────────────────
# ÉTAPE 2 — Standardiser les types de contrat
# ──────────────────────────────────────────────────────
def standardiser_contrat(contrat):
    if pd.isna(contrat) or str(contrat).strip() == "Non précisé":
        return "Non précisé"

    c = str(contrat).lower().strip()

    # Ignorer les valeurs de salaire
    if "f cfa" in c or "k/" in c or " m/" in c:
        return "Non précisé"

    # Stage
    if any(k in c for k in ["stage", "stagiaire", "internship", "intern"]):
        return "Stage"

    # Alternance → Stage
    if any(k in c for k in ["alternance", "apprentissage"]):
        return "Stage"

    # Freelance
    if any(k in c for k in ["freelance", "free-lance", "indépendant"]):
        return "Freelance"

    # Intérim → CDD
    if "intérim" in c:
        return "CDD"

    # CDD (avant CDI pour éviter faux positifs)
    if "cdd" in c:
        return "CDD"

    # CDI
    if "cdi" in c:
        return "CDI"

    # Temps complet / temps plein
    if any(k in c for k in ["temps complet", "temps plein", "full time"]):
        return "Temps complet"

    # Temps partiel
    if any(k in c for k in ["temps partiel", "part time"]):
        return "Temps partiel"

    # Télétravail → Non précisé (pas un type de contrat)
    if any(k in c for k in ["sans télétravail", "télétravail"]):
        return "Non précisé"

    return "Non précisé"

df["Type de contrat"] = df["Type de contrat"].apply(standardiser_contrat)
print(f"\n-- Contrats standardisés :")
print(df["Type de contrat"].value_counts())

# ──────────────────────────────────────────────────────
# ÉTAPE 3 — Normalisation des noms de villes
# ──────────────────────────────────────────────────────
VILLES_MAPPING = {
    "Dakar": [
        "dakar", "mermoz", "almadies", "sacré", "sacre", "point e",
        "fann", "liberté", "ouakam", "yoff", "ngor", "pikine",
        "guédiawaye", "parcelles", "thiaroye", "rufisque", "bargny",
        "diamniadio", "sébikotane", "plateau", "hann", "sicap",
        "vdn", "grand dakar", "médina", "gueule tapee", "bel-air",
        "corniche", "rocade", "triangle sud", "voie de degagement"
    ],
    "Thiès": [
        "thiès", "thies", "mbour", "saly", "somone", "joal", "sandiara"
    ],
    "Saint-Louis": [
        "saint-louis", "saint louis", "st-louis", "st louis"
    ],
    "Ziguinchor": [
        "ziguinchor", "ziginchor", "cap skirring", "oussouye"
    ],
    "Kaolack":      ["kaolack"],
    "Touba":        ["touba", "mbacké"],
    "Tambacounda":  ["tambacounda", "tamba"],
    "Kolda":        ["kolda"],
    "Matam":        ["matam"],
    "Louga":        ["louga"],
    "Fatick":       ["fatick"],
    "Diourbel":     ["diourbel"],
    "Sédhiou":      ["sédhiou", "sedhiou"],
    "Kaffrine":     ["kaffrine"],
    "Kédougou":     ["kédougou", "kedougou"],
    "Télétravail":  ["télétravail", "teletravail", "remote", "à distance", "en ligne"],
}

def normaliser_ville(ville):
    if pd.isna(ville) or str(ville).strip() == "Non précisé":
        return "Non précisé"

    v = str(ville).lower().strip()

    for ville_standard, keywords in VILLES_MAPPING.items():
        for kw in keywords:
            if kw in v:
                return ville_standard

    if "sénégal" in v or "senegal" in v:
        return "Sénégal (autre)"

    return "Non précisé"

df["Ville"] = df["Ville"].apply(normaliser_ville)
print(f"\n-- Villes normalisées :")
print(df["Ville"].value_counts())

# ──────────────────────────────────────────────────────
# ÉTAPE 4 — Suppression des doublons
# ──────────────────────────────────────────────────────
avant = len(df)
df = df.drop_duplicates(subset=["Intitulé du poste", "Entreprise"])
apres = len(df)
print(f"\n-- Doublons supprimés : {avant - apres} | Avant : {avant} → Après : {apres}")

# ──────────────────────────────────────────────────────
# ÉTAPE 5 — Gestion des valeurs manquantes
# ──────────────────────────────────────────────────────
df = df.fillna("Non précisé")
df = df.replace("", "Non précisé")

avant = len(df)
df = df[df["Intitulé du poste"] != "Non précisé"]
print(f"-- Lignes sans titre supprimées : {avant - len(df)}")

print(f"\nVALEURS MANQUANTES :")
for col in df.columns:
    n = (df[col] == "Non précisé").sum()
    pct = round(n / len(df) * 100, 1)
    print(f"  {col:25} → {n:4} Non précisé ({pct}%)")

# ──────────────────────────────────────────────────────
# ÉTAPE 6 — Sauvegarder
# ──────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
df.to_json(OUTPUT_JSON, orient="records", force_ascii=False)

print(f"\n-- {len(df)} offres nettoyées sauvegardées dans data/cleaned/")