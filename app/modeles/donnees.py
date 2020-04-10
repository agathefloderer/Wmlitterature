#Mise en place des classes de la base de données

from .. app import db
#On importe notre base de données depuis app.py, stockée dans la variable db
import datetime

                                                    ####Femme_de_lettres####

class Femme_de_lettres(db.Model):
#On crée notre modèle Femme_de_lettres. Les modèles permettent de générer automatiquement des requêtes.
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
    #Jointures. 
    #Relations many to one identifiées par des clefs étrangères du côté de la relation simple.
    oeuvres = db.relationship('Oeuvres_principales', cascade="all,delete", backref='romanciere')
    portraits = db.relationship('Portrait', cascade="all,delete", backref='romanciere')
    authorships_femme_de_lettres = db.relationship("Authorship_femme_de_lettres", back_populates='femme_de_lettres_femme_de_lettres')

    @staticmethod
    #@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

    def creer_romanciere(new_nom_naissance, new_prenom_naissance, new_nom_auteur, new_prenom_auteur, new_date_naissance, new_lieu_naissance, new_date_mort, new_lieu_mort, new_pseudonyme):
        """
        Fonction qui permet de créer une nouvelle romancière et de l'ajouter la base de données (ajout rendu possible par un utilisateur)
        :param new_nom_naissance: nom de famille de naissance de la romancière
        :param new_prenom_naissance: prénom de naissance de la romancière
        :param new_nom_auteur: nom d'auteur de la romancière
        :param new_prenom_auteur: prénom d'auteur de la romancière 
        :param new_date_naissance: date de naissance de la romancière
        :param new_lieu_naissance: lieu de naissance (ville ou village) de la romancière
        :param new_date_mort: date de mort de la romancière
        :param new_lieu_mort: lieu de mort (ville ou village) de la romancière
        :param new_pseudonyme: pseudonyme de la romancière 
        :type param: string
        :returns: tuple (booléen, liste/objet)
         S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet créé (ici une romancière).
        """

        #On crée une liste vide pour les erreurs
        erreurs = []

        #On vérifie que la romancière que l'utilisateur veut ajouter n'existe pas déjà dans la base.
        new_femme_de_lettres = Femme_de_lettres.query.filter(db.and_(Femme_de_lettres.nom_auteur == new_nom_auteur, Femme_de_lettres.prenom_auteur == new_prenom_auteur)).count()
        if new_femme_de_lettres > 0:
            erreurs.append("La romancière existe déjà dans la base de données")

        #On vérifie que l'utilisateur complète au moins deux champs de données considérés comme essentiels
        if not new_nom_auteur:
            erreurs.append("le champ 'nom d'auteur' est obligatoire")
        if not new_prenom_auteur:
            erreurs.append("le champ 'prénom d'auteur' est obligatoire")
        #Les autres données ne sont pas forcément disponibles et sont donc optionnelles.
        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        #On vérifie que la longueur des caractères de la date ne dépasse pas la limite de 10 (format MM-JJ-AAAA)
        if new_date_naissance:
            if not len(new_date_naissance) == 10 or not len(new_date_mort) == 10:
                erreurs.append("Les dates doivent faire 10 caractères. Format MM-JJ-AAAA demandé.")
            if len(erreurs) > 0:
                return False, erreurs

         # Si on a au moins une erreurs, on affiche un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        # S'il n'y a pas d'erreur, on ajoute une nouvelle entrée dans la table femme_de_lettres avec les champs correspondant aux paramètres du modèle
        created_romanciere = Femme_de_lettres(
            nom_naissance=new_nom_naissance,
            prenom_naissance=new_prenom_naissance,
            nom_auteur=new_nom_auteur,
            prenom_auteur=new_prenom_auteur,
            date_naissance=new_date_naissance,
            lieu_naissance=new_lieu_naissance,
            date_mort=new_date_mort,
            lieu_mort=new_lieu_mort,
            pseudonyme=new_pseudonyme)

        #On ouvre un double bloc "try-except" afin de gérer les erreurs
        try:
             # On ajoute la romanciere a la base de donnees
            db.session.add(created_romanciere)
            db.session.commit()
           

            return True, new_femme_de_lettres
        #Exécution de except uniquement si une erreur apparaît. 
        except Exception as erreur_creation:
            return False, [str(erreur_creation)]

    @staticmethod
    #@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

    def modifier_romanciere(Id_femme, Nom_naissance, Prenom_naissance, Nom_auteur, Prenom_auteur, Date_naissance, Lieu_naissance, Date_mort, Lieu_mort, Pseudonyme):
        """
        Fonction qui permet de modifier les informations d'une romancière dans la base de données (modifications rendues possibles par un utilisateur.rice).
        :param Id_femme: identifiant numérique de la romancière
        :param Nom_naissance: nom de famille de naissance de la romancière
        :param Prenom_naissance: prénom de naissance de la romancière
        :param Nom_auteur: nom d'auteur de la romancière
        :param Prenom_auteur: prénom dauteur de la romancière 
        :param Date_naissance: date de naissance de la romancière
        :param Lieu_naissance: lieu de naissance (ville ou village) de la romancière
        :param Date_mort: date de mort de la romancière 
        :param Lieu_mort: lieu de mort (ville ou village) de la romancière 
        :param Pseudonyme: pseudonyme de la romancière 
        :type Id_femme: integer
        :type Nom_naissance, Prenom_naissance, Nom_auteur, Prenom_auteur, Date_naissance, Lieu_naissance, Date_mort, Lieu_mort, Pseudonyme: string
        :returns: tuple (booléen, liste/objet)
         S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet mis à jour (ici une romanciere).
        """

        #On crée une liste vide pour les erreurs
        erreurs=[]

        #On vérifie que l'utilisateur complète au moins deux champs de données considérés comme essentiels
        if not Nom_auteur:
            erreurs.append("le champ 'nom d'auteur' est obligatoire")
        if not Prenom_auteur:
            erreurs.append("le champ 'prénom d'auteur' est obligatoire")
        #Les autres données ne sont pas forcément disponibles et sont donc optionnelles.
        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        #On récupère une romancière dans la base grâce à son identifiant
        update_femme_de_lettres = Femme_de_lettres.query.get(Id_femme)

        #On vérifie que l'utilisateur-trice modifie au moins un champ

        if update_femme_de_lettres.nom_naissance == Nom_naissance \
                and update_femme_de_lettres.prenom_naissance == Prenom_naissance \
                and update_femme_de_lettres.nom_auteur == Nom_auteur \
                and update_femme_de_lettres.prenom_naissance == Nom_naissance \
                and update_femme_de_lettres.date_naissance == Date_naissance \
                and update_femme_de_lettres.lieu_naissance == Lieu_naissance \
                and update_femme_de_lettres.date_mort == Date_mort \
                and update_femme_de_lettres.lieu_mort == Lieu_mort \
                and update_femme_de_lettres.pseudonyme == Pseudonyme :
            erreurs.append("Aucune modification n'a été réalisée")

        if len(erreurs) > 0:
            return False, erreurs

        #On vérifie que la longueur des caractères de la date ne dépasse pas la limite de 10 (format MM-JJ-AAAA)
        if Date_naissance:
            if not len(Date_naissance) == 10 or not len(Date_mort) == 10:
                erreurs.append("Les dates doivent faire 10 caractères. Format MM-JJ-AAAA demandé.")
            if len(erreurs) > 0:
                return False, erreurs

         # Si on a au moins une erreurs, on affiche un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        #S'il n'y a pas d'erreurs, on met à jour les données de la romancière :
        else :
            update_femme_de_lettres.nom_naissance=Nom_naissance
            update_femme_de_lettres.prenom_naissance=Prenom_naissance
            update_femme_de_lettres.nom_auteur=Nom_auteur
            update_femme_de_lettres.prenom_auteur=Prenom_auteur
            update_femme_de_lettres.date_naissance=Date_naissance
            update_femme_de_lettres.lieu_naissance=Lieu_naissance
            update_femme_de_lettres.date_mort=Date_mort
            update_femme_de_lettres.lieu_mort=Lieu_mort
            update_femme_de_lettres.pseudonyme=Pseudonyme

        #On ajoute un bloc "try-except" afin de "gérer" les erreurs
        try:
            # On ajoute la romanciere a la base de donnees
            db.session.add(update_femme_de_lettres)
            db.session.commit()

            return True, update_femme_de_lettres

        #Exécution de except uniquement si une erreur apparaît. 
        except Exception as erreur:
            return False, [str(erreur)]                     


    @staticmethod
    def supprimer_romanciere(Id_femme, Nom_naissance, Prenom_naissance, Nom_auteur, Prenom_auteur, Date_naissance, Lieu_naissance, Date_mort, Lieu_mort, Pseudonyme):
        """
        Fonction qui permet de supprimer la notice d'une romancière.
        :param Id_femme: identifiant numérique de la romancière
        :param Nom_naissance: nom de famille de naissance de la romanciere
        :param Prenom_naissance: prenom de naissance de la romanciere
        :param Nom_auteur: nom d'auteur de la romancière
        :param Prenom_auteur: prénom d'auteur de la romancière 
        :param Date_naissance: date de naissance de la romancière
        :param Lieu_naissance: lieu de naissance (ville ou village) de la romancière
        :param Date_mort: date de mort de la romancière 
        :param Lieu_mort: lieu de mort (ville ou village) de la romancière 
        :param Pseudonyme: pseudonyme de la romancière 
        :type Id_femme: integer
        :type Nom_naissance, Prenom_naissance, Nom_auteur, Prenom_auteur, Date_naissance, Lieu_naissance, Date_mort, Lieu_mort, Pseudonyme: string
        :returns: booleens
        """

        #On récupère une romancière dans la base grâce à son identifiant
        delete_femme_de_lettres = Femme_de_lettres.query.get(Id_femme)

        delete_femme_de_lettres.id_femme = Id_femme
        delete_femme_de_lettres.nom_naissance=Nom_naissance
        delete_femme_de_lettres.prenom_naissance=Prenom_naissance
        delete_femme_de_lettres.nom_auteur=Nom_auteur
        delete_femme_de_lettres.prenom_auteur=Prenom_auteur
        delete_femme_de_lettres.date_naissance=Date_naissance
        delete_femme_de_lettres.lieu_naissance=Lieu_naissance
        delete_femme_de_lettres.date_mort=Date_mort
        delete_femme_de_lettres.lieu_mort=Lieu_mort
        delete_femme_de_lettres.pseudonyme=Pseudonyme

        #On ajoute un bloc "try-except" afin de "gérer" les erreurs
        try:
            #On supprime la romancière de la base de données
            db.session.delete(delete_femme_de_lettres)
            db.session.commit()
            return True, delete_femme_de_lettres

        except Exception as erreur:
            return False, [str(erreur)]

                                                    ####Oeuvres_principales#####

class Oeuvres_principales(db.Model):
#On crée notre modèle Oeuvres_principales.
    __tablename__ = "oeuvres_principales"
    id_oeuvre = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text)
    date_premiere_pub = db.Column(db.Text)
    editeur = db.Column(db.Text)
    lieu_publication = db.Column(db.Text)
    nombre_pages = db.Column(db.Text)
    resume = db.Column(db.Text)
    #Jointure
    oeuvres_principales_id_femmme = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))
    authorships_oeuvres_principales = db.relationship("Authorship_oeuvres_principales", back_populates="oeuvres_principales_oeuvres_principales")

    @staticmethod
    #@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

    def creer_oeuvres_principales(new_titre, new_date_premiere_pub, new_editeur, new_lieu_publication, new_nombre_pages, new_resume, id_femme):
        """
        Fonction qui permet de créer une nouvelle oeuvre et de l'ajouter à la base de données (ajout rendu possible par un utilisateur)
        :param new_titre: titre de l'oeuvre
        :param new_date_premiere_pub: date de la première publication de l'oeuvre
        :param new_editeur: nom et prénom de l'éditeur
        :param new_lieu_publication: ville où a été publiée l'oeuvre
        :param new_nombre_pages: nombre de pages de l'ouvrage
        :type param: string
        :returns: tuple (booléen, liste/objet)
         S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet créé (ici new_oeuvres_principales).
        """

        #On crée une liste vide pour les erreurs
        erreurs=[]

         #On vérifie que l'utilisateur complète au moins un champ de données considéré comme essentiel
        if not new_titre:
            erreurs.append("le champ 'titre' est obligatoire")
        #Les autres données ne sont pas forcément disponibles et sont donc optionnelles.


        if new_date_premiere_pub:
            if not len(new_date_premiere_pub) == 4:
                erreurs.append("La date de l'année de réalisation  doit faire 4 caractères. Format AAAA demandé.")
            if len(erreurs) > 0:
                return False, erreurs


        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        # S'il n'y a pas d'erreur, on ajoute une nouvelle entrée dans la table oeuvres_principales avec les champs correspondant aux paramètres du modèle.
        created_oeuvres_principales = Oeuvres_principales(
            titre = new_titre,
            date_premiere_pub = new_date_premiere_pub,
            editeur = new_editeur,
            lieu_publication = new_lieu_publication,
            nombre_pages = new_nombre_pages,
            resume = new_resume,
            oeuvres_principales_id_femmme=id_femme)


        #On ouvre un double bloc "try-except" afin de gérer les erreurs
        try:
             # On ajoute le portrait a la base de donnees
            db.session.add(created_oeuvres_principales)
            db.session.commit()
           

            return True, created_oeuvres_principales
        #Exécution de except uniquement si une erreur apparaît. 
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    #@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

    def modifier_oeuvres_principales(id_oeuvre, Titre, Date_premiere_pub, Editeur, Lieu_publication, Nombre_pages, Resume):
        """
        Fonction qui permet de modifier les informations d'une oeuvre dans la base de données (modifications rendues possibles par un utilisateur.rice).
        :param id_oeuvre: identifiant numérique de l'oeuvre
        :param Titre: titre de l'oeuvre
        :param Date_premiere_pub: Date de la première publication de l'oeuvre
        :param Editeur: éditeur ou maison d'édition de l'oeuvre
        :param Lieu_publication: lieu de publication de l'oeuvre
        :param Nombre_pages: nombre de pages de l'oeuvre
        :param Resume: résumé de l'oeuvre
        :type id_oeuvre: integer
        :type Titre, Date_premiere_pub, Editeur, Lieu_publication, Nombre_pages, Resume: string
        :returns: tuple (booléen, liste/objet)
         S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet mis à jour (ici une oeuvre).
        """

        #On crée une liste vide pour les erreurs
        erreurs=[]

        #On vérifie que l'utilisateur complète au moins deux champs de données considérés comme essentiels
        if not Titre:
            erreurs.append("le champ 'titre' est obligatoire")
        #Les autres données ne sont pas forcément disponibles et sont donc optionnelles.
        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        #On récupère une oeuvre dans la base grâce à son identifiant
        update_oeuvres_principales = Oeuvres_principales.query.get(id_oeuvre)

        #On vérifie que l'utilisateur-trice modifie au moins un champ

        if update_oeuvres_principales.titre == Titre \
                and update_oeuvres_principales.date_premiere_pub == Date_premiere_pub \
                and update_oeuvres_principales.editeur == Editeur \
                and update_oeuvres_principales.lieu_publication == Lieu_publication \
                and update_oeuvres_principales.nombre_pages == Nombre_pages \
                and update_oeuvres_principales.resume == Resume:
            erreurs.append("Aucune modification n'a été réalisée")

        if len(erreurs) > 0:
            return False, erreurs


        #S'il n'y a pas d'erreurs, on met à jour les données de l'oeuvre :
        else :
            update_oeuvres_principales.titre=Titre
            update_oeuvres_principales.date_premiere_pub=Date_premiere_pub
            update_oeuvres_principales.editeur=Editeur
            update_oeuvres_principales.lieu_publication=Lieu_publication
            update_oeuvres_principales.nombre_pages=Nombre_pages
            update_oeuvres_principales.resume=Resume

        #On ajoute un bloc "try-except" afin de "gérer" les erreurs
        try:
            # On ajoute le portrait à la base de données
            db.session.add(update_oeuvres_principales)
            db.session.commit()

            return True, update_oeuvres_principales

        #Exécution de except uniquement si une erreur apparaît. 
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def supprimer_oeuvres_principales(id_oeuvre, Titre, Date_premiere_pub, Editeur, Lieu_publication, Nombre_pages, Resume):
        """
        Fonction qui permet de supprimer la notice d'une oeuvre.
        :param id_oeuvre: identifiant numérique de l'oeuvre
        :param Titre: titre de l'oeuvre
        :param Date_premiere_pub: Date de la première publication de l'oeuvre
        :param Editeur: éditeur ou maison d'édition de l'oeuvre
        :param Lieu_publication: lieu de publication de l'oeuvre
        :param Nombre_pages: nombre de pages de l'oeuvre
        :param Resume: résumé de l'oeuvre
        :type id_oeuvre: integer
        :type Titre, Date_premiere_pub, Editeur, Lieu_publication, Nombre_pages, Resume: string
        :returns: booleens
        """

        #On récupère une oeuvre dans la base grâce à son identifiant
        delete_oeuvres_principales = Oeuvres_principales.query.get(id_oeuvre)

        delete_oeuvres_principales.id_oeuvre = id_oeuvre
        delete_oeuvres_principales.titre = Titre
        delete_oeuvres_principales.date_premiere_pub = Date_premiere_pub
        delete_oeuvres_principales.editeur = Editeur
        delete_oeuvres_principales.lieu_publication = Lieu_publication
        delete_oeuvres_principales.nombre_pages = Nombre_pages
        delete_oeuvres_principales.resume = Resume
    
        #On ajoute un bloc "try-except" afin de "gérer" les erreurs
        try:
            #On supprime le portrait de la base de données
            db.session.delete(delete_oeuvres_principales)
            db.session.commit()
            return True, delete_oeuvres_principales
        except Exception as erreur:
            return False, [str(erreur)]


                                                                ####Portrait####
class Portrait(db.Model):
#On crée notre modèle Portrait.
    __tablename__="portrait"
    id_portrait = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    url_portrait = db.Column(db.Text)
    nom_createur = db.Column(db.Text)
    prenom_createur = db.Column(db.Text)
    annee_realisation = db.Column(db.Text)
    techniques = db.Column(db.Text)
    lieu_conservation = db.Column(db.Text)
    #Jointure
    portrait_id_femme = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))
    authorships_portrait = db.relationship("Authorship_portrait", back_populates='portrait_portrait')



    @staticmethod
    #@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

    def creer_portrait(new_url_portrait, new_nom_createur, new_prenom_createur, new_annee_realisation, new_techniques, new_lieu_conservation, id_femme):
        """
        Fonction qui permet de créer une nouveau portrait et de l'ajouter à la base de données (ajout rendu possible par un utilisateur)
        :param new_url_portrait: url du portrait pour appeler l'image dans l'application
        :param new_nom_createur: nom de la personne ayant produit le portrait
        :param new_prenom_createur: prénom de la personne ayant produit le portrait
        :param new_annee_realisation: année où le portrait a été réalisé
        :param new_lieu_conservation: institut de conservation du portrait, s'il y en a une
        :param id_femme : identifiant numérique de la romancière qui est représenté par le portrait
        :type new_url_portrait, new_nom_createur, new_prenom_createur, new_annee_realisation, new_techniques, new_lieu_conservation : string
        :type id_femme: integer
        :returns: tuple (booléen, liste/objet)
         S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet créé (ici un portrait).
        """

        #On crée une liste vide pour les erreurs
        erreurs = []

        #On vérifie que l'utilisateur complète au moins un champ de données considérés comme essentiels
        if not new_url_portrait:
            erreurs.append("le champ 'url du portrait' est obligatoire")
        #Les autres données ne sont pas forcément disponibles et sont donc optionnelles.


        if new_annee_realisation:
            if not len(new_annee_realisation) == 4:
                erreurs.append("La date de l'année de réalisation  doit faire 4 caractères. Format AAAA demandé.")
            if len(erreurs) > 0:
                return False, erreurs



        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs


        # S'il n'y a pas d'erreur, on ajoute une nouvelle entrée dans la table portrait avec les champs correspondant aux paramètres du modèle
        created_portrait = Portrait(
            url_portrait = new_url_portrait,
            nom_createur = new_nom_createur,
            prenom_createur = new_prenom_createur,
            annee_realisation = new_annee_realisation,
            techniques = new_techniques,
            lieu_conservation = new_lieu_conservation,
            portrait_id_femme = id_femme)

        #On ouvre un double bloc "try-except" afin de gérer les erreurs
        try:
             # On ajoute le portrait a la base de donnees
            db.session.add(created_portrait)
            db.session.commit()
           

            return True, created_portrait
        #Exécution de except uniquement si une erreur apparaît. 
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    #@staticmethod permet d'intéragir avec une classe pour un objet qui n'existe pas encore.

    def modifier_portrait(id_portrait, Url_portrait, Nom_createur, Prenom_createur, Annee_realisation, Techniques, Lieu_conservation):
        """
        Fonction qui permet de modifier les informations d'un portrait dans la base de données (modifications rendues possibles par un utilisateur.rice).
        :param id_portrait : identifiant numérique du portrait
        :param Url_portrait: url du portrait pour appeler l'image dans l'application
        :param Nom_createur: nom de la personne ayant produit le portrait
        :param Prenom_createur: prénom de la personne ayant produit le portrait
        :param Annee_realisation: année où le portrait a été réalisé
        :param Lieu_conservation: institut de conservation du portrait, s'il y en a une
        :type Url_portrait, Nom_createur, Prenom_createur, Annee_realisation, Techniques, Lieu_conservation : string
        :returns: tuple (booléen, liste/objet)
         S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet mis à jour (ici une oeuvre).
        """

        #On crée une liste vide pour les erreurs
        erreurs=[]

        #On récupère une oeuvre dans la base grâce à son identifiant
        update_portrait = Portrait.query.get(id_portrait)

        #On vérifie que l'utilisateur-trice modifie au moins un champ

        if update_portrait.url_portrait == Url_portrait \
                and update_portrait.nom_createur == Nom_createur \
                and update_portrait.prenom_createur == Prenom_createur \
                and update_portrait.annee_realisation == Annee_realisation \
                and update_portrait.techniques == Techniques \
                and update_portrait.lieu_conservation == Lieu_conservation :
            erreurs.append("Aucune modification n'a été réalisée")

        if len(erreurs) > 0:
            return False, erreurs


        #S'il n'y a pas d'erreurs, on met à jour les données du portrait :
        else :
            update_portrait.url_portrait = Url_portrait 
            update_portrait.nom_createur = Nom_createur 
            update_portrait.prenom_createur = Prenom_createur
            update_portrait.annee_realisation = Annee_realisation
            update_portrait.techniques = Techniques
            update_portrait.lieu_conservation = Lieu_conservation

        #On ajoute un bloc "try-except" afin de "gérer" les erreurs
        try:
            # On ajoute le portrait a la base de donnees
            db.session.add(update_portrait)
            db.session.commit()

            return True, update_portrait

        #Exécution de except uniquement si une erreur apparaît. 
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def supprimer_portrait(id_portrait, Url_portrait, Nom_createur, Prenom_createur, Annee_realisation, Lieu_conservation):
        """
        Fonction qui permet de supprimer un portrait de la base de données
        :param id_portrait : identifiant numérique du portrait
        :param Url_portrait: url du portrait pour appeler l'image dans l'application
        :param Nom_createur: nom de la personne ayant produit le portrait
        :param Prenom_createur: prénom de la personne ayant produit le portrait
        :param Annee_realisation: année où le portrait a été réalisé
        :param Lieu_conservation: institut de conservation du portrait, s'il y en a une
        :type Url_portrait, Nom_createur, Prenom_createur, Annee_realisation, Techniques, Lieu_conservation : string
        :returns: booleens
        """

        #On récupère une oeuvre dans la base grâce à son identifiant
        delete_portrait = Portrait.query.get(id_portrait)

        delete_portrait.id_portrait = id_portrait
        delete_portrait.url_portrait = Url_portrait
        delete_portrait.nom_createur = Nom_createur
        delete_portrait.prenom_createur = Prenom_createur
        delete_portrait.annee_realisation = Annee_realisation
        delete_portrait.lieu_conservation = Lieu_conservation
        
        #On ajoute un bloc "try-except" afin de "gérer" les erreurs
        try:
            #On supprime le portrait de la base de données
            db.session.delete(delete_portrait)
            db.session.commit()
            return True, delete_portrait
        except Exception as erreur:
            return False, [str(erreur)]



                                                                ####Authorship####

class Authorship_femme_de_lettres(db.Model):
#On crée notre modèle Authorship pour la table Femme_de_lettres.
    __tablename__ = "authorship_femme_de_lettres"
    authorship_femme_de_lettres_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_femme_de_lettres_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_femme_de_lettres_id_femme = db.Column(db.Integer, db.ForeignKey('femme_de_lettres.id_femme'))
    authorship_femme_de_lettres_date = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    #Jointures
    user_femme_de_lettres = db.relationship("User", back_populates="author_femme_de_lettres")
    femme_de_lettres_femme_de_lettres = db.relationship("Femme_de_lettres", back_populates="authorships_femme_de_lettres")

class Authorship_oeuvres_principales(db.Model):
#On crée notre modèle Authorship pour la table Oeuvres_principales.
    __tablename__="authorship_oeuvres_principales"
    authorship_oeuvres_principales_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_oeuvres_principales_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_oeuvres_principales_id_oeuvre = db.Column(db.Integer, db.ForeignKey('oeuvres_principales.id_oeuvre'))
    authorship_oeuvres_principales_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #Jointures
    user_oeuvres_principales = db.relationship("User", back_populates="author_oeuvres_principales")
    oeuvres_principales_oeuvres_principales = db.relationship("Oeuvres_principales", back_populates="authorships_oeuvres_principales")

class Authorship_portrait(db.Model):
#On crée notre modèle Authorship pour la table Portrait.
    __tablename__="authorship_portrait"
    authorship_portrait_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_portrait_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_portrait_id_portrait = db.Column(db.Integer, db.ForeignKey('portrait.id_portrait'))
    authorship_portrait_date = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    #Jointures
    user_portrait = db.relationship("User", back_populates="author_portrait")
    portrait_portrait = db.relationship("Portrait", back_populates="authorships_portrait")
