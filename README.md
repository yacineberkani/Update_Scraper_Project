# PDF Scraper Project

![img](https://github.com/yacineberkani/Scraper_Project/blob/main/Ajouter%20un%20titre%20(1).png)

## Description

Ce projet permet de récupérer des articles scientifiques en PDF à partir d'un prompt saisi en langage naturel. Le projet suit les étapes suivantes :

1. Extraction des mots-clés à partir du prompt.
2. Scraping de PubMed pour récupérer les métadonnées des articles en format CSV.
3. Extraction des DOI à partir du fichier CSV.
4. Téléchargement des articles en PDF à partir de Sci-Hub en utilisant les DOI.

## Structure du projet

Le projet est organisé en plusieurs fichiers Python :
- `__init__.py` : Fichier d'initialisation qui importe toutes les bibliothèques nécessaires.
- `Scraper_pdf.py`: Contient les fonctions pour télécharger les fichiers PDF à partir de Sci-Hub.
- `Scraper_PubMed.py`: Contient les fonctions pour scraper PubMed et récupérer les métadonnées des articles.
- `utils.py`: Contient les fonctions utilitaires pour traiter les prompts et extraire les mots-clés.
- `main.py`: Script principal qui orchestre l'ensemble des étapes du projet.

## Installation

1. Assurez-vous d'avoir Python installé sur votre système. Si ce n'est pas le cas, vous pouvez le télécharger à partir du site officiel : [python.org](https://www.python.org/).

2. Clônez ce référentiel GitHub sur votre machine locale en utilisant la commande suivante :
   
    ```sh
    git clone https://github.com/votre_utilisateur/Scraper_Project.git
    ```

3. Accédez au répertoire du projet :
   
    ```sh
    cd Scraper_Project
    ```

4. Installez les dépendances requises en exécutant la commande suivante :
   
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation
**Étape 1: Extraction des mots-clés**
Le fichier `utils.py`contient les fonctions nécessaires pour traiter le prompt saisi en langage naturel et extraire les mots-clés.

**Étape 2: Scraping de PubMed**
Le fichier `Scraper_PubMed.py` contient les fonctions pour scraper PubMed en utilisant les mots-clés extraits et pour sauvegarder les métadonnées des articles en format CSV.

**Étape 3: Extraction des DOI**
Extrait les DOI des articles à partir du fichier CSV généré.

**Étape 4: Téléchargement des PDF**
Le fichier `Scraper_pdf.py` contient les fonctions pour télécharger les articles en PDF à partir de Sci-Hub en utilisant les DOI extraits.

**Exécution du script principal**
Le fichier main.py orchestre l'ensemble des étapes du projet. Vous pouvez exécuter le script principal pour lancer le processus complet :

**Exécutez le script `main.py` en utilisant la commande suivante :**
  ```sh
  python main.py
  ```
## Exemple d'utilisation
1. Suivez les instructions à l'écran pour saisir votre requête de recherche, spécifier le nombre d'articles à récupérer, et télécharger son PDF.
2. Le script extrait les mots-clés du prompt.
3. Le script scrape PubMed pour récupérer les métadonnées des articles et les sauvegarde en format CSV.
4. Le script extrait les DOI à partir du fichier CSV.
5. Le script télécharge les articles en PDF à partir de Sci-Hub en utilisant les DOI extraits.


## Auteur

BERKANI Yacine
