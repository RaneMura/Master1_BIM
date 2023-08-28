-- Suppression de la base existante
DROP TABLE article_x_auteur;
DROP TABLE articles;
DROP TABLE auteurs;
DROP TABLE journaux;

-- Table des journaux
CREATE TABLE journaux (
  issn         CHAR(9) PRIMARY KEY
                       CONSTRAINT issn_ok CHECK(issn ~ '^[0-9]{4}-[0-9]{4}$'),
  nom_journal  TEXT NOT NULL,
  abreviation  TEXT NOT NULL,
  editeur      TEXT NOT NULL
);

-- Table des auteurs
CREATE TABLE auteurs (
  nom          TEXT,
  prenom       TEXT,
  CONSTRAINT auteurs_pkey PRIMARY KEY (nom,prenom)
);

-- Table des articles
CREATE TABLE articles (
  titre        TEXT NOT NULL,
  issn         CHAR(9) REFERENCES journaux(issn)
                       ON UPDATE CASCADE ON DELETE CASCADE,
  volume       SMALLINT CONSTRAINT volume_ok CHECK(0 <= volume),
  debut        SMALLINT NOT NULL,
  fin          SMALLINT NOT NULL,
  annee        SMALLINT NOT NULL CONSTRAINT annee_ok CHECK(1000 <= annee AND annee <= 2100),
  doi          TEXT PRIMARY KEY,
  CONSTRAINT pages CHECK(debut <= fin)
);

-- Table de relation article - auteur
CREATE TABLE article_x_auteur (
  doi          TEXT REFERENCES articles(doi)
                    ON UPDATE CASCADE ON DELETE CASCADE,
  nom          TEXT,
  prenom       TEXT,
  rang         SMALLINT Constraint rang_ok CHECK(1 <= rang),
  CONSTRAINT article_x_auteur_fkey
    FOREIGN KEY(nom,prenom)
    REFERENCES auteurs(nom,prenom)
    MATCH FULL
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT article_x_auteur_pkey PRIMARY KEY (doi,nom,prenom)
);

\i ~/MU4BM748/fill_journaux.sql
\i ~/MU4BM748/fill_auteurs.sql
\i ~/MU4BM748/fill_articles.sql
\i ~/MU4BM748/fill_article_x_auteur.sql

