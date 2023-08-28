-- suppression 
DROP TABLE frequences;
DROP TABLE echantillons;
DROP TABLE populations_x_langues;
DROP TABLE populations;
DROP TABLE regions;
DROP TABLE langues;
DROP TABLE alleles;
DROP TABLE sites;
DROP TABLE loci_x_roles;
DROP TABLE roles_locus;
DROP TABLE loci;
DROP TABLE bandes;
DROP TABLE chromosomes;


-- chromosome : 
CREATE TABLE chromosomes(
nom_chromosome TEXT PRIMARY KEY
);

-- bandes:
CREATE TABLE bandes(
position_bande TEXT PRIMARY KEY,
nom_chromosome TEXT REFERENCES chromosomes(nom_chromosome)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- loci:
CREATE TABLE loci(
locus_uid TEXT PRIMARY KEY,
nom_locus TEXT,
symbole_locus TEXT,
position_bande TEXT REFERENCES bandes(position_bande)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- role locus :
CREATE TABLE roles_locus(
nom_role TEXT PRIMARY KEY
);

-- loci,roles:
CREATE TABLE loci_x_roles(
nom_role TEXT REFERENCES roles_locus(nom_role)
	ON UPDATE CASCADE ON DELETE CASCADE,
locus_uid TEXT REFERENCES loci(locus_uid)
	ON UPDATE CASCADE ON DELETE CASCADE,
CONSTRAINT loci_x_roles_pkey PRIMARY KEY (locus_uid,nom_role)
);

-- sites :
CREATE TABLE sites(
site_uid TEXT PRIMARY KEY,
nom_site TEXT,
locus_uid TEXT REFERENCES loci(locus_uid)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- alleles:
CREATE TABLE alleles(
allele_uid SERIAL PRIMARY KEY,
nom_allele TEXT,
symbole_allele TEXT,
site_uid TEXT REFERENCES sites(site_uid) 
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- langues : 
CREATE TABLE langues(
nom_langue TEXT PRIMARY KEY
);


-- regions :
CREATE TABLE regions(
nom_region TEXT PRIMARY KEY
);

-- pop : 
CREATE TABLE populations(
pop_uid TEXT PRIMARY KEY,
nom_population TEXT,
nom_region TEXT REFERENCES regions(nom_region)
	ON UPDATE CASCADE ON DELETE CASCADE  
);

-- popxlang:
CREATE TABLE populations_x_langues(
pop_uid TEXT REFERENCES populations(pop_uid)
	ON UPDATE CASCADE ON DELETE CASCADE,
nom_langue TEXT REFERENCES langues(nom_langue)
	ON UPDATE CASCADE ON DELETE CASCADE,
range TEXT,
CONSTRAINT populations_x_langues_pkey
	PRIMARY KEY(pop_uid,nom_langue)
);


-- ech:
CREATE TABLE echantillons(
echantillon_uid TEXT PRIMARY KEY,
nom_echantillon TEXT,
taille_echantillon INTEGER,
pop_uid TEXT REFERENCES populations(pop_uid)
	ON UPDATE CASCADE ON DELETE CASCADE
);


-- freq:
CREATE TABLE frequences(
echantillon_uid TEXT REFERENCES echantillons(echantillon_uid)
	ON UPDATE CASCADE ON DELETE CASCADE,
allele_uid INTEGER REFERENCES alleles(allele_uid)
	ON UPDATE CASCADE ON DELETE CASCADE,
frequence DOUBLE PRECISION,
CONSTRAINT frequences_pkey
	PRIMARY KEY(echantillon_uid,allele_uid)
);

--table temporaire :
CREATE TABLE import(
	locus_uid TEXT,
	nom_locus TEXT,
	symbole_locus TEXT,
	role_locus TEXT,
	position_bande TEXT
);
--table temporaire 2: 
CREATE TABLE import2(
	pop_uid TEXT,
	nom_population TEXT,
	nom_region TEXT,
	langue_primaire TEXT,
	langue_secondaire TEXT
);

--table temporaire 3
CREATE TABLE import3(
        frequence DOUBLE PRECISION,
        nom_allele TEXT,
        symbole_allele TEXT,
        echantillon_uid TEXT
);



-- Copie chromosomes et bandes
\copy chromosomes (nom_chromosome) FROM '/home/sharane/chromosomes.csv' CSV HEADER;
\copy bandes (nom_chromosome,position_bande) FROM '/home/sharane/bandes.csv' DELIMITER ',' CSV HEADER;


-- Copie loci, role_locus, loci_x_roles  
\copy import (locus_uid,nom_locus,symbole_locus,role_locus,position_bande) FROM '/home/sharane/loci(1).csv' DELIMITER ',' CSV HEADER;
INSERT INTO roles_locus SELECT role_locus FROM import GROUP BY role_locus;
INSERT INTO loci SELECT locus_uid,nom_locus,symbole_locus,position_bande FROM import;

-- Copie de sites,alleles,langues
\copy sites (locus_uid,site_uid,nom_site) FROM '/home/sharane/sites(1).csv' DELIMITER ',' CSV HEADER;
\copy alleles (site_uid,nom_allele,symbole_allele) FROM '/home/sharane/alleles.csv' DELIMITER ',' CSV HEADER;
\copy langues(nom_langue) FROM '/home/sharane/langues.csv' CSV HEADER;

-- Copie de regions, populations,echantillons
\copy import2 FROM '/home/sharane/populations.csv' DELIMITER ',' CSV HEADER;
INSERT INTO regions SELECT nom_region FROM import2 GROUP BY nom_region;
INSERT INTO populations SELECT pop_uid,nom_population,nom_region FROM import2;
\copy echantillons (pop_uid,echantillon_uid,taille_echantillon,nom_echantillon) FROM '/home/sharane/echantillons.csv' DELIMITER ',' CSV HEADER;

-- Copie de populations_x_langues
INSERT INTO populations_x_langues SELECT pop_uid, langue_primaire FROM import2;

-- Copie de frequences
\copy import3 (frequence, nom_allele, symbole_allele, echantillon_uid) FROM '/home/sharane/frequences.csv' DELIMITER ',' CSV HEADER; 
INSERT INTO frequences SELECT frequence,echantillon_uid FROM import3;


DROP TABLE import;
DROP TABLE import2;
DROP TABLE import3;

