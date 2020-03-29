#module principal de lapplication (initialisation et configuration)

from flask import Flask
#On importe le module Flask, ainsi que la fonction render_template (depuis le module Flask)
from flask_sqlalchemy import SQLAlchemy
#On importe SQLAlchemy
from flask_login import LoginManager
#On importe flask_login
import os
from .constantes import SECRET_KEY


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics)
#On donne ensuite un nom a lapplication

app.config['SECRET_KEY'] = SECRET_KEY
#On configure le secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./romanciere.sqlite'
#On configure lapplication avec les informations necessaires pour se connecter
db = SQLAlchemy(app)
# On initie lobjet SQLAlchemy en lui fournissant lapplication comme variable et en le stockant dans la variable `db`.

# On met en place la gestion dutilisateur-rice-s
login = LoginManager(app)

from .routes import routes