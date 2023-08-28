#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ManipSeqADN.h"
#include "ManipSeqSimple.h"


//Allocation et desallocation
tySeqADN* newSeqADN(){
    
    tySeqADN *ts = malloc(sizeof(tySeqADN));
	if (ts==NULL){
		printf("Allocation BUG");
		return NULL;
	}

    ts->seq = NULL;
    ts->comp = NULL;
    ts->lg = 0;
    ts->GC = -1; 

	return ts;
}

//Liberation de sequence
void freeSeqADN(tySeqADN *pS){
    if (pS->seq!=NULL){
        FreeSeq(pS->seq);
    }
    if (pS->comp!=NULL){
        FreeSeq(pS->comp);
    }
    free(pS);
}


/***********************************************/
tySeqADN* complementaire(tySeqADN *pS){
    
    tySeqADN *tscomp = newSeqADN();
    tscomp->seq = pS->seq;
    tscomp->comp = BrinComplementaire(pS->seq,pS->lg);
    tscomp->lg = pS->lg;
    tscomp->GC = pS->GC;

	return tscomp;
}

/*******************************/

//Compter le nombre de sequences dans un fichier fasta
int CompterNbSeq(char *nomFi){
    
    //Création d'un pointeur FILE
    FILE *pFi=NULL;
    char buffer[1000];
    // Ouverture du fichier 
    pFi=fopen(nomFi, "r");

    //Check de la bonne ouverture du fichier
    if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier\n");
        return 1;
    }
    
    int nbl = 0;
    while(fgets(buffer,1000,pFi)){
        if (buffer[0]=='>')  
            {
            nbl++;
            }
    }
    fclose(pFi);

    return nbl;

}

/******************************/

//Lire une sequence fasta dans un pointeur FILE
tySeqADN *LireUneSeqFasta(FILE *pFi){
   
   if(pFi==NULL){
        printf ("Erreur du fichier\n");
        return NULL;
    }


    tySeqADN *ts = newSeqADN();
    char buffer[1000];    
    int i = 0;
    ts->seq = malloc(sizeof(char));
    ts->seq[0]='\0';

    while(fgets(buffer,1000,pFi)){
       if(buffer[0]!='>'){
           int lg = strlen(buffer);
           if(buffer[lg-1]=='\n'){
               buffer[lg-1]='\0';
           }
           
            ts->lg+=strlen(buffer);
            ts->seq = realloc(ts->seq,(ts->lg+1)*sizeof(char));
            strcat(ts->seq,buffer);
            i=1;
       }
        else if (i==1) {break;}
    }
    
    ts->comp = BrinComplementaire(ts->seq,ts->lg);
    return ts;
}

/*****************************************/

//Retourne la lecture d'une sequence fasta sous un tySeqADN
tySeqADN *LireFastaSimple(char *nomFi){
    
    FILE *pFi=NULL;
    pFi = fopen(nomFi,"r");
    if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier\n");
        return NULL;
    }
    
    tySeqADN *ts = LireUneSeqFasta(pFi);

    fclose(pFi);
    return ts;
}

/*******************************/

//Lecture de toutes les séquences FASTA
tySeqADN **LireFastaMul(char *nomFi, int *nbSeq){
    
    *nbSeq = CompterNbSeq(nomFi);
    
    tySeqADN **tabseq = malloc(sizeof(tySeqADN) * (*nbSeq));

    FILE *pFi=NULL;
    pFi = fopen(nomFi,"r");
    if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier\n");
        return NULL;
    }

    for (int i=0;i<(*nbSeq);i++){
        tabseq[i] = LireUneSeqFasta(pFi);
    }

    fclose(pFi);

    return tabseq; 
}

/*float BiaisCodons(char *nomFi){
    
    cds_biais = cds_sans_biais = alea_biais = alea_sans_biais = 0;
    
    int *nbSeq = 0;
    tySeqADN **tabseq = LireFastaMul(nomFi,nbSeq);
    
    for(int i = 0; i<*nbSeq;i++){
        
        char *seq = NewSeq(tabseq[i]->lg);
        InitSeqAleav2(seq,tabseq[i]->lg);

        
        chi2icds = calcChi2Conformite(tabseq[i]->seq,tabseq[i]->lg)
        chi2ialea = calcChi2Conformite(tabseq[i]->seq,tabseq[i]->lg)
        
        
        if (chi2icds>5.99){
            cds_sans_biais++;

        }
        if (chi2icds<5.99){
            cds_biais++;
            
        }
    }
    return 0.0
}
*/




