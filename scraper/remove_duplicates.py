import pandas as pd

def remove_duplicates(df, columns):
    """
    Détecte et supprime les doublons dans un DataFrame selon les colonnes choisies.
    """
    # détecter les doublons
    duplicates = df[df.duplicated(subset=columns)]
    print("Nombre de doublons détectés :", len(duplicates))

    # supprimer les doublons
    df_clean = df.drop_duplicates(subset=columns, keep="first")
    df_clean = df_clean.reset_index(drop=True)

    return df_clean


# ----------------------------------------
# Ce bloc ne fait partie d'aucune fonction
# Il sert à tester ton script directement
# ----------------------------------------
if __name__ == "__main__":

    # Exemple de données factices
    data = {
        "titre": ["Data Analyst", "Data Scientist", "Data Analyst"],
        "entreprise": ["Orange", "Wave", "Orange"],
        "ville": ["Dakar", "Dakar", "Dakar"]
    }

    df = pd.DataFrame(data)

    # On utilise la fonction remove_duplicates
    df_clean = remove_duplicates(df, ["titre", "entreprise", "ville"])

    print("\nDataFrame après suppression des doublons :")
    print(df_clean)