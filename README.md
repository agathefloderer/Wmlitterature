# WmLitterature

ATTENTION : application en cours de développement.

## Présentation du projet

"WmLitterature" est une application Web, reposant sur une base de données, qui répertorie des femmes de lettres françaises, et plus spécifiquement des romancières.

Cette application a été créée dans le cadre du master 2 Technologies numériques appliquées à l'histoire de l'Ecole nationale des chartes. Elle est développée avec *Python3*.

En ce qui concerne le design de l'application, *Boostrap* a été utilisé.

## Comment procéder au lancement de WmLitterature ?

### Pré-requis

- Il nécessaire d'installer Python3 sur son ordinateur pour faire fonctionner cette application. 
- Il est également nécessaire d'installer virtualenv à l'aide de la commande suivante: `pip install virtualenv`

### Premier lancement
Afin de lancer l'application pour la première fois, il est nécessaire de procéder aux étapes suivantes :
- Cloner le repository : `git clone https://github.com/agathefloderer/Wmlitterature.git`. 
- Créer un environnement virtuel dédié à l'application (et donc créer cette environnement virtuel à l'intérieur du repository) : `virtualenv -p python3 env`
- Pour activer l'environnement virtuel, il faut taper : `source env/bin/activate`. Cette étape sera nécessaire à chaque nouveau lancement de l'application.
- Installer les packages nécessaires pour le lancement de l'application : `pip install -r requirements.txt`
- Lancer le fichier run.py : `python3 run.py`

### Autres lancements
- Se placer à l'intérieur du repository via le terminal et taper : `source env/bin/activate`
- Lancer le fichier run.py : `python3 run.py`

## Contributeur 
Agathe Floderer
