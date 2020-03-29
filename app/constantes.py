#On stocke dans constantes.py un "secret" qui permettra a Flask deffectuer des transactions securisees

from warnings import warn

femme_par_page = 5
SECRET_KEY = "JE SUIS UN SECRET !"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par defaut n'a pas ete change, vous devriez le faire", Warning)
