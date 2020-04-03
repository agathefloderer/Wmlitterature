#Module principal de l'application (initialisation et configuration)

from flask import Flask
#On importe le module Flask depuis la librairie flask

from flask_sqlalchemy import SQLAlchemy
#On importe SQLAlchemy. SQLAlchemy nous permet de lier la base de données à l'application et de faire des requêtes sur cette base

from flask_login import LoginManager
#On installe flask_login, qui permet de gérer les utilisateurs

import os
#Module nous permettant d'intéragir avec le système sur lequel python est en train de 'tourner'. Ce package permet donc de faire des opérations liées au système

from .constantes import SECRET_KEY
#On importe depuis le fichier constantes.py le SECRET_KEY

#'Commandes' liées au module os :
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
#On stocke le chemin du fichier courant. 
templates = os.path.join(chemin_actuel, "templates")
#On stocke le chemin vers les templates
statics = os.path.join(chemin_actuel, "static")
#On stocke le chemin vers les statics

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics)
#On instancie l'application. 
#Le premier argument correspond au nom de l'application.
#On ajoute deux arguments qui permettent de faire le lien vers les dossiers déclars via les commandes os (définition des dossiers templates et static).
#Attention : app correspond ici à une variable appartenant à la classe Flask et non au package app, initialisé avec le package app et contenant l'application.

app.config['SECRET_KEY'] = SECRET_KEY
#On configure le secret. Ce paramètre est indispensable pour l'utilisation de sessions ou tout ce qui impliquerait des éléments de sécruité avancée 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./romanciere.sqlite'
#On configure l'uri de la base de données à utiliser. 

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#S'il est défini sur "True" Flask-SQLAlchemy suit les modifications des objets et émet des signaux. 
#La valeur par défaut est "False", de qui active le suivi mais émet un avertissement indiquant qu'il sera désactivé par défaut à l'avenir.

db = SQLAlchemy(app)
# On initie l'objet SQLAlchemy en lui fournissant l'application comme variable et en le stockant dans la variable `db`.

login = LoginManager(app)
# On met en place la gestion d'utilisateur-rice-s

from .routes import routes, error
#On relie nos routes à l'application.