from .. app import db

import datetime

class Femme_de_lettres(db.Model):
#On cree notre modele Femme_de_lettres. Les modeles permettent de generer automatiquement des requetes.
    id_femme = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # On enregistre ensuite les differents champs du modele.
    nom_naissance = db.Column(db.Text)
    prenom_naissance = db.Column(db.Text)
    nom_auteur = db.Column(db.Text)
    prenom_auteur = db.Column(db.Text)
    date_naissance = db.Column(db.Text)
    lieu_naissance = db.Column(db.Text)
    date_mort = db.Column(db.Text)
    lieu_mort = db.Column(db.Text)
    pseudonyme = db.Column(db.Text)
    #Jointures
    oeuvres = db.relationship('Oeuvres_principales', backref='romanciere')
    portraits = db.relationship('Portrait', backref='romanciere')
    authorships = db.relationship("Authorship", back_populates='femme_de_lettres')

    @staticmethod
    def create_person(new_nom_naissance, new_prenom_naissance, new_nom_auteur, new_prenom_auteur, new_date_naissance, new_lieu_naissance, new_date_mort, new_lieu_mort, new_pseudonyme):
        """
        Fonction qui permet de creer une nouvelle romanciere dans la base de donnees (ajout rendu possible par un utilisateur)
        :param new_nom_naissance: nom de famille de naissance de la romanciere (str)
        :param new_prenom_naissance: prenom de naissance de la romanciere (str)
        :param new_nom_auteur: nom dauteur de la romanciere (str)
        :param new_prenom_auteur: prenom dauteur de la romanciere (str)
        :param new_date_naissance: date de naissance de la romanciere (str)
        :param new_lieu_naissance: lieu de naissance (ville ou village) de la romanciere (str)
        :param new_date_mort: date de mort de la romanciere (str)
        :param new_lieu_mort: lieu de mort (ville ou village) de la romanciere (str)
        :param new_pseudonyme: pseudonyme de la romanciere (str)
        :return:
        """
        erreurs = []
        if not new_nom_auteur:
            erreurs.append("Le champ 'nom d'auteur' est obligatoire.")
        if not new_prenom_auteur:
            erreurs.append("Le champ 'prénom d'auteur' est obligatoire.")
        #Les autres donnees ne sont pas forcement disponibles et sont donc optionnelles.
        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        # Si non, on ajoute une nouvelle entree femme_de_lettres dans la table femme_de_lettres avec les champs correspondant aux paramètres du modèle
        new_femme_de_lettres = Femme_de_lettres(
            nom_naissance=new_nom_naissance,
            prenom_naissance=new_prenom_naissance,
            nom_auteur=new_nom_auteur,
            prenom_auteur=new_prenom_auteur,
            date_naissance=new_date_naissance,
            lieu_naissance=new_lieu_naissance,
            date_mort=new_date_mort,
            lieu_mort=new_lieu_mort,
            pseudonyme=new_pseudonyme)

        try:
             # ajout de la romanciere a la base de donnees
            db.session.add(new_femme_de_lettres)
            db.session(commit)
           

            return True, new_femme_de_lettres
        except Exception as erreur_creation:
            return False, [str(erreur_creation)]

class Oeuvres_principales(db.Model):
    __tablename__ = "oeuvres_principales"
    id_oeuvre = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text)
    date_premiere_pub = db.Column(db.Text)
    editeur = db.Column(db.Text)
    lieu_publication = db.Column(db.Text)
    nombre_pages = db.Column(db.Text)
    oeuvres_principales_id_femmme = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))

class Portrait(db.Model):
    __tablename__="portrait"
    id_portrait = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    url_portrait = db.Column(db.Text)
    nom_createur = db.Column(db.Text)
    prenom_createur = db.Column(db.Text)
    annee_realisation = db.Column(db.Text)
    techniques = db.Column(db.Text)
    lieu_conservation = db.Column(db.Text)
    portrait_id_femme = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_femme_de_lettres_id = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    #default peut prendre le nom d'une fonction. On necrit pas la fonction directement car on ne veut pas que la fonction sexecute au moment ou on redige notre script. 
    user = db.relationship("User", back_populates="authorships")
    femme_de_lettres = db.relationship("Femme_de_lettres", back_populates="authorships")

    