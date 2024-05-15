import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
import os
import google.generativeai as genai
import config
from dotenv import load_dotenv

load_dotenv()



def prediction(liste_parfums, df):
    
    """
    Cette fonction effectue une prédiction de recommandation de parfums basée sur la similarité de Jaccard.

    Elle prend en entrée une liste de parfums aimés par un utilisateur,
    calcule un nouveau profil utilisateur en agrégeant les embeddings correspondants à ces parfums,
    puis calcule la similarité de Jaccard entre ce nouveau profil utilisateur et les autres profils de parfums.
    Enfin, elle retourne les parfums recommandés triés par ordre décroissant de similarité de Jaccard.

    Args:
        liste_parfums (list): La liste des parfums aimés par l'utilisateur.
        df (pandas.DataFrame): Le DataFrame contenant les embeddings des parfums.

    Returns:
        pandas.DataFrame: Un DataFrame contenant les parfums recommandés et leur probabilité de similarité.

    Raises:
        ValueError: Si la liste des parfums est vide ou si le DataFrame des embeddings est vide.
        KeyError: Si la colonne 'Embeddings' n'est pas présente dans le DataFrame.
    """

    new_user = np.zeros(df.shape[1])  # Initialisation d'une série de zéros pour un nouveau profil utilisateur

    # Calcul du nouveau profil utilisateur
    for parfum in liste_parfums:
        new_user += df.loc[parfum]
    new_user[new_user > 1] = 1 
    df.loc['new_user'] = new_user
    
    
    # Calcul de la similarité de Jaccard
    jaccard_distances = pdist(df.values, metric='jaccard')
    jaccard_similarity_array = 1 - squareform(jaccard_distances)
    jaccard_similarity_df = pd.DataFrame(jaccard_similarity_array, index=df.index, columns=df.index)
    
    # Récupération des similarités pour le nouvel utilisateur
    jaccard_similarity_series = jaccard_similarity_df.loc['new_user']
    
    # Suppression des parfums d'entrée
    jaccard_similarity_series = jaccard_similarity_series.drop(list(liste_parfums))
    
    # Trier les valeurs de similarité de la plus élevée à la plus basse
    ordered_similarities = jaccard_similarity_series.sort_values(ascending=False)
    
    # Supprimer le profil utilisateur après la prédiction
    df = df.drop(index='new_user')
    
    dict_of_dicts = ordered_similarities.to_dict()
    data = pd.DataFrame(list(dict_of_dicts.values()), index=list(dict_of_dicts.keys()), columns=['probabilite'])
    return data.iloc[1:]




 


ma_cle = os.getenv('gemini_key')
genai.configure(api_key=ma_cle)
model = config.model

def calcul_emb(description_utilisateur, model):
    """
    Calcule l'embedding d'une description utilisateur en utilisant un modèle spécifié.
    Args:
        description_utilisateur (str): La description de l'utilisateur pour laquelle l'embedding doit être calculé.
        model (str): Le modèle utilisé pour calculer l'embedding.
    Returns:
        numpy.ndarray: L'embedding de la description utilisateur, représenté sous forme de tableau NumPy.
        
    Raises:
        ValueError: Si le modèle spécifié n'est pas valide ou si la description utilisateur est vide.
    """

    embedding = genai.embed_content(model=model,
                                    content=description_utilisateur,
                                    task_type="retrieval_document")
    return np.array(embedding["embedding"]).reshape(1, -1)




def calcul_similarite(embedding_utilisateur, embedding):
    """
    Calcule la similarité cosinus entre deux vecteurs d'embeddings.
    Args:
        embedding_utilisateur (numpy.ndarray): L'embedding de la desciption de l'utilisateur, représenté sous forme de tableau NumPy.
        embedding (numpy.ndarray): L'embedding à comparer avec l'embedding de l'utilisateur, représenté sous forme de tableau NumPy.
    Returns:
        float: La similarité cosinus entre les deux embeddings.
        
    Raises:
        ValueError: Si l'une des embeddings n'est pas valide ou si elles n'ont pas la même dimension.
    """
    embedding = np.array(embedding).reshape(1, -1)  # Convertir en tableau NumPy avant de remodeler
    return cosine_similarity(embedding, np.array(embedding_utilisateur).reshape(1, -1))[0][0]



def prediction_embe(description_utilisateur, df, model):
    """
    Cette fonction effectue une prédiction basée sur l'embedding de la description utilisateur.

    Elle calcule l'embedding de la description utilisateur en utilisant le modèle spécifié,
    puis calcule la similarité cosinus entre cet embedding et les embeddings stockés dans le DataFrame.
    Enfin, elle classe les résultats par ordre décroissant de similarité.

    Args:
        description_utilisateur (str): La description de l'utilisateur pour laquelle la prédiction doit être effectuée.
        df (pandas.DataFrame): Le DataFrame contenant les embeddings des parfums et d'autres informations.
        model (str): Le modèle utilisé pour calculer l'embedding de la description utilisateur.

    Returns:
        pandas.DataFrame: Un DataFrame contenant les noms des parfums et les probabilités de similarité, classés par ordre décroissant de similarité.

    Raises:
        ValueError: Si le modèle spécifié n'est pas valide ou si la description utilisateur est vide.
        KeyError: Si la colonne 'Embeddings' n'est pas présente dans le DataFrame.
    """
    vecteur_utilisateur = calcul_emb(description_utilisateur, model)
    df['probabilite'] = df['Embeddings'].map(lambda emb: calcul_similarite(emb, vecteur_utilisateur))
    data = df[['nom_parfum', 'probabilite']]
    data.set_index('nom_parfum', inplace=True)
    data = data.sort_values(by='probabilite', ascending=False)
    return data  

