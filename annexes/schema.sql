BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "portrait" (
	"id_portrait"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"url_portrait"	TEXT,
	"nom_createur"	TEXT,
	"prenom_createur"	TEXT,
	"annee_realisation"	TEXT,
	"techniques"	TEXT,
	"lieu_conservation"	TEXT,
	"portrait_id_femme"	INTEGER NOT NULL,
	"provenance_image"	TEXT,
	FOREIGN KEY("portrait_id_femme") REFERENCES "femme_de_lettres"("id_femme") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "authorship_portrait" (
	"authorship_portrait_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"authorship_portrait_user_id"	INTEGER NOT NULL,
	"authorship_portrait_id_portrait"	INTEGER NOT NULL,
	"authorship_portrait_date"	DATETIME DEFAULT CURENT_TIMESTAMP,
	FOREIGN KEY("authorship_portrait_id_portrait") REFERENCES "portrait"("id_portrait"),
	FOREIGN KEY("authorship_portrait_user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "authorship_femme_de_lettres" (
	"authorship_femme_de_lettres_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"authorship_femme_de_lettres_user_id"	INTEGER NOT NULL,
	"authorship_femme_de_lettres_id_femme"	INTEGER NOT NULL,
	"authorship_femme_de_lettres_date"	DATETIME DEFAULT CURENT_TIMESTAMP,
	FOREIGN KEY("authorship_femme_de_lettres_id_femme") REFERENCES "femme_de_lettres"("id_femme"),
	FOREIGN KEY("authorship_femme_de_lettres_user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "authorship_oeuvres_principales" (
	"authorship_oeuvres_principales_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"authorship_oeuvres_principales_user_id"	INTEGER NOT NULL,
	"authorship_oeuvres_principales_id_oeuvre"	INTEGER NOT NULL,
	"authorship_oeuvres_principales_date"	DATETIME DEFAULT CURENT_TIMESTAMP,
	FOREIGN KEY("authorship_oeuvres_principales_id_oeuvre") REFERENCES "oeuvres_principales"("id_oeuvre"),
	FOREIGN KEY("authorship_oeuvres_principales_user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"user_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_nom"	TINYTEXT NOT NULL,
	"user_login"	VARCHAR(45) NOT NULL,
	"user_email"	TINYTEXT NOT NULL,
	"user_password"	VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "femme_de_lettres" (
	"id_femme"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nom_naissance"	TEXT,
	"prenom_naissance"	TEXT,
	"nom_auteur"	TEXT NOT NULL,
	"prenom_auteur"	TEXT NOT NULL,
	"date_naissance"	TEXT,
	"lieu_naissance"	TEXT,
	"date_mort"	TEXT,
	"lieu_mort"	TEXT,
	"pseudonyme"	TEXT
);
CREATE TABLE IF NOT EXISTS "oeuvres_principales" (
	"id_oeuvre"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"titre"	TEXT,
	"date_premiere_pub"	TEXT,
	"editeur"	TEXT,
	"lieu_publication"	TEXT,
	"nombre_pages"	TEXT,
	"oeuvres_principales_id_femmme"	INTEGER NOT NULL,
	"resume"	TEXT,
	FOREIGN KEY("oeuvres_principales_id_femmme") REFERENCES "femme_de_lettres"("id_femme") ON DELETE CASCADE
);
INSERT INTO "portrait" VALUES (1,'https://upload.wikimedia.org/wikipedia/commons/f/fb/Claire_de_Duras.jpg',NULL,NULL,'1840',NULL,NULL,2,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (3,'https://upload.wikimedia.org/wikipedia/commons/e/ee/George_Sand.PNG','CHARPENTIER','Auguste','1838',NULL,'Musée de la Vie romantique - Paris',3,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (4,'https://upload.wikimedia.org/wikipedia/commons/d/d1/Th%C3%A9r%C3%A8se_Bentzon.jpg',NULL,NULL,'1905','Peinture',NULL,4,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (5,'https://upload.wikimedia.org/wikipedia/commons/b/b4/Solange_Dudevant-_Cl%C3%A9singer_%281828-1899%29.jpg','CLESINGER','Auguste','1849',NULL,'Musée de la vie romantique - Paris',5,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (6,'https://upload.wikimedia.org/wikipedia/commons/9/95/Eug%C3%A9nie_Foa_%281796-1852%29.png','BECQUET','',NULL,'Gravure','Bibliothèque de Bordeaux',7,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (7,'https://upload.wikimedia.org/wikipedia/commons/1/15/Marie-Louise_Gagneur.png','PETIT','Pierre','1872','Photographie','Gallica',8,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (8,'https://upload.wikimedia.org/wikipedia/commons/b/b1/Jane_de_La_Vaud%C3%A8re.jpg','LAUDA','E. de','1902',NULL,NULL,10,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (9,'https://upload.wikimedia.org/wikipedia/commons/b/b0/Raoul_de_Navery_BNF_Gallica.jpg',NULL,NULL,'1875','Photographie','Bibliothèque nationale de France',12,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (10,'https://upload.wikimedia.org/wikipedia/commons/2/25/Olga_de_Pitray-S%C3%A9gur.jpg','BARRIAS','Félix Joseph','1859',NULL,NULL,14,'Wikimedia Commons');
INSERT INTO "portrait" VALUES (11,'https://upload.wikimedia.org/wikipedia/commons/d/d6/Jean-Baptiste_Fran%C3%A7ois_Desoria_-_Portrait_de_Constance_Pipelet.jpg','DESORIA','Jean Baptiste François','1797','Peinture',NULL,17,'Wikimedia Commons');
INSERT INTO "femme_de_lettres" VALUES (1,'MARONNAT','Anne Pierrette','AMERO','Marie','1838-04-03','Luzy','1913-30-12','Neuilly-sur-Seine','Daniel Arnault');
INSERT INTO "femme_de_lettres" VALUES (2,'COETNEMPREN DE KERSAINT','Claire Louisa Rose Bonne de','DURAS','Claire de','1777-03-22','Brest','1828-01-16','Nice','Claire Lechat de Kersaint');
INSERT INTO "femme_de_lettres" VALUES (3,'DUPIN','Amantine Aurore Lucile','SAND','Georges','1804-07-01','Paris','1876-06-08','Nohant',NULL);
INSERT INTO "femme_de_lettres" VALUES (4,'SOLMS','Marie Thérèse de','BENTZON','Thérèse','1840-09-21','Seine-Port','1907-02-07','Paris ou Meudon',NULL);
INSERT INTO "femme_de_lettres" VALUES (5,'DUDEVANT-SAND','Solange','CLESINGER-SAND','Solange','1828-09-13','Nohant','1899-03-17','Paris','Dubois de Vavray');
INSERT INTO "femme_de_lettres" VALUES (6,'CONSTANT DE REBECQUE','Anne Marie Louise','ESTOURNELLES','Louise','1792-06-04','Brevans','1860-02-08','La Flèche',NULL);
INSERT INTO "femme_de_lettres" VALUES (7,'RODRIGUES-HENRIQUES','Rebecca Eugénie','FOA','Eugénie','1796-06-10','Bordeaux','1852-05-03','Paris','Edmond de Fontanes');
INSERT INTO "femme_de_lettres" VALUES (8,'MIGNEROT','Marie Louise','GAGNEUR','Marie Louise','1832-05-25','Domblans','1902-02-17','Paris','Duchesse Lauriane');
INSERT INTO "femme_de_lettres" VALUES (9,'PABAN','Clotilde Marie','COLLIN DE PLANCY','Clotide Marie','1790','Paris',NULL,NULL,'Marie dHeures');
INSERT INTO "femme_de_lettres" VALUES (10,'LA VAUDERE','Jane de','SCRIVE','Jeanne',' 1857-04-15','Paris','1908-07-26','Paris',NULL);
INSERT INTO "femme_de_lettres" VALUES (11,'WEILL','Jeanne','MAY','Dick','1859-03-94','Alger','1925-08-14',NULL,NULL);
INSERT INTO "femme_de_lettres" VALUES (12,'SAFFRAY','Eugénie Caroline','NAVERY','Raoul de','1828-05-27','Ploërmel','1885-05-17','La Ferté-sous-Jarre',NULL);
INSERT INTO "femme_de_lettres" VALUES (13,NULL,NULL,'OSMONT','Anne','1872-08-02','Toulouse','1953-05-13','Paris',NULL);
INSERT INTO "femme_de_lettres" VALUES (14,'SEGUR','Alberte Olga de','PITRAY','Olga de ','1835-10-01','Les Nouettes','1920-01-15','Caudebec-en-Caux',NULL);
INSERT INTO "femme_de_lettres" VALUES (15,'','','QUERANGAL','Julie de','1802-02-2','Paris','1844-09-08','Paris','Mme Augustin Thierry');
INSERT INTO "femme_de_lettres" VALUES (16,'CAMUSAT','Louise Léonie','ROUZADE','Léonie','1839','Paris','1916',NULL,NULL);
INSERT INTO "femme_de_lettres" VALUES (17,'THEIS','Constance Marie de','SALM','Constance de','1767-09-07','Nantes','1845-04-13','Paris','Constance D. T. Pipelet');
INSERT INTO "femme_de_lettres" VALUES (18,'',NULL,'ULLIAC-TREMADEURE','Sophie','1794-04-19','Lorient','1862-04-21','Paris','Mademoiselle Dudrezène');
INSERT INTO "oeuvres_principales" VALUES (1,'Fille de Lorraine','1895','Oudin et Cie','Paris',NULL,1,NULL);
INSERT INTO "oeuvres_principales" VALUES (2,'Fakirs et jongleurs','1889','Editions Firmin-Didot et Cie','Paris','64',1,NULL);
INSERT INTO "oeuvres_principales" VALUES (3,'L''Etoile du nord','1903','Firmin-Didot et Cie','Paris','144',1,NULL);
INSERT INTO "oeuvres_principales" VALUES (4,'Le Calvaire de Roseline','1911','Société française d''imprimerie et de librairie','Paris','315',1,NULL);
INSERT INTO "oeuvres_principales" VALUES (5,'Ourika','1825','Ladvocat','Paris',NULL,2,NULL);
INSERT INTO "oeuvres_principales" VALUES (6,'Edouard','1825','Ladvocat','Paris',NULL,2,NULL);
INSERT INTO "oeuvres_principales" VALUES (7,'Olivier ou le Secret','1971','Edition José Corti','Paris',NULL,2,NULL);
INSERT INTO "oeuvres_principales" VALUES (8,'Mémoires de Sophie, suivi de Amélie et Pauline : Romans d''émigration','2011','Editions Manucius','Paris',NULL,2,NULL);
INSERT INTO "oeuvres_principales" VALUES (9,'Indiana','1823','J.-P. Roret','Paris',NULL,3,NULL);
INSERT INTO "oeuvres_principales" VALUES (10,'Lélia','1833','H. Dupuy','Paris',NULL,3,NULL);
INSERT INTO "oeuvres_principales" VALUES (11,'La Mare au diable','1846','E. Proux','Paris',NULL,3,NULL);
INSERT INTO "oeuvres_principales" VALUES (12,'La Petite Fadette','1849','A. Lebègue','Bruxelles',NULL,3,NULL);
INSERT INTO "oeuvres_principales" VALUES (13,'Tony','1885','C. Lévy','Paris',NULL,4,NULL);
INSERT INTO "oeuvres_principales" VALUES (14,'Constance','1891','Calmann Lévy','Paris',NULL,4,NULL);
INSERT INTO "oeuvres_principales" VALUES (15,'Contes de tous les pays','1888','J. Hetzel','Paris','276',4,NULL);
INSERT INTO "oeuvres_principales" VALUES (16,'Au-dessus de l''Abîme','1904','C. Lévy','Paris','349',4,NULL);
INSERT INTO "oeuvres_principales" VALUES (17,'Jacques Bruneau','1870','Michel Lévy','Paris','312',5,NULL);
INSERT INTO "oeuvres_principales" VALUES (18,'Carl Robert','1889','Calmann-Lévy','Paris','343',5,NULL);
INSERT INTO "oeuvres_principales" VALUES (19,'Alphonse et Mathilde','1819','Brissot-Thivars','Paris',NULL,6,NULL);
INSERT INTO "oeuvres_principales" VALUES (20,'Pascaline','1821','C. Villet','Paris',NULL,6,NULL);
INSERT INTO "oeuvres_principales" VALUES (21,'Deux femmes','1836','Schwartz et Gagnot','Paris','428',6,NULL);
INSERT INTO "oeuvres_principales" VALUES (22,'Les Contes de ma bonne. Les cinq infortunes des sabots de Ramouniche','1880','E. Ardent','Limoges','140',7,NULL);
INSERT INTO "oeuvres_principales" VALUES (23,'Les Deux amis','1884','E. Ardent','Limoges',NULL,7,NULL);
INSERT INTO "oeuvres_principales" VALUES (24,'La Laide','1832','C. Vimont','Paris',NULL,7,NULL);
INSERT INTO "oeuvres_principales" VALUES (25,'Une métamorphose',NULL,'Vve Dondey-Dupré','Paris',NULL,7,NULL);
INSERT INTO "oeuvres_principales" VALUES (26,'La Croisade noire : roman contemporain','1865','A. Faure','Paris','583',8,NULL);
INSERT INTO "oeuvres_principales" VALUES (27,'Les Vierges russes','1880','Edouard Dentu','Paris','524',8,NULL);
INSERT INTO "oeuvres_principales" VALUES (28,'Le Supplice de lamant','1888','Edouard Dentu','Paris','468',8,NULL);
INSERT INTO "oeuvres_principales" VALUES (29,'Un chevalier de sacristie','1881','Edouard Dentu','Paris','524',8,NULL);
INSERT INTO "oeuvres_principales" VALUES (30,'La Fournaise','1885','Edouard Dentu','Paris','488',8,NULL);
INSERT INTO "oeuvres_principales" VALUES (31,'Le Désert dans Paris','1824','Pollet','Paris',NULL,9,NULL);
INSERT INTO "oeuvres_principales" VALUES (32,'Jane Shore','1824','J.-N. Barba','Paris',NULL,9,NULL);
INSERT INTO "oeuvres_principales" VALUES (33,'Un Homme','1832','Bohaire','Paris',NULL,9,NULL);
INSERT INTO "oeuvres_principales" VALUES (34,'Les Demi sexes','1897','P. Ollendorff','Paris','303',10,NULL);
INSERT INTO "oeuvres_principales" VALUES (35,'La Mystérieuse','1902','E. Flammarion','Paris',NULL,10,NULL);
INSERT INTO "oeuvres_principales" VALUES (36,'Le Harem de Syta, roman passionnel','1904','A. Méricant','Paris',NULL,10,NULL);
INSERT INTO "oeuvres_principales" VALUES (37,'Sapho, dompteuse','1908','A. Méricant','Paris',NULL,10,NULL);
INSERT INTO "oeuvres_principales" VALUES (38,'L''Affaire Allard','1892','C. Lévy','Paris','328',11,NULL);
INSERT INTO "oeuvres_principales" VALUES (39,'Le cas de Georges d''Arrel','1892','C. Lévy','Paris',NULL,11,NULL);
INSERT INTO "oeuvres_principales" VALUES (40,'L''Alouette','1898','Editions de la Revue blanche','Paris',NULL,11,NULL);
INSERT INTO "oeuvres_principales" VALUES (41,'Peblo et Simplette','1858','E. Dentu','Paris','141',12,NULL);
INSERT INTO "oeuvres_principales" VALUES (42,'Le Trésor de l''abbaye','1876','C. Blérit','Paris','336',12,NULL);
INSERT INTO "oeuvres_principales" VALUES (43,'La Fille sauvage','1902','H. Gautier','Paris','327',12,NULL);
INSERT INTO "oeuvres_principales" VALUES (44,'Le Duel de la veuve','1891','H. Gautier','Paris','240',12,NULL);
INSERT INTO "oeuvres_principales" VALUES (45,'Le Sequin d''or','1907','Hachette','Paris','247',13,NULL);
INSERT INTO "oeuvres_principales" VALUES (46,'Le Petit ramoneur','1898','R. Haton','Paris','280',14,NULL);
INSERT INTO "oeuvres_principales" VALUES (47,'L''Usine et le château','1891','Hachette et Cie','Paris','269',14,NULL);
INSERT INTO "oeuvres_principales" VALUES (49,'Limace et Brouillone','1898','H. Oudin','Paris','112',14,NULL);
INSERT INTO "oeuvres_principales" VALUES (50,'Entre Parias','1879','Blériot frères','Paris','228',14,NULL);
INSERT INTO "oeuvres_principales" VALUES (51,'Adelaïde : Mémoires d''une jeune fille','1839','J. Tessier','Paris',NULL,15,NULL);
INSERT INTO "oeuvres_principales" VALUES (52,'Scènes de moeurs et de caractères au XIXe et au XVIIIe siècle','1835','J. Tessier','Paris',NULL,15,NULL);
INSERT INTO "oeuvres_principales" VALUES (53,'Le Monde renversé','1872','Lachaud','Paris','198',16,NULL);
INSERT INTO "oeuvres_principales" VALUES (54,'Voyage de Théodose à l''île de l''Utopie','1872','Lachaud','Paris','251',16,NULL);
INSERT INTO "oeuvres_principales" VALUES (55,'Vingt-quatre heures d''une femme sensible','1824','A. Bertrand','Paris','196',17,NULL);
INSERT INTO "oeuvres_principales" VALUES (56,'Camille, ou Amitié et imprudence','1800','Théâtre-Français','Paris','',17,NULL);
INSERT INTO "oeuvres_principales" VALUES (57,'Mes Soixante ans','1833','Didot','Paris',NULL,17,NULL);
INSERT INTO "oeuvres_principales" VALUES (58,'Emilie ou la jeune fille auteur','1836','Didier','Paris','352',18,NULL);
INSERT INTO "oeuvres_principales" VALUES (59,'Souvenirs d''une vieille femme','1861',NULL,NULL,NULL,18,NULL);
INSERT INTO "oeuvres_principales" VALUES (60,'Le Petit bossu et la famille du sabotier, ouvrage instructif','1860','N. Grosjean','Nancy','296',18,NULL);
COMMIT;
