import pandas as pd

data_parfum = pd.read_pickle("data.pkl")  #Donner des description et des vecteurs de embedding

data_binaire = pd.read_csv('donnee_binaire.csv', index_col='nom_parfum')  ## donnee des carracteristiques avec des 0 et 1


