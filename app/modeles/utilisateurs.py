#Mise en place de la classe User. Mise en place des fonctionnalités de création d'un compte utilisateur et de la connexion à l'application

from werkzeug.security import generate_password_hash, check_password_hash
#On importe les outils generate_password_hash et check_password_hash depuis werkzeug pour hascher les mots de passe des utilisateurs
from flask_login import UserMixin
#La classe user doit implémenter les propriétés et méthodes suivantes : is_authenticated, is_active, is_anonymous, get_id(identifier)
#Pour facilier l'implémentation d'une classe user, on peut utiliser UserMixin qui fournit des implémentations par défaut pour toutes ces propriétés et méthodes.
from sqlalchemy import or_
#Grâce à cette commande, on peut utiliser l'opérateur 'or' dans les fonctions destiner à requêter la base de données.


from .. app import db, login
#On importe notre base de données depuis app.py, stockée dans la variable db. On importe également login, destiné à la gestion des utilisateur-rice-s

#On crée notre modèle 'User'.
class User(UserMixin, db.Model):
#En ajoutant UserMixin à db.Model, on donne à python l'information que User est à la fois un UserMixin et un db.Model
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    #Jointure
    author_femme_de_lettres = db.relationship("Authorship_femme_de_lettres", back_populates="user_femme_de_lettres")
    author_oeuvres_principales = db.relationship("Authorship_oeuvres_principales", back_populates="user_oeuvres_principales")
    author_portrait = db.relationship("Authorship_portrait", back_populates="user_portrait")


    def get_id(self):
        """
        Fonction permettant de retourner l'identifiant de l'objet en cours d'utilisation
        :returns: identifiant de l'utilisateur
        :rtype: int
        """ 
        return (self.user_id)

    @staticmethod
    #@staticmethod permet d'intérafur avec une classe pour un objet qui n'existe pas encore.
    def identification(login, motdepasse):
        """ Identifie un utilisateur. Si cela fonctionne, renvoie les données de l'utilisateur.

        :param login: Login de l'utilisateur
        :param motdepasse: Mot de passe envoyé par l'utilisateur
        :returns: Si réussite, données de l'utilisateur. Sinon None
        :rtype: User or None
        """
        utilisateur = User.query.filter(User.user_login == login).first()
        if utilisateur and check_password_hash(utilisateur.user_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """ Crée un compte utilisateur-rice. Retourne un tuple (booleen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste derreur
        Sinon, elle renvoie True suivi des donnée enregistrée

        :param login: Login de l'utilisateur-rice
        :param email: Email de l'utilisateur-rice
        :param nom: Nom de l'utilisateur-rice
        :param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)

        """
        erreurs = []
        if not login:
            erreurs.append("le login fourni est vide")
        if not email:
            erreurs.append("l'email fourni est vide")
        if not nom:
            erreurs.append("le nom fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("le mot de passe fourni est vide ou trop court")

        # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = User.query.filter(
            db.or_(User.user_email == email, User.user_login == login)
        ).count()
        if uniques > 0:
            erreurs.append("l'email ou le login sont déjà inscrits dans notre base de données")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur
        utilisateur = User(
            user_nom=nom,
            user_login=login,
            user_email=email,
            user_password=generate_password_hash(motdepasse)
        )

        #On ouvre un double bloc "try-except" afin de gérer les erreurs
        try:
            # On l'ajoute au transport vers la base de donnees
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
        #Exécution de except uniquement si une erreur apparaît. 
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.user_id

@login.user_loader
#  fonction qui permet de récuperer un utilisateur en fonction de son identifiant
def trouver_utilisateur_via_id(identifiant):
    return User.query.get(int(identifiant))
