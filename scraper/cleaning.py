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
# ÉTAPE 2 — Sauvegarder les titres originaux
# ──────────────────────────────────────────────────────
df["Intitulé du poste original"] = df["Intitulé du poste"].copy()

# ──────────────────────────────────────────────────────
# ÉTAPE 3 — Normalisation des intitulés de poste
# ──────────────────────────────────────────────────────

# Dictionnaire de mapping
METIERS_MAPPING = {
    # Développement
    "Développeur Full Stack": ["full stack", "fullstack", "full-stack", "developpeur full"],
    "Développeur Frontend": ["front-end", "frontend", "front end"],
    "Développeur Backend": ["back-end", "backend", "back end"],
    "Développeur Web": ["developpeur web", "développeur web", "web developer"],
    "Développeur Mobile": ["mobile", "android", "ios", "swift", "kotlin", "flutter"],
    "Développeur Java": ["java", "spring boot"],
    "Développeur Python": ["python", "django", "flask"],
    "Développeur PHP": ["php", "laravel", "symfony"],
    "Développeur JavaScript": ["javascript", "js", "node.js", "nodejs", "angular", "react", "vue"],
    "Ingénieur Logiciel": ["software engineer", "software developer", "ingenieur logiciel", "ingénieur logiciel"],
    "Data Scientist": ["data scientist", "machine learning", "ia", "intelligence artificielle"],
    "Data Analyst": ["data analyst", "analyste de données", "analyste data"],
    "Data Engineer": ["data engineer", "ingénieur data", "ingenieur data"],
    
    # IT / Infrastructure
    "Administrateur Système": ["administrateur système", "systeme", "sysadmin", "system administrator"],
    "Administrateur Réseau": ["administrateur réseau", "reseau", "network"],
    "Ingénieur Réseau": ["ingenieur réseau", "ingénieur réseau", "network engineer"],
    "Technicien Support": ["support informatique", "helpdesk", "help desk", "support it", "it support"],
    "Technicien Informatique": ["technicien informatique", "it technician"],
    "Ingénieur Sécurité": ["sécurité informatique", "cybersécurité", "cybersecurity", "security"],
    "DevOps": ["devops"],
    "Cloud": ["cloud", "aws", "azure", "gcp"],
    "Base de Données": ["dba", "base de données", "database"],
    "ERP": ["erp", "sap", "odoo"],
    
    # Gestion de projet
    "Chef de Projet IT": ["chef de projet informatique", "project manager it"],
    "Chef de Projet Digital": ["chef de projet digital", "digital project manager"],
    "Chef de Projet": ["chef de projet", "project manager", "gestionnaire de projet"],
    "Product Manager": ["product manager", "chef produit"],
    "Product Owner": ["product owner"],
    "Scrum Master": ["scrum master"],
    "PMO": ["pmo", "project management officer"],
    
    # Commercial / Marketing
    "Commercial Terrain": ["commercial terrain", "commerciale terrain"],
    "Commercial Sédentaire": ["commercial sédentaire", "commerciale sédentaire"],
    "Commercial B2B": ["commercial b2b", "business to business"],
    "Business Developer": ["business developer", "développeur d'affaires", "developpeur d'affaires"],
    "Account Manager": ["account manager", "chargé de comptes", "charge de comptes"],
    "Key Account Manager": ["key account", "kam", "grands comptes"],
    "Chargé d'Affaires": ["chargé d'affaires", "charge d'affaires"],
    "Conseiller Commercial": ["conseiller commercial", "conseillère commercial"],
    "Téléconseiller": ["téléconseiller", "teleconseiller", "télévendeur", "televendeur"],
    "Vendeur": ["vendeur", "vendeuse"],
    "Chef des Ventes": ["chef des ventes", "sales manager"],
    "Directeur Commercial": ["directeur commercial", "directrice commercial"],
    
    # Marketing / Communication
    "Community Manager": ["community manager", "community"],
    "Social Media Manager": ["social media", "réseaux sociaux", "reseaux sociaux"],
    "Content Manager": ["content", "créateur de contenu", "createur de contenu"],
    "Marketing Digital": ["marketing digital", "digital marketing"],
    "Marketing Manager": ["responsable marketing", "marketing manager"],
    "Chargé Marketing": ["chargé marketing", "charge marketing"],
    "Brand Manager": ["brand manager", "chef de marque"],
    "Graphiste": ["graphiste", "graphic designer", "infographiste"],
    "Motion Designer": ["motion design"],
    "Webdesigner": ["webdesigner", "web designer"],
    "UX/UI Designer": ["ux", "ui", "ux/ui"],
    
    # Finance / Comptabilité
    "Comptable": ["comptable"],
    "Comptable Junior": ["comptable junior", "assistant comptable"],
    "Comptable Senior": ["comptable senior", "comptable sénior"],
    "Chef Comptable": ["chef comptable"],
    "Contrôleur de Gestion": ["contrôleur de gestion", "controleur de gestion"],
    "Auditeur": ["auditeur", "auditeur interne", "audit"],
    "Analyste Financier": ["analyste financier", "financial analyst"],
    "Responsable Financier": ["responsable financier", "directeur financier", "daf"],
    "Trésorier": ["trésorier", "tresorier"],
    "Gestionnaire de Paie": ["gestionnaire de paie", "chargé paie", "charge paie"],
    "Fiscaliste": ["fiscaliste"],
    
    # RH / Administration
    "Responsable RH": ["responsable rh", "directeur rh", "drh", "hr manager"],
    "Chargé RH": ["chargé rh", "charge rh", "hr officer"],
    "Assistant RH": ["assistant rh", "assistante rh", "hr assistant"],
    "Recruteur": ["recruteur", "recruteuse", "talent acquisition"],
    "Formateur": ["formateur", "formatrice"],
    "Assistant Administratif": ["assistant administratif", "assistante administrative"],
    "Assistant de Direction": ["assistant de direction", "assistante de direction"],
    "Secrétaire": ["secrétaire", "secretaire"],
    "Office Manager": ["office manager"],
    "Standardiste": ["standardiste", "réceptionniste", "receptionniste"],
    
    # Logistique / Transport
    "Logisticien": ["logisticien", "logisticienne", "logistique"],
    "Responsable Logistique": ["responsable logistique", "directeur logistique"],
    "Supply Chain Manager": ["supply chain"],
    "Gestionnaire de Stock": ["gestionnaire de stock", "magasinier"],
    "Acheteur": ["acheteur", "acheteuse"],
    "Transitaire": ["transitaire", "déclarant en douane", "declarant en douane"],
    "Chauffeur": ["chauffeur", "conducteur", "livreur"],
    "Chauffeur Poids Lourd": ["chauffeur poids lourd", "chauffeur pl", "conducteur pl"],
    "Livreur": ["livreur", "coursier"],
    "Cariste": ["cariste"],
    
    # BTP / Génie Civil
    "Ingénieur Génie Civil": ["génie civil", "genie civil"],
    "Architecte": ["architecte"],
    "Conducteur de Travaux": ["conducteur de travaux"],
    "Chef de Chantier": ["chef de chantier"],
    "Technicien BTP": ["technicien btp", "technicienne btp"],
    "Topographe": ["topographe", "géomètre", "geometre"],
    "Électricien Bâtiment": ["électricien bâtiment", "electricien bâtiment"],
    "Plombier": ["plombier"],
    "Maçon": ["maçon", "macon"],
    "Peintre": ["peintre bâtiment", "peintre en bâtiment"],
    "Ferrailleur": ["ferrailleur", "ferrailleuse"],
    "Coffreur": ["coffreur", "coffreuse"],
    "Soudeur": ["soudeur", "soudeuse"],
    
    # Santé / Médical
    "Médecin": ["médecin", "medecin"],
    "Infirmier": ["infirmier", "infirmière"],
    "Sage-femme": ["sage-femme", "sage femme"],
    "Pharmacien": ["pharmacien", "pharmacienne"],
    "Biologiste": ["biologiste"],
    "Technicien de Laboratoire": ["technicien de laboratoire"],
    "Aide-Soignant": ["aide-soignant", "aide soignant"],
    
    # Enseignement / Formation
    "Enseignant": ["enseignant", "enseignante", "professeur"],
    "Maître": ["maître", "maitre"],
    "Professeur Maths": ["mathématiques", "maths"],
    "Professeur Anglais": ["anglais", "english teacher"],
    "Professeur Français": ["français"],
    "Professeur SVT": ["svt", "sciences de la vie"],
    "Professeur Physique-Chimie": ["physique", "chimie"],
    "Professeur Philosophie": ["philosophie"],
    "Professeur Économie": ["économie", "economie"],
    "Formateur": ["formateur", "formatrice"],
    
    # Direction
    "Directeur Général": ["directeur général", "directrice générale", "dg"],
    "Directeur Général Adjoint": ["directeur général adjoint", "dga"],
    "Directeur": ["directeur", "directrice"],
    "Directeur des Opérations": ["directeur des opérations", "directrice des opérations", "do"],
    "Directeur Technique": ["directeur technique", "directrice technique", "cto"],
    "Directeur Administratif et Financier": ["directeur administratif et financier", "daf"],
    "Directeur Commercial": ["directeur commercial", "directrice commercial"],
    "Directeur Marketing": ["directeur marketing", "directrice marketing"],
    "Directeur RH": ["directeur rh", "directrice rh", "drh"],
    "Directeur des Systèmes d'Information": ["directeur des systèmes d'information", "dsi"],
    "Responsable": ["responsable"],
    
    # Autres
    "Conseiller": ["conseiller", "conseillère"],
    "Analyste": ["analyste"],
    "Consultant": ["consultant", "consultante"],
    "Agent de Sécurité": ["agent de sécurité", "agent de securite", "gardien"],
    "Agent de Nettoyage": ["agent de nettoyage", "femme de ménage", "femme de menage"],
    "Cuisinier": ["cuisinier", "cuisinière"],
    "Serveur": ["serveur", "serveuse"],
    "Hôtesse": ["hôtesse", "hotesse", "hôte", "hote"],
    "Employé": ["employé", "employée"],
}

def normaliser_metier(titre):
    """Normalise un titre de poste"""
    if pd.isna(titre) or str(titre).strip() == "":
        return "Non précisé"
    
    t = str(titre).lower().strip()
    
    # Supprimer les informations parasites
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(r'\b(h/f|h\s*/f)\b', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\bref\s*[:\s]*[a-z0-9]+\b', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\s+', ' ', t).strip()
    
    # Chercher la meilleure correspondance
    for metier_standard, variantes in METIERS_MAPPING.items():
        for variante in variantes:
            if variante in t:
                if len(variante.split()) == 1 and len(variante) <= 4:
                    if re.search(r'\b' + re.escape(variante) + r'\b', t):
                        return metier_standard
                else:
                    return metier_standard
    
    return titre

df["Intitulé du poste"] = df["Intitulé du poste"].apply(normaliser_metier)

print("\n-- Métiers normalisés (avant affinage) :")
print(df["Intitulé du poste"].value_counts().head(20))

# ──────────────────────────────────────────────────────
# ÉTAPE 4 — Affiner les "Responsable" génériques (OPTION 2)
# ──────────────────────────────────────────────────────
def affiner_responsable(titre):
    """Transforme 'Responsable' en titre plus spécifique si possible"""
    if titre == "Responsable" or "responsable" in str(titre).lower():
        t = str(titre).lower()
        if "commercial" in t or "vente" in t:
            return "Responsable Commercial"
        elif "marketing" in t:
            return "Responsable Marketing"
        elif "financier" in t or "finance" in t:
            return "Responsable Financier"
        elif "rh" in t or "ressources" in t:
            return "Responsable RH"
        elif "technique" in t:
            return "Responsable Technique"
        elif "logistique" in t or "transport" in t:
            return "Responsable Logistique"
        elif "projet" in t or "project" in t:
            return "Chef de Projet"
        elif "administratif" in t:
            return "Responsable Administratif"
        elif "qualité" in t or "qualite" in t:
            return "Responsable Qualité"
        elif "hse" in t:
            return "Responsable HSE"
        elif "sécurité" in t or "securite" in t:
            return "Responsable Sécurité"
        elif "informatique" in t or "it" in t or "système" in t:
            return "Responsable Informatique"
    return titre

df["Intitulé du poste"] = df["Intitulé du poste"].apply(affiner_responsable)

print("\n-- Métiers normalisés (après affinage des Responsable) :")
print(df["Intitulé du poste"].value_counts().head(20))

# ──────────────────────────────────────────────────────
# ÉTAPE 5 — Standardiser les types de contrat
# ──────────────────────────────────────────────────────
def standardiser_contrat(contrat):
    if pd.isna(contrat) or str(contrat).strip() == "":
        return "Non précisé"
    
    c = str(contrat).lower().strip()
    
    if any(x in c for x in ["f cfa", "fcfa", "franc cfa", "k/", " m/", "million", "salaire"]):
        return "Non précisé"
    
    if any(k in c for k in ["stage", "stagiaire", "internship", "intern"]):
        return "Stage"
    
    if any(k in c for k in ["alternance", "apprentissage"]):
        return "Alternance"
    
    if any(k in c for k in ["freelance", "free-lance", "indépendant"]):
        return "Freelance"
    
    if any(k in c for k in ["intérim", "interim"]):
        return "Intérim"
    
    if "cdd" in c:
        return "CDD"
    
    if "cdi" in c:
        return "CDI"
    
    if any(k in c for k in ["temps complet", "temps plein", "full time", "plein temps"]):
        return "Temps plein"
    
    if any(k in c for k in ["temps partiel", "part time", "mi-temps"]):
        return "Temps partiel"
    
    return "Non précisé"

df["Type de contrat"] = df["Type de contrat"].apply(standardiser_contrat)

print(f"\n-- Contrats standardisés :")
print(df["Type de contrat"].value_counts())

# ──────────────────────────────────────────────────────
# ÉTAPE 6 — Normalisation des noms de villes
# ──────────────────────────────────────────────────────
VILLES_MAPPING = {
    "Dakar": [
        "dakar", "mermoz", "almadies", "sacré cœur", "sacre coeur", "point e",
        "fann", "liberté", "ouakam", "yoff", "ngor", "pikine", "keur massar",
        "guédiawaye", "parcelles", "thiaroye", "rufisque", "bargny", "sébikotane",
        "diamniadio", "plateau", "hann", "sicap", "vdn", "grand dakar", "médina",
        "medina", "gueule tapee", "bel-air", "corniche", "rocade", "colobane",
        "hlm", "dieuppeul", "fass", "grand yoff", "sipres", "foire"
    ],
    "Thiès": [
        "thiès", "thies", "mbour", "saly", "somone", "joal", "fadiouth", "popenguine",
        "sandiara", "tivaouane", "khombole", "pout"
    ],
    "Saint-Louis": [
        "saint-louis", "saint louis", "st-louis", "st louis", "richard toll", "dagana",
        "podor", "ross bethio"
    ],
    "Ziguinchor": [
        "ziguinchor", "ziginchor", "cap skirring", "oussouye", "bignona", "sédhiou",
        "sedhiou", "kolda", "vélingara", "velingara"
    ],
    "Kaolack": ["kaolack", "nga", "gandiaye", "sibassor"],
    "Touba": ["touba", "mbacké", "mbacke"],
    "Tambacounda": ["tambacounda", "tamba", "bakel", "goudiry"],
    "Louga": ["louga", "linguère", "kebemer", "kebemeer", "dahra"],
    "Fatick": ["fatick", "foundiougne", "passy", "sokone", "diofior"],
    "Diourbel": ["diourbel"],
    "Kaffrine": ["kaffrine"],
    "Kédougou": ["kédougou", "kedougou", "saraya", "salia"],
    "Matam": ["matam", "kanel", "ranérou", "ranerou"],
    "Télétravail": ["télétravail", "teletravail", "remote", "à distance", "en ligne", "home office", "travail à domicile"],
}

def normaliser_ville(ville):
    if pd.isna(ville) or str(ville).strip() == "":
        return "Non précisé"
    
    v = str(ville).lower().strip()
    
    if " / " in v:
        v = v.split(" / ")[0]
    
    for kw in VILLES_MAPPING["Dakar"]:
        if kw in v:
            return "Dakar"
    
    for ville_standard, keywords in VILLES_MAPPING.items():
        if ville_standard != "Dakar":
            for kw in keywords:
                if kw in v:
                    return ville_standard
    
    if "sénégal" in v or "senegal" in v:
        return "Sénégal (autre)"
    
    return "Non précisé"

df["Ville"] = df["Ville"].apply(normaliser_ville)

print(f"\n-- Villes normalisées :")
print(df["Ville"].value_counts().head(10))

# ──────────────────────────────────────────────────────
# ÉTAPE 7 — Créer des colonnes utiles avec CATÉGORIE AMÉLIORÉE (OPTION 1)
# ──────────────────────────────────────────────────────

def extraire_niveau(titre):
    """Extrait le niveau du poste"""
    if pd.isna(titre):
        return "Non précisé"
    
    t = str(titre).lower()
    
    if any(k in t for k in ["stagiaire", "intern", "stage", "apprenti", "alternance"]):
        return "Stage"
    elif any(k in t for k in ["junior", "débutant", "debutant"]):
        return "Junior"
    elif any(k in t for k in ["senior", "sénior", "expert", "lead", "principal"]):
        return "Senior"
    elif any(k in t for k in ["responsable", "manager", "chef", "superviseur", "directeur"]):
        return "Responsable"
    
    return "Non précisé"

df["Niveau"] = df["Intitulé du poste original"].apply(extraire_niveau)

def extraire_categorie_ameliore(titre):
    """Version améliorée avec plus de mots-clés (OPTION 1)"""
    if pd.isna(titre):
        return "Non précisé"
    
    t = str(titre).lower()
    
    categories_detail = {
        "Informatique / IT": [
            "dev", "développeur", "developer", "data", "informatique", "it", 
            "système", "réseau", "support", "logiciel", "technicien", "helpdesk",
            "cloud", "devops", "sécurité", "cyber", "dba", "base de données",
            "programmeur", "code", "java", "python", "javascript", "php"
        ],
        "Marketing / Communication": [
            "marketing", "communication", "community", "graphiste", "designer", 
            "social media", "brand", "contenu", "ux", "ui", "réseaux sociaux",
            "publicité", "pub", "campagne", "créatif", "création"
        ],
        "Commercial / Vente": [
            "commercial", "vente", "business", "account", "kam", "conseiller",
            "chargé d'affaires", "téléconseiller", "vendeur", "prospection",
            "clientèle", "négociation", "commerce"
        ],
        "Finance / Comptabilité": [
            "comptable", "finance", "audit", "contrôleur", "fiscal", "trésorier",
            "paie", "facturier", "gestionnaire", "bank", "banque", "comptabilité",
            "financier", "bilan", "compte", "budget"
        ],
        "RH / Administration": [
            "rh", "ressources humaines", "administratif", "secrétaire", "assistant",
            "office", "standardiste", "recrutement", "formation", "paie",
            "gestion du personnel", "hr", "people"
        ],
        "Logistique / Transport": [
            "logistique", "transport", "magasinier", "livreur", "chauffeur",
            "stock", "approvisionnement", "transitaire", "douane", "cariste",
            "fret", "expédition", "livraison", "flotte"
        ],
        "BTP / Construction": [
            "btp", "génie civil", "chantier", "architecte", "maçon", "coffreur",
            "ferrailleur", "peintre", "plombier", "électricien", "topographe",
            "construction", "bâtiment", "travaux", "ouvrier"
        ],
        "Santé / Médical": [
            "médecin", "infirmier", "sage-femme", "pharmacien", "biologiste",
            "laboratoire", "dentiste", "vétérinaire", "clinique", "santé",
            "médical", "soins", "hôpital"
        ],
        "Enseignement / Formation": [
            "enseignant", "professeur", "formateur", "éducation", "instituteur",
            "maître", "coach", "training", "cours", "pédagogie", "école",
            "lycée", "université", "formation"
        ],
        "Direction": [
            "directeur", "directrice", "daf", "cto", "dg", "responsable",
            "manager", "chef", "head", "lead", "superviseur", "coordinateur"
        ],
        "Hôtellerie / Restauration": [
            "cuisinier", "serveur", "barman", "hôtesse", "restaurant",
            "hôtel", "hôtellerie", "chef de rang", "réceptionniste", "résidence"
        ],
        "Sécurité": [
            "agent de sécurité", "gardien", "sécurité", "surveillance",
            "vigile", "protection"
        ],
    }
    
    for cat, mots in categories_detail.items():
        for mot in mots:
            if mot in t:
                return cat
    
    return "Non précisé"

df["Catégorie"] = df["Intitulé du poste"].apply(extraire_categorie_ameliore)

print(f"\n-- Distribution des catégories (améliorée) :")
print(df["Catégorie"].value_counts())

# ──────────────────────────────────────────────────────
# ÉTAPE 8 — Analyse des compétences (OPTION 3)
# ──────────────────────────────────────────────────────
def analyser_competences(comp):
    """Analyse les compétences demandées"""
    if pd.isna(comp) or comp == "Non précisé":
        return {}
    
    comp = str(comp).lower()
    
    competences_cles = {
        "anglais": ["anglais", "english", "bilingual", "langue"],
        "francais": ["français", "french"],
        "gestion": ["gestion", "management", "manager", "pilotage"],
        "communication": ["communication", "relation", "contact"],
        "bureautique": ["excel", "word", "powerpoint", "office", "pack office", "bureautique"],
        "comptabilité": ["comptabilité", "saisie", "facture", "bilan", "comptable"],
        "vente": ["vente", "prospection", "clientèle", "négociation"],
        "technique": ["technique", "maintenance", "réparation", "dépannage"],
        "leadership": ["leadership", "équipe", "animer", "encadrer"],
        "informatique": ["python", "java", "javascript", "html", "css", "sql", "php"],
        "réseau": ["réseau", "cisco", "routeur", "switch"],
        "sécurité": ["sécurité", "hse", "prévention", "risque"],
        "qualité": ["qualité", "iso", "norme", "conformité"],
        "marketing": ["marketing", "digital", "réseaux sociaux", "community"],
        "logistique": ["logistique", "transport", "stock", "approvisionnement"],
    }
    
    resultats = {}
    for key, mots in competences_cles.items():
        if any(mot in comp for mot in mots):
            resultats[key] = True
    
    return resultats

# Appliquer l'analyse des compétences et créer des colonnes
print("\n-- Analyse des compétences en cours...")
competences_data = df["Compétences demandées"].apply(analyser_competences)

# Convertir le dictionnaire en colonnes
for comp in ["anglais", "francais", "gestion", "communication", "bureautique", 
             "comptabilité", "vente", "technique", "leadership", "informatique",
             "réseau", "sécurité", "qualité", "marketing", "logistique"]:
    df[f"Comp_{comp}"] = competences_data.apply(lambda x: 1 if comp in x else 0)

print(f"-- {len([c for c in df.columns if c.startswith('Comp_')])} colonnes de compétences ajoutées")

# ──────────────────────────────────────────────────────
# ÉTAPE 9 — Suppression des doublons
# ──────────────────────────────────────────────────────
avant = len(df)
df = df.drop_duplicates(subset=["Intitulé du poste", "Entreprise"])
apres = len(df)
print(f"\n-- Doublons supprimés : {avant - apres} | Avant : {avant} → Après : {apres}")

# ──────────────────────────────────────────────────────
# ÉTAPE 10 — Gestion des valeurs manquantes
# ──────────────────────────────────────────────────────
df = df.fillna("Non précisé")
df = df.replace("", "Non précisé")

avant = len(df)
df = df[df["Intitulé du poste"] != "Non précisé"]
print(f"-- Lignes sans titre supprimées : {avant - len(df)}")

print(f"\nVALEURS MANQUANTES :")
for col in df.columns:
    if not col.startswith("Comp_"):  # Ignorer les colonnes de compétences
        n = (df[col] == "Non précisé").sum()
        pct = round(n / len(df) * 100, 1)
        print(f"  {col:30} → {n:4} Non précisé ({pct}%)")

# ──────────────────────────────────────────────────────
# ÉTAPE 11 — Sauvegarder
# ──────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

df.to_json(
    OUTPUT_JSON,
    orient="records",
    force_ascii=False
)

print(f"\n-- {len(df)} offres nettoyées sauvegardées dans data/cleaned/")