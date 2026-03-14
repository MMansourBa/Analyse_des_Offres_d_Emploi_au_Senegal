import pandas as pd
import re
import os
import nltk
from collections import Counter
import json

# Télécharger les ressources NLTK nécessaires (à faire une seule fois)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ──────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "cleaned", "offres_emploi_senegal_cleaned.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "cleaned", "offres_emploi_senegal_with_skills.csv")

# ──────────────────────────────────────────────────────
# DICTIONNAIRES DE COMPÉTENCES
# ──────────────────────────────────────────────────────

# Compétences techniques par domaine
TECH_SKILLS = {
    # Programmation / Développement
    "python": ["python", "py"],
    "java": ["java", "j2ee"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "php": ["php"],
    "c#": ["c#", "csharp", "c sharp"],
    "c++": ["c++", "cpp"],
    "ruby": ["ruby", "rails"],
    "go": ["golang", "go lang"],
    "rust": ["rust"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "dart": ["dart"],
    "flutter": ["flutter"],
    "react": ["react", "reactjs", "react.js"],
    "angular": ["angular", "angularjs", "angular.js"],
    "vue": ["vue", "vuejs", "vue.js"],
    "svelte": ["svelte"],
    "node.js": ["node", "nodejs", "node.js"],
    "django": ["django"],
    "flask": ["flask"],
    "laravel": ["laravel"],
    "symfony": ["symfony"],
    "spring": ["spring", "spring boot"],
    ".net": [".net", "dotnet"],
    
    # Bases de données
    "sql": ["sql", "mysql", "postgresql", "postgres", "oracle", "sql server"],
    "nosql": ["nosql", "mongodb", "cassandra", "redis", "elasticsearch"],
    "base de données": ["base de données", "database", "db"],
    
    # Data / IA
    "data science": ["data science", "datascience"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "ia": ["ia", "intelligence artificielle", "ai"],
    "big data": ["big data", "hadoop", "spark"],
    "data analysis": ["data analysis", "analyse de données"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau software"],
    "spss": ["spss"],
    "r": ["r language", "r studio"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    
    # Cloud / DevOps
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "devops": ["devops"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "git": ["git", "github", "gitlab"],
    "ci/cd": ["ci/cd", "cicd"],
    
    # ERP / CRM
    "sap": ["sap"],
    "oracle": ["oracle erp"],
    "salesforce": ["salesforce"],
    "odoo": ["odoo"],
    
    # Réseaux / Sécurité
    "réseau": ["réseau", "network", "cisco", "ccna"],
    "sécurité": ["sécurité", "security", "cybersécurité", "cybersecurity"],
    "firewall": ["firewall"],
    "tcp/ip": ["tcp/ip", "tcp ip"],
    
    # Design / Graphisme
    "photoshop": ["photoshop"],
    "illustrator": ["illustrator"],
    "indesign": ["indesign"],
    "figma": ["figma"],
    "sketch": ["sketch"],
    "adobe xd": ["adobe xd", "xd"],
    "canva": ["canva"],
    
    # Comptabilité / Finance
    "comptabilité": ["comptabilité", "accounting"],
    "gestion": ["gestion", "management"],
    "audit": ["audit"],
    "fiscalité": ["fiscalité", "fiscal", "tax"],
    "paie": ["paie", "payroll"],
    "sap fi": ["sap fi", "sap finance"],
    "sage": ["sage", "saari"],
    
    # Logistique
    "gestion de stock": ["gestion de stock", "stock management"],
    "supply chain": ["supply chain"],
    "transport": ["transport"],
    "douane": ["douane", "customs"],
    "logistique": ["logistique"],
    
    # Marketing
    "seo": ["seo", "référencement"],
    "sea": ["sea", "ads", "adwords"],
    "social media": ["social media", "réseaux sociaux"],
    "emailing": ["emailing", "email marketing"],
    "content marketing": ["content marketing", "marketing de contenu"],
}

# Soft skills
SOFT_SKILLS = {
    "communication": ["communication", "communiquer", "relationnel"],
    "travail en équipe": ["travail en équipe", "esprit d'équipe", "collaboration", "teamwork"],
    "autonomie": ["autonomie", "autonome", "indépendant"],
    "rigueur": ["rigueur", "rigoureux", "précision", "détail"],
    "organisation": ["organisation", "organisé", "planification"],
    "gestion du temps": ["gestion du temps", "time management", "priorisation"],
    "résolution de problèmes": ["résolution de problèmes", "problem solving", "analyse"],
    "leadership": ["leadership", "leader", "management d'équipe"],
    "adaptabilité": ["adaptabilité", "flexibilité", "adaptation"],
    "créativité": ["créativité", "créatif", "innovation"],
    "négociation": ["négociation", "persuasion", "convaincre"],
    "empathie": ["empathie", "écoute", "bienveillance"],
    "réactivité": ["réactivité", "réactif", "urgence"],
    "prise de décision": ["prise de décision", "decision making"],
    "gestion du stress": ["gestion du stress", "pression", "stress"],
    "sens du service": ["sens du service", "service client", "client"],
    "proactivité": ["proactivité", "proactif", "initiative"],
    "curiosité": ["curiosité", "curieux", "apprentissage"],
    "persévérance": ["persévérance", "persévérant", "détermination"],
    "intégrité": ["intégrité", "honnêteté", "éthique"],
}

# Langues
LANGUAGES = {
    "français": ["français", "french", "fr"],
    "anglais": ["anglais", "english", "en", "bilingual"],
    "wolof": ["wolof"],
    "arabe": ["arabe", "arabic"],
    "portugais": ["portugais", "portuguese"],
    "espagnol": ["espagnol", "spanish"],
    "allemand": ["allemand", "german"],
    "italien": ["italien", "italian"],
    "chinois": ["chinois", "chinese", "mandarin"],
}

# Niveaux d'expérience
EXPERIENCE_LEVELS = {
    "0-1 an": ["débutant", "junior", "stagiaire", "0 an", "1 an", "première expérience"],
    "2-5 ans": ["2 ans", "3 ans", "4 ans", "5 ans", "confirmé", "intermédiaire"],
    "5-10 ans": ["6 ans", "7 ans", "8 ans", "9 ans", "10 ans", "sénior", "senior"],
    "10+ ans": ["10 ans d'expérience", "11 ans", "12 ans", "13 ans", "14 ans", "15 ans", "expert"],
}

# Secteurs d'activité
SECTORS = {
    "Informatique / IT": ["informatique", "it", "digital", "tech", "software", "logiciel", "développement"],
    "Banque / Finance": ["banque", "finance", "assurance", "banking", "financial"],
    "Commerce / Distribution": ["commerce", "distribution", "vente", "retail", "grande distribution"],
    "BTP / Construction": ["btp", "construction", "bâtiment", "génie civil", "chantier"],
    "Industrie": ["industrie", "industriel", "fabrication", "production", "usine"],
    "Transport / Logistique": ["transport", "logistique", "supply chain", "fret", "transitaire"],
    "Télécommunications": ["télécom", "telecom", "mobile", "fibre", "réseau"],
    "Énergie / Mines": ["énergie", "mine", "pétrole", "gaz", "oil", "gas", "solaire", "renouvelable"],
    "Santé / Pharmacie": ["santé", "médical", "pharmacie", "clinique", "hôpital"],
    "Agriculture": ["agriculture", "agroalimentaire", "agro", "ferme", "culture"],
    "Hôtellerie / Restauration": ["hôtel", "restaurant", "tourisme", "hôtellerie"],
    "Éducation / Formation": ["éducation", "enseignement", "formation", "école", "université"],
    "Conseil / Services": ["conseil", "consulting", "cabinet", "services"],
    "ONG / Humanitaire": ["ong", "humanitaire", "développement", "association"],
    "Administration publique": ["administration", "public", "état", "ministère", "collectivité"],
}

# ──────────────────────────────────────────────────────
# FONCTIONS D'EXTRACTION
# ──────────────────────────────────────────────────────

def nettoyer_texte(texte):
    """Nettoie le texte pour l'analyse"""
    if pd.isna(texte) or texte == "Non précisé":
        return ""
    
    texte = str(texte).lower()
    # Supprimer les caractères spéciaux
    texte = re.sub(r'[^\w\s]', ' ', texte)
    # Supprimer les espaces multiples
    texte = re.sub(r'\s+', ' ', texte)
    return texte.strip()

def extraire_competences_techniques(texte, dictionnaire=TECH_SKILLS):
    """Extrait les compétences techniques du texte"""
    if not texte:
        return []
    
    texte = nettoyer_texte(texte)
    competences_trouvees = []
    
    for comp, variantes in dictionnaire.items():
        for var in variantes:
            # Recherche avec limites de mots
            pattern = r'\b' + re.escape(var) + r'\b'
            if re.search(pattern, texte):
                competences_trouvees.append(comp)
                break
    
    return list(set(competences_trouvees))  # Éliminer les doublons

def extraire_soft_skills(texte, dictionnaire=SOFT_SKILLS):
    """Extrait les soft skills du texte"""
    if not texte:
        return []
    
    texte = nettoyer_texte(texte)
    skills_trouvees = []
    
    for skill, variantes in dictionnaire.items():
        for var in variantes:
            pattern = r'\b' + re.escape(var) + r'\b'
            if re.search(pattern, texte):
                skills_trouvees.append(skill)
                break
    
    return list(set(skills_trouvees))

def extraire_langues(texte, dictionnaire=LANGUAGES):
    """Extrait les langues mentionnées"""
    if not texte:
        return []
    
    texte = nettoyer_texte(texte)
    langues_trouvees = []
    
    for langue, variantes in dictionnaire.items():
        for var in variantes:
            pattern = r'\b' + re.escape(var) + r'\b'
            if re.search(pattern, texte):
                langues_trouvees.append(langue)
                break
    
    return list(set(langues_trouvees))

def extraire_experience(texte, dictionnaire=EXPERIENCE_LEVELS):
    """Extrait le niveau d'expérience requis"""
    if not texte:
        return "Non précisé"
    
    texte = nettoyer_texte(texte)
    
    for niveau, mots in dictionnaire.items():
        for mot in mots:
            if mot in texte:
                return niveau
    
    # Chercher les mentions d'années avec des patterns
    pattern_annees = r'(\d+)\s*(?:ans?|années?)'
    match = re.search(pattern_annees, texte)
    if match:
        annees = int(match.group(1))
        if annees <= 1:
            return "0-1 an"
        elif annees <= 5:
            return "2-5 ans"
        elif annees <= 10:
            return "5-10 ans"
        else:
            return "10+ ans"
    
    return "Non précisé"

def extraire_secteur(texte, dictionnaire=SECTORS):
    """Détermine le secteur d'activité"""
    if not texte:
        return "Non précisé"
    
    texte = nettoyer_texte(texte)
    
    for secteur, mots in dictionnaire.items():
        for mot in mots:
            if mot in texte:
                return secteur
    
    return "Non précisé"

def extraire_salaire(texte):
    """Extrait les informations de salaire si présentes"""
    if not texte:
        return {}
    
    texte = str(texte).lower()
    resultat = {}
    
    # Pattern pour FCFA
    pattern_fcfa = r'(\d+[\s]*[kkm]?[\s]*(?:fcfa|f[-\s]*cfa|franc cfa))'
    match = re.search(pattern_fcfa, texte)
    if match:
        resultat['mention_salaire'] = True
        resultat['salaire_texte'] = match.group(1)
    
    return resultat

def extraire_toutes_competences(row):
    """Fonction principale qui extrait toutes les compétences d'une ligne"""
    # Combiner le titre et les compétences pour l'analyse
    titre = str(row.get('Intitulé du poste', ''))
    competences = str(row.get('Compétences demandées', ''))
    texte_complet = f"{titre} {competences}"
    
    # Extraire les différentes catégories
    tech_skills = extraire_competences_techniques(texte_complet, TECH_SKILLS)
    soft_skills = extraire_soft_skills(texte_complet, SOFT_SKILLS)
    langues = extraire_langues(texte_complet, LANGUAGES)
    experience = extraire_experience(texte_complet, EXPERIENCE_LEVELS)
    secteur = extraire_secteur(texte_complet, SECTORS)
    salaire_info = extraire_salaire(competences)
    
    return pd.Series({
        'tech_skills': tech_skills,
        'soft_skills': soft_skills,
        'langues': langues,
        'experience_requise': experience,
        'secteur': secteur,
        'mention_salaire': salaire_info.get('mention_salaire', False),
        'salaire_texte': salaire_info.get('salaire_texte', ''),
    })

# ──────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("EXTRACTION DES COMPÉTENCES AVEC NLP")
    print("=" * 60)
    
    # Charger les données nettoyées
    print(f"\n📂 Chargement des données : {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    print(f"✅ {len(df)} offres chargées")
    
    # Appliquer l'extraction
    print("\n🔍 Extraction des compétences en cours...")
    resultats = df.apply(extraire_toutes_competences, axis=1)
    
    # Ajouter les colonnes au dataframe
    for col in resultats.columns:
        df[col] = resultats[col]
    
    print("✅ Extraction terminée")
    
    # Statistiques
    print("\n" + "=" * 60)
    print("STATISTIQUES D'EXTRACTION")
    print("=" * 60)
    
    # Compétences techniques
    all_tech = []
    for skills in df['tech_skills']:
        if isinstance(skills, list):
            all_tech.extend(skills)
    
    tech_counts = Counter(all_tech)
    print("\n📊 Top 15 compétences techniques :")
    for skill, count in tech_counts.most_common(15):
        print(f"  {skill:20} → {count:3} offres")
    
    # Soft skills
    all_soft = []
    for skills in df['soft_skills']:
        if isinstance(skills, list):
            all_soft.extend(skills)
    
    soft_counts = Counter(all_soft)
    print("\n🧠 Top 10 soft skills :")
    for skill, count in soft_counts.most_common(10):
        print(f"  {skill:20} → {count:3} offres")
    
    # Langues
    all_lang = []
    for lang in df['langues']:
        if isinstance(lang, list):
            all_lang.extend(lang)
    
    lang_counts = Counter(all_lang)
    print("\n🌍 Langues demandées :")
    for lang, count in lang_counts.most_common():
        print(f"  {lang:10} → {count:3} offres")
    
    # Expérience
    print("\n📅 Niveaux d'expérience :")
    exp_counts = df['experience_requise'].value_counts()
    for exp, count in exp_counts.items():
        print(f"  {exp:15} → {count:3} offres ({count/len(df)*100:.1f}%)")
    
    # Secteurs
    print("\n🏢 Secteurs d'activité :")
    secteur_counts = df['secteur'].value_counts().head(10)
    for secteur, count in secteur_counts.items():
        print(f"  {secteur:25} → {count:3} offres")
    
    # Salaires
    print("\n💰 Mentions de salaire :")
    mentions = df['mention_salaire'].sum()
    print(f"  Offres avec mention de salaire : {mentions} ({mentions/len(df)*100:.1f}%)")
    
    # Sauvegarder
    print(f"\n💾 Sauvegarde des résultats...")
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    # Sauvegarder aussi en JSON pour analyse
    json_output = OUTPUT_FILE.replace('.csv', '.json')
    df.to_json(json_output, orient='records', force_ascii=False)
    
    print(f"✅ Fichier sauvegardé : {OUTPUT_FILE}")
    print(f"✅ Fichier JSON : {json_output}")
    
    # Créer un résumé JSON des statistiques
    resume = {
        'total_offres': len(df),
        'top_tech_skills': dict(tech_counts.most_common(20)),
        'top_soft_skills': dict(soft_counts.most_common(20)),
        'langues': dict(lang_counts),
        'experience': exp_counts.to_dict(),
        'secteurs': secteur_counts.to_dict(),
        'mentions_salaire': int(mentions),
    }
    
    resume_file = os.path.join(os.path.dirname(INPUT_FILE), 'analyse_competences_resume.json')
    with open(resume_file, 'w', encoding='utf-8') as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Résumé sauvegardé : {resume_file}")
    print("\n" + "=" * 60)
    print("EXTRACTION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)

if __name__ == "__main__":
    main()