#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ManipSeqADN.h"
#include "ManipSeqSimple.c"


/*Allocation et desallocation*/
tySeqADN* newSeqADN(){
    
    tySeqADN *ts = malloc(sizeof(tySeqADN));
	if (ts==NULL){
		printf("Allocation BUG");
		return NULL;
	}

    ts->seq = NULL;
    ts->lg = 0;
    ts->GC = -1; 

	return ts;
}

void freeSeqADN(tySeqADN *pS){
    if (pS->seq!=NULL){
        FreeSeq(pS->seq);
    }
    free(pS);
}


/***********************************************/
tySeqADN* complementaire(tySeqADN *pS){
    
    tySeqADN *tscomp = newSeqADN();
    tscomp->seq = BrinComplementaire(pS->seq,pS->lg);
    tscomp->lg = pS->lg;
    tscomp->GC = pS->GC;

	return tscomp;
}



/******************************/
tySeqADN *readFasta(char *nomFi){


	return NULL;
}



