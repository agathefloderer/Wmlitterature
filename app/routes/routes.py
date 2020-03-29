from flask import render_template, request, flash, redirect

from ..app import app, login
from ..modeles.donnees import Femme_de_lettres, Oeuvres_principales, Portrait, Profession
from ..modeles.utilisateurs import User
from ..constantes import femme_par_page
from flask_login import login_user, current_user, logout_user

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
    romancieres = Femme_de_lettres.query.order_by(Femme_de_lettres.nom_auteur).all()
    portraits = Portrait.query.all()
    return render_template("pages/galerie.html", nom="WmLitterature", portraits=portraits, romancieres=romancieres)

@app.route("/recherche")
def recherche():
    # On preferera lutilisation de .get() ici qui nous permet d'eviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)
    
    if isinstance(page, str) and page.isdigit():
    	page = int(page)
    else :
    	page = 1

    # On cree une liste vide de resultat (qui restera vide par defaut si on na pas de mot cle)
    resultats = []

    # On fait de meme pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Femme_de_lettres.query.filter(
            Femme_de_lettres.nom_auteur.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=femme_par_page)
        titre = "Resultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)

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