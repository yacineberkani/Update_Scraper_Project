from __init__ import * 

# Fonction pour extraire les mots-clés en français
def extraire_mots_cles_fr(requete):
    """
    Utilise le modèle de langue française de spaCy pour extraire les mots-clés d'une requête en français.
    
    Args:
        requete (str): La requête de l'utilisateur.
        
    Returns:
        str: Les mots-clés extraits de la requête, sous forme d'une chaîne de caractères.
    """
    nlp = spacy.load("fr_core_news_sm")
    requete_utilisateur = requete.lower()
    doc = nlp(requete_utilisateur)
    mots_cles = []
    for token in doc:
        if (token.pos_ == "NOUN" and token.dep_ not in ["ROOT","obj"]) or \
           (token.pos_ == "ADV" ) or \
           (token.pos_ == "PRON" and token.dep_ != "dep") or \
           (token.dep_ == "ROOT" and token.pos_ not in ["NOUN","VERB"]) or \
           (token.pos_ == "ADJ" ) or \
           (token.pos_ == "PROPN" and token.dep_ in ["nmod","punct"]):
            if not token.is_stop and not token.is_punct and token.text.lower() not in ['article', 'articles']:
                mots_cles.append(token.text)
    mots_cles_format = ' '.join(mots_cles)
    return mots_cles_format

# Fonction pour extraire les mots-clés en anglais
def extraire_mots_cles_en(requete):
    """
    Utilise le modèle de langue anglaise de spaCy pour extraire les mots-clés d'une requête en anglais.
    
    Args:
        requete (str): La requête de l'utilisateur.
        
    Returns:
        str: Les mots-clés extraits de la requête, sous forme d'une chaîne de caractères.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(requete)
    mots_cles = []
    for token in doc:
        if (token.pos_ == "NOUN" ) or  (token.dep_ == "punct") or \
           (token.pos_ == "ADV") or (token.dep_ == "pobj") or \
           (token.pos_ == "PROPN" and token.dep_ != "dep") or \
           (token.pos_ == "ADJ" ) :
            if not token.is_stop and not token.is_punct and token.text.lower() not in ['article', 'articles']:
                mots_cles.append(token.text)
    mots_cles_format = ' '.join(mots_cles)
    return mots_cles_format

# Fonction pour détecter la langue d'un texte
def detect_language(text):
    """
    Détecte la langue d'un texte donné.
    
    Args:
        text (str): Le texte dont la langue doit être détectée.
        
    Returns:
        str: 'français' si la langue détectée est le français, sinon 'anglais'.
    """
    lang = detect(text)
    if lang == 'fr':
        return 'français'
    else:
        return 'anglais'

# Fonction pour formater un mot-clé
def format_mot(motcle):
    """
    Formate un mot-clé en remplaçant les espaces par des '+' pour les requêtes HTTP.
    
    Args:
        motcle (str): Le mot-clé à formater.
        
    Returns:
        str: Le mot-clé formaté.
    """
    if ' ' in motcle:
        format_motcle = motcle.replace(' ', '+')
    else:
        format_motcle = motcle
    return format_motcle
# Fonction pour calculer la similarité cosinus entre un mot-clé et les titres des articles
def calculate_similarity(keyword, article_titles):
    """
    Calcule la similarité cosinus entre un mot-clé et les titres des articles.
    
    Args:
        keyword (str): Le mot-clé à comparer.
        article_titles (list): Une liste de titres d'articles.
        
    Returns:
        array: Un tableau de similarités.
    """
    keyword_vector = [keyword]
    corpus = keyword_vector + article_titles
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    keyword_tfidf_vector = tfidf_matrix[0]
    article_titles_tfidf_matrix = tfidf_matrix[1:]
    cosine_similarities = cosine_similarity(keyword_tfidf_vector, article_titles_tfidf_matrix)
    return cosine_similarities.flatten()





def traite_query(query):
    """
    Utilise spaCy pour traiter une requête en anglais et la formate pour une recherche.
    
    Args:
        query (str): La requête à traiter.
        
    Returns:
        str: La requête traitée et formatée.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    mots_cles = []
    for token in doc:
        if not token.is_stop and not token.is_punct and token.text.lower():
            mots_cles.append(token.text)
                
    mots_cles_format = '+'.join(mots_cles)
    
    return mots_cles_format

def saisie_requete():
    """
    Fonction pour saisir la requête de recherche de l'utilisateur.
    """
    mot_cle = str(input('Veuillez saisir votre requête : '))
    return mot_cle




def selection_extraction_mots_cles(mot_cle, langue):
    """
    Fonction pour sélectionner la fonction d'extraction des mots-clés en fonction de la langue détectée.
    """
    if langue == 'français':
        mots_cles_format = extraire_mots_cles_fr(mot_cle)
        print("Langue détectée ==> Français")
    else:
        mots_cles_format = extraire_mots_cles_en(mot_cle)
        print("Langue détectée ==> Anglais")
    return mots_cles_format


def saisie_nombre_resultats():
    """
    Fonction pour saisir le nombre d'articles souhaités par l'utilisateur.
    """
    num = int(input('Nombre de résultats souhaités : '))
    return num

def NameFolder(mots_cles_format, num):
    """
    Génère le nom du dossier pour enregistrer les fichiers PDF des articles.

    Args:
        mots_cles_format (str): Les mots-clés de recherche, formatés pour utilisation dans un nom de dossier.
        num (int): Le nombre d'articles souhaités.

    Returns:
        str: Le nom du dossier généré.
    """
    # Remplace les espaces dans les mots-clés par des underscores
    # et ajoute le nombre d'articles à la fin du nom du dossier
    folder_name = mots_cles_format.replace(' ', '_') + '_' + str(num)
    return folder_name

    
# Fonction pour créer un dossier s'il n'existe pas déjà
def create_folder(folder_name):
    """
    Crée un dossier s'il n'existe pas déjà.
    
    Args:
        folder_name (str): Le nom du dossier à créer.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    


def construction_url_requete(url, num, mots_cles_format):
    """
    Fonction pour construire l'URL de la requête avec les paramètres fournis par l'utilisateur.
    """
    url = url.replace('NUM', str(num))
    url = url.replace('KEYWORD', format_mot(mots_cles_format))
    return url


def gestion_contexte_SSL():
    """
    Fonction pour gérer le contexte SSL et éviter les avertissements.
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


def enregistrement_articles_csv(articles_data, mots_cles_format, num):
    """
    Fonction pour enregistrer les données des articles dans un fichier CSV.
    """
    df = pd.DataFrame(articles_data)
    df.columns = ['Auteur', 'Nom_Article', 'Journal', 'Date', 'DOI', 'Résumé', 'Lien']
    similarity_scores = calculate_similarity(mots_cles_format, df['Nom_Article'].tolist())
    df['Similarité_Cosinus'] = similarity_scores
    df = df.sort_values(by='Similarité_Cosinus', ascending=False)
    file_name = mots_cles_format.replace(' ', '_') + '_' + str(num) + '.csv'
    df.to_csv(file_name)
    print("Fichier CSV enregistré avec succès.")
    return file_name


def choix_article(df):
    """
    Fonction pour afficher les articles disponibles et demander à l'utilisateur de choisir un article.
    """
    print("Liste des articles disponibles :")
    for index, nom_article in enumerate(df['Nom_Article'], start=1):
        print(f"{index}. {nom_article}")

    choix = int(input("Veuillez choisir le numéro de l'article : "))
    return choix



