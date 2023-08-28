#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "ManipSeqSimple.h"
#include "ManipSeqADN.h"


int main(){
    
    int n = 1000;

    tySeqADN *pS, *pComp;//, *pS2;
    
    pS = newSeqADN();
    pS->seq = NewSeq(n);
    pS->lg = n;
    InitSeqAlea(pS->seq,n);

    pComp = complementaire(pS);
    
    printf("Affichage de la sequence initiale : \n\n");
    AfficheSeq(pS->seq,pS->lg);

    printf("\n\nAffichage de la sequence complementaire : \n\n");
    AfficheSeq(pComp->seq,pComp->lg);
    
    
    //Compilation double : gcc -Wall -o tests ManipSeqSimple.c Main.c
    
    //struct _tySeqADN a;
    //entier b;
    //tySeqADN c = {NULL,200, -1}; seulement a l'initialisation

    //a.lg = 10;
    //a.seq = NewSeq(a.lg)

    //tySeqADN *pA = NULL;
    //pA = malloc(sizeof(tySeqADN));
    //pI = &(a.lg);

    //(*pA).lg = 20;
    // equivalent a pA->lg = 20;

    //points quand c'est des types simples (a) et fleches quand c'est des pointeurs (pA);

    return 0;
}
    
