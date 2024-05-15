import streamlit as st
import pandas as pd
from fonction import prediction, prediction_embe
from dotenv import load_dotenv
import os
import config

from donnees import data_parfum, data_binaire



model = config.model
st.set_page_config(layout="wide")

st.title('Bienvenue sur AKIA PARFUM !') 

##################################################################################################
# Barre latérale pour les entrées
with st.sidebar:
    st.markdown("<h1>SAISISSEZ VOS INFORMATIONS</h1>", unsafe_allow_html=True)
    
    nombre = st.number_input(label='Nombre de parfums souhaités :', step=1, format='%d')
    nombre = int(nombre)
    
    
    parfums_prefere = st.multiselect(
        "Sélectionnez vos parfums préférés.",
        list(data_binaire.index)
    )
    
    
    details_rechercher = st.text_input("Décrivez le parfum de vos rêves.")
    
    parfums_detestes = st.multiselect(
        "Sélectionnez des parfums que vous n'aimez pas.",
        list(data_binaire.index)
    )
    

    
    if parfums_detestes:
        liste_deteste = list(prediction(parfums_detestes, data_binaire)[0:10].index) 
        liste_deteste.extend(parfums_detestes)
######################################################################################################
# Diviser la page en deux colonnes
col1, col2 = st.columns([1, 4])  

# Dans la colonne (col2), afficher les résultats
with col2:
    st.markdown("<h3>NOS SUGGESTIONS</h3>", unsafe_allow_html=True)
    parfums_suggeres = None
    p = 0  #la variable p sera utiliser dans la suite du code, elle permet de pouvoir noter les parfums apres les recommandation
    
    ####################################################################
    #EVALUATION DES DEUX MODELS ET PREDICTIONS
    
    if parfums_prefere:
        prediction_caracteristique = prediction(parfums_prefere, data_binaire)
        
    if details_rechercher:
        prediction_desciption = prediction_embe(details_rechercher, data_parfum, model)
        
    
       
        
    #################################################################### 
    #ELEMENTS A AFFICHES
    
    #####CAS 1 : Liste de parfums favoris et description du parfum de reve
    if parfums_prefere and details_rechercher:
        data = pd.concat([prediction_caracteristique, prediction_desciption])
        predictions = data.groupby(level=0)['probabilite'].mean()
        predictions = predictions.drop(parfums_prefere)
        
        if parfums_detestes:
            liste_deteste = list(prediction(parfums_detestes, data_binaire)[0:10].index)
            liste_deteste.extend(parfums_detestes)
            predictions = predictions.drop(liste_deteste)
            
        predictions = predictions.sort_values(ascending=False)
        parfums_suggeres = predictions[0:nombre]
        p = 1
        st.write(parfums_suggeres)
       
        
     ##### CAS 2 : description du parfum de reve    
    if not parfums_prefere and details_rechercher:
        if parfums_detestes:
            prediction_desciption = prediction_desciption.drop(liste_deteste)
        parfums_suggeres = prediction_desciption[0:nombre]
        p = 1
        st.write(parfums_suggeres)
        
        
    ##### CAS 3 : Liste de parfums favoris 
    if not details_rechercher and parfums_prefere:
        if parfums_detestes:
            prediction_caracteristique = prediction_caracteristique.drop(liste_deteste)
        parfums_suggeres = prediction_caracteristique[0:nombre]
        p = 1
        st.write(parfums_suggeres)
    if not details_rechercher and not parfums_prefere:
        st.write('Bienvenue ! Veuillez choisir les parfums que vous aimez ou décrire le parfum de vos rêves.')
        
    
    #############################################################################################

### NOTEZ NOS SUGGESTIONS 
liste = []
description_ = ''

with st.sidebar:
    st.markdown("<h1>Notez nos suggestions sur 10</h1>", unsafe_allow_html=True)
    if p == 1:
        form_counter = 0
        form_counter += 1
        with st.form(key=f'rating_form_{form_counter}'):
            parfum = st.selectbox("Choisir un parfum :", list(parfums_suggeres.index))
            note = st.number_input("Entrez une note :", min_value=1, max_value=10)
            nom = st.text_input("Entrer votre nom.")
            if parfum:
                if parfums_prefere :
                    liste = parfums_prefere
                    if not details_rechercher:
                        proba = parfums_suggeres.loc[parfum].values[0]
                        
                if details_rechercher:
                    description_ = details_rechercher
                    if not parfums_prefere:
                        proba = parfums_suggeres.loc[parfum].values[0]
                    
                #proba = parfums_suggeres.loc[parfum].values[0]
                
                if details_rechercher and  parfums_prefere:
                    proba = parfums_suggeres.loc[parfum]
                
            submitted = st.form_submit_button("Enregistrer la note")
            if submitted:
                with open("notes.txt", "a") as file:
                    file.write(f"{nom},{liste},{description_},{parfum},{proba},{note}\n")
                st.success("Note enregistrée avec succès !")
    else:
        st.write('En notant nos recommandations, vous contribuez à améliorer la qualité des suggestions qui vous sont proposées.')
