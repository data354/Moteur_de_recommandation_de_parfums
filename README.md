	***
#### Presentation du projet
Ce projet consiste a la  mise en oeuvre d'une application de recommandation de parfum basée sur ma methode du contents-based filterings.
Dans un monde où les choix de parfums sont vastes et parfois écrasants, notre objectif était de créer une solution innovante, basée sur l'IA pour simplifier le processus de sélection pour nos clients

###### Rappel
La "filtration basée sur le contenu" (contents-based filtering en anglais) est une méthode utilisée dans les systèmes de recommandation pour suggérer des éléments à un utilisateur en fonction de caractéristiques intrinsèques des éléments eux-mêmes ou de leurs description
***

***
## La realisation du projet comporte trois phases.
1. [Traitement et Mise en Forme des Données ]                                   
2. [Mise en Place de l'Application et Développement des Fonctions ]
3. [Implémentation et Test ]

***
***
#### packages neccessaires
```python
$ import streamlit as st
$ import numpy as np
$ import pandas as pd
$ import os
$ from scipy.spatial.distance import pdist, squareform
$ from sklearn.metrics.pairwise import cosine_similarity
$ import google.generativeai as genai
```
***
***

# Phase de Réalisation du Projet
***
### Phase 1 : Traitement et Mise en Forme des Données
Ce projet repose sur l'utilisation de deux types de données prétraitées disponibles dans le fichier "donnees.py" : 

data_parfum :

Un jeu de données de 3000 parfums.
Colonnes :
* "nom" : Nom du parfum.
* "utilisation" : Chaîne de caractères représentant les moments d'utilisation possibles du parfum.
* "description" : Chaîne de caractères décrivant le parfum.
* "embedding" : Représentation vectorielle de l'incorporation de la description réalisée avec Gemini.


data_binaire :

* Un jeu de données indexant les parfums et leurs caractéristiques.
* Colonnes :
* Indexation des parfums.
* Caractéristiques des parfums représentées par des valeurs binaires (1 si le parfum possède la caractéristique, 0 sinon).

***
### Phase 2:  Mise en Place de l'Application et Développement des Fonctions
 Cette application repose sur deux fonctions presentes dans le ficher "fonction_recom.py" 


* La premiere est la fonction 

```python
def prediction(chaine):
    ..........................................

```


Cette fonction, nommée "prediction", prend en entrée une chaîne de caractères représentant une liste de noms de parfums séparés par des virgules. Elle calcule ensuite un profil utilisateur basé sur ces parfums en utilisant une approche de similarité de Jaccard.

Voici un résumé des étapes effectuées par la fonction :

* Initialisation du profil utilisateur : Création d'un vecteur de zéros pour représenter le nouvel utilisateur.

* Calcul du profil utilisateur : Pour chaque parfum dans la liste d'entrée, la fonction ajoute les caractéristiques du parfum au profil utilisateur.

* Normalisation : Les valeurs du profil utilisateur sont normalisées pour être comprises entre 0 et 1.

* Calcul de la similarité de Jaccard : La fonction calcule la similarité de Jaccard entre le nouvel utilisateur et tous les autres utilisateurs (parfums) dans le jeu de données.

* Sélection des parfums similaires : Les parfums les plus similaires au nouvel utilisateur sont identifiés et classés par ordre de similarité décroissante.

* Préparation des résultats : Les résultats sont retournés sous forme d'un DataFrame contenant les parfums similaires et leur probabilité associée.

Cette fonction permet ainsi de prédire les parfums qui pourraient plaire à un utilisateur en se basant sur ses préférences initiales.






* La seconde est la fonction 

```python
def prediction_embe(chaine):
	............................................

```


Cette fonction, nommée "prediction_embe", prend en entrée une chaîne de caractères représentant une description de parfum. Elle utilise un modèle d'embedding pré-entraîné pour représenter la description sous forme d'un vecteur. Ensuite, elle calcule la similarité cosinus entre ce vecteur et les vecteurs d'embedding de tous les parfums dans le jeu de données.

Voici un résumé des étapes effectuées par la fonction :

* Initialisation du modèle d'embedding : Le modèle d'embedding pré-entraîné est chargé.

* Représentation de la description : La description du parfum est convertie en un vecteur d'embedding à l'aide du modèle chargé.

* Calcul des similarités : La fonction calcule la similarité cosinus entre le vecteur d'embedding de la description donnée et les vecteurs d'embedding de tous les parfums dans le jeu de données.

* Tri des similarités : Les parfums sont classés par ordre de similarité décroissante par rapport à la description donnée.

* Préparation des résultats : Les résultats sont retournés sous forme d'un DataFrame contenant les noms des parfums similaires et leur probabilité associée.

Cette fonction permet ainsi de recommander des parfums similaires en se basant sur la similarité entre la description d'un parfum donné et les descriptions des parfums dans le jeu de données.


***
***

***

***
## Remarque
#### L'application dispose propose egalement une option de notation des suggestion, les notes obtenues peuvent etre utilisées pour entrainer un nouveau model basé sur du filtrage collaboratif
#### Cela peut permettre d'augmenter la précision  et la qualité de nos recommandations
***


***
## Utilisation de l'application

Suivre les Etape suivantes pour lancer l'application:

* Cloner l'application
* Ouvrir le projet cloner dans VScode 
* Lancer l'application dans le terminal via la commande **streamlit run app.py**

***

## EN CONCLUSION

En conclusion, notre projet de moteur de recommandation de parfum représente une avancée significative dans le domaine de la personnalisation des recommandations produits. Grâce à notre approche méthodique en trois phases, nous avons réussi à créer une solution robuste et adaptable qui répond aux besoins changeants de nos clients. Nous sommes impatients de continuer à développer et à améliorer notre moteur de recommandation dans le but de fournir une expérience client toujours plus exceptionnelle.

#### Les contributions et les remarques sont les bienvenues.

### Merci pour votre attention !!
***
