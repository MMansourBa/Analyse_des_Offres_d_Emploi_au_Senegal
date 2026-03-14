import pandas as pd
import os

# ── Charger les deux fichiers ──
df_emploidakar    = pd.read_csv("data/raw/offres_emploi_raw.csv", encoding="utf-8-sig")
df_goafricaonline = pd.read_csv("data/raw/offres_goafricaonline_raw.csv", encoding="utf-8-sig")

print(f"EmploiDakar    : {len(df_emploidakar)} offres")
print(f"GoAfricaOnline : {len(df_goafricaonline)} offres")

# ── Fusionner ──
df_final = pd.concat([df_emploidakar, df_goafricaonline], ignore_index=True)
print(f"\nTotal fusionné : {len(df_final)} offres")

# ── Sauvegarder ──
df_final.to_csv("data/raw/offres_emploi_senegal_raw.csv", index=False, encoding="utf-8-sig")
df_final.to_json("data/raw/offres_emploi_senegal_raw.json", orient="records", force_ascii=False)

print("Fichiers sauvegardés dans data/raw/")