# Utilisez une image de base avec Python
FROM python:3.10.12

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier des dépendances (requirements.txt) dans le conteneur
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez tout le contenu du répertoire local dans le répertoire de travail du conteneur
COPY . .

# Commande pour exécuter l'application Streamlit quand le conteneur démarre
CMD ["streamlit", "run", "app.py"]