# Ce fichier contient le code principal du serveur Flask pour l'application NiortConnect (**Projet SNIR2**).
# Il expose des API RESTful pour gérer la base de données **NiortConnectBDD.db**.
# Auteurs: El Guennouni Rim (SNIR2)
# Profs: Mr David Salle, Mme Candillier Sanae

import socket
from flask import Flask, jsonify, request, render_template, session
import sqlite3
import logging


# Configuration du journal pour afficher les messages de niveau DEBUG et supérieur
logging.basicConfig(level=logging.DEBUG)

# Création de l'instance Flask
app = Flask(__name__)
# Définition du chemin d'accès à la base de données
db_path = 'NiortConnectBDD.db'


@app.route('/')
def index():
    """
    **Page d'accueil**

    Cette fonction gère la route `/` et retourne un message indiquant que c'est la page d'accueil.

    :return: Un message "Ceci est la page d'accueil".
    """
    return "Ceci est la page d'accueil"


def get_db_connection():
    """Etablit une connexion à la base de données et la retourne."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Route pour la connexion
@app.route('/connexion', methods=['POST'])
def login():
    login_data = request.json
 
    if not login_data or ('email' not in login_data and 'pseudo' not in login_data) or 'password' not in login_data:
        return jsonify({'error': 'Veuillez fournir un email/pseudo et un mot de passe valide.'}), 400

    email = login_data.get('email')
    pseudo = login_data.get('pseudo')
    password = login_data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    if email:
        cur.execute('SELECT * FROM Utilisateur WHERE email = ?', (email,))
    elif pseudo:
        cur.execute('SELECT * FROM Utilisateur WHERE pseudo = ?', (pseudo,))
    else:
        conn.close()
        return jsonify({'error': 'Veuillez fournir un email/pseudo valide.'}), 400

    utilisateur = cur.fetchone()
    conn.close()

    if utilisateur and utilisateur['password'] == password:
        session['user_id'] = utilisateur['id']
        return jsonify({'message': 'Connexion réussie.'}), 200
    else:
        return jsonify({'error': 'Identifiants invalides.'}), 401


# Route pour l'inscription
@app.route('/inscription', methods=['POST'])
def register():
    register_data = request.json

    if not register_data or 'email' not in register_data or 'pseudo' not in register_data or 'password' not in register_data:
        return jsonify({'error': 'Veuillez fournir un email, un pseudo et un mot de passe.'}), 400

    email = register_data.get('email')
    pseudo = register_data.get('pseudo')
    password = register_data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    # Vérifier si l'utilisateur avec cet email ou pseudo existe déjà
    cur.execute('SELECT * FROM Utilisateur WHERE email = ? OR pseudo = ?', (email, pseudo))
    existing_user = cur.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'L\'utilisateur avec cet email ou pseudo existe déjà.'}), 409

    # Insérer le nouvel utilisateur dans la base de données
    cur.execute('INSERT INTO Utilisateur (email, pseudo, password, fkRole, fkProfil) VALUES (?, ?, ?, ?, ?)',
                (email, pseudo, password, 1, 1))  # Ici, vous devez définir fkRole et fkProfil en fonction de votre logique
    conn.commit()
    conn.close()

    return jsonify({'message': 'Inscription réussie.'}), 201

@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    """Récupère tous les utilisateurs et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Utilisateur')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    utilisateurs = [dict(row) for row in rows]

    conn.close()
    return jsonify(utilisateurs)


@app.route('/utilisateurs/<int:id>', methods=['GET'])
def get_utilisateur(id):
    """Récupère l'utilisateur avec l'ID spécifié et le renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Utilisateur WHERE id = ?', (id,))
    utilisateur_row = cur.fetchone()  # Obtenir la ligne de l'utilisateur

    if utilisateur_row:
        # Convertir la ligne de l'utilisateur en un dictionnaire
        utilisateur_dict = dict(utilisateur_row)
        conn.close()
        return jsonify(utilisateur_dict)
    else:
        conn.close()
        return jsonify({'message': 'Utilisateur non trouvé'}), 404


@app.route('/commentaires', methods=['GET'])
def get_commentaires():
    """Récupère tous les commentaires et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Commentaire')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    commentaires = [dict(row) for row in rows]

    conn.close()
    return jsonify(commentaires)

@app.route('/publicationsCm', methods=['GET'])
def get_publications_with_comments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            p.id AS publication_id, 
            p.titre, 
            p.contenu AS publication_contenu, 
            p.categorie, 
            p.datePublication AS publication_date, 
            u.pseudo AS utilisateur_pseudo, 
            c.id AS commentaire_id, 
            c.contenu AS commentaire_contenu, 
            cu.pseudo AS commentaire_auteur
        FROM 
            Publication p
        JOIN 
            Utilisateur u ON p.fkUtilisateur = u.id
        LEFT JOIN 
            Commentaire c ON p.id = c.fkPublication
        LEFT JOIN 
            Utilisateur cu ON c.fkUtilisateur = cu.id
        ORDER BY 
            p.datePublication DESC
    ''')
    
    rows = cur.fetchall()
    conn.close()

    publications = {}
    
    for row in rows:
        pub_id = row['publication_id']
        if pub_id not in publications:
            publications[pub_id] = {
                'pseudo': row['utilisateur_pseudo'],
                'titre': row['titre'],
                'message': row['publication_contenu'],
                'date_publication': row['publication_date'],
                'nombre_vote': 5,  # Remplacer par la logique appropriée
                'categorie': row['categorie'],
                'commentaire': []
            }
        
        if row['commentaire_id']:
            publications[pub_id]['commentaire'].append({
                'auteur': row['commentaire_auteur'],
                'contenu': row['commentaire_contenu']
            })
    
    return jsonify(list(publications.values()))


@app.route('/commentaires/contenu', methods=['GET'])
def get_contenu():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT contenu FROM Commentaire')
    rows = cur.fetchall()

    # Récupérer uniquement le contenu des commentaires
    contenu_commentaires = [row['contenu'] for row in rows]

    conn.close()
    return jsonify(contenu_commentaires)


@app.route('/ecoles', methods=['GET'])
def get_Ecoles():
    """Récupère tous les écoles et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Ecole')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    ecoles = [dict(row) for row in rows]

    conn.close()
    return jsonify(ecoles)


@app.route('/etats', methods=['GET'])
def get_Etats():
    """Récupère tous les états et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Etat')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    etats = [dict(row) for row in rows]

    conn.close()
    return jsonify(etats)


@app.route('/profils', methods=['GET'])
def get_Profils():
    """Récupère tous les profils et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Profil')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    profils = [dict(row) for row in rows]

    conn.close()
    return jsonify(profils)


@app.route('/publications/last', methods=['GET'])
def get_Publications():
    """Récupère les dernières publications et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            Utilisateur.pseudo AS pseudo, 
            Publication.*
        FROM 
            Publication 
        JOIN 
            Utilisateur ON Publication.fkUtilisateur = Utilisateur.id
        Where 
            fkEtat = 3 
        ORDER BY 
            Publication.datePublication DESC
        LIMIT 2
    ''')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    publications = []
    for row in rows:
        publication = {
            'pseudo': row['pseudo'],
            'titre': row['titre'],
            'message': row['contenu'],
            'date_publication': row['datePublication'],  # Convertir la date en format ISO 8601 si nécessaire
            'nombre_vote': 5,  # Par exemple, à remplacer par la logique de votre application
            'categorie': row['categorie'],
            'commentaire': []  # Liste vide, à remplir avec la logique de récupération des commentaires
        }
        publications.append(publication)

    conn.close()
    return jsonify(publications)


@app.route('/publications/new', methods=['POST'])
def create_publication():
    logging.debug(f"Chemin de la requête: {request.path}, Méthode: {request.method}, Content-Type: {request.content_type}")
    logging.debug(f"Données de la requête: {request.data}")
    
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type doit être application/json'}), 400
    
    new_publication = request.json
    if new_publication is None:
        return jsonify({'error': 'Données JSON invalides'}), 400

    logging.debug(f"Données JSON analysées: {new_publication}")
    titre = new_publication.get('titre')
    message = new_publication.get('message')
    categorie = new_publication.get('categorie')

    if not titre or not message or not categorie:
        return jsonify({'error': 'Les champs titre, message et categorie sont requis.'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Publication (titre, contenu, categorie, fkUtilisateur ,datePublication) VALUES (?, ?, ?, ?,datetime('now'))",
                    (titre, message, categorie, 1))  # Remplacer '1' par l'ID utilisateur approprié
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de l'insertion dans la base de données: {e}")
        return jsonify({'error': 'Erreur lors de l\'insertion dans la base de données'}), 500
    finally:
        conn.close()
    
    return jsonify({'message': 'Publication créée avec succès.'}), 201







@app.route('/publications/categorie/<categorie>', methods=['GET'])
def get_publications_by_category(categorie):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Publication WHERE categorie = ?', (categorie,))
    rows = cur.fetchall()

    publications = [dict(row) for row in rows]

    conn.close()

    return jsonify(publications)


@app.route('/roles', methods=['GET'])
def get_Roles():
    """Récupère tous les rôles et les renvoie en JSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Role')
    rows = cur.fetchall()

    # Convertir les objets Row en dictionnaires
    roles = [dict(row) for row in rows]

    conn.close()
    return jsonify(roles)

# Lancement de l'application Flask en mode debug
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
