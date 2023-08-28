#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "Rain.h"

//Question 2
int sommeTab(tyCase tab[], int n){
	int i, s=0;
	for (i=0; i<n;i++)
		s+=tab[i].eau;
	return s;
}

//Question 3
int maximumBarreTab(tyCase tab[], int n){

	int iMax=0, i;
	
	for(i=1;i<n;i++)
		if(tab[i].barre>tab[iMax].barre)
			iMax=i;
	return iMax;
	
}

//Question 4
void fillWater(tyCase tab[], int n)
{
 
 	int  i=0, eau;
	
	int iMax=maximumBarreTab(tab, n);
	
	/* Remplissage du tableau de l'indice 0 jusqu'au max*/
	eau=tab[0].barre;
	tab[0].eau=tab[0].barre;
	for(i=1;i<iMax;i++){
		if(tab[i].barre>eau)
			eau=tab[i].barre;
		tab[i].eau=eau;
 	}

	/* Remplissage à l'envers du tableau de la fin jusqu'au max*/
	eau=tab[n-1].barre;
	for(i=n-2;i>=iMax;i--){
		tab[i].eau=eau;
		if(tab[i].barre>eau)
			eau=tab[i].barre;
 	}

    return ;

}

//Question 5
void afficheRainWatter(tyCase *tab, int n){

	int iC, iL;
	int iMax;

	iMax=maximumBarreTab(tab,n);
	/*Nombre de lignes = la barre la plus haute*/
	for(iL=tab[iMax].barre; iL>0;iL--){
		/*Nombre de colonnes = nombres de barres -1 (*2 ). On traite la dernière à part*/
			for(iC=0; iC<n-1;iC++){
				/*La barre*/
				if(tab[iC].barre>=iL)
					printf("|");
				else
					printf(" ");
				/*L'eau*/
				if(tab[iC].eau>=iL)
					printf("~");
				else
					printf(" ");				
			}
			/*dernière barre*/
			if(tab[iC].barre>=iL)
					printf("|\n");
				else
					printf(" \n");

	}
	for(iC=0; iC<n-1;iC++)
		printf("--");
	printf("-\n");
}


//Question 7
int compter_lignes(char *nomFichier){
	FILE *pFi;
	int nbL=0;
	char c;
	
	pFi=fopen(nomFichier, "r");
	if(pFi==NULL){
		fprintf(stderr, "compter_lignes:: Ne peut ouvrir %s\nEXITING\n", nomFichier);
		exit(1);
	}
	while((c=fgetc(pFi))!=EOF)
		if (c=='\n')
			nbL++;
	fclose(pFi);
	return nbL;
}

//Question 8
tyCase *lire_tableau(char *nomFichier, int *p_nbVal){
	FILE *pFi;
	tyCase *tab;
	int i;
	
	*p_nbVal=compter_lignes(nomFichier);

	tab=malloc(*p_nbVal*sizeof(tyCase));

	pFi=fopen(nomFichier, "r");
	if(pFi==NULL){
		fprintf(stderr, "lire_tableau:: Ne peut ouvrir %s\nEXITING\n", nomFichier);
		exit(1);
	}
	
	for(i=0; i<*p_nbVal;i++){
		fscanf(pFi, " %d", &tab[i].barre);
		tab[i].eau=0;
	}
	fclose(pFi);
	return tab;
}


