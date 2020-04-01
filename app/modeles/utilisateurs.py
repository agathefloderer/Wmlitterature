from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import or_

from .. app import db, login

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    #Jointure
    authorships = db.relationship("Authorship", back_populates="user")

    def get_id(self):
        """
        Fonction permettant de retourner l'identifiant de l'objet en cours d'utilisation
        :returns: identifiant de l'utilisateur
        :rtype: int
        """ 
        return (self.user_id)

    @staticmethod
    def identification(login, motdepasse):
        """ Identifie un utilisateur. Si cela fonctionne, renvoie les donnees de lutilisateurs.

        :param login: Login de l'utilisateur
        :param motdepasse: Mot de passe envoye par lutilisateur
        :returns: Si reussite, donnees de lutilisateur. Sinon None
        :rtype: User or None
        """
        utilisateur = User.query.filter(User.user_login == login).first()
        if utilisateur and check_password_hash(utilisateur.user_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """ Cree un compte utilisateur-rice. Retourne un tuple (booleen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi dune liste derreur
        Sinon, elle renvoie True suivi de la donnee enregistree

        :param login: Login de lutilisateur-rice
        :param email: Email de lutilisateur-rice
        :param nom: Nom de lutilisateur-rice
        :param motdepasse: Mot de passe de lutilisateur-rice (Minimum 6 caracteres)

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

        # On cree un utilisateur
        utilisateur = User(
            user_nom=nom,
            user_login=login,
            user_email=email,
            user_password=generate_password_hash(motdepasse)
        )

        try:
            # On l'ajoute au transport vers la base de donnees
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilise

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.user_id

@login.user_loader
#  fonction qui permet de recuperer un utilisateur en fonction de son identifiant
def trouver_utilisateur_via_id(identifiant):
    return User.query.get(int(identifiant))
