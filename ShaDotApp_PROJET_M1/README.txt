----------------------------------------------------------------------------------------

                                    	ShaDotApp

----------------------------------------------------------------------------------------

ShaDotApp est un programme qui permet de construire des dotplots à partir de protéomes 
bactériens présents dans une base de données en PostgreSQL via une interface graphique 
sous Tkinter et codé en Python 3.

----------------------------------------------------------------------------------------

                        	I-Fonctionnalités de l'application

----------------------------------------------------------------------------------------

L'application permet d'effectuer les les fonctions suivantes:
    - Créer , supprimer une base de données ou changer entre plusieurs
    - Exécuter un BLASTp entre deux organismes bactériens de votre choix
    - Afficher un dotplot en fonction des conditions que vous pourrez imposer via 
        les possibilités proposées par l'application.
    - Sauvegarder vos dotplots.
    - Sélectionner le type de plot ou une extraction des données sous format txt.


----------------------------------------------------------------------------------------

                                    II-Pré-requis

---------------------------------------------------------------------------------------- 

Concernant PostgreSQL, vous avez deux possibilités :
    - Soit vous êtes sur un serveur le possédant, vous pouvez passer aux packages
    - Soit vous êtes sur votre propre ordinateur et vous voulez travailler en local

Si vous souhaitez travailler en local, il vous faut installer PostgreSQL, pour cela
voici le lien  et suivez les instructions : https://www.postgresql.org/download/

Il faudra également installer la commande blastp du NCBI en local, si l'application ne
se trouve pas sur un serveur ne possédant pas la commande . Voici la commande si 
vous êtes sur Linux\Ubuntu : 
	
	COMMANDE : sudo apt-get install ncbi-blast+
	
Si vous êtes sur Windows ou Mac, voici un lien pour l'installer:
	lien : https://www.ncbi.nlm.nih.gov/books/NBK569861/

Une fois que vous êtes ici, voici les packages qui vont être utilisé, il sera 
également mentionné si certains sont inclus ou non nativement avec Python 3 :

    - python3 : au cas où, ce n'est pas souvent le cas, voici le lien pour l'installer 
        https://www.python.org/downloads/ 
    
    - csv : présent nativement avec Python, permet de travailler avec des fichiers csv

    - copy : présent nativement avec Python, permet de créer une copie d'un objet 

    - subprocess : présent nativement avec Python, permet de créer une copie d'un objet 
    
    - os : présent nativement avec Python, permet d'intéragir avec le système
    
    - re : présent nativement avec Python, permet d'exploiter les RegEx
    
    - time : présent nativement avec Python, permet de mesurer le temps
    
    - tkinter : présent nativement avec Python, permet de créer une copie d'un objet 

    - matplotlib : absent, permet de créer des visualisations de données

    - numpy : absent, permet de travailler avec des matrices

    - psycopg2 :  absent, permet de travailler avec des bases de données PostgreSQL 
    
    - customtkinter : un module similaire à Tkinter pour obtenir une interface moderne. 
    	Ce module est nécessaire pour lancer le programme ShaDotApp_CTK.py.
    	
    

Voici les commandes pour installer les packages absents si elles ne sont pas disponibles:

	A saisir sur le terminal :

    	- Pour numpy : 
    		COMMANDE : pip3 install numpy

    	- Pour matplotlib : 
    		COMMANDE : pip3 install matplotlib

    	- Pour tkinter : 
    		COMMANDE :pip3 install tkinter

    	- Pour psycopg2 : 
    		COMMANDE :pip3 install psycopg2
    	
    	- Pour  customtkinter: 
    		COMMANDE :pip3 install customtkinter

----------------------------------------------------------------------------------------

                                    III-Démarrage

----------------------------------------------------------------------------------------


Concernant la base de données, il n'y a pas de soucis si vous êtes sur le serveur Obiwan.

Cependant, si vous n'avez pas de base de données nativement, vous avez deux options :
	- vous pouvez charger la base avec le fichier SHADOTAPP_backup.sql situé dans le 
	dossier Data/.Dump
	- vous pouvez la créer à l'intérieur de l'application dans le menu "Aide" (IV)
	
	
Si vous souhaitez créer la base à partir du dump voici les commandes à saisir sur le 
terminal, en vous situant dans le dossier racine de l'application et en nommant la base 
"SHADOTAPP" obligatoirement dans cette situation :

	- Pour créer la base vide : 
		COMMANDE : createdb SHADOTAPP
	
	- Pour charger la base à partir du dump:
		COMMANDE : psql SHADOTAPP < .Dump/SHADOTAPP_backup.sql


Pour exécuter l'application, voici la commande à effectuer sur le terminal:
	COMMANDE : python3 ShaDotApp.py
	
Si vous avez installé customtkinter:
	COMMANDE : python2 ShaDotApp_CTK.py
	
Une interface s'ouvre sur la fenêtre. L'interface peut varier dans la version CTK et 
notamment l'absence des onglets Fichiers, Aide et Base de données intégré directement
dans la fenêtre principale. Le fichier ShaDotApp_CTK_Dynamic_Plot dans le dossier
"Developpement" fonctionne mais contient quelques erreurs mais celui-ci est une 
piste d'améloiration pour avoir un affichage dynamique du dotplot.

La description suivante est fidèle au programme ShaDotApp.py.

----------------------------------------------------------------------------------------

                              IV-Fonctionnement de la GUI

----------------------------------------------------------------------------------------

								  IV.A - Les onglets

----------------------------------------------------------------------------------------

Sur cette interface trois onglets sont disponibles :
	- "Fichier"
	- "Base de données"
	- "Aide"
	
L'onglet "Fichier" contient une option "Quitter" pour fermer l'application

L'onglet "Base de données contient deux options : 
	- "Ajouter un organisme" : Permet d'ajouter un organisme dans la sélction 
	   d'organismes présent sur la fenêtre principale
	   
	- "Sélectionner un BLAST" : Permet de sélectionner un BLAST déja présent dans 
	   la base de données.
	
L'onglet "Aide" possède une option "Vous n'êtes pas sur OBIWAN" : celui-ci permet de 
créer une base de données si aucune n'est présente sur le serveur ou chez vous en local 
	
	
----------------------------------------------------------------------------------------

							IV.A.1 - "Ajouter un organisme"

----------------------------------------------------------------------------------------

Cette option vous ouvre une fenêtre, cela est nécessaire si vous souhaitez ajouter un 
nouvel organisme dans la liste de sélection de la fenêtre principale. 

Cela est surtout fait pour que vous puissiez choisir les organismes à injecter et ne 
pas engrendrer l'injection totale des protéomes qui sont aux alentours de 9000.

Pour cela, veuillez sélectionner un organisme représenté par son nom et son numéro 
d'assembly en cliquant dessus avec la souris.

Si vous souhaitez avoir des détails sur un organisme, appuyez sur "Infos" pour avoir
un descriptif apparaître dans une autre fenêtre.

Si vous souhaitez l'ajouter, appuyez sur le bouton "Ajouter", le bouton reste appuyé 
durant l'ajout dans la base et retire l'organisme de la grande liste.

Fermez la fenêtre une fois fini avec la croix de fermeture en haut à droite.

----------------------------------------------------------------------------------------

							IV.A.2 - "Sélectionnez un BLAST"

----------------------------------------------------------------------------------------

Cette option vous ouvre une fenêtre, cela est nécessaire si vous souhaitez éxecuter un 
dotplot sur un blast précis.

La fenêtre contient un tableau avec à gauche le numéro d'éxécution du blast et 
à droite les noms et numéro d'assembly des organismes du BLAST.

Pour enregister votre sélection, cliquez sur la ligne que vous souhaitez et appuyer sur
le bouton "Sélectionner" : vous verrez apparaître le numéro d'éxécution à côté de la
mention "Blast sélectionné : "

Fermez la fenêtre une fois fini avec la croix de fermeture en haut à droite.

----------------------------------------------------------------------------------------

						  IV.A.3 - "Vous n'êtes pas sur OBIWAN"

----------------------------------------------------------------------------------------

Si vous n'avez pas de base de données initialement présente, vous verrez que les listes
de sélection et que les deux fenêtres sont également vides.

Pour cela, veuillez définir un nom dans l'espace prévu et appuyer sur "Vérification" 
si une base est déja présente ou si le nom de base est disponible. Si un base est déja 
présente, vous verrez une mention : "Inutile de créer : BASE EXISTANTE POUR L'APP" et 
il ne sera pas possible d'en créer.

Si le feu vert vous est accordé, appuyez sur le bouton "Créer" et la base sera crée, 
vous pourrez voir l'évolution dans le terminal. La fenêtre se ferme automatiquement.

----------------------------------------------------------------------------------------

						  		V - Fenêtre principale

----------------------------------------------------------------------------------------

						  	    V.A - Sélection et BLAST	
						  	    
----------------------------------------------------------------------------------------

Vous avez deux barres de sélection en face des mentions "Espèce 1" et "Espèce 2". 
Vous pouvez sélectionner dans la liste les espèces pour lesquelles vous souhaitez 
exécuter un blast et également avoir des informations sur les espèces choisis, même 
si vous n'en choisissez qu'une seule.

Pour avoir des informations sur les organismes sélectionnés, cliquez sur un organisme 
dans la liste et appuyez sur le bouton "Infos esp". Vous pouvez fermer la fenêtre avec 
la croix en haut à droite.

Pour exécuter le BLAST, sélectionnez les DEUX espèces et appuyez sur "Blast ! ". 
Cela prend environ deux minutes : la commande blastp est longue en exécution.
Le bouton reste appuyé jusqu'à la fin de l'injection du BLAST dans la base de données.

LE BLAST est crée avec une e-value de 1e-4

ATTENTION : SI VOUS OBSERVEZ DES METIONS AVEC "Hyphens ..." SUR LE TERMINAL, C'EST 
NORMAL. IL S'AGIT D'UN FORMATAGE QUI ÉLIMINE LES LIGNES AVEC DES MAUVAISES QUOTES.

----------------------------------------------------------------------------------------

						  	    V.B - Critères de séléction	
						  	    
----------------------------------------------------------------------------------------

Vous avez 3 conditions sur les critères BLAST : 
	- la couverture du hit (entre 0 et 1, si en float -> ex : 0.3)
	- la e-value (de la forme XeY -> ex : 1e-40)
	- le pourcentage d'identité de séquence (entre 1 et 100, si en float - > ex :  1.6)
	
Si vous voulez choisir un critère, veuillez cocher la case du critère et saisissez la 
valeur de seuil dans la case correspondante sur la même ligne.

La couverture du hit permet de sélectionner les protéines dont la couverture de la 
séquence query et la séquence subject sont supérieurs au seuil imposé.

La e-value permet de sélectionner les protéines dont la e-value issu du BLAST est 
inférieure au seuil imposé.

Le pourcentage d'identité  permet de sélectionner les protéines dont ce pourcentage 
est supérieur au seuil imposé.

Vous avez également 2 conditions CD-Search qui est de développement qui sont juste 
présent mais n'influent pas sur le BLAST.

----------------------------------------------------------------------------------------

						  	    V.C - Choix de la représentation 
						  	    
----------------------------------------------------------------------------------------

Vous avez une mention "Style de plot ou Extraction" avec une sélection permettant de 
choisir le type d'information que vous souhaitez obtenir suite au traitement par les 
critères après appui sur le bouton "Lancer":

	- "scatter" : affichera un scatter plot pour une visualisation globale du dotplot  
	
	- "imshow" : affichera un plot en imshow pour une visualisation précise du dotplot
		(il faudra cependant zoomer pour visualiser les phénomenes du duplication)
		
	- "txt : peut aller jusqu'à 20 Mo" : va créer un fichier dans le dossier 
	   "Data/Stringence" qui va contenir la liste des protéines considérées comme 
	   homologues dans ce fichier. 
	   Il est fortement recommandé de supprimer les fichiers après utilisation 
	   car ceux_ci pèsent environ 20 Mo.

Ensuite suit deux emplacements pour saisir la taille de la fenêtre et le seuil de 
stringence.

Le seuil de stringence ne doit pas être supérieur à la taille de la fenêtre. 

----------------------------------------------------------------------------------------

						  	    	VI - Dotplot 
						  	    
----------------------------------------------------------------------------------------

Si vous avez fait vos choix de critères et sélectionné "scatter" ou "imshow" et saisi
les critères de stringence : appuyez sur le bouton "Lancer ! ".

Cela va afficher en maximum 5 secondes un dotplot "épais" ou "fin" en fonction des
choix respectifs. Il est fait sous matplotlib donc vous avez des options de zoom,
la sélection d'une zone, et enregister le dotplot sous format .png en appuyant sur le
logo "disquette" en bas de la fenêtre. 

Vous pouvez fermer la fenêtre avec la croix une fois fini.

----------------------------------------------------------------------------------------

				VII - Remarques concernant les fichiers et dossiers
						  	    
----------------------------------------------------------------------------------------

- VEUILLEZ NE PAS MODIFIER LA STRUCTURE DES DOSSIERS, NE SUPPRIMEZ PAS LE DOSSIER 
DATA CAR CELUI-CI CONTIENT LES FICHIERS NÉCESSAIRES POUR CRÉER ET ALIMENTER UNE BASE 
DE DONNÉES INITIALE.

- NE DÉPLACEZ PAS LE CODE "ShaDotApp.py"

VOICI LA STRUCUTRE DU DOSSIER SHADOTAPP : 

---- ShaDotApp
  	  |
  	  ---- .Base (tout le dossier est caché)
  	  	|	 |
  	  	|    ---- Blastp
  	  	|	   |	|
		|	   |    ---------- QUERY-GCA_000014865.1_ASM1486v1_translated_cds__DB GCA_000009985.1_ASM998v1_translated_cds.out
		|	   |	  |
		|	   |	  -------- QUERY-GCA_001580455.1_ASM158045v1_translated_cds__DB-GCA_000215705.1_ASM21570v1_translated_cds.out
		|	   |	  |
		|	   |	  -------- QUERY-GCA_002843685.1_ASM284368v1_translated_cds__DB-GCA_000026265.1_ASM2626v1_translated_cds.out
		|	   |		  				  
  	  	|	   -- Proteomes		
  	  	|	   |    |	  
		|	   |	--------- GCA_000009985.1_ASM998v1_translated_cds.faa
  	  	|	   |      |  
  	  	|	   |      ------- GCA_000014865.1_ASM1486v1_translated_cds.faa  
  	  	|	   |      |  
  	  	|	   |      ------- GCA_000026265.1_ASM2626v1_translated_cds.faa  					 
  	  	|	   |      |  
  	  	|	   |      ------- GCA_000215705.1_ASM21570v1_translated_cds.faa
  	  	|	   |      |  
  	  	|	   |      ------- GCA_001580455.1_ASM158045v1_translated_cds.faa  
  	  	|	   |      |  
  	  	|	   |      ------- GCA_002843685.1_ASM284368v1_translated_cds.faa      
  	  	|      |
  	  	|	   -- Cog_ProkBank	
  	  	|	        |	  
		|	   	    --------- cognames2003-2014.tab.txt
  	  	|	         |  
  	  	|	         -------- fun2003-2014.tab.txt 
  	  	|	         |  
  	  	|	         -------- prokaryotes_complete-genomes.csv 	
  	  	|
  	  	|
  	  	-- .Dump (tout le dossier est caché)
  	  	|	 |
  	  	|	 ---- SHADOTAPP_backup.sql
  	  	|	 
		-- Stringence
		|	 |
		|    ---- (Vide)
		|
		-- Developpement
		|	 |
		|    ---- ShaDotApp_CTK_Dynamic_Plot.py
        |	
		-- README.txt
		|
		-- Resume_Projet_KMURALI.pdf
		|
		-- ShaDotApp.py
		|
		-- ShaDotApp_CTK.py

			 
Pour voir les dossiers cachés : faire sur le terminal : ls -lah

La base initialement crée par dump ou par l'onglet "Aide" : contiendra les éléments suivants :
	- Les protéomes des souche K-12 (substr. MG1655) et souche IAI1 d'Escherichia coli
 	- Les protéomes des organismes Ramlibacter sp. 5-10 et Ramlibacter tataouinensis TTB310
	- Les protéomes des organismes Magnetococcus marinus MC-1 et Magnetospirillum magneticum AMB-1
	- Les blasts respectifs des trois couples de protéomes ci-dessus
	- Une banque de prokaryotes issu du fichier "prokaryotes_complete-genomes.csv" 	
  	- Une banque d'identifiants CD-SEARCH et de fonctions issu des fichiers "cognames2003-2014.tab.txt" et "prokaryotes_complete-genomes.csv "
		
			 
----------------------------------------------------------------------------------------

							VIII - Test rapide de Dynamic Plot
						  	    
----------------------------------------------------------------------------------------			 
			 
Allez dans le dossier Developpement, avec customtkinter d'installé, et executez:
	COMMANDE : python3 ShaDotApp_CTK_Dynamic_Plot.py
	
Dessus, dirigez vous dans l'onglet "Selection BLAST et conditions"
Choisissez un Blast comme celui des souches E.coli puis appuyez sur Lancer.

Une fenetre va s'ouvrir. Saisissez les valeurs de seuil que vous souhaitez mais vous
êtes obligé de mettre une valeur de taille de fenetre et de seuil de stringence.

Appuyez sur le bouton correspondant au Scatter ou Imshow et le dotplot va apparaitre.
Modifiez et réexecuter pour obtenir un nouveau dotplot.
----------------------------------------------------------------------------------------

									IX - Contact
						  	    
----------------------------------------------------------------------------------------

Application crée par Sharane K.Murali

Pour plus d'informations :
	- mail : sharane.k_murali@etu.sorbonne-université.fr
	
Merci d'utiliser cette application, celle-ci ne possède pas de licence et pourra 
être mis sur un GitHub.
