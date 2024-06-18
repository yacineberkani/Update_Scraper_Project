from __init__ import *

# Fonction pour supprimer les crochets d'une chaîne de caractères
def strip_brackets(s): 
    """
    Supprime les crochets '[' et ']' d'une chaîne de caractères.
    
    Args:
        s (str): La chaîne de caractères dont les crochets doivent être supprimés.
        
    Returns:
        str: La chaîne de caractères sans les crochets.
    """
    no_brackets = "" 
    dont_want = ['[', ']']
    for char in s: 
        if char not in dont_want:
            no_brackets += char
    return no_brackets 

# Fonction pour extraire les informations bibliographiques d'un article à partir de la structure XML
def get_bibliography(soup):
    """
    Extrait les informations bibliographiques d'un article à partir de la structure XML fournie par BeautifulSoup.
    
    Args:
        soup: L'objet BeautifulSoup représentant l'article.
        
    Returns:
        list: Une liste contenant les informations bibliographiques de l'article.
    """
    article = soup.find('article')
    journal = soup.find('journal')
    listauteur = article.find('authorlist')
    auteur = ""
    if listauteur:
        initials = listauteur.find_all('initials')
        lastnames = listauteur.find_all('lastname')
        for i in range(len(lastnames)):
            if i < len(initials):
                initial = initials[i].text
                auteur += initial
                auteur += '. '
            else:
                auteur += ' '
            nom = lastnames[i].text
            auteur += nom
            if i == len(lastnames) - 2:
                auteur += ' and '
            elif i != len(lastnames) - 1:
                auteur += ', '
        auteur += ", "

    titreArticle = ''
    if article.find('articletitle'):
            titreArticle = ''
            titre_str = article.find('articletitle').text
            titre_str = strip_brackets(titre_str)
            titreArticle  += titre_str
            if titreArticle [-1] == '.':
                titreArticle  += ''
            else:
                titreArticle  += '.'           
    titreJournal = ''
    if journal.find('title'):
        titreJournal = journal.find('title').text
        titreJournal += ' '
     
    JournalIssue = journal.find('journalissue')
    month = JournalIssue.find('month')
    date = ''
    if month:
        month = JournalIssue.find('month').text
        if len(month)<3:
            month_int = int(str(month))
            month = calendar.month_abbr[month_int]
        year = JournalIssue.find('year').text
        date = '('
        date += month
        date += '. '
        date += year
        date += '). '
    elif JournalIssue.find('year'):
        date = '('
        date += JournalIssue.find('year').text
        date += '). '      
    else: ''

    if soup.find('articleid'):
        doi_pii = article.find_all('elocationid')
        doi_pii_str = ""
        if len(doi_pii)>1:
            if 'doi' in str(doi_pii[0]):
                doi_pii = doi_pii[0].text
                doi_pii_str += doi_pii
            elif 'doi' in str(doi_pii[1]):
                doi_pii = doi_pii[1].text
                doi_pii_str += doi_pii
        elif len(doi_pii) == 1:
            if 'doi' in str(doi_pii[0]):
                doi_pii = doi_pii[0].text
                doi_pii_str += doi_pii
            elif 'pii' in str(doi_pii[0]):
                doi_pii = doi_pii[0].text
                doi_pii_str += doi_pii
    resume = ''
    if article.find('abstracttext'):
        resume = article.find('abstracttext').text
    
    result = []
    result.append(auteur)
    result.append(titreArticle)
    result.append(titreJournal)
    result.append(date)
    result.append(doi_pii_str)
    result.append(resume)

    return result

# Fonction pour récupérer les identifiants PubMed des articles correspondant à une requête
def get_pubmed_ids(url, num):
    """
    Récupère les identifiants PubMed des articles correspondant à une requête à partir de l'URL de l'API PubMed et du nombre d'articles souhaités.
    
    Args:
        url (str): L'URL de l'API PubMed.
        num (int): Le nombre d'articles souhaités.
        
    Returns:
        list: Une liste d'identifiants PubMed.
    """
    pageweb = urllib.request.urlopen(url).read()
    dict_page = json.loads(pageweb)
    return dict_page["esearchresult"]["idlist"]

# Fonction pour récupérer les données des articles à partir de leurs identifiants PubMed
def get_article_data(pubmed_ids):
    """
    Récupère les données des articles à partir de leurs identifiants PubMed en utilisant l'API d'E-utilities de NCBI.
    
    Args:
        pubmed_ids (list): Une liste d'identifiants PubMed.
        
    Returns:
        list: Une liste de listes contenant les informations bibliographiques de chaque article.
    """
    articles_data = []
    for link in pubmed_ids:
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=idlist"
        url = url.replace('idlist', link)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        article = get_bibliography(soup)
        lien = f"https://www.ncbi.nlm.nih.gov/pubmed/{link}"
        article.append(lien) 
        articles_data.append(article)
    return articles_data
# Fonction pour récupérer les liens vers les versions PDF des articles à partir des identifiants PMC
def get_pmc_links(pubmed_ids):
    """
    Récupère les liens vers les versions PDF des articles à partir des identifiants PMC en utilisant l'API de NCBI.
    
    Args:
        pubmed_ids (list): Une liste d'identifiants PMC.
        
    Returns:
        list: Une liste de liens vers les PDF.
    """
    pmc_links = []
    for pmid in pubmed_ids:
        pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=json"
        response = requests.get(pmc_url)
        if response.status_code == 200:
            data = response.json()
            if 'records' in data:
                for record in data['records']:
                    if 'pdf_url' in record:
                        pmc_links.append(record['pdf_url'])
    return pmc_links
