import os
import json
from bioservices import BioModels

s = BioModels()

def get_all_models(query):
    models = []
    offset = 0
    while True:
        try:
            search_results = s.search(query, offset=offset, numResults=20)
            if 'models' not in search_results or not search_results['models']:
                break
            models.extend(search_results['models'])
            offset += 20
            print(f"Recherche... {len(models)} modèles trouvés.")
        except Exception as e:
            print(f"Erreur : {e}")
            break
    return models

def download_and_enrich(model_data, base_directory):
    model_id = model_data['id']
    
    # On récupère les métadonnées complètes pour voir les annotations
    try:
        full_metadata = s.get_model(model_id)
        annotations = str(full_metadata.get("annotations", "")).lower()
        
        # 1. Classement précis par Code MONDO / DOID
        # On définit quel dossier correspond à quel code
        if "mondo_0005109" in annotations or "doid_526" in annotations:
            sub_folder = "VIH"
        elif "mondo_0005066" in annotations or "doid_0080600" in annotations:
            sub_folder = "COVID-19"
        elif "mondo_0018076" in annotations or "doid_399" in annotations:
            sub_folder = "Tuberculosis"
        elif "mondo_0005136" in annotations or "doid_2265" in annotations:
            sub_folder = "Malaria"
        elif "mondo_0005131" in annotations or "doid_9455" in annotations:
            sub_folder = "Influenza"
        else:
            sub_folder = "Other_Infections"

        directory = os.path.join(base_directory, sub_folder)
        os.makedirs(directory, exist_ok=True)

        # 2. Sauvegarde JSON et XML
        json_path = os.path.join(directory, f"{model_id}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=4, ensure_ascii=False)
            
        sbml_content = s.get_model_download(model_id)
        if sbml_content:
            with open(os.path.join(directory, f"{model_id}.xml"), 'wb') as f:
                f.write(sbml_content)
            print(f"✅ {model_id} classé dans {sub_folder}")

    except Exception as e:
        print(f"❌ Erreur sur {model_id}: {e}")

def main():
    # 2. LA QUERIE PAR ONTOLOGIE
    # On cherche les modèles qui ont ces codes dans leurs métadonnées
    # Exemple : MONDO_0005066 (COVID), MONDO_0005109 (HIV), etc.
    mondo_ids = ["MONDO_0005109", "MONDO_0005066", "MONDO_0018076", "MONDO_0005136", "MONDO_0005131"]
    
    # On construit la requête : "MONDO_0005109 OR MONDO_0005066 ..."
    ontology_query = " OR ".join(mondo_ids)
    
    # Requête finale combinée
    query = f'({ontology_query}) AND curationstatus:"Manually curated" AND modelformat:"SBML"'

    base_dir = "Infectio_Ontology_Data"
    models = get_all_models(query)

    for m in models:
        download_and_enrich(m, base_dir)

if __name__ == "__main__":
    main()
