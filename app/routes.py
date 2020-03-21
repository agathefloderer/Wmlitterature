from flask import render_template

from .app import app
from .modeles.donnees import Femme_de_lettres

@app.route("/")
# Le decorateur app.route cree une associaton entre lURL donnee comme argument et la fonction. Comme nous sommes sur la page daccueil, on ecrit lURL("/")
def accueil():
    romancieres = Femme_de_lettres.query.order_by(Femme_de_lettres.nom_auteur.asc()).all()
    #Maintenant que notre modele est mis en place, on peut faire des requetes. Ici, on recupere l'integralite des lieux.NB : on recupere les donnees au moment de lexecution des routes.
    return render_template("pages/accueil.html", nom="WmLitterature", romancieres=romancieres)
    #Declaration et retour du template accueil. 
    #La fonction render_template prend en premier argument le chemin du template (a partir du sous-dossier du template), puis les arguments nommes.Ces arguments sont ensuite utilises comme des variables dans les templates.

@app.route("/romanciere/<int:id_femme>")
#Definition de routes a parametres. On conditionne le type de id_femme (il s'agit d'un nombre entier)
def romanciere(id_femme):
    unique_femme = Femme_de_lettres.query.get(id_femme)
    #On utilise .query pour les clefs primaires. 
    return render_template("pages/romancieres.html", nom="WmLitterature", romanciere=unique_femme)