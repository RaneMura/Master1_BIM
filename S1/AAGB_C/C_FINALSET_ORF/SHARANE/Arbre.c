#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ManipSeqADN.h"
#include "ManipSeqSimple.h"
#include "Arbre.h"

tyArbre *Ajouter_ORF(tyArbre *pA, char *seq, int nbcodons,int complementaire){
    
    tyArbre *pNew;
    if(pA == NULL){
        pNew = malloc(sizeof(tyArbre));
        pNew->pFG = NULL;
        pNew->pFD = NULL;
        pNew->seq = seq;
        pNew->nbcodons = nbcodons;
        pNew->complementaire = complementaire;

        
        return pNew;
    }

    //STRNCMP RETOURNE 0 SI SEQ EST IDENTIQUE A PA->SEQ , INFÉRIEUR A 0 SI SEQ EST AVANT PA->SEQ DANS L'ORDRE ALPHABETIQUE, POSITIF SI SEQ EST APRES.
    int n;

    if(nbcodons<pA->nbcodons){
        n = nbcodons;
    }
    else{
        n = pA->nbcodons;
    }

    int c = strncmp(seq,pA->seq,n*3);

    if(c<0 || (c==0 && nbcodons<=pA->nbcodons)){
        pA->pFG = Ajouter_ORF(pA->pFG,seq,nbcodons,complementaire);
    }

    else{
        pA->pFD = Ajouter_ORF(pA->pFD,seq,nbcodons,complementaire);
    }

    return pA;
}


//lE BUT EST PEUT ETRE
//DANS LE GÉNOME, TROUVER UN CODON START
//JUMP JUSQU'À UN CERTAIN SEUIL : 300NT OU 100CD
//TROUVER UN CODON STOP
 

tyArbre *Rechercher_ORF_Une_Phase(char *seq, int lg, int nbMinCodons,tyArbre *pA,int complementaire){
    
    int i;
    
    for(i = 0;i<lg;i+=3){
        
        if(estStart(seq+i)){

            int iStop;
            
            for(iStop = i+nbMinCodons*3;iStop<lg;iStop+=3){
                if(estStop(seq+iStop)){
                    /*if (complementaire==0){
                        pA = Ajouter_ORF(pA,seq+i,(iStop-i)/3+1,complementaire);
                        break;
                    }
                    else if (complementaire==1){
                        pA = Ajouter_ORF(pA,rev(seq+i,lg-iStop),(iStop-i)/3+1,complementaire);
                        break;
                    }*/
                    pA = Ajouter_ORF(pA,seq+i,(iStop-i)/3+1,complementaire);
                    break;
                }
            }
            i = iStop;
        }
    }
    return pA;
    
}

tyArbre *Rechercher_ORF(tySeqADN* pS, int nbMinCodons){
    tyArbre *pA = NULL;
   
    pA = Rechercher_ORF_Une_Phase(pS->seq,pS->lg,nbMinCodons,pA,0);
    pA = Rechercher_ORF_Une_Phase(pS->seq+1,pS->lg-1,nbMinCodons,pA,0);
    pA = Rechercher_ORF_Une_Phase(pS->seq+2,pS->lg-2,nbMinCodons,pA,0);

    pA = Rechercher_ORF_Une_Phase(pS->comp,pS->lg,nbMinCodons,pA,1);
    pA = Rechercher_ORF_Une_Phase(pS->comp+1,pS->lg-1,nbMinCodons,pA,1);
    pA = Rechercher_ORF_Une_Phase(pS->comp+2,pS->lg-2,nbMinCodons,pA,1);

    return pA;

}

tyArbre *readFasta(char *nomFi,int nbMinCodons){
    int nbSeq = 0;
    tySeqADN **ts = LireFastaMul(nomFi,&nbSeq);

    tyArbre *pA = NULL;
    for(int i = 0;i<nbSeq;i++){
        pA = Rechercher_ORF(ts[i],nbMinCodons);
    }
    return pA;

}



void Afficher_ORF(tyArbre *pA){
    
    if(pA==NULL){
        return;
    }

    printf("Sequence : ");  
    int i;
    for(i=0;i<pA->nbcodons*3;i++){
        printf("%c",pA->seq[i]);
    }
    printf("\n");
    printf("Nb codons : %d\n", pA->nbcodons);
    printf("Complémentaire ? %d\n\n",pA->complementaire);
    
    Afficher_ORF(pA->pFG);
    Afficher_ORF(pA->pFD);


}

int nbORF(tyArbre *pA, int *ORFsens, int *ORFcomp){
    
    if(pA==NULL){
        return 0;
    }

    if(pA->complementaire==1){
        *ORFcomp+=1;
    }
    else if (pA->complementaire==0){
        *ORFsens+=1;
    }

    return 1 + nbORF(pA->pFG,ORFsens,ORFcomp) + nbORF(pA->pFD,ORFsens,ORFcomp);
}

int nbFeuilles(tyArbre *pA){
    
    if(pA==NULL){
        return 0;
    }

    if(pA->pFG==NULL && pA->pFD==NULL){
        return 1 + nbFeuilles(pA->pFG) + nbFeuilles(pA->pFD);
    }

    else{
         return nbFeuilles(pA->pFG) + nbFeuilles(pA->pFD);
    }

}

int profondeur(tyArbre *pA){
    
    int profG,profD = 0;


    if(pA==NULL){
        fprintf(stderr,"Arbre NULL dans profondeur !\n");
        exit(1);
    }

    if(pA->pFG==NULL && pA->pFD==NULL){
        return 0;
    }

    if(pA->pFG!=NULL){
        profG = profondeur(pA->pFG);
    }

    if(pA->pFD!=NULL){
        profD = profondeur(pA->pFD);
    }

    if (profG>profD){
        return profG +1;
    }
    return profD +1;

}

void freeArbre(tyArbre *pA){
    
    if(pA==NULL){
        return;
    }

    freeArbre(pA->pFG);
    freeArbre(pA->pFD);

    free(pA);
}


