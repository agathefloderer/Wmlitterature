# Table dassociation necessaire a la declaration dune relation many-to-many entre la table femme_de_lettres et la profession dans notre db
HasProfession = db.Table("hasProfession",
    db.Column("id_hasProfession", db.Integer, unique=True, nullable=False, primary_key=True),
    db.Column("hasProfession_id_femme", db.Integer, db.ForeignKey("femme_de_lettres.id_femme"), primary_key=True),
    db.Column("hasProfession_id_profession", db.Integer, db.ForeignKey("profession.id_profession"), primary_key=True)
    )

class Profession(db.Model):
    id_profession = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label = db.Column(db.Text)

 A ajouter dans la classe femme_de_lettres :     professions = db.relationship('Profession', secondary=HasProfession, backref=db.backref("romanciere"))
