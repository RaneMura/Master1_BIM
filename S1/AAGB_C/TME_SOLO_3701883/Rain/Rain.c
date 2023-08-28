#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "Rain.h"

//Question 2
int sommeTab(tyCase tab[], int n){
	int sum = 0;
	for (int i =0;i<n-1;i++){
		sum += tab[i].eau;
	}
	return sum;
}

//Question 3
int maximumBarreTab(tyCase tab[], int n){

	int max_bar = 0;
	for(int i=0;i<n;i++){
		if(tab[i].barre > max_bar){
			max_bar = tab[i].barre;
		}
	} 
	return max_bar;
	
}

//Question 4
void fillWater(tyCase tab[], int n){

	int maxim = maximumBarreTab(tab,n);

	for(int i =0;tab[i].barre<maxim;i++){
		for(int j = n-1;tab[j].barre<maxim;j--){
			if (tab[i].barre < tab[j].barre){
				tab[i].eau = tab[j].barre;
			}
			else{
				tab[i].eau = tab[i].barre;
			}
		}

	}
}

//Question 5
void afficheRainWatter(tyCase *tab, int n){

	int maxibar = maximumBarreTab(tab,n);

	int i;
	int k;

	for(i = 0;i<maxibar;i++){
		for(k=0;k<n;k++){
			if (tab[k].barre == maxibar-i){
				printf("|");
			}
			if(tab[k].eau == maxibar - i){
				printf("~");
			}
		}
		printf("\n");
	}

	for(i = 0; i<2*n-1;i++){
		printf("_");
	}
	printf("\n");
}


//Question 7
int compter_lignes(char *nomFichier){
	
	FILE *pFi=NULL;
    char buffer[1000];
    pFi=fopen(nomFichier, "r");


    if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier cl\n");
        return 1;
    }
    
    int nbl = 0;
    while(fgets(buffer,1000,pFi)){
		nbl++;
    }
    fclose(pFi);

    return nbl;
}

//Question 8
tyCase *lire_tableau(char *nomFichier, int *p_nbVal){

	*p_nbVal = compter_lignes(nomFichier);
	tyCase *tc = malloc(sizeof(tyCase)*(*p_nbVal));

	for(int i =0;i<*p_nbVal;i++ ){
		tc[i].barre = 0;
		tc[i].eau = 0;
	}

	FILE *pFi=NULL;
    pFi=fopen(nomFichier, "r");

	if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier lt\n");
        return NULL;
    }

	for(int i = 0;i<*p_nbVal;i++){
		fscanf(pFi,"%d\n",&tc[i].barre );
	}

	fclose(pFi);

	for(int i = 0;i<*p_nbVal;i++){
		tc[i].eau = 0;
	}

	return tc;
}


