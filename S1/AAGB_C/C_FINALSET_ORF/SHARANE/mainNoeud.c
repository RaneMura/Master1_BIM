#include <stdio.h>
#include <stdlib.h>

typedef struct _tyNoeud{
    char c;
    struct _tyNoeud *pFG,*pFD;
}tyNoeud;

int U(int n){
    if(n==0){
        return 5;
    }

    return 3*U(n-1)+9;
}

void Afficher_Arbre_infixe(tyNoeud *pN){
    //GRD
    if(pN==NULL){
        return;
    }

    
    Afficher_Arbre_infixe(pN->pFG);
    printf("%d ",pN->c);
    Afficher_Arbre_infixe(pN->pFD);
}

void Afficher_Arbre_postfixe(tyNoeud *pN){
    //GDR
    if(pN==NULL){
        return;
    }

    
    Afficher_Arbre_postfixe(pN->pFG);
    Afficher_Arbre_postfixe(pN->pFD);
    printf("%d ",pN->c);
}

void Afficher_Arbre_prefixe(tyNoeud *pN){
    //RGD

    if(pN==NULL){
        return;
    }

    printf("%d ",pN->c);
    Afficher_Arbre_prefixe(pN->pFG);
    Afficher_Arbre_prefixe(pN->pFD);
}

int nbNoeuds(tyNoeud *pN){
    
    if(pN==NULL){
        return 0;
    }

    return 1 + nbNoeuds(pN->pFG) + nbNoeuds(pN->pFD);
}

int nbFeuilles(tyNoeud *pN){
    
    if(pN==NULL){
        return 0;
    }

    if(pN->pFG==NULL && pN->pFD==NULL){
        return 1 + nbFeuilles(pN->pFG) + nbFeuilles(pN->pFD);
    }

    else{
         return nbFeuilles(pN->pFG) + nbFeuilles(pN->pFD);
    }

}

int profondeur(tyNoeud *pN){
    
    int profG,profD = 0;


    if(pN==NULL){
        fprintf(stderr,"Arbre NULL dans profondeur !\n");
        exit(1);
    }

    if(pN->pFG==NULL && pN->pFD==NULL){
        return 0;
    }

    if(pN->pFG!=NULL){
        profG = profondeur(pN->pFG);
    }

    if(pN->pFD!=NULL){
        profD = profondeur(pN->pFD);
    }

    if (profG>profD){
        return profG +1;
    }
    return profD +1;

}

tyNoeud* Ajout_ABR(tyNoeud *pA, char v){
    
    tyNoeud *pN;
    if(pA ==NULL){
        pN = malloc(sizeof(tyNoeud));
        pN->c = v;
        pN->pFG = NULL;
        pN-> pFD = NULL;
        return pN;
    }

    if(v>pA->c){
        pA->pFD = Ajout_ABR(pA->pFD,v);
    }
    else{
        pA->pFG = Ajout_ABR(pA->pFG,v);
    }

    return pA;
}

void Detruire_ABR(tyNoeud *pN){
    
    if(pN==NULL){
        return;
    }

    Detruire_ABR(pN->pFG);
    Detruire_ABR(pN->pFD);
    free(pN);
}

tyNoeud* Recherche(tyNoeud *pA,char v){

    if(pA ==NULL){
        fprintf(stderr,"Arbre NULL dans Recherche  ou valeur absente de l'arbre!\n");
        exit(1);
    }


    if(v == pA->c){
        printf("La valeur %d est presente dans l'arbre\n",v);
        return pA;
    }

    if(v>pA->c){
        return Recherche(pA->pFD,v);
    }
    else{
        return Recherche(pA->pFG,v);
    }

}

int main(){

/*
    //Racine
    tyNoeud* pR;
    pR = malloc(sizeof(tyNoeud));
    pR->c = 5;
    
    //Fils G n1
    pR->pFG =  malloc(sizeof(tyNoeud));
    pR->pFG->c = 3;

    //Fils G/G n2
    pR->pFG->pFG =  malloc(sizeof(tyNoeud));
    pR->pFG->pFG->c = 2;

    //Feuille G/G/G ET G/G/D n3
    pR->pFG->pFG->pFG = NULL;
    pR->pFG->pFG->pFD = NULL;

     //Fils G/D n2
    pR->pFG->pFD =  malloc(sizeof(tyNoeud));
    pR->pFG->pFD->c = 4;

    //Feuille G/D/G ET G/D/D n3
    pR->pFG->pFD->pFG = NULL;
    pR->pFG->pFD->pFD = NULL;

    //Fils D n1
    pR->pFD =  malloc(sizeof(tyNoeud));
    pR->pFD->c = 9;

    //Feuille D/G ET D/D n2    
    pR->pFD->pFG = NULL;
    pR->pFD->pFD = NULL;

    printf("Parcours infixe de l'arbre : \n");
    Afficher_Arbre_infixe(pR);
    printf("\n");

    printf("Parcours prefixe de l'arbre : \n");
    Afficher_Arbre_prefixe(pR);
    printf("\n");

    printf("Parcours postfixe de l'arbre : \n");
    Afficher_Arbre_postfixe(pR);
    printf("\n");

    printf("Nombre de noeuds dans l'arbre : %d\n", nbNoeuds(pR));
    printf("Nombre de feuilles dans l'arbre : %d\n", nbFeuilles(pR));
    printf("Profondeur de l'arbre : %d\n", profondeur(pR));

*/
    //Creer Arbre bleu avec Ajout_ABR   

    tyNoeud *pR = NULL;
    pR = Ajout_ABR(pR,5);
    pR = Ajout_ABR(pR,3);
    pR = Ajout_ABR(pR,4);
    pR = Ajout_ABR(pR,2);
    pR = Ajout_ABR(pR,9);

    // Afficher, compter les noeuds, les feuilles et calculer la profondeur

    printf("Parcours infixe de l'arbre : \n");
    Afficher_Arbre_infixe(pR);
    printf("\n");

    printf("Parcours prefixe de l'arbre : \n");
    Afficher_Arbre_prefixe(pR);
    printf("\n");

    printf("Parcours postfixe de l'arbre : \n");
    Afficher_Arbre_postfixe(pR);
    printf("\n");

    printf("Nombre de noeuds dans l'arbre : %d\n", nbNoeuds(pR));
    printf("Nombre de feuilles dans l'arbre : %d\n", nbFeuilles(pR));
    printf("Profondeur de l'arbre : %d\n", profondeur(pR));

    //Recherche 3
    tyNoeud *pS = NULL;
    pS = Recherche(pR,8);
    printf("%d\n",pS->c);

    // Liberer 

    Detruire_ABR(pR);

    return 0;

}
