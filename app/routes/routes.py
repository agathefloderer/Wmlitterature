from flask import render_template, request, flash, redirect
from sqlalchemy import or_
from flask_login import login_user, current_user, logout_user, login_required

from app.app import app, login
from app.modeles.donnees import Femme_de_lettres, Oeuvres_principales, Portrait
from app.modeles.utilisateurs import User
from app.constantes import femme_par_page

@app.route("/")
# Le decorateur app.route cree une associaton entre lURL donnee comme argument et la fonction. Comme nous sommes sur la page daccueil, on ecrit lURL("/")
def accueil():
    return render_template("pages/accueil.html", nom="WmLitterature")

#Routes pour les pages d'index 

@app.route("/index_romanciere")
def index_romanciere() :
    romancieres = Femme_de_lettres.query.order_by(Femme_de_lettres.nom_auteur).all()
    #Maintenant que notre modele est mis en place, on peut faire des requetes. Ici, on recupere l'integralite des lieux.NB : on recupere les donnees au moment de lexecution des routes.
    return render_template("pages/index_romanciere.html", nom="WmLitterature", romancieres=romancieres)
    #Declaration et retour du template accueil. 
    #La fonction render_template prend en premier argument le chemin du template (a partir du sous-dossier du template), puis les arguments nommes.Ces arguments sont ensuite utilises comme des variables dans les templates.

@app.route("/romanciere/<int:id_femme>")
#Definition de routes a parametres. On conditionne le type de id_femme (il s'agit d'un nombre entier)
def romanciere(id_femme):
    unique_femme = Femme_de_lettres.query.get(id_femme)
    #On utilise .query pour les clefs primaires.
    oeuvres = unique_femme.oeuvres
    portraits = unique_femme.portraits
    return render_template("pages/romanciere.html", nom="WmLitterature", romanciere=unique_femme, oeuvres=oeuvres, portraits=portraits)

@app.route("/galerie")
def portrait():
    romanciere = Femme_de_lettres.query.all()
    portraits = Portrait.query.all()
    return render_template("pages/galerie.html", nom="WmLitterature", portraits=portraits, romanciere=romanciere)

@app.route("/recherche")
def recherche():
    """
    Fonction permettant d'effectuer de la recherche plein-texte
    """
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)
    
    if isinstance(page, str) and page.isdigit():
    	page = int(page)
    else :
    	page = 1

    # On crée une liste vide de résultat (qui restera vide par defaut si on n'a pas de mot clef)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
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

@app.route("/creer_romanciere", methods=["GET", "POST"])
@login_required
def creer_romanciere():
    """ Route permettant a l'utilisateur de créer une notice romancière """
    femme_de_lettres = Femme_de_lettres.query.all()
    if request.method == "POST":
        status, data = Femme_de_lettres.create_person(
        new_nom_naissance=request.form.get("new_nom_naissance", None),
        new_prenom_naissance=request.form.get("new_prenom_naissance", None),
        new_nom_auteur=request.form.get("new_nom_auteur", None),
        new_prenom_auteur=request.form.get("new_prenom_auteur", None),
        new_date_naissance=request.form.get("new_date_naissance", None),
        new_lieu_naissance=request.form.get("new_lieu_naissance", None),
        new_date_mort=request.form.get("new_date_mort", None),
        new_lieu_mort=request.form.get("new_lieu_mort", None),
        new_pseudonyme=request.form.get("new_pseudonyme", None)
        )

        if status is True:
            flash("Création d'une nouvelle romanciere réussie !", "success")
            return redirect("/creer_romanciere")
        else:
            flash("La création d'une nouvelle romanciere a échoué pour les raisons suivantes : " + ", ".join(data), "danger")
            return render_template("pages/creer_romanciere.html")
    else:
        return render_template("pages/creer_romanciere.html", nom="WmLitterature")

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gerant les inscriptions
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
            flash("Enregistrement effectue. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont ete rencontrees : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gerant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous etes deja connecte-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a ete envoye
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuee", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants nont pas ete reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous etes deconnecte-e", "info")
    return redirect("/")