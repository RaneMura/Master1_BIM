import psycopg2
import subprocess
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import os
import re
import copy
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc

class Dotplot():
    
    #Initialisation 
    def __init__(self):
        self.main_w = tk.Tk()
        
        self.database_name = "SHADOTAPP"
        self.esplist = list()
        self.assembly = list()
        self.plot_option_list = ["scatter","imshow","txt : peut aller jusqu'à 20 Mo"]
        self.plot_option = "scatter"


        self.bl_selection = 0
        
        #Création fenetre
        self.creeBase()

        #Création de la barre de menu
        self.creerMenu()

        #Placement des widgets
        self.placerWidget()

        self.main_w.mainloop()

    
    #Creation de l'interface
    def creeBase(self):
        
        #Fixation d'une taille minimale de fenetre
        self.main_w.minsize(500,700)

        #Titre
        self.main_w.title('ShaDotApp')

        #Taille minimum
        self.main_w.geometry("500x700") 

        #Mise à jour du nom de la base
        self.set_db_name()

        #Mise à jour de la liste des organismes
        self.set_esp_list()
        

    #Création du menu
    def creerMenu(self):

        #Creation de la barre de menu
        self.barre = tk.Menu(self.main_w)

        #CASE FICHIER
        self.file_menu = tk.Menu(self.barre,tearoff=0)
        self.file_menu.add_command(label="Quitter",command = self.main_w.quit)

        #CASE BASE DE DONNÉES 
        self.db_menu = tk.Menu(self.barre,tearoff=0)
        self.db_menu.add_command(label="Ajouter un organisme",command = self.update_esp)
        self.db_menu.add_command(label="Selectionner un BLAST",command = self.bl_fenetre)


        #CASE AIDE 
        self.aide_menu = tk.Menu(self.barre,tearoff=0)
        self.aide_menu.add_command(label="Vous n'êtes pas sur OBIWAN ?",command = self.creer_serveur_abs)
        
        #Cascade d'assemblage
        self.barre.add_cascade(label="Fichier", menu=self.file_menu)        
        self.barre.add_cascade(label="Base de données", menu=self.db_menu)
        self.barre.add_cascade(label="Aide", menu=self.aide_menu)

        self.main_w.config(menu=self.barre)

    def placerWidget(self):    
        #Text de selection
        self.select_txt = tk.Label(self.main_w, text = "Séléctionnez les deux espèces")
        self.select_txt.grid(row=0, column =0,columnspan = 4,padx = 10, pady =10, sticky = "nsew")

        #Separation
        self.separ = ttk.Separator(self.main_w,orient="horizontal")
        self.separ.grid(row=1, column = 0, columnspan=4, padx =10,pady = 10, sticky = "nsew")

        #Initialisation du combobox Espece1
        self.espece1 = tk.Label(self.main_w,text = "Espèce 1 ")
        self.espece1.grid(row = 2,column = 0,padx = 10, pady = 10, sticky="ew")

        self.espece1_menu = ttk.Combobox(self.main_w,values = self.esplist,height=4)
        self.espece1_menu.grid(row = 2,column = 1,columnspan=2, padx=10,pady=10,sticky="ew")

        self.espece1_menu.bind('<Key>',self.clavier_esp1)
        self.espece1_menu.bind('<Button-1>',self.clavier_esp1)

        #Initialisation du combobox Espece2
        self.espece2 = tk.Label(self.main_w, text ="Espèce 2 ")
        self.espece2.grid(row = 4,column = 0,padx=10,pady=10,sticky="ew")

        self.espece2_menu = ttk.Combobox(self.main_w, values = self.esplist,height = 4)
        self.espece2_menu.grid(row=4,column=1,columnspan=2,padx=10,pady=10,sticky="ew")
        
        self.espece2_menu.bind('<Key>',self.clavier_esp2)
        self.espece2_menu.bind('<Button-1>',self.clavier_esp2)
                
        #Bouton Infos sur les espèces
        self.infos_esp = tk.Button(self.main_w, text = "Infos esp",command=self.info_esp)
        self.infos_esp.grid(row=2,column = 3,rowspan = 2, padx = 10,pady =10,sticky="nsew")

        #Bouton Blast sur les espèces
        self.blast_esp = tk.Button(self.main_w, text = "Blast !",command=self.blast_esp)
        self.blast_esp.grid(row=3,column = 3,rowspan = 2, padx = 10,pady =10,sticky="nsew")

        #Deuxieme separateur
        self.separ2 = ttk.Separator(self.main_w,orient="horizontal")
        self.separ2.grid(row=5, column = 0, columnspan=4, padx =10,pady = 10, sticky = "nsew")

        #Text de choix
        self.select_txt = tk.Label(self.main_w, text = "Choisissez les conditions à appliquer")
        self.select_txt.grid(row=6, column =0,columnspan = 4,padx = 10, pady =10, sticky = "nsew")

        #Troisième separateur
        self.separ3 = ttk.Separator(self.main_w,orient="horizontal")
        self.separ3.grid(row=7, column = 0, columnspan=4, padx =10,pady = 10, sticky = "nsew")

        #Text de Blast
        self.blast_txt = tk.Label(self.main_w, text = "Conditions sur les critères BLAST")
        self.blast_txt.grid(row=8, column =0,columnspan = 4,padx = 10, pady =10, sticky = "nsew")

        #Checkboxes Blast
        self.var_hit = tk.BooleanVar(value=False)
        self.var_eval = tk.BooleanVar(value=False)
        self.var_ident = tk.BooleanVar(value=False)
        
        self.hit_cover = tk.Checkbutton(self.main_w,text = "Couverture du hit" ,variable = self.var_hit,offvalue=False,onvalue=True)
        self.blast_e_val = tk.Checkbutton(self.main_w,text = "E-value",variable=self.var_eval,offvalue=False,onvalue=True )
        self.ident = tk.Checkbutton(self.main_w,text = "Identité de séquence",variable=self.var_ident,offvalue=False,onvalue=True)
        
        self.hit_cover.grid(row = 9,column = 0,columnspan=2, padx = 10,pady=10,sticky="w")
        self.blast_e_val.grid(row = 10,column = 0,columnspan=2, padx = 10,pady=10,sticky="w")
        self.ident.grid(row = 11,column = 0,columnspan=2, padx = 10,pady=10,sticky="w")

        #Entry Blast

        self.hit_entry = tk.Entry(self.main_w,width=10)
        self.e_val_entry = tk.Entry(self.main_w,width=10)
        self.ident_entry = tk.Entry(self.main_w,width=10)
 
        self.label_hit = tk.Label(self.main_w, text="Seuil ->")
        self.label_hit.grid(row=9,column=2, columnspan = 1,padx = 10,pady=10,sticky="w")
        self.label_e = tk.Label(self.main_w, text="Seuil ->")
        self.label_e.grid(row=10,column=2, columnspan = 1, padx = 10,pady=10,sticky="w")
        self.label_ident = tk.Label(self.main_w, text="Seuil->")
        self.label_ident.grid(row=11,column=2, columnspan = 1, padx = 10,pady=10,sticky="w")

        self.hit_entry.grid(row = 9,column = 3, padx = 10,pady=10,sticky="e")
        self.e_val_entry.grid(row = 10,column = 3, padx = 10,pady=10,sticky="e")
        self.ident_entry.grid(row = 11,column = 3, padx = 10,pady=10,sticky="e")

        #Text de CD-Search
        self.cd_txt = tk.Label(self.main_w, text = "Conditions sur les critères CD-Search (en dev : non fonctionnel)")
        self.cd_txt.grid(row=12, column =0,columnspan = 4,padx = 10, pady =10, sticky = "nsew")

        #Checkboxes CD-Search
        self.var_func = tk.BooleanVar(value=False)
        self.var_fam = tk.BooleanVar(value=False)
        
        self.anno_func = tk.Checkbutton(self.main_w,text = "Annotation fonctionnelle COG " ,variable=self.var_func,offvalue=False,onvalue=True)
        self.anno_famille =  tk.Checkbutton(self.main_w,text = "Famille fonctionnelle",variable=self.var_fam,offvalue=False,onvalue=True)
        
        self.anno_func.grid(row = 13,column = 0, columnspan=2,padx = 10,pady=10,sticky="w")
        self.anno_famille.grid(row = 13,column = 2, columnspan=2,padx = 10,pady=10,sticky="w")

        #Plot style
        self.plot_label = tk.Label(self.main_w, text = "Style de plot ou Extraction")
        self.plot_label.grid(row=14, column=0,padx=10,pady=10,sticky = 'w')

        self.plot_label_cbx =  ttk.Combobox(self.main_w,values = self.plot_option_list,height=4)
        self.plot_label_cbx.grid(row = 14,column = 1,columnspan=2, padx=10,pady=10,sticky="ew")

        #Text de Stringence
        self.cd_txt = tk.Label(self.main_w, text = "Conditions sur les critères de stringence (réduction de bruit)")
        self.cd_txt.grid(row=15, column =0,columnspan = 4,padx = 10, pady =10, sticky = "nsew")

        self.taille_f_entry = tk.Entry(self.main_w,width = 10)
        self.label_taille_f = tk.Label(self.main_w, text="Taille de fenetre ->")
        self.label_taille_f.grid(row = 16,column = 0,columnspan=2, padx = 10,pady=10,sticky="w")
        self.taille_f_entry.grid(row = 16,column = 1, padx = 10,pady=10,sticky="e")

        self.stringence_entry = tk.Entry(self.main_w,width=10)
        self.label_stringence = tk.Label(self.main_w, text="Seuil->")
        self.label_stringence.grid(row = 16,column = 2,columnspan=2, padx = 10,pady=10,sticky="w")
        self.stringence_entry.grid(row = 16,column = 3, padx = 10,pady=10,sticky="e")

        #Bouton de lancement
        lancer_dp = tk.Button(self.main_w, text = "Lancer !",command=self.afficher_dotplot)
        lancer_dp.grid(row=17,column = 0,rowspan = 3,columnspan=4,padx = 10,pady =10,sticky="nsew")

        #Centrer les widgets
        self.main_w.columnconfigure(0 ,weight=1)
        self.main_w.columnconfigure(1,weight=1)
        self.main_w.columnconfigure(2,weight=1)     

    #FONCTIONS
    
    #Set de la base
    def set_db_name(self):
        #Check dans la base 
        conn = psycopg2.connect(dbname="postgres")
        cur=conn.cursor()

        cur.execute("SELECT datname FROM pg_database WHERE datname LIKE 'SHADOTAPP%'")
        db_extraction_list = cur.fetchall()
        conn.close()

        if db_extraction_list!=[]:
            self.database_name = db_extraction_list[0][0]
        else:
            self.database_name =  ""


    #Initialisation de la liste de espèces présentes dans la base
    def set_esp_list(self):
        
        if self.database_name!="":
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            #Recherche
            cur.execute("SELECT DISTINCT prokaryote_bank.name_org,prokaryote_bank.assembly_no FROM prokaryote_bank NATURAL JOIN proteines ORDER BY prokaryote_bank.name_org ASC;")

            #Recup result query
            esp_init = cur.fetchall()
            #Fermeture
            conn.close()

            if esp_init!=[]:
                #Stockage:
                self.esplist = [esp_init[i][0] for i in range(len(esp_init))]
                self.assembly = [esp_init[i][1] for i in range(len(esp_init))]

    #Mise a jour de la liste des espèces
    def update_esp(self):
        
        #Création d'une fenêtre toplevel 
        self.update_fenetre = tk.Toplevel(self.main_w)
        self.update_fenetre.title("Mise a jour de la liste de base des espèces")
        
        if self.database_name!="":

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            #Recherche
            cur.execute("SELECT prokaryote_bank.name_org,prokaryote_bank.assembly_no FROM prokaryote_bank WHERE NOT EXISTS (SELECT * FROM proteines WHERE proteines.name_org = prokaryote_bank.name_org AND proteines.assembly_no = prokaryote_bank.assembly_no) ORDER BY prokaryote_bank.name_org ASC;")

            #Recup result query
            esp_upd_list = cur.fetchall()
            
            #Stockage:
            self.upd_esplist = [esp_upd_list[i][0] for i in range(len(esp_upd_list))]
            self.upd_assembly = [esp_upd_list[i][1] for i in range(len(esp_upd_list))]
            upd_aff = [(esp_upd_list[i][0],esp_upd_list[i][1]) for i in range(len(esp_upd_list)) ] 

            #Fermeture
            conn.close()
            
            #Création de la listbox et du scrollbar
            lisesp = tk.Variable(value=upd_aff)
        
        else : 
            lisesp = []

        self.listbox = tk.Listbox(self.update_fenetre,listvariable= lisesp,selectmode=tk.SINGLE)
        self.scroll = tk.Scrollbar(self.update_fenetre, orient="vertical",command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)
                    
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.scroll.grid(row=0,column=1,sticky="ns")
        
        #Informations
        self.bouton_info = tk.Button(self.update_fenetre, text = "Infos",command=self.info_solo_esp)

        #Bouton Ajout
        self.bouton_ajout = tk.Button(self.update_fenetre, text = "Ajouter",command=self.ajout_dans_esplist_et_maj)

        self.bouton_info.grid(row=1,column = 0, pady=10,padx=(10,5))
        self.bouton_ajout.grid(row=1,column = 1, pady=10,padx=(5,10))
        
        #Dimensionnement
        self.update_fenetre.rowconfigure(0,weight=1)
        self.update_fenetre.columnconfigure(0,weight=1)
        self.listbox.rowconfigure(0,weight=1)
        self.listbox.columnconfigure(0,weight=1)

        self.update_fenetre.geometry("300x300")
        self.update_fenetre.mainloop()

    #Connaître l'information pour une espèce
    def info_solo_esp(self):
        
        #Récupération de la valeur choisie dans la listbox
        if self.listbox.curselection()!=():
            
            index_selection = self.listbox.curselection()[0]

            esp_selection = self.listbox.get(index_selection)
            
            #Recuperation infos esp
            info_esp = ()

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            #Recherche
            if esp_selection!="Vide":
                cur.execute("SELECT * FROM prokaryote_bank WHERE name_org ='"+self.upd_esplist[index_selection]+"' AND assembly_no = '"+ self.upd_assembly[index_selection]+"';")
                a = cur.fetchall()
                info_esp = a[0]
            
            #Fermeture
            conn.close()

        else: 
            info_esp = ('Non choisi','-','-','-','-','-','-','-','-')
        
        liste_specs = ["Nom : ","Organisme : ","Biosample : ","BioProject : ","Assembly_no : ","Taille (Mb) : ","Taux de GC (%)","Nombre de CDS : ","Lien FTP :" ]
        


        #Creation d'une fenetre et affichage des informations
        #Preparation des listes pour iteration
        fenetre_type = {"padx" : 10, "pady" : 10,"borderwidth":1,"relief":"solid"}
        label_type = {"font": ("Arial",11), "anchor" :"w"}            
        liste_labels = ["Informations","Espèce"]
        col_correction=[0,2]
        
        self.info_fenetre = tk.Toplevel(self.update_fenetre)
        
        #Création des frames pour chaque espece
        self.esp_frames = [tk.Frame(self.info_fenetre,**fenetre_type) for _ in range(2)]
        
        #Création de chaque espace
        for i, esp_frame in enumerate(self.esp_frames):
            
            esp_frame.grid(row = 0, column=col_correction[i], sticky="nsew")
            
            tk.Label(esp_frame, text=liste_labels[i],**label_type).grid(row=0,column=0)
            
            #Initialiser la colonne d'informations
            if i==0:
                for j in range(9):
                    tk.Label(esp_frame, text=liste_specs[j],**label_type).grid(row=j+1,column=0)
            #Initialiser la colonne des espèces
            if i!=0:
                for j in range(9):
                    tk.Label(esp_frame, text=str(info_esp[j]),**label_type).grid(row=j+1,column=0)

        #Séparateurs

        self.sep_espv1 = ttk.Separator(self.info_fenetre, orient="vertical")
        self.sep_espv1.grid(row=0,column=1, rowspan = 9, padx=10, sticky="ns")

        self.info_fenetre.mainloop()

    #Ajout de l'espèce choisie dans la base
    def ajout_dans_esplist_et_maj(self):
        
        if self.listbox.curselection()!=():
            #Récupérer la valeur
            index_selection = self.listbox.curselection()[0]

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            cur.execute("SELECT ftp_link FROM prokaryote_bank WHERE name_org ='"+self.upd_esplist[index_selection]+"' AND assembly_no='"+self.upd_assembly[index_selection]+"';")
            
            #Telechargement du fichier faa
            url = cur.fetchall()[0][0]
            lastpart = url.split("/")[-1]
            gzfilename = lastpart+"_translated_cds.faa.gz"
            finalfilename =  lastpart+"_translated_cds.faa"
            finalurl = url+"/"+gzfilename

            #Récupération et extraction
            subprocess.run(["wget", finalurl])
            subprocess.run(["gzip","-d",gzfilename])

            #Lecture et ajout du fichier dans la table proteomes

            with open(finalfilename,'r') as file:
                id = ""
                seq =""
                filename = self.upd_assembly[index_selection]
                rank = 1
                for line in file:
                    
                    #Parcours de chaque ligne
                    line = line.strip()
                    if line[0]==">":
                        if id!="":
                            cur.execute("INSERT INTO proteines(protein_id,seq,len,assembly_no,rank) VALUES (%s,%s,%s,%s,%s);",(id,seq,len(seq),filename,rank))
                            id = ""
                            seq = ""
                            rank+=1

                        id = re.search(r"lcl\|(\S+)", line).group(1)
                    else: 
                        seq+=line
                
                cur.execute("INSERT INTO proteines(protein_id,seq,len,assembly_no,rank) VALUES (%s,%s,%s,%s,%s);",(id,seq,len(seq),filename,rank))
                cur.execute("UPDATE proteines SET name_org=prokaryote_bank.name_org FROM prokaryote_bank WHERE proteines.assembly_no = prokaryote_bank.assembly_no AND proteines.name_org IS NULL;")

                conn.commit()

            conn.close()

            subprocess.run(["rm",finalfilename])

            #Mise a jour des listes esplist et assembly
            self.esplist.append(self.upd_esplist.pop(index_selection))
            self.assembly.append(self.upd_assembly.pop(index_selection))
            
            self.listbox.delete(index_selection)

    #Fenetre de sélection de blast dans la base
    def bl_fenetre(self):
        
        self.blast_fenetre = tk.Toplevel(self.main_w)
        self.blast_fenetre.title("Liste de BLAST dans la base")
        
        #Création listbox
        self.listbox = tk.Listbox(self.blast_fenetre,selectmode=tk.SINGLE)

        if self.database_name!="":
            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            #Recherche
            cur.execute("SELECT DISTINCT blast_results.blast_exec_number, proteine1.name_org, proteine1.assembly_no, proteine2.name_org, proteine2.assembly_no FROM blast_results LEFT JOIN proteines AS proteine1 ON blast_results.query_seqid = proteine1.protein_id LEFT JOIN proteines AS proteine2 ON blast_results.subject_seqid = proteine2.protein_id ORDER by blast_results.blast_exec_number;")
            #Recup result query
            blast_res_base= cur.fetchall()
            
            #Fermeture
            conn.close()


            for ligne in blast_res_base:
                fusion_ligne = ligne[1]+" : "+ligne[2]+" ||| "+ligne[3]+ " : "+ligne[4]
                format_ligne = [f"{ligne[0]:^15}",fusion_ligne]
                self.listbox.insert(tk.END,format_ligne)

        #Création scrollbar
        self.scroll = tk.Scrollbar(self.blast_fenetre, orient="vertical",command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)

        #Création des labels d'intitulé
        self.b1= tk.Label(self.blast_fenetre, text = "N°Blast",relief="solid",width = 10)
        self.b2= tk.Label(self.blast_fenetre, text = "Nom Organisme Query : Assembly n° ||| Nom Organisme Subject : Assembly n°",relief="solid",width = 120)

        self.b1.grid(row=0,column=0,sticky="w")
        self.b2.grid(row=0,column=1,sticky="ew")
        
        self.listbox.grid(row=1, column=0,columnspan = 2,sticky="nsew")
        self.scroll.grid(row=1,column=2,sticky="ns")
        
        #Label d'affichage de séléction
        self.bouton_select_aff = tk.Label(self.blast_fenetre,text ="Blast sélectionné : "+str(self.bl_selection))
        
        #Bouton de séléction
        self.bouton_select = tk.Button(self.blast_fenetre, text = "Selectionner",command=self.blast_select)
        self.bouton_select.grid(row=2,column = 0,columnspan=1, pady=10,padx=(10,5))
        
        self.bouton_select_aff.grid(row=2,column = 1, columnspan=1,pady=10)

        #Dimensionnement
        self.blast_fenetre.rowconfigure(0,weight=0)
        self.blast_fenetre.rowconfigure(1,weight=1)

        self.blast_fenetre.columnconfigure(0,weight=0)
        self.blast_fenetre.columnconfigure(1,weight=1)

        self.blast_fenetre.mainloop()

    #Récupération de la valeur de séléction
    def blast_select(self):
        if self.listbox.curselection()!=():
            index_selection = self.listbox.curselection()[0]
            self.bl_selection = int(self.listbox.get(index_selection)[0])
            self.bouton_select_aff.config(text = "Blast sélectionné : "+str(self.bl_selection))

            
    #Creation d'une nouvelle base
    def creer_serveur_abs(self):
        
        #Création de fenetre 
        self.bd = tk.Toplevel(self.main_w)
        
        self.bd.minsize(700,350)
        
        self.bd.title("Création de base de données")

        #Partie explications
        self.explication1_label = tk.Label(self.bd, text = "Vous êtes ici car vous n'êtes pas sur le serveur OBIWAN et que vous voulez avoir la base de données sur votre poste.\n\n Pour cela, comme précisé dans le Readme, vous devez être en possession du logiciel PostgreSQL.\n\n Si c'est le cas, vous allez pouvoir créer votre base de données avec les fichiers intiaux fournis.\n\n")
        self.explication1_label.grid(row = 0,column=0,columnspan =2,padx = 10, pady = 10,sticky = 'ew')
        
        self.nom_bd_label = tk.Label(self.bd, text = "Veuillez définir un nom pour votre base -> ")
        self.nom_bd_label.grid(row=1,column=0,padx=10,pady=10,sticky='w')

        self.nom_bd_entry = tk.Entry(self.bd,width = 40)
        self.nom_bd_entry.grid(row = 1,column=1,padx=10, pady=10, sticky='w')

        self.presence_label = tk.Label(self.bd, text = "Saisissez le nom dans la barre ci-dessus puis appuyez sur Vérification")
        self.presence_label.grid(row = 2,column=0, columnspan =1,padx = 10, pady = 10,sticky = 'w')           

        #Bouton de vérification
        self.presence_bt = tk.Button(self.bd, text="Vérification", command=self.verif_presence_bd)
        self.presence_bt.grid(row = 2, column = 1, columnspan = 1, padx=10,pady=10, sticky = 'nsew')

        self.explication2_label = tk.Label(self.bd, text = "\nAppuyez sur le bouton Créer pour lancer la création de la base.\nVous pouvez suivre l'avancée de la création sur le terminal qui ne prendra au maximum 30 secondes.\n\n")
        self.explication2_label.grid(row = 3,column=0, columnspan =2,padx = 10, pady = 10,sticky = 'ew')

        #Bouton de création
        self.creation_bt = tk.Button(self.bd, text="Créer", command=self.import_bd)
        self.creation_bt.grid(row = 4, column = 0, columnspan = 2, padx=10,pady=10, sticky = 'nsew')           

        self.bd.grid_columnconfigure(0,weight=1)
        self.bd.mainloop()

    #Vérification de présence dans la base
    def verif_presence_bd(self):
        
        if self.database_name=="":
            nom = self.nom_bd_entry.get()
            if nom!="SHADOTAPP":
                nom = "SHADOTAPP-"+self.nom_bd_entry.get()

            #Check dans la base 
            conn = psycopg2.connect(dbname="postgres")
            cur=conn.cursor()

            cur.execute("SELECT 1 FROM pg_database WHERE datname ='"+str(nom)+"';")
            test = cur.fetchone()

            conn.close()

            if test is None:
                self.presence_label.config(text = "Nom de base de données DISPONIBLE")
                self.creation_bt.config(state="normal")
        
        if self.database_name!="": 
            self.presence_label.config(text = "Inutile de créer : BASE EXISTANTE POUR L'APP")
            self.creation_bt.config(state="disabled")


    #Fonction d'importation de la base
    def import_bd(self):

        self.verif_presence_bd()
        
        if self.database_name=="":
            #Récupération du nom de la base
            database_name = "SHADOTAPP-"+self.nom_bd_entry.get()

            start = time.time()

            #Création de la base, des tables et injection des données

            print("Création de la base vide ...")
            subprocess.run(["createdb",database_name])
            print("Base vide crée !")

            print("Connexion à la base...")
            conn = psycopg2.connect("dbname = "+database_name)
            cur = conn.cursor()

            print("Création de la table famille...")
            cur.execute("""CREATE TABLE famille(
                            family_code TEXT PRIMARY KEY,
                            family TEXT
                        );""")

            print("Création de la table cog_identification...")
            cur.execute("""CREATE TABLE cog_identification(
                            cog_id TEXT,
                            family_code TEXT REFERENCES famille,
                            cog_function  TEXT,
                            CONSTRAINT cog_identification_pkey PRIMARY KEY(cog_id,family_code)
                        );""")
            
            print("Création de la table prokaryote_bank...")
            cur.execute("""CREATE TABLE prokaryote_bank(
                            name_org TEXT,
                            organism_group TEXT,
                            biosample TEXT,
                            bioproject TEXT,
                            assembly_no TEXT,
                            size_mb FLOAT,
                            gc_percent FLOAT,
                            nb_cds INTEGER,
                            ftp_link TEXT,
                            CONSTRAINT prokaryote_bank_pkey PRIMARY KEY(name_org,assembly_no) 
                        ); """)
            
            print("Création de la table proteines...")
            cur.execute("""CREATE TABLE proteines(
                            protein_id TEXT,
                            seq TEXT,
                            len INTEGER,
                            name_org TEXT,
                            assembly_no TEXT,
                            rank INTEGER,
                            CONSTRAINT proteines_pkey PRIMARY KEY(protein_id),
                            CONSTRAINT proteines_fkey FOREIGN KEY(name_org,assembly_no) REFERENCES prokaryote_bank(name_org,assembly_no) ON UPDATE CASCADE ON DELETE CASCADE
                            );""")
            print("Création de la table blast_results...")
            cur.execute("""CREATE TABLE blast_results(
                            blast_exec_number INTEGER,
                            blast_rank INTEGER,
                            query_seqid TEXT REFERENCES proteines(protein_id),
                            subject_seqid TEXT REFERENCES proteines(protein_id),
                            percent_ident FLOAT,
                            b_length INTEGER,
                            gapopen INTEGER,
                            mismatch INTEGER,
                            q_start INTEGER,
                            q_end INTEGER,
                            s_start INTEGER,
                            s_end INTEGER,
                            blast_e_val FLOAT,
                            blast_bitscore FLOAT,
                            cover_q FLOAT,
                            cover_s FLOAT,
                            CONSTRAINT blast_pkey PRIMARY KEY(blast_exec_number,blast_rank,query_seqid,subject_seqid)
                            );""")
            
            print("Les tables sont créees !")
            
            print("Remplissage de la table famille ...")
            with open('.Base/Cog_ProkBank/fun2003-2014.tab.txt','r') as file:
                
                #zapper le header
                next(file)

                for line in file:
                    
                    #Parcours de chaque ligne
                    colonne = line.split()
                
                    cur.execute("INSERT INTO famille (family_code,family) VALUES (%s,%s)",(colonne[0],colonne[1])) 
                
                #Renvoi a la base
                conn.commit()
            
            print("Remplissage de la table cog_identification ...")
            with open('.Base/Cog_ProkBank/cognames2003-2014.tab.txt','r') as file:
                
                #zapper le header
                next(file)

                for line in file:
                    
                    #Parcours de chaque ligne
                    colonne = line.split()
                    
                    #Séparation utile pour la catégorie fonctionnelle
                    for i in colonne[1]:
                        cur.execute("INSERT INTO cog_identification (cog_id,family_code,cog_function) VALUES (%s,%s,%s);",(colonne[0],i,colonne[2])) 

                #Renvoi a la base
                conn.commit()
                
            print("Remplissage de la table prokaryote_bank ...")
            with open('.Base/Cog_ProkBank/prokaryotes_complete-genomes.csv','r') as file:

                csvfile = csv.reader(file)

                #zapper le header
                next(csvfile)

                for colonne in csvfile:
                    #Parcours de chaque ligne
                    cur.execute("INSERT INTO prokaryote_bank (name_org,organism_group,biosample,bioproject,assembly_no,size_mb,gc_percent,nb_cds,ftp_link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",(colonne[0],colonne[1],colonne[3],colonne[4],colonne[5],colonne[7],colonne[8],colonne[12],colonne[14])) 

                #Renvoi a la base
                conn.commit()                
            cur.execute("DELETE FROM prokaryote_bank WHERE ftp_link=''")

            print("Remplissage de la table proteines ...")
            
            prot_number = 1
            prot_path = '.Base/Proteomes'
            for faa in os.listdir(prot_path):
                print("Traitement du fichier n°",prot_number)
                faa_name = os.path.join(prot_path,faa)
                with open(faa_name,'r') as file:
                        print(faa_name)
                        id = ""
                        seq =""
                        filename = re.search(r"./(GCA_\d{9}\.\d)_.*", faa_name).group(1)
                        rank = 1
                        for line in file:
                            
                            #Parcours de chaque ligne
                            line = line.strip()
                            if line[0]==">":
                                if id!="":
                                    cur.execute("INSERT INTO proteines(protein_id,seq,len,assembly_no,rank) VALUES (%s,%s,%s,%s,%s);",(id,seq,len(seq),filename,rank))
                                    id = ""
                                    seq = ""
                                    rank+=1

                                id = re.search(r"lcl\|(\S+)", line).group(1)
                            else: 
                                seq+=line
                        
                        cur.execute("INSERT INTO proteines(protein_id,seq,len,assembly_no,rank) VALUES (%s,%s,%s,%s,%s);",(id,seq,len(seq),filename,rank))
                        cur.execute("UPDATE proteines SET name_org=prokaryote_bank.name_org FROM prokaryote_bank WHERE proteines.assembly_no = prokaryote_bank.assembly_no AND proteines.name_org IS NULL;")

                        conn.commit()
                
                prot_number+=1
            
            print("Remplissage de la table blast_results ...")
            blastp_number = 1
            blastp_path = '.Base/Blastp'
            for blastp in os.listdir(blastp_path):
                print("Traitement du fichier n° ",blastp_number)
                blastp_name = os.path.join(blastp_path,blastp)
                
                blastp_rank  = 1
                with open(blastp_name,'r') as file:
                    
                    #zapper le header
                    next(file)
                    for line in file:
                        
                        #Parcours de chaque ligne
                        colonne = line.split()
                        id1 = re.search(r"lcl\|(\S+)", colonne[0]).group(1)

                        cur.execute("INSERT INTO blast_results (blast_exec_number,blast_rank,query_seqid,subject_seqid,percent_ident,b_length,mismatch,gapopen,q_start,q_end,s_start,s_end,blast_e_val,blast_bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(blastp_number,blastp_rank,id1,colonne[1],colonne[2],colonne[3],colonne[4],colonne[5],colonne[6],colonne[7],colonne[8],colonne[9],colonne[10],colonne[11])) 
                        
                        blastp_rank +=1
                    conn.commit()

                cur.execute("UPDATE blast_results SET cover_q = trunc(((q_end-q_start)::float/ proteines.len)*1000)/1000  FROM proteines WHERE blast_results.query_seqid=proteines.protein_id ;")
                cur.execute("UPDATE blast_results SET cover_s = trunc(((s_end-s_start)::float/ proteines.len)*1000)/1000  FROM proteines WHERE blast_results.subject_seqid=proteines.protein_id ;")

                conn.commit()

                blastp_number+=1

            conn.close()

            end = time.time()
            temps = end-start

            #Mise a jour des instances 
            self.database_name = database_name
            self.set_esp_list()
            print(f"\nBase remplie !\nTemps de remplissage de la base : {temps} seconds\n")

            self.bd.destroy()

    #Filtrage des saisies des especes
    def filtrage_continu(self,var):
        search = var.get()
        espece_filtre = [esp for esp in self.esplist if esp.lower().startswith(search) or esp.startswith(search) ]
        if search!='':
            var["values"] = espece_filtre
        else:
            var["values"] = self.esplist

    #Association évenement et mise a jour de la barre
    def clavier_esp1(self,evt):
        self.filtrage_continu(self.espece1_menu)

    #Association evenement et mise à jour de la barre
    def clavier_esp2(self,evt):
        self.filtrage_continu(self.espece2_menu)

    def info_esp(self):        
        #Récupération index Espece 1
        esp1_choisi = self.espece1_menu.get()
        index_assembly_esp1 = self.espece1_menu.current()
        if index_assembly_esp1==-1:
            esp1_choisi  = "Vide"
        
        count1 = 0
        for i in range(index_assembly_esp1):
            if self.esplist[i] == esp1_choisi:
                count1 +=1
        
        index_f_esp1 = index_assembly_esp1 - count1

        
        #Récupération index Espece 2
        esp2_choisi = self.espece2_menu.get()
        index_assembly_esp2 = self.espece2_menu.current()
        if index_assembly_esp2==-1:
            esp2_choisi  = "Vide"
        
        count2 = 0
        for i in range(index_assembly_esp2):
            if self.esplist[i] == esp2_choisi:
                count2 +=1
        
        index_f_esp2 = index_assembly_esp2 - count2
        
        #Récupération infos esp1 et esp2 
        info_esp1 = ()
        info_esp2 = ()

        liste_info = [info_esp1,info_esp2]            
        liste_index_f = [index_f_esp1, index_f_esp2]
        liste_choix = [esp1_choisi,esp2_choisi]

        if self.database_name!="":
            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            #Recherche
            for i in range(2):
                if liste_choix[i]!="Vide":
                    cur.execute("SELECT * FROM prokaryote_bank WHERE name_org ='"+self.esplist[liste_index_f[i]]+"' AND assembly_no = '"+ self.assembly[liste_index_f[i]]+"';")
                    a = cur.fetchall()
                    liste_info[i] = a[0]

                else: 
                    liste_info[i] = ('Non choisi','-','-','-','-','-','-','-','-')
        
            #Fermeture
            conn.close()
        
        else :
           
           liste_info = [('Non existant ','-','-','-','-','-','-','-','-') for i in range(2)]      
        
        liste_specs = ["Nom : ","Organisme : ","Biosample : ","BioProject : ","Assembly_no : ","Taille (Mb) : ","Taux de GC (%)","Nombre de CDS : ","Lien FTP :" ]

        
        #Création d'une fenetre et affichage des informations
        #Préparation des listes pour itération
        fenetre_type = {"padx" : 10, "pady" : 10,"borderwidth":1,"relief":"solid"}
        label_type = {"font": ("Arial",11), "anchor" :"w"}            
        liste_labels = ["Informations","Espèce 1", "Espèce 2"]
        col_correction=[0,2,4]
        
        self.info_fenetre = tk.Toplevel(self.main_w)
        
        #Création des frames pour chaque espece
        self.esp_frames = [tk.Frame(self.info_fenetre,**fenetre_type) for _ in range(3)]
        
        #Création de chaque espace
        for i, esp_frame in enumerate(self.esp_frames):
            
            esp_frame.grid(row = 0, column=col_correction[i], sticky="nsew")
            
            tk.Label(esp_frame, text=liste_labels[i],**label_type).grid(row=0,column=0)
            
            #Initialiser la colonne d'informations
            if i==0:
                for j in range(9):
                    tk.Label(esp_frame, text=liste_specs[j],**label_type).grid(row=j+1,column=0)
            #Initialiser la colonne des espèces
            if i!=0:
                for j in range(9):
                    tk.Label(esp_frame, text=str(liste_info[i-1][j]),**label_type).grid(row=j+1,column=0)

        #Séparateurs

        sep_espv1 = ttk.Separator(self.info_fenetre, orient="vertical")
        sep_espv1.grid(row=0,column=1, rowspan = 9, padx=10, sticky="ns")

        sep_espv2 = ttk.Separator(self.info_fenetre, orient="vertical")
        sep_espv2.grid(row=0,column=3, rowspan = 9, padx=10, sticky="ns")

        self.info_fenetre.mainloop()

    #Execution blast
    def blast_esp(self):

        #Récupération index Espece 1
        esp1_choisi = self.espece1_menu.get()
        index_assembly_esp1 = self.espece1_menu.current()
        if index_assembly_esp1==-1:
            esp1_choisi  = "Vide"
        
        count1 = 0
        for i in range(index_assembly_esp1):
            if self.esplist[i] == esp1_choisi:
                count1 +=1
        
        #Récupération du bon indice
        index_f_esp1 = index_assembly_esp1 - count1

        
        #Récupération index Espece 2
        esp2_choisi = self.espece2_menu.get()
        index_assembly_esp2 = self.espece2_menu.current()
        if index_assembly_esp2==-1:
            esp2_choisi  = "Vide"
        
        count2 = 0
        for i in range(index_assembly_esp2):
            if self.esplist[i] == esp2_choisi:
                count2 +=1
        
        #Récupération du bon indice
        index_f_esp2 = index_assembly_esp2 - count2

        if esp1_choisi!="Vide" and esp2_choisi!="Vide":
            #Récupération infos esp1 et esp2
            ftp1 = ""
            ftp2 = "" 
            liste_ftp = [ftp1,ftp2]
            liste_lastpart = ["",""]      
            liste_gz = ["",""]      
            liste_index_f = [index_f_esp1, index_f_esp2]
            liste_choix = [esp1_choisi,esp2_choisi]
            liste_faa = ["",""]

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            print("Récupération des fichiers ...")
            #Recherche
            for i in range(2):
                cur.execute("SELECT ftp_link FROM prokaryote_bank WHERE name_org ='"+liste_choix[i]+"' AND assembly_no='"+self.assembly[liste_index_f[i]]+"';")
                liste_ftp[i] = cur.fetchall()[0][0]
                liste_lastpart[i] = liste_ftp[i].split("/")[-1]
                liste_gz[i] = liste_lastpart[i]+"_translated_cds.faa.gz"
                liste_faa[i] = liste_lastpart[i]+"_translated_cds.faa"
                liste_ftp[i] = liste_ftp[i]+"/"+liste_gz[i]

                #Récupération et extraction
                subprocess.run(["wget", liste_ftp[i]])
                subprocess.run(["gzip","-d",liste_gz[i]])
                        
            nom_sortie_blast = "QUERY-"+liste_faa[0]+"__DB-"+liste_faa[1]+".out"

            print("Blast en cours : environ 2 minutes")
            #Blast execution
            subprocess.run(["blastp", "-query",liste_faa[0],"-subject",liste_faa[1],"-evalue", "1e-4", "-out",nom_sortie_blast,"-outfmt","6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"]) 
            print("Blast fini !")

            cur.execute("SELECT COUNT(DISTINCT(blast_exec_number)) FROM blast_results;")
            blastnum = cur.fetchall()[0][0]+1

            print("Ajout dans la base...")
            #Injection du blast dans la base
            with open(nom_sortie_blast,'r') as file:
                
                #zapper le header
                #next(file)
                rank = 1
                for line in file:
                    
                    #Parcours de chaque ligne
                    colonne = line.split()
                    id1 = re.search(r"lcl\|(\S+)", colonne[0]).group(1)
                    id2 = re.search(r"lcl\|(\S+)", colonne[1]).group(1) 

                    #Séparation utile pour la catégorie fonctionnelle
                    cur.execute("INSERT INTO blast_results (blast_exec_number,blast_rank,query_seqid,subject_seqid,percent_ident,b_length,mismatch,gapopen,q_start,q_end,s_start,s_end,blast_e_val,blast_bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(blastnum,rank,id1,id2,colonne[2],colonne[3],colonne[4],colonne[5],colonne[6],colonne[7],colonne[8],colonne[9],colonne[10],colonne[11])) 
                    rank+=1
                #Renvoi a la base
                conn.commit()

            cur.execute("UPDATE blast_results SET cover_q = trunc(((q_end-q_start)::float/ proteines.len)*1000)/1000  FROM proteines WHERE blast_results.query_seqid=proteines.protein_id ;")
            cur.execute("UPDATE blast_results SET cover_s = trunc(((s_end-s_start)::float/ proteines.len)*1000)/1000  FROM proteines WHERE blast_results.subject_seqid=proteines.protein_id ;")

            conn.commit()

            conn.close()
            print("Blast ajouté !")
            
            subprocess.run(["rm",liste_faa[0]])
            subprocess.run(["rm",liste_faa[1]])
            subprocess.run(["rm",nom_sortie_blast])

    #Lancement        
    def afficher_dotplot(self,*args):
        
        #Stockage identitié blast
        blastno = self.bl_selection
        
        #Valeur par défaut
        self.defaulteval = 1e-30
        self.listetxt = []
        #Ligne de commande prete
        self.commandline = "SELECT p1.rank, p2.rank, p1.name_org,p2.name_org,blast_results.query_seqid, blast_results.subject_seqid,blast_results.blast_e_val FROM blast_results JOIN proteines AS p1 ON blast_results.query_seqid = p1.protein_id JOIN proteines AS p2 ON blast_results.subject_seqid = p2.protein_id WHERE blast_exec_number = "+str(blastno)+""
        
        #Vérification des checkboxes et valeurs
        if self.var_ident.get()==True and self.ident_entry.get()!="":
            self.commandline = self.commandline+" AND percent_ident>"+str(self.ident_entry.get())+""
            self.listetxt.append(str(self.ident_entry.get()))
        
        else : 
            self.listetxt.append("None")

        if self.var_hit.get()==True and self.hit_entry.get()!="":
            self.commandline = self.commandline+" AND cover_q>"+str(self.hit_entry.get())+" AND  cover_s>"+str(self.hit_entry.get())+""
            self.listetxt.append(str(self.hit_entry.get()))

        else : 
            self.listetxt.append("None")

        if self.var_eval.get()==True and self.e_val_entry.get()!="":
            self.commandline = self.commandline +" AND blast_e_val<"+str(self.e_val_entry.get())+""
            self.listetxt.append(str(self.e_val_entry.get()))

        if self.var_ident.get()==self.var_hit.get()==self.var_eval.get()==False:
            self.commandline = self.commandline +" AND blast_e_val<"+str(self.defaulteval)+""
            self.listetxt.append(str(self.defaulteval))
 
        self.commandline = self.commandline+";"

        #Récupération de la taille fenetre et seuil de stringence
        
        if ((self.taille_f_entry.get()!="" and self.taille_f_entry.get().isdigit()) and (self.stringence_entry.get()!="") and self.stringence_entry.get().isdigit()) and blastno!=0:

            self.taille_fen = int(self.taille_f_entry.get())
            self.seuil_strin = int(self.stringence_entry.get())

            self.listetxt.append(str(self.taille_f_entry.get()))
            self.listetxt.append(str(self.stringence_entry.get()))


            if self.taille_fen>=self.seuil_strin and self.taille_fen>0 and self.seuil_strin>0:

                #Connexion
                conn = psycopg2.connect("dbname="+self.database_name+"")
                #Curseur
                cur = conn.cursor()

                #Recherche
                cur.execute(self.commandline)

                #Récup résult query
                blast_test = np.array(cur.fetchall())
                name_query = blast_test[0][2]
                name_subject = blast_test[0][3]
                
                #récupération nombre de prot dans chaque 

                cur.execute("SELECT COUNT(*) FILTER (WHERE proteines.name_org = '"+name_query +"') AS count_p1, COUNT(*) FILTER (WHERE proteines.name_org = '"+name_subject +"') AS count_p2 FROM proteines;")
                len_x,len_y  = cur.fetchall()[0]

                #Fermeture
                conn.close()

                if self.taille_fen<min(len_x,len_y):

                    c_l = np.array(blast_test[:, :2]).astype(int)
                    c_l = c_l-1

                    #Algorithme de stringence
                    def window_matrix_numpy(c_arr,len_x,len_y, fenetre, seuil):
                        matrice_i = np.zeros((len_x,len_y),dtype=np.int8)
                        for i in range(c_arr.shape[0]):
                            matrice_i[c_arr[i,0],c_arr[i,1]] = 1

                        matrice_copy = copy.deepcopy(matrice_i)

                        for i in range(fenetre):
                            matrice_copy[:len_x-i,:len_y-i] = matrice_copy[:len_x-i,:len_y-i] + matrice_i[i:,i:]
                        
                        matrice_bool = matrice_copy >=seuil
                        matrice_show = matrice_bool.astype(int)
                        
                        x,y = np.where(matrice_copy >=seuil)

                        return matrice_show,x,y
                    
                    mat_show,x,y = window_matrix_numpy(c_l,len_x,len_y,self.taille_fen,self.seuil_strin)

                    #Affichage en scatter
                    if self.plot_label_cbx.get()=="scatter":
                        plt.figure(figsize=(5,5))
                        plt.gca().invert_yaxis()
                        plt.gca().set_facecolor('#000033')
                        plt.scatter(x,y,s=0.01,c = '#FFFF00')
                        plt.title('Dotplot en Scatter : Vue globale')
                        plt.xlabel(name_query)
                        plt.ylabel(name_subject)
                        plt.show()

                    #Affichage avec imshow
                    if self.plot_label_cbx.get()=="imshow":
                        plt.figure(figsize=(5,5))
                        plt.gca().invert_yaxis()
                        plt.gca().set_facecolor('#000033')

                        ny = ['#000033','#FFFF00']
                        cmap = mc.LinearSegmentedColormap.from_list('NY',ny)
                        plt.title('Dotplot en ImShow : Vue précise')
                        im = plt.imshow(mat_show, cmap = cmap)
                        plt.xlabel(name_query)
                        plt.ylabel(name_subject)
                        plt.show()

                    #Stockage dans un fichier
                    if self.plot_label_cbx.get()=="txt : peut aller jusqu'à 20 Mo":
                        x = x+1
                        y = y+1

                        tx = tuple(x.tolist())
                        ty = tuple(y.tolist())

                        conn = psycopg2.connect("dbname=raneproj")

                        #Curseur
                        cur = conn.cursor()

                        #Recherche
                        cur.execute("""SELECT  * FROM blast_results
                                JOIN proteines AS p1 ON blast_results.query_seqid = p1.protein_id 
                                JOIN proteines AS p2 ON blast_results.subject_seqid = p2.protein_id 
                                WHERE blast_exec_number = '1' AND p1.rank IN """+str(tx)+""" AND p2.rank IN """+str(ty)+""" ;""")


                        #Récup résult query
                        stringence_copy = cur.fetchall()
                        conn.close()

                        print(self.listetxt)

                        filename = "Stringence_Text/Stringence_Blast_"+str(blastno)+"_"+str(stringence_copy[0][20])+"_"+str(stringence_copy[0][26])+".txt"
                        with open(filename, 'w') as file:
                            file.write("ShaDotApp : Résultats de la stringence suite au blast n°"+str(blastno)+"\n\n")
                            file.write("Organisme query : "+str(stringence_copy[0][19])+"\n")
                            file.write("Assembly query : "+str(stringence_copy[0][20])+"\n")
                            file.write("Organisme subject : "+str(stringence_copy[0][25])+"\n")
                            file.write("Assembly subject : "+str(stringence_copy[0][26])+"\n\n")
                            file.write("Conditions :\n")
                            file.write("\tCouverture du hit : "+self.listetxt[1]+"\n")
                            file.write("\tE-value : "+self.listetxt[2]+"\n")
                            file.write("\tPourcentage d'identité : "+self.listetxt[0]+"\n")
                            file.write("\tTaille de fenêtre: "+self.listetxt[3]+"\n")
                            file.write("\tSeuil de Stringence : "+self.listetxt[4]+"\n\n")


                            file.write("Protein query\tQuery length\tProtein subject\tSubject length\t\n")
                            file.write("Blast_length\tIdentity percentage\tGapopen\tMismatch\tQ_start\tQ_end\tS_start\tS_end\tCover_Q\tCover_S\tE-value\tBitscore\t\n")
                            file.write("Sequence query\n")
                            file.write("Sequence subject\n\n")
                            
                            for i in range(len(stringence_copy)):
                                file.write("["+str(stringence_copy[i][2])+"]\t["+str(stringence_copy[i][18])+"]\t["+str(stringence_copy[i][3])+"]\t["+str(stringence_copy[i][24])+"]\n")
                                file.write("["+str(stringence_copy[i][5])+"]\t["+str(stringence_copy[i][4])+"]\t["+str(stringence_copy[i][6])+"]\t["+str(stringence_copy[i][7])+"]\t["+str(stringence_copy[i][8])+"]\t["+str(stringence_copy[i][9])+"]\t["+str(stringence_copy[i][10])+"]\t["+str(stringence_copy[i][11])+"]\t["+str(stringence_copy[i][14])+"]\t["+str(stringence_copy[i][15])+"]\t["+str(stringence_copy[i][12])+"]\t["+str(stringence_copy[i][13])+"]\n")
                                file.write("Q>"+str(stringence_copy[i][17])+"\n")
                                file.write("S>"+str(stringence_copy[i][23])+"\n\n")

                            file.close()
                        
                        print("Extraction faite avec succès !")

test = Dotplot()
