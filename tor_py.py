from __init__ import *


# Liste des User-Agents pour simuler différents navigateurs lors des requêtes HTTP
user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def search_save_pdf(pdf_url, folder_name, sess):
    """
    Recherche et télécharge un fichier PDF à partir d'une URL et l'enregistre dans un dossier spécifié.
    
    Args:
        pdf_url (str): L'URL du fichier PDF à télécharger.
        folder_name (str): Le nom du dossier dans lequel enregistrer le fichier PDF.
        session: La session de requêtes à utiliser pour le téléchargement.
        
    Returns:
        str: Le chemin du fichier enregistré.
    """
    try:
        headers = {"User-Agent": rd.choice(user_agents)}
        response = sess.get(pdf_url, headers=headers, stream=True)
        response.raise_for_status()
        file_name = f"article_{uuid.uuid4()}.pdf"
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement du PDF {pdf_url}: {str(e)}")
        return None
    except Exception as ex:
        print(f"Une erreur inattendue s'est produite : {str(ex)}")
        return None

def read_csv(file_name):
    """
    Lit un fichier CSV et retourne une liste de DOI.
    
    Args:
        file_name (str): Le fichier CSV à lire.
    
    Returns:
        list: Liste des DOI.
    """
    base = pd.read_csv(file_name, usecols=['DOI'])
    base.dropna(inplace=True)
    DOIs = list(base['DOI'])
    return DOIs

def generate_base_urls(dois):
    """
    Génère les URLs de base pour chaque DOI.
    
    Args:
        dois (list): Liste des DOI.
    
    Returns:
        list: Liste des URLs de base.
    """
    sci_hub_base = "https://sci-hub.st"
    url_doi = [f"{sci_hub_base}/{doi}" for doi in dois]
    return url_doi

def fetch_pdf_urls(base_urls, sess):
    """
    Récupère les URLs des fichiers PDF à partir des URLs de base.
    
    Args:
        base_urls (list): Liste des URLs de base.
        session: La session de requêtes à utiliser pour les requêtes.
    
    Returns:
        list: Liste des URLs des fichiers PDF.
    """
    pdf_urls = []
    for url in base_urls:
        response = sess.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            embed_tag = soup.find('embed', type='application/pdf')
            if embed_tag:
                download_link = embed_tag['src']
                pdf_urls.append(f"https://sci-hub.st{download_link}")
            else:
                print("Article non disponible")
        else:
            print(f"Erreur lors de la requête HTTP : {response.status_code}")
    pdf_list = [url.split('#')[0] for url in pdf_urls]
    return pdf_list

def clean_pdf_urls(pdf_urls):
    """
    Nettoie les URLs des fichiers PDF pour une utilisation correcte.
    
    Args:
        pdf_urls (list): Liste des URLs des fichiers PDF.
    
    Returns:
        list: Liste des URLs nettoyées.
    """
    cleaned_urls = []
    for url in pdf_urls:
        parts = url.split('/')
        pdf_url = ""
        for i in range(len(parts) - 1, -1, -1):
            if 'sci-hub.st' in parts[i] and 'downloads' not in parts[i]:
                pdf_url = '/'.join(parts[i:])
                break
            elif 'sci-hub.st' in parts[i] and 'downloads' in parts[i]:
                pdf_url = '/'.join(parts[i+1:])
                break
        if pdf_url.startswith('sci-hub.st//'):
            pdf_url = pdf_url[len('sci-hub.st//'):]
        cleaned_urls.append(pdf_url)
    return cleaned_urls

def download_pdfs(cleaned_urls, folder, sess):
    """
    Télécharge les fichiers PDF et les enregistre dans le dossier spécifié.
    
    Args:
        cleaned_urls (list): Liste des URLs nettoyées des fichiers PDF.
        folder (str): Le nom du dossier dans lequel enregistrer les fichiers PDF.
        session: La session de requêtes à utiliser pour les téléchargements.
    
    Returns:
        int: Nombre de fichiers PDF téléchargés avec succès.
    """
    num_articles = 0
    for url in cleaned_urls:
        pdf_url = f"https://{url}"
        file_path = search_save_pdf(pdf_url, folder, sess)
        if file_path:
            num_articles += 1
    return num_articles

def download_pdf(file_name, folder):
    """
    Télécharge les fichiers PDF correspondant à un fichier csv et les enregistre dans un dossier spécifié.
    
    Args:
        file_name (str): Le fichier csv.
        folder (str): Le nom du dossier dans lequel enregistrer les fichiers PDF.
    """
    dois = read_csv(file_name)
    base_urls = generate_base_urls(dois)
    
    with TorRequests() as tor_requests:
        with tor_requests.get_session() as sess:
            pdf_urls = fetch_pdf_urls(base_urls, sess)
            cleaned_urls = clean_pdf_urls(pdf_urls)
            num_articles = download_pdfs(cleaned_urls, folder, sess)
            print(f"Nombre total d'articles téléchargés avec succès : {num_articles}")
