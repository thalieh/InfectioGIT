import os
import requests

def get_ontology_id(disease_name, ontology="mondo"):
    """Cherche l'ID officiel via l'API OLS de l'EBI"""
    url = f"https://www.ebi.ac.uk/ols/api/search?q={disease_name}&ontology={ontology}&exact=true"
    try:
        response = requests.get(url)
        data = response.json()
        if data['response']['numFound'] > 0:
            # On récupère le premier résultat (le plus pertinent)
            return data['response']['docs'][0]['short_form']
    except:
        return None
    return "Non trouvé"

def generate_standard_files():
    maladies = ["Tuberculosis", "HIV", "Influenza", "COVID-19", "Malaria", "Dengue", "Chikungunya", "Mpox"]
    output_dir = "DOI_DOID_MONDO"
    os.makedirs(output_dir, exist_ok=True)

    # Pour MONDO et DOID (Recherche automatique)
    for onto in ["mondo", "doid"]:
        with open(os.path.join(output_dir, f"{onto}.txt"), "w") as f:
            for m in maladies:
                id_found = get_ontology_id(m, onto)
                f.write(f"{m}: {id_found}\n")
        print(f"✅ Fichier {onto}.txt généré.")

    print(f"\n📍 Les fichiers sont prêts dans le dossier '{output_dir}'")

if __name__ == "__main__":
    generate_standard_files()
