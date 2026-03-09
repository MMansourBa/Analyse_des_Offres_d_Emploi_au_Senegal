import pandas as pd
import re

# Dictionnaire de standardisation des contrats
CONTRATS_MAPPING = {
    # CDI
    "cdi": "CDI",
    "contrat a duree indeterminee": "CDI",
    "contrat à durée indéterminée": "CDI",
    "indetermine": "CDI",
    "indéterminé": "CDI",
    "permanent": "CDI",
    "temps plein": "CDI",
    "full time": "CDI",

    # CDD
    "cdd": "CDD",
    "contrat a duree determinee": "CDD",
    "contrat à durée déterminée": "CDD",
    "determinee": "CDD",
    "déterminée": "CDD",
    "temporaire": "CDD",
    "temp": "CDD",
    "temporary": "CDD",
    "fixed term": "CDD",

    # Stage
    "stage": "Stage",
    "stagiaire": "Stage",
    "internship": "Stage",
    "intern": "Stage",
    "alternance": "Stage",
    "apprentissage": "Stage",

    # Freelance
    "freelance": "Freelance",
    "free-lance": "Freelance",
    "independant": "Freelance",
    "indépendant": "Freelance",
    "consultant": "Freelance",
    "prestataire": "Freelance",
    "mission": "Freelance",
}

# Dictionnaire de normalisation des villes
VILLES_MAPPING = {
    # Dakar
    "dak": "Dakar",
    "dakar": "Dakar",
    "dakaar": "Dakar",
    "plateau": "Dakar",
    "almadies": "Dakar",
    "mermoz": "Dakar",
    "ouakam": "Dakar",
    "liberté": "Dakar",
    "fann": "Dakar",

    # Thiès
    "thies": "Thiès",
    "thiès": "Thiès",
    "thies ville": "Thiès",

    # Saint-Louis
    "saint louis": "Saint-Louis",
    "saint-louis": "Saint-Louis",
    "st louis": "Saint-Louis",
    "st-louis": "Saint-Louis",

    # Ziguinchor
    "ziguinchor": "Ziguinchor",
    "ziginchor": "Ziguinchor",
    "zig": "Ziguinchor",

    # Kaolack
    "kaolack": "Kaolack",
    "kao": "Kaolack",

    # Touba
    "touba": "Touba",

    # Mbour
    "mbour": "Mbour",
    "m'bour": "Mbour",

    # Rufisque
    "rufisque": "Rufisque",
    "rufi": "Rufisque",

    # Diourbel
    "diourbel": "Diourbel",

    # Louga
    "louga": "Louga",

    # Tambacounda
    "tambacounda": "Tambacounda",
    "tamba": "Tambacounda",

    # Kolda
    "kolda": "Kolda",

    # Matam
    "matam": "Matam",

    # Fatick
    "fatick": "Fatick",

    # Sédhiou
    "sedhiou": "Sédhiou",
    "sédhiou": "Sédhiou",

    # Kédougou
    "kedougou": "Kédougou",
    "kédougou": "Kédougou",

    # Kaffrine
    "kaffrine": "Kaffrine",
}


#Donction pour la Standardisation des contrats
def standardiser_contrat(contrat):
    """
    Convertit une variante de contrat en valeur standard :
    CDI, CDD, Stage ou Freelance
    """
    if pd.isna(contrat) or contrat == "":
        return "Non précisé"

    contrat_clean = contrat.lower().strip()
    contrat_clean = re.sub(r'\s+', ' ', contrat_clean)

    for variante, standard in CONTRATS_MAPPING.items():
        if variante in contrat_clean:
            return standard

    return "Autre"


def standardiser_colonne_contrats(df, colonne="type_contrat"):
    """
    Applique la standardisation sur toute une colonne
    """
    if colonne not in df.columns:
        print(f"Colonne '{colonne}' introuvable")
        return df

    df[colonne] = df[colonne].apply(standardiser_contrat)
    return df


# Fonction pour la normalisation des villes
def normaliser_ville(ville):
    """
    Convertit une variante de ville en nom standard
    ex: 'Dak' → 'Dakar', 'Thies' → 'Thiès'
    """
    if pd.isna(ville) or ville == "":
        return "Non précisé"

    ville_clean = ville.lower().strip()
    ville_clean = re.sub(r'\s+', ' ', ville_clean)

    for variante, standard in VILLES_MAPPING.items():
        if variante == ville_clean:
            return standard

    # Retourner la ville avec première lettre en majuscule
    return ville.strip().title()


def normaliser_colonne_villes(df, colonne="ville"):
    """
    Applique la normalisation sur toute une colonne
    """
    if colonne not in df.columns:
        print(f"Colonne '{colonne}' introuvable")
        return df

    df[colonne] = df[colonne].apply(normaliser_ville)
    return df


# Fonction principale pour nettoyage generale des donnees
def nettoyer_donnees(df):
    """
    Applique tout le nettoyage sur le DataFrame
    """
    print("Nettoyage en cours...")

    # 1. Standardisation des contrats
    df = standardiser_colonne_contrats(df)
    print("- Contrats standardisés")

    # 2. Normalisation des villes
    df = normaliser_colonne_villes(df)
    print("- Villes normalisées")

    print("Nettoyage termine !")
    return df


# TEST
if __name__ == "__main__":

    # Données de test
    test_data = {
        "poste": [
            "Développeur Web",
            "Data Analyst",
            "Comptable",
            "Designer",
            "Chef de projet",
            "Commercial",
            "Ingénieur",
            "Assistant RH"
        ],
        "type_contrat": [
            "CDI",
            "contrat à durée indéterminée",
            "CDD",
            "Stage",
            "internship",
            "Freelance",
            "temporaire",
            None
        ],
        "ville": [
            "Dak",
            "Dakar",
            "Thies",
            "Saint Louis",
            "Tamba",
            "Zig",
            "Kao",
            "Rufi"
        ]
    }

    df = pd.DataFrame(test_data)

    print("=== AVANT nettoyage ===")
    print(df)

    df = nettoyer_donnees(df)

    print("\n=== APRES nettoyage ===")
    print(df)