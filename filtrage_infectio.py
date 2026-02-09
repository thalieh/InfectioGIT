import os
import json
from bioservices import BioModels

# 1. Initialisation
s = BioModels()

def get_all_models(query):
    models = []
    offset = 0
    while True:
        try:
            # On récupère les résultats par page de 20 pour aller plus vite
            search_results = s.search(query, offset=offset, numResults=20)
            if 'models' not in search_results or not search_results['models']:
                break
            models.extend(search_results['models'])
            offset += 20
            print(f"Recherche en cours... {len(models)} modèles trouvés.")
        except Exception as e:
            print(f"Erreur de recherche : {e}")
            break
    return models

def download_and_enrich(model_data, base_directory):
    model_id = model_data['id']
    # On récupère le nom et la description pour un classement précis
    name = model_data.get('name', "")
    description = model_data.get('description', "")
    text_to_search = (name + " " + description).lower()
    
    # 2. Classement par maladie
    if any(w in text_to_search for w in ["tb", "tuberculosis", "tuberculose"]):
        sub_folder = "Tuberculosis"
    elif "hiv" in text_to_search or "vih" in text_to_search:
        sub_folder = "VIH"
    elif "influenza" in text_to_search or "grippe" in text_to_search:
        sub_folder = "Influenza"
    elif any(w in text_to_search for w in ["covid", "sars-cov-2", "coronavirus"]):
        sub_folder = "COVID-19"
    elif "malaria" in text_to_search or "paludisme" in text_to_search:
        sub_folder = "Malaria"
    elif any(w in text_to_search for w in ["dengue", "chikungunya"]):
        sub_folder = "Dengue_Chikungunya"
    elif "mpox" in text_to_search or "monkeypox" in text_to_search:
        sub_folder = "Mpox"
    else:
        sub_folder = "Other_Infections"

    directory = os.path.join(base_directory, sub_folder)
    os.makedirs(directory, exist_ok=True)

    # 3. Récupération des données et téléchargement
    try:
        # Récupération des métadonnées complètes
        full_metadata = s.get_model(model_id)
        
        # Sauvegarde du fichier JSON (Métadonnées)
        json_path = os.path.join(directory, f"{model_id}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=4, ensure_ascii=False)
            
        # Téléchargement du fichier SBML (.xml) - Le "vrai" modèle
        sbml_content = s.get_model_download(model_id)
        xml_path = os.path.join(directory, f"{model_id}.xml")
        with open(xml_path, 'wb') as f:
            f.write(sbml_content)
            
        print(f"✅ Modèle {model_id} sauvegardé dans {sub_folder}")
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {model_id}: {e}")

def main():
    # 4. Requête ciblée sur tes maladies (Curated = Qualité vérifiée)
    query = ('(TB OR Tuberculosis OR HIV OR VIH OR Influenza OR COVID-19 OR '
             'Malaria OR Dengue OR Chikungunya OR Mpox OR Monkeypox) '
             'AND curationstatus:"Manually curated" AND modelformat:"SBML"')

    base_dir = "InfectioGIT_Data"
    print(f"Démarrage de l'extraction vers le dossier : {base_dir}")
    
    models = get_all_models(query)

    for m in models:
        # Appel de la fonction corrigée (download_and_enrich)
        download_and_enrich(m, base_dir)

    print("\nTerminé ! Vérifie le dossier InfectioGIT_Data.")

if __name__ == "__main__":
    main()
