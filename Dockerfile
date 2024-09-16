# Utiliser une image de base Python 3.9 slim
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis dans le conteneur
COPY requirements.txt .
COPY app.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application Flask écoute
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "./app.py"]
