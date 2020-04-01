Route pour éditer une romancière : 


@app.route("/editer_romanciere", methods=["POST", "GET"])
@login_required
def editer_romanciere(id_femme):
    """
    Route permettant à l'utilisateur de modifier un formulaire avec les données d'une romancière
    :param id_femme : identifiant numérique de la romancière récupéré depuis la page romanciere
    """

    #On renvoie sur la page html les éléments de l'objet new_femme_de_lettres correspondant à l'identifiant de la route 
    if request.method == "GET":
        femme_de_lettre_origine = Femme_de_lettres.query.get(id_femme)
        return render_template("pages/editer_romanciere.html", femme_de_lettre_origine=femme_de_lettre_origine)

    #On récupère les données du formulaire modifié
    else: 
        status, femme_de_lettres_modif= Femme_de_lettres.edit_romanciere(
            new_id_femme = id_femme,
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
    if status is True:
            flash("Modification des données d'une romanciere réussie !", "success")
            return render_template("pages/romanciere.html", unique=femme_de_lettres_modif)
    else:
        flash("La modification des données d'une a échoué pour les raisons suivantes : " + ", ".join(data), "danger")
        femme_de_lettre_origine = Femme_de_lettres.query.get(id_femme)
        return render_template("pages/editer_romanciere.html", femme_de_lettre_origine=femme_de_lettre_origine)



A ajouter à donnees.py

@staticmethod
    def edit_romanciere(new_nom_naissance, new_prenom_naissance, new_nom_auteur, new_prenom_auteur, new_date_naissance, new_lieu_naissance, new_date_mort, new_lieu_mort, new_pseudonyme):
        """
        Fonction qui permet de modifier les informations d'une romancière dans la base de données (modifications rendues possibles par un utilisateur.rice).
        :param new_nom_naissance: nom de famille de naissance de la romanciere (str)
        :param new_prenom_naissance: prenom de naissance de la romanciere (str)
        :param new_nom_auteur: nom dauteur de la romanciere (str)
        :param new_prenom_auteur: prenom dauteur de la romanciere (str)
        :param new_date_naissance: date de naissance de la romanciere (str)
        :param new_lieu_naissance: lieu de naissance (ville ou village) de la romanciere (str)
        :param new_date_mort: date de mort de la romanciere (str)
        :param new_lieu_mort: lieu de mort (ville ou village) de la romanciere (str)
        :param new_pseudonyme: pseudonyme de la romanciere (str)
        :returns: tuple
        """

        #On crée une liste vide pour les erreurs
        erreurs=[]

        #On vérifie que l'utilisateur complète au moins deux champs de données considérés comme essentiels
        if not new_nom_auteur:
            erreurs.append("le champ 'nom d'auteur' est obligatoire")
        if not new_prenom_auteur:
            erreurs.append("le champ 'prénom d'auteur' est obligatoire")
        #Les autres données ne sont pas forcément disponibles et sont donc optionnelles.
        #Si on a au moins une erreur, retourner un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        #On récupère une romancière dans la base grâce à son identifiant
        new_femme_de_lettres = Femme_de_lettres.query.get(id)

        #On vérifie que l'utilisateur modifie au moins un des champs

        if new_femme_de_lettres.nom_naissance == new_nom_naissance \
                and new_femme_de_lettres.prenom_naissance == new_prenom_naissance \
                and new_femme_de_lettres.nom_auteur == new_nom_auteur \
                and new_femme_de_lettres.prenom_auteur == new_prenom_auteur \
                and new_femme_de_lettres.date_naissance == new_date_naissance \
                and new_femme_de_lettres.lieu_naissance == new_lieu_naissance \
                and new_femme_de_lettres.date_mort == new_date_mort \
                and new_femme_de_lettres.lieu_mort == new_lieu_mort \
                and new_femme_de_lettres.pseudonyme == new_pseudonyme :
            erreurs.append("Aucune modification n'a été réalisée")

        if len(erreurs) > 0:
            return False, erreurs

        #On vérifie que la longueur des caractères de la date ne dépasse pas la limite de 10 (format MM-JJ-AAAA)
        if new_date_naissance:
            if not len(new_date_naissance) == 10 or not len(new_date_mort) == 10:
                erreurs.append("Les dates doivent faire 10 caractères. Format MM-JJ-AAAA demandé.")
            if len(erreurs) > 0:
                return False, erreurs

        # Si on a au moins une erreurs, on affiche un message d'erreur
        if len(erreurs) > 0:
            return False, erreurs

        # S'il n'y a pas d'erreur, on met à jour les données de la romancière
        else :
            new_femme_de_lettres.nom_naissance=new_nom_naissance
            new_femme_de_lettres.prenom_naissance=new_prenom_naissance
            new_femme_de_lettres.nom_auteur=new_nom_auteur
            new_femme_de_lettres.prenom_auteur=new_prenom_auteur
            new_femme_de_lettres.date_naissance=new_date_naissance
            new_femme_de_lettres.lieu_naissance=new_lieu_naissance
            new_femme_de_lettres.date_mort=new_date_mort
            new_femme_de_lettres.lieu_mort=new_lieu_mort
            new_femme_de_lettres.pseudonyme=new_pseudonyme

        try:
            # On ajoute la romanciere a la base de donnees
            db.session.add(new_femme_de_lettres)
            db.session.commit()

            return True, new_femme_de_lettres

        except Exception as erreur_modification:
            return False, [str(erreur_modification)]
