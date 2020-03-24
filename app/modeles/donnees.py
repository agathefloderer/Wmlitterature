from .. app import db

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
    femme_de_lettres = db.relationship("Femme_de_lettres", back_populates="oeuvres_principales")

class Oeuvres_principales(db.Model):
    __tablename__ = "oeuvres_principales"
    id_oeuvre = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text)
    date_premiere_pub = db.Column(db.Text)
    editeur = db.Column(db.Text)
    lieu_publication = db.Column(db.Text)
    nombre_pages = db.Column(db.Text)
    oeuvres_principales_id_femmme = (db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))

class Portrait(db.Model):
    id_portrait = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    url_portrait = db.Column(db.Text)
    nom_createur = db.Column(db.Text)
    prenom_createur = db.Column(db.Text)
    annee_realisation = db.Column(db.Text)
    techniques = db.Column(db.Text)
    lieu_conservation = db.Column(db.Text)
    portrait_id_femme = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))
    