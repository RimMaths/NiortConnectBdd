BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Etat" (
	"id"	INTEGER,
	"description"	TEXT UNIQUE,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Utilisateur" (
	"id"	INTEGER,
	"email"	TEXT UNIQUE,
	"pseudo"	TEXT UNIQUE,
	"password"	TEXT,
	"fkRole"	INTEGER,
	"fkProfil"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("fkProfil") REFERENCES "Profil"("id"),
	FOREIGN KEY("fkRole") REFERENCES "Role"("id")
);
CREATE TABLE IF NOT EXISTS "Commentaire" (
	"id"	INTEGER,
	"fkPublication"	INTEGER,
	"fkUtilisateur"	INTEGER,
	"contenu"	TEXT,
	"datePublication"	DATETIME,
	"estValide"	BOOLEAN,
	PRIMARY KEY("id"),
	FOREIGN KEY("fkPublication") REFERENCES "Publication"("id"),
	FOREIGN KEY("fkUtilisateur") REFERENCES "Utilisateur"("id")
);
CREATE TABLE IF NOT EXISTS "Ecole" (
	"id"	INTEGER,
	"nom"	TEXT,
	"domaineEmail"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Role" (
	"id"	INTEGER,
	"Description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Preferences_Utilisateur" (
	"id"	INTEGER,
	"fkUtilisateur"	INTEGER,
	FOREIGN KEY("fkUtilisateur") REFERENCES "Utilisateur"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Profil" (
	"id"	INTEGER,
	"Ecole"	INTEGER,
	"NivEtude"	INTEGER,
	FOREIGN KEY("Ecole") REFERENCES "Ecole"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Publication" (
	"id"	INTEGER,
	"fkUtilisateur"	INTEGER,
	"categorie"	TEXT,
	"contenu"	TEXT,
	"datePublication"	DATETIME,
	"dateExpiration"	DATETIME,
	"fkEtat"	INTEGER DEFAULT 2,
	"vote"	INTEGER DEFAULT 0,
	"titre"	TEXT,
	FOREIGN KEY("fkUtilisateur") REFERENCES "Utilisateur",
	FOREIGN KEY("fkEtat") REFERENCES "Etat"
);
INSERT INTO "Etat" VALUES (1,'crée');
INSERT INTO "Etat" VALUES (2,'en vérification');
INSERT INTO "Etat" VALUES (3,'publié');
INSERT INTO "Etat" VALUES (4,'expiré');
INSERT INTO "Utilisateur" VALUES (1,'test@example.com','Alice','motDePasse1',1,1);
INSERT INTO "Utilisateur" VALUES (2,'exemple2@formation-isfac.com','Bob','motDePasse2',1,2);
INSERT INTO "Utilisateur" VALUES (3,'exemple3@ensemblescolaire-niort.com','Charlie','motDePasse3',2,1);
INSERT INTO "Utilisateur" VALUES (4,'exemple4@lecnam.com','Sokhna','motdepasse3',2,1);
INSERT INTO "Utilisateur" VALUES (5,'exemple5@lecnam.com','Emilie','motdepasse4',1,2);
INSERT INTO "Commentaire" VALUES (3,3,3,'Oui c est vrai ','2024-03-08 11:00:00',1);
INSERT INTO "Ecole" VALUES (1,'ICSSA','ensemblescolaire-niort.com');
INSERT INTO "Ecole" VALUES (2,'le cnam','lecnam.net');
INSERT INTO "Ecole" VALUES (3,'ISFAC','formation-isfac.com');
INSERT INTO "Role" VALUES (1,'utilisateur');
INSERT INTO "Role" VALUES (2,'moderateur');
INSERT INTO "Role" VALUES (3,'administrateur');
INSERT INTO "Profil" VALUES (1,1,3);
INSERT INTO "Profil" VALUES (2,3,4);
INSERT INTO "Profil" VALUES (3,2,2);
INSERT INTO "Profil" VALUES (4,3,1);
INSERT INTO "Profil" VALUES (5,3,5);
INSERT INTO "Profil" VALUES (6,2,1);
INSERT INTO "Profil" VALUES (7,3,2);
INSERT INTO "Profil" VALUES (8,2,4);
INSERT INTO "Profil" VALUES (9,3,3);
INSERT INTO "Profil" VALUES (10,1,1);
INSERT INTO "Publication" VALUES (3,3,'Etude','La dernière fois jai pu etudié moi et mes amis dans une salle fermée à la bibliotheque Pierre-Moinot','2024-03-08 10:00:00','2024-03-09 10:00:00',4,NULL,NULL);
INSERT INTO "Publication" VALUES (14,5,'divertissement','Bonjour à tous ! Y a des Réductions de 50% sur les cartes au Nouveau Cinéma','2024-06-30 15:09:36',NULL,2,0,'Réduction Billet Cinéma');
INSERT INTO "Publication" VALUES (15,2,'Restauration','Hello, Je suis allé au Resto BFF de la Brêche et ils disent qu'' il y'' a maintenant des réductions avec la carte étudiante !','2024-06-24 10:30:00',NULL,2,0,'Nouvelle Restaurant avec Réduction Etudiant');
INSERT INTO "Publication" VALUES (16,3,'Santé','Pour tous les étudiants de Niort qui n''ont pas encore de medecin, un atelier sera organisé prochainement à la breche regroupant des personnels de santé pour trouver son medecin traitant.','2024-06-17 14:00:00',NULL,2,0,'Un medecin traitant pour tous, la nouvelle politique de la CPAM');
INSERT INTO "Publication" VALUES (17,4,'Shopping','Jusqu''au 15 Avril, retrouvez des réductions jusqu''à -40% à Gemo, Avenue de Paris','2024-06-14 14:00:00',NULL,2,0,'Solde chez Gemo');
INSERT INTO "Publication" VALUES (NULL,1,'Étude','  Gg','2024-06-10 17:18:34',NULL,2,0,' Dfg');
INSERT INTO "Publication" VALUES (NULL,1,'Logement','Cc','2024-06-10 17:18:41',NULL,2,0,'Cc');
INSERT INTO "Publication" VALUES (14,5,'divertissement','Bonjour à tous ! Y a des Réductions de 50% sur les cartes au Nouveau Cinéma','2024-06-30 15:09:36',NULL,2,0,'Réduction Billet Cinéma');
COMMIT;
