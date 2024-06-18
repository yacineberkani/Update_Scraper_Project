from Scraper_PubMed import *
#from Scraper_pdf import *
from tor_py import *
from utils import *

def main():
    """
    Fonction principale pour exécuter le programme de recherche et de téléchargement d'articles scientifiques.
    """
    # URL de l'API PubMed pour effectuer la recherche
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=NUM&sort=relevance&term=KEYWORD"
    
    # Saisie de la requête de l'utilisateur
    mot_cle = saisie_requete()
    
    # Détection de la langue de la requête
    langue = detect_language(mot_cle)
    
    # Sélection et extraction des mots-clés en fonction de la langue détectée
    mots_cles_format = selection_extraction_mots_cles(mot_cle, langue)
    
    # Saisie du nombre d'articles souhaités par l'utilisateur
    num = saisie_nombre_resultats()
    
    # Construction de l'URL de la requête avec les paramètres fournis par l'utilisateur
    url = construction_url_requete(url, num, mots_cles_format)
    
    # Gestion du contexte SSL pour éviter les avertissements
    gestion_contexte_SSL()
    
    # Récupération des identifiants PubMed des articles correspondant à la requête
    pubmed_ids = get_pubmed_ids(url, num)
    
    # Récupération des données des articles à partir de leurs identifiants PubMed
    articles_data = get_article_data(pubmed_ids)
    
    # Enregistrement des données des articles dans un fichier CSV
    file_name = enregistrement_articles_csv(articles_data, mots_cles_format, num)
    
    # Création d'un dossier pour enregistrer les fichiers PDF
    name_folder = NameFolder(mots_cles_format, num)
    create_folder(name_folder)
        
    # Téléchargement des fichier pdf 
    download_pdf(file_name, name_folder)
    
if __name__ == "__main__":
    main()
