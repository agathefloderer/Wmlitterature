#Appel de l'application pour son lancement.

from app.app import app
#A partir du fichier app.py, contenu dans le dossier app, on importe la variable app, correspondant à l'application.

if __name__ == "__main__":
#On vérifie que le ficher est celui couramment executé
	app.run(debug=True)
# On lance un serveur de test via app.run()
