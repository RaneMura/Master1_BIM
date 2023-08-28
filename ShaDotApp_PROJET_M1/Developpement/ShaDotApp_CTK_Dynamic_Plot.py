from tkinter.messagebox import YES
import psycopg2
import subprocess
import tkinter as tk
from tkinter import Y, filedialog as fd
from tkinter import ttk
import os
import re
import copy
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from sklearn.cluster import KMeans

#Apparence
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  

class Dotplot():
    #Initialisation 
    def __init__(self):

        self.main_w = ctk.CTk()
        
        self.database_name = "SHADOTAPP"
        self.showlist_2esp = list()
        self.showlist_1esp = list()
        
        self.liste_info_1esp = ['Non existant ','-','-','-','-','-','-','-','-']
        self.liste_info_2esp = [['Non existant ','-','-','-','-','-','-','-','-'],['Non existant ','-','-','-','-','-','-','-','-']]
        
        self.espece_filtre = list()
        
        self.infos_titre = ["Nom ","Organisme","BioSample","BioProject","Assembly n°","Taille (Mb)", "Taux de GC (%)", "Nombre de CDS", "Lien FTP"]
        self.liste_parsee = list()
        self.ajout_frame_rb_alpha = list()
        self.blast_frame_rb = list()

        self.radio = tk.StringVar(value="")

        self.bl_selection = tk.IntVar(value=0)
        self.blast_dans_base = 0

        self.dp_query = ""
        self.dp_subject = ""

        self.cluster_nb = 0

        self.cluster_array =[]
        
        #Options de plot
        self.plot_var = tk.StringVar(value="scatter")

        #Création fenetre
        self.creeBase()
        
        #Création de la barre de menu
        self.creerMenu()

        #Placement des widgets
        self.placerWidget()

        self.main_w.protocol("WM_DELETE_WINDOW", self.main_w.quit)

        self.main_w.mainloop()

    
    #Creation de l'interface
    def creeBase(self):
        
        #Fixation d'une taille minimale de fenetre
        self.main_w.minsize(900,500)

        self.main_w.maxsize(1000,500)
        #Titre
        self.main_w.title('ShaDotApp')

        #Taille minimum
        self.main_w.geometry("900x500")

        #Definir la limite des grid
        self.main_w.grid_columnconfigure(1,weight=1) 
        self.main_w.grid_columnconfigure((2,3),weight=0) 
        self.main_w.rowconfigure((0,1,2),weight=1) 

        self.set_db_name()
        
        #Initialisation de la liste de base
        self.set_esp_list() 
        self.set_list_esp_ajout()

    #Création du menu
    def creerMenu(self):

        #Creation du frame a gauche
        self.barre = ctk.CTkFrame(self.main_w,width= 200, corner_radius=0)
        self.barre.grid(row=0,column=0, rowspan=4,sticky="nsew")
        self.barre.grid_rowconfigure(4,weight=1)
        
        #Case titre
        self.nomapp = ctk.CTkLabel(self.barre, text = "ShaDotApp",font = ctk.CTkFont(size=15, weight="bold"))
        self.nomapp.grid(row=0, column=0, padx= 10, pady = 10)


        #Bouton pour création de base :
        self.bouton_base = ctk.CTkButton(self.barre, text = "Pas de base ?", command= self.creer_serveur_abs)
        self.bouton_base.grid(row=4, column = 0, padx =10, pady = 10)

        if self.database_name!="":
            self.bouton_base.configure(state = "disabled")
            self.bouton_base.configure(text = "Base OK")

        #Apparence (inspiré du tuto ctk)
        self.apparence_label = ctk.CTkLabel(self.barre, text="Thème", anchor="w")
        self.apparence_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.apparence_optionemenu = ctk.CTkOptionMenu(self.barre, values=["Light", "Dark", "System"],
                                                                       command=self.changer_apparence)
        self.apparence_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
                
        #Mise à l'échelle (inspiré du tuto ctk)

        self.echelle = ctk.CTkLabel(self.barre, text="Echelle UI:", anchor="w")
        self.echelle.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.echelle_optionemenu = ctk.CTkOptionMenu(self.barre, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.changer_echelle)
        self.echelle_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


    def placerWidget(self):    
        #Création de l'espace Séléction d'espèce
        self.tabview_haut = ctk.CTkTabview(self.main_w,width = 400, height = 200)
        self.tabview_haut.grid(row=0, column = 1,columnspan = 3,padx = (10,10), pady = (10,10), sticky = "nsew")
        self.tabview_haut.add("Selection des organismes")
        self.tabview_haut.add("Ajouter un organisme")
        self.tabview_haut.add("Selection de BLAST et conditions")

        #######################################################################################################

        #Configuration des grid l'oglet séléction
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(0,weight = 1)
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(1,weight = 1)
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(2,weight = 1)
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(3,weight = 1)
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(4,weight = 1)
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(5,weight = 1)
        self.tabview_haut.tab("Selection des organismes").grid_columnconfigure(6,weight = 1)

        self.tabview_haut.tab("Selection des organismes").grid_rowconfigure(0,weight = 0)
        self.tabview_haut.tab("Selection des organismes").grid_rowconfigure(1,weight = 0)
        self.tabview_haut.tab("Selection des organismes").grid_rowconfigure(2,weight = 2)

        #Label des organismes
        self.label_esp1= ctk.CTkLabel(self.tabview_haut.tab("Selection des organismes"),text = "Organisme n°1")
        self.label_esp1.grid(row=0,column=0, padx=5, pady=2,sticky="ew")
    
        self.label_esp2= ctk.CTkLabel(self.tabview_haut.tab("Selection des organismes"),text = "Organisme n°2")
        self.label_esp2.grid(row=1,column=0, padx=5, pady=2,sticky="ew")
        
        #Combobox de séléction
        self.combobox_esp1 = ctk.CTkComboBox(self.tabview_haut.tab("Selection des organismes"),values=self.showlist_2esp,width = 200, command = self.click_esp)
        self.combobox_esp1.grid(row=0, column=1,columnspan=5 ,padx=5, pady=5 ,sticky="ew")
        
        self.combobox_esp2 = ctk.CTkComboBox(self.tabview_haut.tab("Selection des organismes"),values=self.showlist_2esp,width = 200, command = self.click_esp)
        self.combobox_esp2.grid(row=1, column=1, columnspan=5, padx=5, pady=5,sticky="ew")
    
        self.tabview_haut_esp = ctk.CTkTabview(self.tabview_haut.tab("Selection des organismes"),width = 300, height = 100)
        self.tabview_haut_esp.grid(row=2, column = 0,columnspan = 7,padx = (5,5), pady = (5,5), sticky = "nsew")

        #Bouton Blast :

        self.blast_bouton = ctk.CTkButton(self.tabview_haut.tab("Selection des organismes"), text = "BLAST", command=self.blast_esp)
        self.blast_bouton.grid(row=0, column=6, rowspan = 2, padx=5, pady=5, sticky = "nsew")

        #Tab avec infos organisme : 
        self.tabview_haut_esp.add("Infos Organisme n°1")
        self.tabview_haut_esp.add("Infos Organisme n°2")

        self.combobox_esp1.bind('<Button-1>',self.click_esp)
        self.combobox_esp2.bind('<Button-1>',self.click_esp)

        self.combobox_esp1.bind('<Key>',self.clavier_esp1)
        self.combobox_esp2.bind('<Key>',self.clavier_esp2)

        #Remplissage avec les Informations pour organisme 1
        self.esp1_nom= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Nom : "+str(self.liste_info_2esp[0][0]))
        self.esp1_nom.grid(row=0,column=0, padx=5,sticky="w")

        self.esp1_org= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Organisme : "+str(self.liste_info_2esp[0][1]))
        self.esp1_org.grid(row=1,column=0, padx=5,sticky="w")

        self.esp1_bios= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "BioSample : "+str(self.liste_info_2esp[0][2]))
        self.esp1_bios.grid(row=2,column=0, padx=5,sticky="w")

        self.esp1_biop= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "BioProject : "+str(self.liste_info_2esp[0][3]))
        self.esp1_biop.grid(row=3,column=0, padx=5,sticky="w")

        self.esp1_assem= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Assembly n° : "+str(self.liste_info_2esp[0][4]))
        self.esp1_assem.grid(row=4,column=0, padx=5,sticky="w")

        self.esp1_size= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Taille (Mb) : "+str(self.liste_info_2esp[0][5]))
        self.esp1_size.grid(row=5,column=0, padx=5, sticky="w")

        self.esp1_gc= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Taux de GC (%) : "+str(self.liste_info_2esp[0][6]))
        self.esp1_gc.grid(row=6,column=0, padx=5,sticky="w")

        self.esp1_cds= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Nombre de CDS : "+str(self.liste_info_2esp[0][7]))
        self.esp1_cds.grid(row=7,column=0, padx=5, sticky="w")

        self.esp1_ftp= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°1"),text = "Lien FTP : "+str(self.liste_info_2esp[0][8]))
        self.esp1_ftp.grid(row=8,column=0, padx=5, sticky="w")

        #Remplissage avec les Informations pour organisme 2
        self.esp2_nom= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Nom : "+str(self.liste_info_2esp[1][0]))
        self.esp2_nom.grid(row=0,column=0, padx=5, sticky="w")

        self.esp2_org= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Organisme : "+str(self.liste_info_2esp[1][1]))
        self.esp2_org.grid(row=1,column=0, padx=5, sticky="w")

        self.esp2_bios= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "BioSample : "+str(self.liste_info_2esp[1][2]))
        self.esp2_bios.grid(row=2,column=0, padx=5,sticky="w")

        self.esp2_biop= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "BioProject : "+str(self.liste_info_2esp[1][3]))
        self.esp2_biop.grid(row=3,column=0, padx=5, sticky="w")

        self.esp2_assem= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Assembly n° : "+str(self.liste_info_2esp[1][4]))
        self.esp2_assem.grid(row=4,column=0, padx=5, sticky="w")

        self.esp2_size= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Taille (Mb) : "+str(self.liste_info_2esp[1][5]))
        self.esp2_size.grid(row=5,column=0, padx=5, sticky="w")

        self.esp2_gc= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Taux de GC (%) : "+str(self.liste_info_2esp[1][6]))
        self.esp2_gc.grid(row=6,column=0, padx=5, sticky="w")

        self.esp2_cds= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Nombre de CDS : "+str(self.liste_info_2esp[1][7]))
        self.esp2_cds.grid(row=7,column=0, padx=5, sticky="w")

        self.esp2_ftp= ctk.CTkLabel(self.tabview_haut_esp.tab("Infos Organisme n°2"),text = "Lien FTP : "+str(self.liste_info_2esp[1][8]))
        self.esp2_ftp.grid(row=8,column=0, padx=5,sticky="w")

        self.info_esp()

        #######################################################################################################

        #Configuration des grid de l'onglet Ajout
        self.tabview_haut.tab("Ajouter un organisme").grid_columnconfigure(0,weight = 0)
        self.tabview_haut.tab("Ajouter un organisme").grid_columnconfigure(1,weight = 0)
        self.tabview_haut.tab("Ajouter un organisme").grid_columnconfigure(2,weight = 1)
        self.tabview_haut.tab("Ajouter un organisme").grid_columnconfigure(3,weight = 1)
        self.tabview_haut.tab("Ajouter un organisme").grid_columnconfigure(4,weight = 3)


        self.tabview_haut.tab("Ajouter un organisme").grid_rowconfigure(0,weight = 0)
        self.tabview_haut.tab("Ajouter un organisme").grid_rowconfigure(1,weight = 0)
        self.tabview_haut.tab("Ajouter un organisme").grid_rowconfigure(2,weight = 0)
        
        #Agencement de la fenêtre d'ajout
        
        self.alpha_label = ctk.CTkLabel(self.tabview_haut.tab("Ajouter un organisme"), text = "Ecrivez les deux \npremières lettres : ")
        self.alpha_label.grid(row=0, column=0, padx = 5, pady=10, sticky="nw")

        self.alpha_entry = ctk.CTkEntry(self.tabview_haut.tab("Ajouter un organisme"))
        self.alpha_entry.grid(row=0, column=1  ,padx = 5, pady=10, sticky="nw")

        self.ajout_search_bouton = ctk.CTkButton(self.tabview_haut.tab("Ajouter un organisme"), text = "Chercher", command=self.parser)
        self.ajout_search_bouton.grid(row=0, column=2 ,padx=5, pady=10, sticky = "new")
        
        self.tabview_haut_ajout = ctk.CTkTabview(self.tabview_haut.tab("Ajouter un organisme"))
        self.tabview_haut_ajout.grid(row=0, column = 4, rowspan = 2, padx = 10 , pady = 10, sticky = "nsew")
    
        self.tabview_haut_ajout.add("Informations sur l'organisme choisi")

        self.ajout_frame = ctk.CTkScrollableFrame(self.tabview_haut.tab("Ajouter un organisme"),label_text= "Organisme à ajouter")
        self.ajout_frame.grid(row=1,column =0 ,columnspan = 3,padx = 5, pady = 5, sticky = "nsew")

        self.ajout_add_bouton = ctk.CTkButton(self.tabview_haut.tab("Ajouter un organisme"), text = "Ajouter", command= self.ajout_et_maj)
        self.ajout_add_bouton.grid(row=2, column=0,columnspan=5,padx=10, pady=10, sticky = "sew")

        #Remplissage avec les Informations pour organisme 1
        self.esp_ajout_nom= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Nom : "+str(self.liste_info_1esp[0]))
        self.esp_ajout_nom.grid(row=0,column=0, padx=5,sticky="w")

        self.esp_ajout_org= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Organisme : "+str(self.liste_info_1esp[1]))
        self.esp_ajout_org.grid(row=1,column=0, padx=5,sticky="w")

        self.esp_ajout_bios= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "BioSample : "+str(self.liste_info_1esp[2]))
        self.esp_ajout_bios.grid(row=2,column=0, padx=5,sticky="w")

        self.esp_ajout_biop= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "BioProject : "+str(self.liste_info_1esp[3]))
        self.esp_ajout_biop.grid(row=3,column=0, padx=5,sticky="w")

        self.esp_ajout_assem= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Assembly n° : "+str(self.liste_info_1esp[4]))
        self.esp_ajout_assem.grid(row=4,column=0, padx=5,sticky="w")

        self.esp_ajout_size= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Taille (Mb) : "+str(self.liste_info_1esp[5]))
        self.esp_ajout_size.grid(row=5,column=0, padx=5, sticky="w")

        self.esp_ajout_gc= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Taux de GC (%) : "+str(self.liste_info_1esp[6]))
        self.esp_ajout_gc.grid(row=6,column=0, padx=5,sticky="w")

        self.esp_ajout_cds= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Nombre de CDS : "+str(self.liste_info_1esp[7]))
        self.esp_ajout_cds.grid(row=7,column=0, padx=5, sticky="w")

        self.esp_ajout_ftp= ctk.CTkLabel(self.tabview_haut_ajout.tab("Informations sur l'organisme choisi"),text = "Lien FTP : "+str(self.liste_info_1esp[8]))
        self.esp_ajout_ftp.grid(row=8,column=0, padx=5, sticky="w")

        self.info_solo_esp()

        #######################################################################################################
         #Configuration des grid de l'onglet Ajout
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_columnconfigure(0,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_columnconfigure(1,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_columnconfigure(2,weight = 1)


        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(0,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(1,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(2,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(3,weight = 0)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(4,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(5,weight = 1)
        self.tabview_haut.tab("Selection de BLAST et conditions").grid_rowconfigure(6,weight = 1)
        
        #Agencement de la fenêtre de séléction blast

        #Frame avec la selection blast
        self.blast_frame = ctk.CTkScrollableFrame(self.tabview_haut.tab("Selection de BLAST et conditions"),label_text= "Choix du BLAST : N°"+str(self.bl_selection.get()))
        self.blast_frame.grid(row=0,column =0,columnspan = 3,padx = 5, pady = 5, sticky = "nsew")

        self.bl_fenetre()
       
        #Bouton lancer 

        self.lancer_bouton = ctk.CTkButton(self.tabview_haut.tab("Selection de BLAST et conditions"),text = "Lancer", command = self.fenetre_dotplot)
        self.lancer_bouton.grid(row = 3, column = 1, padx=10, pady=10, sticky = "nsew")

    #FONCTIONS
    
    #Initialisation
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
                self.showlist_2esp = [esp_init[i][0]+" : "+esp_init[i][1] for i in range(len(esp_init))]

    #Ajout d'une espèce
    #Mise a jour de la liste des espèces
    def set_list_esp_ajout(self):
               
        if self.database_name!="":

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            #Recherche
            cur.execute("SELECT prokaryote_bank.name_org,prokaryote_bank.assembly_no FROM prokaryote_bank WHERE NOT EXISTS (SELECT * FROM proteines WHERE proteines.name_org = prokaryote_bank.name_org AND proteines.assembly_no = prokaryote_bank.assembly_no) ORDER BY prokaryote_bank.name_org ASC;")

            #Recup result query
            esp_upd_list = cur.fetchall()
            
            if esp_upd_list!=[]:
            #Stockage:
                self.showlist_1esp = [esp_upd_list[i][0]+" : "+esp_upd_list[i][1] for i in range(len(esp_upd_list))]

            #Fermeture
            conn.close()
    
    def destroy_all(self):
        if self.ajout_frame_rb_alpha!=[]:
            for rbd in self.ajout_frame.winfo_children():
                rbd.destroy()
                self.ajout_frame_rb_alpha.remove(rbd)
            return 
    #Parsing 
    def parser(self):
        
        self.destroy_all()

        self.liste_parsee = []
        if not self.alpha_entry.get().isdigit() and len(self.alpha_entry.get())>1:
            lettre = self.alpha_entry.get()
            self.liste_parsee = [i for  i in self.showlist_1esp if i.startswith(lettre[0].upper()+lettre[1::].lower())]
        
        for i, val in enumerate(self.liste_parsee):
            rb = ctk.CTkRadioButton(self.ajout_frame, command = self.info_solo_esp,variable = self.radio, text = val, value=val)
            rb.grid(row = i, column = 0, padx = 5, pady = 5, sticky="w")
            self.ajout_frame_rb_alpha.append(rb)
        
        self.info_solo_esp()

    #Connaître l'information pour une espèce
    def info_solo_esp(self):
        
        #Récupération index Espece 1
        esp_choisi = self.radio.get()

        if self.database_name!="":
            
            self.infos_labels_ajout = [self.esp_ajout_nom,self.esp_ajout_org,self.esp_ajout_bios, self.esp_ajout_biop,self.esp_ajout_assem,self.esp_ajout_size,self.esp_ajout_gc,self.esp_ajout_cds,self.esp_ajout_ftp]

            if esp_choisi!="" and len(esp_choisi.split(" : "))==2:
                
                #Connexion
                conn = psycopg2.connect("dbname="+self.database_name+"")

                #Curseur
                cur = conn.cursor()
                
                #Recherche
                esp_name,esp_assembly = esp_choisi.split(" : ")
                cur.execute("SELECT * FROM prokaryote_bank WHERE name_org ='"+esp_name+"' AND assembly_no = '"+esp_assembly+"';")
                a = cur.fetchall()
                self.liste_info_1esp = list(a[0])
                org_split = a[0][1].split(";")
                org_str = org_split[0]+" -> "+org_split[1]+" -> "+org_split[2]
                
                for j in range(9):
                    self.infos_labels_ajout[j].configure(text = self.infos_titre[j]+" : "+str(a[0][j]))
                    if j==1:
                        self.infos_labels_ajout[j].configure(text = self.infos_titre[j]+" : "+org_str)

                #Fermeture
                conn.close()

            if len(esp_choisi.split(" : "))<2 or self.radio.get()=="": 
                self.liste_info_1esp = ['Non choisi','-','-','-','-','-','-','-','-']
                for j in range(9):
                    self.infos_labels_ajout[j].configure(text = self.infos_titre[j]+" : "+self.liste_info_1esp[j])
        
        
        if self.liste_info_1esp==[]:
           
            self.liste_info_1esp = ['Non existant ','-','-','-','-','-','-','-','-']
        
    #Ajout de l'espèce choisie dans la base
    def ajout_et_maj(self):
        
        if self.radio.get()!="":
            #Récupérer la valeur
            nom,assembly = self.radio.get().split(" : ")

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            cur.execute("SELECT ftp_link FROM prokaryote_bank WHERE name_org ='"+nom+"' AND assembly_no='"+assembly+"';")
            
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
                filename = assembly
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
            nouveau_prot = nom+" : "+assembly
            
            self.showlist_2esp.append(nouveau_prot)
            
            self.showlist_1esp.remove(nouveau_prot)

            if self.ajout_frame_rb_alpha!=[]:
                for rbd in self.ajout_frame.winfo_children():
                    if isinstance(rbd, ctk.CTkRadioButton) and rbd.cget("value") == nouveau_prot:
                        rbd.destroy()
                        self.ajout_frame_rb_alpha.remove(rbd)
            

    #Sélection de Blast

    #Fenetre de sélection de blast dans la base
    def bl_fenetre(self):
        
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

            for i,ligne in enumerate(blast_res_base):
                fusion_ligne = str(ligne[1])+" : "+str(ligne[2])+" ---------- "+str(ligne[3])+ " : "+str(ligne[4])
                format_ligne = "    "+str(ligne[0])+"    "+" -> "+fusion_ligne
                rb = ctk.CTkRadioButton(self.blast_frame,command = self.blast_select,variable = self.bl_selection, text = format_ligne, value=ligne[0])
                rb.grid(row = i, column = 0, padx = 5, pady = 5, sticky="w")
                self.blast_frame_rb.append(rb)

    #Récupération de la valeur de séléction
    def blast_select(self):
            self.blast_frame.configure(label_text = "Choix du BLAST N°"+str(self.bl_selection.get()))

    #Création de base 
    #Creation d'une nouvelle base
    def creer_serveur_abs(self):
        
        #Création de fenetre 
        self.bd = ctk.CTkToplevel(self.main_w)
        
        self.bd.minsize(700,350)
        
        self.bd.title("Création de base de données")

        #Partie explications
        self.explication1_label = ctk.CTkLabel(self.bd, text = "Vous êtes ici car vous n'êtes pas sur le serveur OBIWAN et que vous voulez avoir la base de données sur votre poste.\n\n Pour cela, comme précisé dans le Readme, vous devez être en possession du logiciel PostgreSQL.\n\n Si c'est le cas, vous allez pouvoir créer votre base de données avec les fichiers intiaux fournis.\n\n")
        self.explication1_label.grid(row = 0,column=0,columnspan =2,padx = 10, pady = 10,sticky = 'ew')
        
        self.nom_bd_label = ctk.CTkLabel(self.bd, text = "Veuillez définir un nom pour votre base -> ")
        self.nom_bd_label.grid(row=1,column=0,padx=10,pady=10,sticky='w')

        self.nom_bd_entry = ctk.CTkEntry(self.bd,width = 40)
        self.nom_bd_entry.grid(row = 1,column=1,padx=10, pady=10, sticky='ew')

        self.presence_label = ctk.CTkLabel(self.bd, text = "Saisissez le nom dans la barre ci-dessus puis appuyez sur Vérification")
        self.presence_label.grid(row = 2,column=0, columnspan =1,padx = 10, pady = 10,sticky = 'w')           

        #Bouton de vérification
        self.presence_bt = ctk.CTkButton(self.bd, text="Vérification", command=self.verif_presence_bd)
        self.presence_bt.grid(row = 2, column = 1, columnspan = 1, padx=10,pady=10, sticky = 'nsew')

        self.explication2_label = ctk.CTkLabel(self.bd, text = "\nAppuyez sur le bouton Créer pour lancer la création de la base.\nVous pouvez suivre l'avancée de la création sur le terminal qui ne prendra au maximum 30 secondes.\n\n")
        self.explication2_label.grid(row = 3,column=0, columnspan =2,padx = 10, pady = 10,sticky = 'ew')

        #Bouton de création
        self.creation_bt = ctk.CTkButton(self.bd, text="Créer", command=self.import_bd)
        self.creation_bt.grid(row = 4, column = 0, columnspan = 2, padx=10,pady=10, sticky = 'nsew')           

        if self.database_name!="":
            self.bouton_base.configure(state = "disabled")
            self.bouton_base.configure(text = "Base OK")

            self.presence_label.configure(text = "Inutile de créer : BASE EXISTANTE POUR L'APP")
            
            self.creation_bt.configure(state = "disabled")
            self.presence_bt.configure(state = "disabled")
        else:
            self.creation_bt.configure(state = "normal")

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
                self.presence_label.configure(text = "Nom de base de données DISPONIBLE")
                self.creation_bt.configure(state="normal")
        
        if self.database_name!="":
            self.bouton_base.configure(text="Base OK")
            self.presence_label.configure(text = "Inutile de créer : BASE EXISTANTE POUR L'APP")
            self.creation_bt.configure(state="disabled")

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
            self.blastp_number = 1
            blastp_path = '.Base/Blastp'
            for blastp in os.listdir(blastp_path):
                print("Traitement du fichier n° ",self.blastp_number)
                blastp_name = os.path.join(blastp_path,blastp)
                
                blastp_rank  = 1
                with open(blastp_name,'r') as file:
                    
                    #zapper le header
                    next(file)
                    for line in file:
                        
                        #Parcours de chaque ligne
                        colonne = line.split()
                        id1 = re.search(r"lcl\|(\S+)", colonne[0]).group(1)

                        cur.execute("INSERT INTO blast_results (blast_exec_number,blast_rank,query_seqid,subject_seqid,percent_ident,b_length,mismatch,gapopen,q_start,q_end,s_start,s_end,blast_e_val,blast_bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(self.blastp_number,blastp_rank,id1,colonne[1],colonne[2],colonne[3],colonne[4],colonne[5],colonne[6],colonne[7],colonne[8],colonne[9],colonne[10],colonne[11])) 
                        
                        blastp_rank +=1
                    conn.commit()

                cur.execute("UPDATE blast_results SET cover_q = trunc(((q_end-q_start)::float/ proteines.len)*1000)/1000  FROM proteines WHERE blast_results.query_seqid=proteines.protein_id ;")
                cur.execute("UPDATE blast_results SET cover_s = trunc(((s_end-s_start)::float/ proteines.len)*1000)/1000  FROM proteines WHERE blast_results.subject_seqid=proteines.protein_id ;")

                conn.commit()

                self.blastp_number+=1
                self.blast_dans_base+=1


            conn.close()
            end = time.time()
            temps = end-start

            #Mise a jour des instances 
            self.database_name = database_name
            
            self.set_db_name()
            self.set_esp_list() 
            self.set_list_esp_ajout()
            self.bl_fenetre()
            print(f"\nBase remplie !\nTemps de remplissage de la base : {temps} seconds\n")

            self.bd.quit()

    #Filtrage des saisies des especes
    def filtrage_continu_2esp(self,var):
        search = var.get()
        self.espece_filtre = [esp for esp in self.showlist_2esp if esp.split(" : ")[0].lower().startswith(search) or esp.split(" : ")[0].startswith(search) or esp.split(" : ")[1].lower().startswith(search) or esp.split(" : ")[1].startswith(search)]
        if search!='':
            var.configure(values = self.espece_filtre)
        else:
            var.configure(values = self.showlist_2esp)

    #Filtrage des saisies des especes
    def filtrage_continu_1esp(self,var):
        search = var.get()
        self.espece_filtre = [esp for esp in self.showlist_1esp if esp.split(" : ")[0].lower().startswith(search) or esp.split(" : ")[0].startswith(search) or esp.split(" : ")[1].lower().startswith(search) or esp.split(" : ")[1].startswith(search)]
        if search!='':
            var.configure(values = self.espece_filtre)
        else:
            var.configure(values = self.showlist_1esp)

    #Association évenement et mise a jour de la barre
    def clavier_esp1(self,evt):
        self.filtrage_continu_2esp(self.combobox_esp1)
        self.info_esp()

    #Association evenement et mise à jour de la barre
    def clavier_esp2(self,evt):
        self.filtrage_continu_2esp(self.combobox_esp2)
        self.info_esp()

    #Association evenement et mise à jour de la barre
    def clavier_esp_solo(self,evt):
        self.filtrage_continu_1esp(self.combobox_ajout)
        self.info_solo_esp()

    #Association evenement et mise à jour de la barre
    def click_esp(self,evt):
        self.info_esp()

    def click_esp_solo(self,evt):
        self.info_solo_esp()

    def info_esp(self):     

        #Récupération index Espece 1
        esp1_choisi = self.combobox_esp1.get()

        #Récupération index Espece 2
        esp2_choisi = self.combobox_esp2.get()

        self.liste_choix = [esp1_choisi,esp2_choisi]

        if self.database_name!="" :
            
            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            self.infos_labels_esp = [[self.esp1_nom,self.esp1_org,self.esp1_bios, self.esp1_biop,self.esp1_assem,self.esp1_size,self.esp1_gc,self.esp1_cds,self.esp1_ftp],[self.esp2_nom,self.esp2_org,self.esp2_bios, self.esp2_biop,self.esp2_assem,self.esp2_size,self.esp2_gc,self.esp2_cds,self.esp2_ftp]]
            #Recherche
            for i in range(2):
                if self.liste_choix[i]!="Vide" and len(self.liste_choix[i].split(" : "))==2:
                    esp_name,esp_assembly = self.liste_choix[i].split(" : ")
                    cur.execute("SELECT * FROM prokaryote_bank WHERE name_org ='"+esp_name+"' AND assembly_no = '"+esp_assembly+"';")
                    a = cur.fetchall()
                    self.liste_info_2esp[i] = list(a[0])
                    org_split = a[0][1].split(";")
                    org_str = org_split[0]+" -> "+org_split[1]+" -> "+org_split[2]
                    
                    for j in range(9):
                        self.infos_labels_esp[i][j].configure(text = self.infos_titre[j]+" : "+str(a[0][j]))
                        if j==1:
                            self.infos_labels_esp[i][j].configure(text = self.infos_titre[j]+" : "+org_str)


                if len(self.liste_choix[i].split(" : "))<2: 
                    self.liste_info_2esp[i] = ['Non choisi','-','-','-','-','-','-','-','-']
                    for j in range(9):
                        self.infos_labels_esp[i][j].configure(text = self.infos_titre[j]+" : "+self.liste_info_2esp[i][j])
        
            #Fermeture
            conn.close()
        
        if self.liste_info_2esp==[[],[]]:
           
            self.liste_info_2esp = [['Non existant ','-','-','-','-','-','-','-','-'],['Non existant ','-','-','-','-','-','-','-','-']]
                    
    #Execution blast
    def blast_esp(self):

        #Récupération index Espece 1
        esp1_choisi = self.combobox_esp1.get()

        #Récupération index Espece 2
        esp2_choisi = self.combobox_esp2.get()

        if esp1_choisi!="" and esp2_choisi!="" and len(esp1_choisi.split(" : "))==2 and len(esp2_choisi.split(" : "))==2:
            #Récupération infos esp1 et esp2
            ftp1 = ""
            ftp2 = "" 
            liste_ftp = [ftp1,ftp2]
            liste_lastpart = ["",""]      
            liste_gz = ["",""]      
            liste_nom = [esp1_choisi.split(" : ")[0],esp2_choisi.split(" : ")[0]]
            liste_assembly = [esp1_choisi.split(" : ")[1],esp2_choisi.split(" : ")[1]]
            liste_faa = ["",""]

            print(liste_nom)
            print(liste_assembly)

            #Connexion
            conn = psycopg2.connect("dbname="+self.database_name+"")

            #Curseur
            cur = conn.cursor()

            print("Récupération des fichiers ...")
            #Recherche
            for i in range(2):
                cur.execute("SELECT ftp_link FROM prokaryote_bank WHERE name_org ='"+liste_nom[i]+"' AND assembly_no='"+liste_assembly[i]+"';")
                liste_ftp[i] = cur.fetchone()[0]
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
            
            self.blast_dans_base+=1

            subprocess.run(["rm",liste_faa[0]])
            subprocess.run(["rm",liste_faa[1]])
            subprocess.run(["rm",nom_sortie_blast])

            fusion_ligne = str(liste_nom[0])+" : "+str(liste_assembly[0])+" ---------- "+str(liste_nom[1])+ " : "+str(liste_assembly[1])
            format_ligne = "    "+str(blastnum)+"    "+" -> "+fusion_ligne

            rb = ctk.CTkRadioButton(self.blast_frame, command = self.blast_select,variable = self.bl_selection, text = format_ligne, value=int(blastnum))
            rb.grid(row = blastnum-1, column = 0, padx = 5, pady = 5, sticky="w")
            self.blast_frame_rb.append(rb)

    #Lancement        
    def recuperer_axes(self,*args):
        
        #Stockage identitié blast
        blastno = self.bl_selection.get()
        
        #Valeur par défaut
        self.defaulteval = 1e-30
        self.listetxt = []
        #Ligne de commande prete
        self.commandline = "SELECT p1.rank, p2.rank, p1.name_org,p2.name_org,blast_results.query_seqid, blast_results.subject_seqid,blast_results.blast_e_val FROM blast_results JOIN proteines AS p1 ON blast_results.query_seqid = p1.protein_id JOIN proteines AS p2 ON blast_results.subject_seqid = p2.protein_id WHERE blast_exec_number = "+str(blastno)+""
        
        #Vérification des checkboxes et valeurs
        if self.entries[3].get()!="":
            self.commandline = self.commandline+" AND percent_ident>"+str(self.entries[3].get())+""
            self.listetxt.append(str(self.entries[3].get()))
        
        else : 
            self.listetxt.append("None")

        if self.entries[0].get()!="":
            self.commandline = self.commandline+" AND cover_q>"+str(self.entries[0].get())+""
            self.listetxt.append(str(self.entries[0].get()))

        else : 
            self.listetxt.append("None")

        if self.entries[1].get()!="":
            self.commandline = self.commandline+" AND cover_s>"+str(self.entries[1].get())+""
            self.listetxt.append(str(self.entries[1].get()))

        else : 
            self.listetxt.append("None")

        if self.entries[2].get()!="":
            self.commandline = self.commandline +" AND blast_e_val<"+str(self.entries[2].get())+""
            self.listetxt.append(str(self.entries[2].get()))

        if self.entries[3].get()==self.entries[0].get()==self.entries[1].get()==self.entries[2].get()=="":
            self.commandline = self.commandline +" AND blast_e_val<"+str(self.defaulteval)+""
            self.listetxt.append(str(self.defaulteval))
 
        self.commandline = self.commandline+";"

        #Récupération de la taille fenetre et seuil de stringence
        
        if ((self.entries[4].get()!="" and self.entries[4].get().isdigit()) and (self.entries[5].get()!="") and self.entries[5].get().isdigit()) and blastno!=0:

            self.taille_fen = int(self.entries[4].get())
            self.seuil_strin = int(self.entries[5].get())

            self.listetxt.append(str(self.entries[4].get()))
            self.listetxt.append(str(self.entries[5].get()))


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

                self.dp_query = name_query
                self.dp_subject = name_subject
                return blastno,mat_show,x,y

    def relancer_s_dotplot(self):
        
        #Enlever l'ancien graphe
        self.ax.clear()
        self.ax.invert_yaxis()

        #Récuperer les nouvelles coordonnées
        _,_,x,y = self.recuperer_axes()
        self.data = np.vstack((x,y)).T
        
        #Récupération du nombre de clusters optimale:
        k = 0

        if self.entries[6].get()=='0' or self.entries[6].get()=='':
            distortions = []
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=500, n_init=10, random_state=0)
                kmeans.fit(self.data)
                distortions.append(kmeans.inertia_)
            
            differences = np.diff(distortions)
            k_index = np.argmax(differences)
            k = k_index + 2
        else : 
            k  = int(self.entries[6].get())
        
        #Application du kMeans
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=0).fit(self.data)

        #On extrait les labels
        labels = kmeans.labels_
        self.cluster_nb = k
        self.cbbx_cluster.configure(values = [str(i) for i in range(self.cluster_nb)])

        self.cluster_points=[[] for _ in range(k)]
        self.data_corrected = self.data + 1
        for i in range(len(self.data)):
            self.cluster_points[labels[i]].append(self.data_corrected[i])

        self.cluster_array = np.array([np.array(cp) for cp in self.cluster_points],dtype=object)

        for i in range(k):
            self.cluster_array[i] = self.cluster_array[i][np.argsort(self.cluster_array[i][:, 0])]

        #Affichage du scatter
        self.scatter_plot = self.ax.scatter(x,y,s=0.01,c = labels)
        plt.colorbar(self.scatter_plot)
        self.scatter_plot.colorbar.remove()
        self.ax.set_xlabel(self.dp_query)
        self.ax.set_ylabel(self.dp_subject)

        self.fig.canvas.draw()
        self.toolbar.update()

    def update_text_box(self,event):
        self.txt_cluster.delete("0.0","end")
        
        selected_cluster = int(self.cbbx_cluster.get())
        self.txt_cluster.insert('end', f'Cluster {selected_cluster}:\n')
        for point in self.cluster_array[selected_cluster]:
            self.txt_cluster.insert('end', f'({point[0]:d}, {point[1]:d})\n')

    def relancer_i_dotplot(self):
        
        self.ax.clear()
        self.ax.invert_yaxis()
        _,m,_,_ = self.recuperer_axes()
        
        im = self.ax.imshow(m, cmap = self.cmap)
        self.ax.set_xlabel(self.dp_query)
        self.ax.set_ylabel(self.dp_subject)      
        
        self.canvas.draw()
        self.toolbar.update()

    
    def afficher_dotplot(self,*args):
        blastno,_,x,y= self.recuperer_axes()

        if self.plot_var.get()=="scatter" or self.plot_var.get()=="imshow":
            self.fenetre_dotplot()

        #Stockage dans un fichier
        if self.plot_var.get()=="txt":
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

            filename = "Stringence_Text/Stringence_Blast_"+str(blastno)+"_"+str(stringence_copy[0][20])+"_"+str(stringence_copy[0][26])+".txt"
            with open(filename, 'w') as file:
                file.write("ShaDotApp : Résultats de la stringence suite au blast n°"+str(blastno)+"\n\n")
                file.write("Organisme query : "+str(stringence_copy[0][19])+"\n")
                file.write("Assembly query : "+str(stringence_copy[0][20])+"\n")
                file.write("Organisme subject : "+str(stringence_copy[0][25])+"\n")
                file.write("Assembly subject : "+str(stringence_copy[0][26])+"\n\n")
                file.write("Conditions :\n")
                file.write("\tCouverture du hit Query: "+self.listetxt[1]+"\n")
                file.write("\tCouverture du hit Subject: "+self.listetxt[2]+"\n")
                file.write("\tE-value : "+self.listetxt[4]+"\n")
                file.write("\tPourcentage d'identité : "+self.listetxt[0]+"\n")
                file.write("\tTaille de fenêtre: "+self.listetxt[4]+"\n")
                file.write("\tSeuil de Stringence : "+self.listetxt[5]+"\n\n")


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
    

    def fenetre_dotplot(self):
        self.dot_fenetre = ctk.CTkToplevel()
        self.dot_fenetre.geometry("1200x600")
        self.dot_fenetre.title("Dotplot")

        self.ny = ['#000033','#FFFF00']
        self.cmap = mc.LinearSegmentedColormap.from_list('NY',self.ny)

        self.dot_fenetre.grid_rowconfigure(0,weight=1)

        self.dot_fenetre.grid_columnconfigure(0,weight=1)
        self.dot_fenetre.grid_columnconfigure(1,weight=1)
        self.dot_fenetre.grid_columnconfigure(2,weight=1)

        #Left frame
        self.left_frame = ctk.CTkFrame(self.dot_fenetre)
        self.left_frame.grid(row = 0, column = 0, padx = 10, pady=10,sticky="nsew")

        self.labels = ["Couverture du hit (Query)","Couverture du hit (Subject)","E-value","Pourcentage d'identité","Taille de la fenêtre","Seuil de stringence","Nombre de clusters"]
        self.placeholders = ["Seuil (float [0;1]) ","Seuil (float [0;1])","Seuil (ex : 1e-30)","Seuil (float [0;100])","Valeur (int [1;x]) ","Valeur (int [1;x])","Valeur (int [1;x])"]
        self.entries = [ctk.CTkEntry(self.left_frame, placeholder_text = self.placeholders[i]) for i in range(7)]

        for i in range(7):
            self.label_left = ctk.CTkLabel(self.left_frame, text = self.labels[i])
            self.label_left.grid(row = i, column = 0, sticky = 'w')
            self.entry_left = self.entries[i]
            self.entry_left.grid(row=i,column = 0, sticky = 'ew')
            #self.left_frame.grid_columnconfigure(1,weight=1)

        self.relancer_bouton = ctk.CTkButton(self.left_frame,text = "Relancer Scatter", command = self.relancer_s_dotplot)
        self.relancer_bouton.grid(row = 7,column=0,padx=10,pady=10,sticky="nsew")

        self.relancer_bouton = ctk.CTkButton(self.left_frame,text = "Relancer Imshow", command = self.relancer_i_dotplot)
        self.relancer_bouton.grid(row = 8,column=0,padx=10,pady=10,sticky="nsew")


        #Middle frame
        self.scatter_frame = ctk.CTkFrame(self.dot_fenetre)
        self.scatter_frame.grid(row=0, column=1, padx=10,pady=10, sticky='nsew')

        self.fig,self.ax = plt.subplots(figsize=(6,4))
        self.ax.set_xlabel(self.dp_query)
        self.ax.set_ylabel(self.dp_subject)

        plt.gca().set_facecolor('#000033')
        #self.fig.subplots_adjust(left=0,right=1,bottom =0,top = 1, wspace = 20, hspace=20)
        
        self.canvas = FigureCanvasTkAgg(self.fig,master = self.scatter_frame)
        self.canvas.draw()
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.scatter_frame)
        self.toolbar.configure(background='black', highlightbackground='black', highlightcolor='black')
        self.toolbar.update()
        
        self.canvas.get_tk_widget().pack(fill='both',expand=True)

        #Right frame
        self.csframe = ctk.CTkFrame(self.dot_fenetre,width=300)
        self.csframe.grid(row=0,column = 2,padx=10,pady=10, sticky = 'nsew')

        self.cbbx_cluster = ctk.CTkComboBox(self.csframe,values = [str(i) for i in range (self.cluster_nb)],command = self.update_text_box)
        self.cbbx_cluster.grid(row =0, column =0, padx=10, pady=10, sticky = "ew")
        
        self.cbbx_cluster.bind('<<Button-1>>', self.update_text_box)
        self.cbbx_cluster.bind('<<Key>>', self.update_text_box)


        self.txt_cluster = ctk.CTkTextbox(self.csframe)
        self.txt_cluster.grid(row=1,column =0,padx=10,pady=10, sticky= 'ns')
        #self.txt_cluster.configure(state="disabled")

        self.dot_fenetre.grid_columnconfigure(0, weight=1)
        self.dot_fenetre.grid_columnconfigure(1, weight=1)
        self.dot_fenetre.grid_columnconfigure(2, weight=1)

        self.dot_fenetre.mainloop()

    #inspiré du tuto ctk
    def changer_apparence(self, nouveau_theme: str):
        ctk.set_appearance_mode(nouveau_theme)

    def changer_echelle(self, nouvelle_echelle: str):
        nouvelle_echelle_float = int(nouvelle_echelle.replace("%", "")) / 100
        ctk.set_widget_scaling(nouvelle_echelle_float)

test = Dotplot()
