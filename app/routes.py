from flask import render_template, request

from .app import app
from .modeles.donnees import Femme_de_lettres, Oeuvres_principales, Portrait

femme_par_page = 5

@app.route("/")
# Le decorateur app.route cree une associaton entre lURL donnee comme argument et la fonction. Comme nous sommes sur la page daccueil, on ecrit lURL("/")
def accueil():
    return render_template("pages/accueil.html", nom="WmLitterature")

#Routes pour les pages d'index 

@app.route("/index_romanciere")
def index_romanciere() :
    romancieres = Femme_de_lettres.query.order_by(Femme_de_lettres.nom_auteur.asc()).all()
    #Maintenant que notre modele est mis en place, on peut faire des requetes. Ici, on recupere l'integralite des lieux.NB : on recupere les donnees au moment de lexecution des routes.
    return render_template("pages/index_romanciere.html", nom="WmLitterature", romancieres=romancieres)
    #Declaration et retour du template accueil. 
    #La fonction render_template prend en premier argument le chemin du template (a partir du sous-dossier du template), puis les arguments nommes.Ces arguments sont ensuite utilises comme des variables dans les templates.

@app.route("/romanciere/<int:id_femme>")
#Definition de routes a parametres. On conditionne le type de id_femme (il s'agit d'un nombre entier)
def romanciere(id_femme):
    unique_femme = Femme_de_lettres.query.get(id_femme)
    #On utilise .query pour les clefs primaires.
    oeuvres = Oeuvres_principales.query.all()
    return render_template("pages/romanciere.html", nom="WmLitterature", romanciere=unique_femme, oeuvres=oeuvres)

@app.route("/galerie")
def portrait():
    portraits = Portrait.query.all()
    return render_template("pages/galerie.html", nom="WmLitterature", portraits=portraits)

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
