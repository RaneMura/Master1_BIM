#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ManipSeqADN.h"
#include "ManipSeqSimple.h"
#include "Arbre.h"

int main(){

    /*
    tySeqADN *pS;
    pS = malloc(sizeof(tySeqADN));
    pS->lg = 27;
    pS->seq = "ACTATGCAATCATACTAAATGTTTTAG";
    pS->comp = BrinComplementaire(pS->seq,pS->lg);

    AfficheSeq(pS->seq,pS->lg);
    AfficheSeq(pS->comp,pS->lg);
    tyArbre *pA;
    pA = Rechercher_ORF(pS,2);

    int tot = 0;
    int nborfs = 0;
    int nborfc = 0;
    tot = nbORF(pA,&nborfs,&nborfc);
    printf("Nombre d'ORF totaux : %d\nNombre d'ORF dans le brin sens : %d\nNombre d'ORF dans le brin antisens : %d\n", tot,nborfs,nborfc);
    Afficher_ORF(pA);
    freeArbre(pA);
    */

	/*
    int nbSeq = 0;
    tySeqADN **ts = LireFastaMul("NC_020075.ffn",&nbSeq);
    printf("Nombre de séquences présentes dans le fichier : %d\n",nbSeq);
    freeSeqADN(ts);
	*/
    
        

    
    tyArbre *pA = NULL;
    pA = readFasta("NC_020075.fna",100);
    int nbf = nbFeuilles(pA);
    int pf = profondeur(pA);
    printf("Nombre de feuilles : %d\n",nbf);
    printf("Profondeur : %d\n",pf);
    int tot = 0;
    int nborfs = 0;
    int nborfc = 0;
    tot = nbORF(pA,&nborfs,&nborfc);
    printf("Nombre d'ORF totaux : %d\nNombre d'ORF dans le brin sens : %d\nNombre d'ORF dans le brin antisens : %d\n", tot,nborfs,nborfc);
    freeArbre(pA);

    
    return 0;
}
