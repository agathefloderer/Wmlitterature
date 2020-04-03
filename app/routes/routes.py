#Définition des url et des fonctions définissant le contenu des pages associées

from flask import render_template, request, flash, redirect
#render_template : relie les templates aux routes
#request : récupère les informations de formulaire
#flash : produit des messages d'alerte
#redirect : retourne une redirection vers l'url d'une autre route 

from sqlalchemy import or_
#Grâce à cette commande, on peut utiliser l'opérateur 'or' dans les fonctions destiner à requêter la base de données.

from flask_login import login_user, current_user, logout_user, login_required
#login_user : valide l'authenfication
#current_user : permet d'obtenir l'utilisateur courant
#logout_user : permet la déconnexion
#login_required : limite la capacité d'accès à une page

from app.app import app, login
#A partir du fichier app.py, contenu dans le dossier app, on importe la variable app, correspondant à l'application.
#On importe également login, destiné à la gestion des utilisateur-rice-s

#On importe les classes, disponibles dans donnees.py et utilisateurs.py, de notre modèle de données. Cela nous permettra ensuite de les requêter :
from app.modeles.donnees import Femme_de_lettres, Oeuvres_principales, Portrait
from app.modeles.utilisateurs import User

from app.constantes import femme_par_page
#A partir du fichier constantes.py, contenu dans le dossier app, on importe la variable femme_par_page

                                                ####PAGES GENERALES####  


@app.route("/")
# Le décorateur app.route crée une associaton entre l'URL donnée comme argument et la fonction. Comme nous sommes sur la page daccueil, on ecrit l'URL("/")
def accueil():
    """Route permettant l'affichage d'une page d'accueil
    """
    return render_template("pages/accueil.html", nom="WmLitterature")
    #La fonction render_template prend en premier argument le chemin du template (à partir du sous-dossier du template), puis les arguments nommés. Ces arguments sont ensuite utilisés comme des variables dans les templates.

@app.route("/index_romanciere")
def index_romanciere() :
    """Route permettant l'affichage de l'index des romancières enregistrées
    """
    romancieres = Femme_de_lettres.query.order_by(Femme_de_lettres.nom_auteur).all()
    #Une fois que le modèles sont mis en place dans donnnees.py et utilisateurs.py, on peut faire des requetes. 
    return render_template("pages/index_romanciere.html", nom="WmLitterature", romancieres=romancieres)

@app.route("/romanciere/<int:id_femme>")
#Définition d'une route a paramètres. On conditionne le type de id_femme (il s'agit d'un nombre entier)
def romanciere(id_femme):
    """Route permettant l'affichage des données concernant une romancière

    :param id_femme : identifiant numérique de la romancière
    """
    unique_femme = Femme_de_lettres.query.get(id_femme)
    oeuvres = unique_femme.oeuvres
    portraits = unique_femme.portraits
    return render_template("pages/romanciere.html", nom="WmLitterature", romanciere=unique_femme, oeuvres=oeuvres, portraits=portraits)

@app.route("/galerie")
def portrait():
    """Route permettant l'affichage de la galerie de portraits des romancières
    """
    romanciere = Femme_de_lettres.query.all()
    portraits = Portrait.query.all()
    return render_template("pages/galerie.html", nom="WmLitterature", portraits=portraits, romanciere=romanciere)

#Recherche
@app.route("/recherche")
def recherche():
    """
    Route permettant d'effectuer de la recherche plein-texte
    """
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)
    
    if isinstance(page, str) and page.isdigit():
    	page = int(page)
    else :
    	page = 1

    # On crée une liste vide de résultat (qui restera vide par defaut si on n'a pas de mot clef)
    resultats = []

    titre = "Recherche"
    if motclef:
    #Si on un mot-clef, on requête la table femme_de_lettres de notre base de données pour vérifier s'il y a des correspondances entre le mot entré par l'utilisateur et les données de notre table
        resultats = Femme_de_lettres.query.filter(
            or_(
                Femme_de_lettres.nom_naissance.like("%{}%".format(motclef)),
                Femme_de_lettres.prenom_naissance.like("%{}%".format(motclef)),
                Femme_de_lettres.nom_auteur.like("%{}%".format(motclef)),
                Femme_de_lettres.prenom_auteur.like("%{}%".format(motclef)),
                Femme_de_lettres.date_naissance.like("%{}%".format(motclef)),
                Femme_de_lettres.lieu_naissance.like("%{}%".format(motclef)),
                Femme_de_lettres.date_mort.like("%{}%".format(motclef)),
                Femme_de_lettres.lieu_mort.like("%{}%".format(motclef)),
                Femme_de_lettres.pseudonyme.like("%{}%".format(motclef)),
                )
        ).order_by(Femme_de_lettres.nom_auteur.asc()).paginate(page=page, per_page=femme_par_page)
        titre = "Résultat pour la recherche '" + motclef + "'"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)


                                                    ####PAGES POUR AJOUT, SUPPRESSION, MODIFICATION ####

@app.route("/creer_romanciere", methods=["GET", "POST"])
@login_required
def creer_romanciere():
    """ Route permettant a l'utilisateur de créer une notice romancière """
    femme_de_lettres = Femme_de_lettres.query.all()
    if request.method == "POST":
        status, data = Femme_de_lettres.create_romanciere(
        new_nom_naissance = request.form.get("new_nom_naissance", None),
        new_prenom_naissance = request.form.get("new_prenom_naissance", None),
        new_nom_auteur = request.form.get("new_nom_auteur", None),
        new_prenom_auteur = request.form.get("new_prenom_auteur", None),
        new_date_naissance = request.form.get("new_date_naissance", None),
        new_lieu_naissance = request.form.get("new_lieu_naissance", None),
        new_date_mort = request.form.get("new_date_mort", None),
        new_lieu_mort = request.form.get("new_lieu_mort", None),
        new_pseudonyme = request.form.get("new_pseudonyme", None)
        )

        if status is True:
            flash("Création d'une nouvelle romanciere réussie !", "success")
            return redirect("/creer_romanciere")
        else:
            flash("La création d'une nouvelle romanciere a échoué pour les raisons suivantes : " + ", ".join(data), "danger")
            return render_template("pages/creer_romanciere.html")
    else:
        return render_template("pages/creer_romanciere.html", nom="WmLitterature")

@app.route("/editer_romanciere", methods=["POST", "GET"])
@login_required
def editer_romanciere(id_femme):
    """
    Route permettant à l'utilisateur de modifier un formulaire avec les données d'une romancière
    :param id_femme : identifiant numérique de la romancière récupéré depuis la page romanciere
    """

    #On renvoie sur la page html les éléments de l'objet new_femme_de_lettres correspondant à l'identifiant de la route 
    if request.method == "GET":
        femme_de_lettre_origine = Femme_de_lettres.query.get(id_femme)
        return render_template("pages/editer_romanciere.html", femme_de_lettre_origine=femme_de_lettre_origine)

    #On récupère les données du formulaire modifié
    else: 
        status, femme_de_lettres_modif= Femme_de_lettres.edit_romanciere(
            new_id_femme = id_femme,
            new_nom_naissance = request.form.get("new_nom_naissance", None),
            new_prenom_naissance = request.form.get("new_prenom_naissance", None),
            new_nom_auteur = request.form.get("new_nom_auteur", None),
            new_prenom_auteur = request.form.get("new_prenom_auteur", None),
            new_date_naissance = request.form.get("new_date_naissance", None),
            new_lieu_naissance = request.form.get("new_lieu_naissance", None),
            new_date_mort = request.form.get("new_date_mort", None),
            new_lieu_mort = request.form.get("new_lieu_mort", None),
            new_pseudonyme = request.form.get("new_pseudonyme", None)
            )
    if status is True:
            flash("Modification des données d'une romanciere réussie !", "success")
            return render_template("pages/romanciere.html")
    else:
        flash("La modification des données d'une a échoué pour les raisons suivantes : " + ", ".join(data), "danger")
        femme_de_lettre_origine = Femme_de_lettres.query.get(id_femme)
        return render_template("pages/editer_romanciere.html", femme_de_lettre_origine=femme_de_lettre_origine)

@app.route("/supprimer_romanciere/<int:nr_romanciere>")
@login_required
def supprimer_romanciere(nr_romanciere):
    """
    Route permettant la suppression d'une romancière dans la base de données
    :param nr_romanciere : identifiant numérique de la personne
    """

    status=Femme_de_lettres.delete_romanciere(new_id_femme=nr_romanciere)
    flash("Suppression de la romancière réussie !" "success")
    return redirect("/index_romanciere")


                                                    ####PAGES POUR LA GESTION DES UTILISATEUR-TRICE-S####

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a ete envoye
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a ete envoye
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """Route gérant les déconnexions
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")