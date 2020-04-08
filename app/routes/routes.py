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

@app.route("/romanciere/oeuvre/<int:id_oeuvre>")
def oeuvre(id_oeuvre):
    """
    Route permettant d'afficher les données d'une oeuvre
    :param id_oeuvre : idenfiant numérique de la romancière
    """
    unique_oeuvre = Oeuvres_principales.query.get(id_oeuvre)
    return render_template("pages/oeuvre.html", nom="WmLitterature", oeuvre=unique_oeuvre)

@app.route("/galerie")
def portrait():
    """Route permettant l'affichage de la galerie de portraits des romancières
    """
    romanciere = Femme_de_lettres.query.all()
    portraits = Portrait.query.all()
    return render_template("pages/galerie.html", nom="WmLitterature", portraits=portraits, romanciere=romanciere)

@app.route("/romanciere/portrait/<int:id_portrait>")
def portrait_individuel(id_portrait):
    """
    Route permettant d'afficher les données d'un portrait
    :param id_portrait : idenfiant numérique de la romancière
    """
    unique_portrait = Portrait.query.get(id_portrait)
    return render_template("pages/portrait.html", nom="WmLitterature", portrait=unique_portrait)

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
def creation_romanciere():
    """ Route permettant a l'utilisateur de créer une notice romancière """
    femme_de_lettres = Femme_de_lettres.query.all()
    if request.method == "POST":
        statut, donnees = Femme_de_lettres.creer_romanciere(
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

        if statut is True:
            flash("Création d'une nouvelle romanciere réussie !", "success")
            return redirect("/creer_romanciere")
        else:
            flash("La création d'une nouvelle romanciere a échoué pour les raisons suivantes : " + ", ".join(donnees), "danger")
            return render_template("pages/creer_romanciere.html")
    else:
        return render_template("pages/creer_romanciere.html", nom="WmLitterature")


@app.route("/modifier_romanciere/<int:identifier>", methods=["POST", "GET"])
@login_required
def modification_romanciere(identifier):
    """
    Route gérant la modification d'une romancière
    :param identifier: identifiant de la romancière
    """
    # On renvoie sur la page html les éléments de l'objet site correspondant à l'identifiant de la route
    if request.method == "GET":
        femme_a_modifier = Femme_de_lettres.query.get(identifier)
        return render_template("pages/modifier_romanciere.html", romanciere=femme_a_modifier)

    # on récupère les données du formulaire modifié
    else:
        statut, donnees= Femme_de_lettres.modifier_romanciere(
            Id_femme=identifier,
            Nom_naissance=request.form.get("Nom_naissance", None),
            Prenom_naissance=request.form.get("Prenom_naissance", None),
            Nom_auteur=request.form.get("Nom_auteur", None),
            Prenom_auteur=request.form.get("Prenom_auteur", None),
            Lieu_naissance=request.form.get("Lieu_naissance", None),
            Date_naissance=request.form.get("Date_naissance", None),
            Lieu_mort=request.form.get("Lieu_mort", None),
            Date_mort=request.form.get("Date_mort", None),
            Pseudonyme=request.form.get("Pseudonyme", None)
        )

        if statut is True:
            flash("Modification réussie !", "success")
            return render_template ("pages/accueil.html")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "danger")
            femme_a_modifier = Femme_de_lettres.query.get(identifier)
            return render_template("pages/modifier_romanciere.html", nom="WmLitterature", romanciere=femme_a_modifier)

@app.route("/supprimer_romanciere/<int:identifier>", methods=["POST", "GET"])
@login_required
def suppression_romanciere(identifier):
    """ 
    Route pour supprimer une romancière dans la base
    :param identifier : identifiant de la romancière
    """
    femme_a_supprimer = Femme_de_lettres.query.get(identifier)

    if request.method == "POST":
        statut, donnees = Femme_de_lettres.supprimer_romanciere(
            Id_femme=identifier,
            Nom_naissance=request.args.get("Nom_naissance", None),
            Prenom_naissance=request.args.get("Prenom_naissance", None),
            Nom_auteur=request.args.get("Nom_auteur", None),
            Prenom_auteur=request.args.get("Prenom_auteur", None),
            Lieu_naissance=request.args.get("Lieu_naissance", None),
            Date_naissance=request.args.get("Date_naissance", None),
            Lieu_mort=request.args.get("Lieu_mort", None),
            Date_mort=request.args.get("Date_mort", None),
            Pseudonyme=request.args.get("Pseudonyme", None)
        )

        if statut is True:
            flash("Suppression réussie !", "success")
            return redirect("/accueil")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "danger")
            return redirect("pages/supprimer_romanciere.html")
    else:
        return render_template("pages/supprimer_romanciere.html", nom="WmLitterature", romanciere=femme_a_supprimer)


@app.route("/romanciere/<int:id_femme>/creer_oeuvre", methods=["GET", "POST"])
@login_required
def creation_oeuvre(id_femme):
    """ 
    Route permettant a l'utilisateur de créer une notice oeuvre 
    :param id_femme : identifiant de la romancière
    """
    
    femme_de_lettres = Femme_de_lettres.query.get(id_femme)

    if request.method == "POST":
        statut, donnees = Oeuvres_principales.creer_oeuvres_principales(
        new_titre = request.form.get("new_titre", None),
        new_date_premiere_pub = request.form.get("new_date_premiere_pub", None),
        new_editeur = request.form.get("new_editeur", None),
        new_lieu_publication = request.form.get("new_lieu_publication", None),
        new_nombre_pages = request.form.get("new_nombre_pages", None), 
        new_resume = request.form.get("resume", None), 
        id_femme = id_femme
        )

        if statut is True:
            flash("Ajout d'une nouvelle oeuvre à la bibliographie de la romancière", "success")
            return redirect("/index_romanciere")
        else:
            flash("L'ajout d'une nouvelle oeuvre a échoué pour les raisons suivantes : " + ", ".join(donnees), "danger")
            return render_template("pages/creer_oeuvre.html")
    else:
        return render_template("pages/creer_oeuvre.html", nom="WmLitterature", romanciere=femme_de_lettres)

@app.route("/modifier_oeuvre/<int:id_oeuvre>", methods=["POST", "GET"])
@login_required
def modification_oeuvre(id_oeuvre):
    """
    Route gérant la modification d'une oeuvre
    :param id_oeuvre: identifiant de l'oeuvre
    """
    # On renvoie sur la page html les éléments de l'objet oeuvre correspondant à l'identifiant de la route
    if request.method == "GET":
        oeuvre_a_modifier = Oeuvres_principales.query.get(id_oeuvre)
        return render_template("pages/modifier_oeuvre.html", oeuvre=oeuvre_a_modifier)

    # on récupère les données du formulaire modifié
    else:
        statut, donnees= Oeuvres_principales.modifier_oeuvres_principales(
            id_oeuvre=id_oeuvre,
            Titre=request.form.get("Titre", None),
            Date_premiere_pub=request.form.get("Date_premiere_pub", None),
            Editeur=request.form.get("Editeur", None),
            Lieu_publication=request.form.get("Lieu_publication", None),
            Nombre_pages=request.form.get("Nombre_pages", None),
            Resume = request.form.get("Resume", None), 
        )

        if statut is True:
            flash("Modification réussie !", "success")
            return render_template ("pages/accueil.html")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "danger")
            oeuvre_a_modifier = Oeuvres_principales.query.get(id_oeuvre)
            return render_template("pages/modifier_oeuvre.html", nom="WmLitterature", oeuvre=oeuvre_a_modifier)


@app.route("/supprimer_oeuvre/<int:id_oeuvre>", methods=["POST", "GET"])
@login_required
def suppression_oeuvre(id_oeuvre):
    """ 
    Route pour supprimer une oeuvre dans la base
    :param identifier : identifiant de l'oeuvre
    """
    oeuvre_a_supprimer = Oeuvres_principales.query.get(id_oeuvre)

    if request.method == "POST":
        statut, donnees = Oeuvres_principales.supprimer_oeuvres_principales(
            id_oeuvre=id_oeuvre,
            Titre=request.args.get("Titre", None),
            Date_premiere_pub=request.args.get("Date_premiere_pub", None),
            Editeur=request.args.get("Editeur", None),
            Lieu_publication=request.args.get("Lieu_publication", None),
            Nombre_pages=request.args.get("Nombre_pages", None),
            Resume=request.args.get("Resume", None)
        )

        if statut is True:
            flash("Suppression réussie !", "success")
            return redirect("/index_romanciere")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "danger")
            return redirect("pages/supprimer_oeuvre.html")
    else:
        return render_template("pages/supprimer_oeuvre.html", nom="WmLitterature", oeuvre=oeuvre_a_supprimer)



@app.route("/romanciere/<int:id_femme>/creer_portrait", methods=["GET", "POST"])
@login_required
def creation_portrait(id_femme):
    """
    Route permettant a l'utilisateur de créer un portrait 
    :param id_femme : identifiant de la romancière
    """
    
    femme_de_lettres = Femme_de_lettres.query.get(id_femme)

    if request.method == "POST":
        statut, donnees = Portrait.creer_portrait(
        new_url_portrait = request.form.get("new_url_portrait", None),
        new_nom_createur = request.form.get("new_nom_createur", None),
        new_prenom_createur = request.form.get("new_prenom_createur", None),
        new_annee_realisation = request.form.get("new_annee_realisation", None),
        new_techniques = request.form.get("new_techniques", None), 
        new_lieu_conservation = request.form.get("new_lieu_conservation", None),
        id_femme = id_femme
        )

        if statut is True:
            flash("Ajout du portrait de la romancière", "success")
            return redirect("/index_romanciere")
        else:
            flash("L'ajout du portrait de la romancière a échoué pour les raisons suivantes : " + ", ".join(donnees), "danger")
            return render_template("pages/creer_portrait.html")
    else:
        return render_template("pages/creer_portrait.html", nom="WmLitterature", romanciere=femme_de_lettres)


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