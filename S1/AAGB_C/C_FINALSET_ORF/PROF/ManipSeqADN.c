
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "ManipSeqADN.h"
#include "ManipSeqSimple.h"


#define MAX_BUFF 10240
#define SIZE_SEQ 1000


/*Allocation et desallocation*/
tySeqADN* NewSeqADN(){

	tySeqADN* pS=NULL;
	pS=(tySeqADN*)malloc(sizeof(tySeqADN));
	if(pS==NULL){
		fprintf(stderr, "NewSeqADN:: Pb Allocation\n");
		return NULL;
	}
	pS->lg=0;
	pS->seq=NULL;
	pS->GC=-1;
	pS->seqComp=NULL;
	
	return pS;
}

tySeqADN* FreeSeqADN(tySeqADN *pS){

	if(pS){
		if(pS->seq)
			free(pS->seq);
		if(pS->seqComp)
			free(pS->seqComp);
		free(pS);
	}
	return NULL;
}



/***********************************************/
void Complementaire(tySeqADN *pS){
	
	pS->seqComp=BrinComplémentaire(pS->seq, pS->lg);

}




/******************************/
tySeqADN *LireUneSeqFasta(FILE *pFi){

	tySeqADN *pS=NULL;
	char buffer[MAX_BUFF];
	int lgBuff, i,  flag=0;
	
	pS=NewSeqADN();
	
	while(fgets(buffer, MAX_BUFF, pFi)){
		if(buffer[0]!='>'){
			flag=1;
			lgBuff=strlen(buffer);
			if(buffer[lgBuff-1]=='\n'){
				buffer[lgBuff-1]='\000';
				lgBuff--;
			}
			assert(lgBuff>0);
			//printf("last car: <%c>\n", buffer[lgBuff-1]);
			pS->seq=(char*)realloc(pS->seq, sizeof(char)*(pS->lg+lgBuff));
			if(pS->seq==NULL){
				fprintf(stderr, "readFasta:: pb de malloc\n Exiting...\n");
				exit(1);
			}
			for(i=0;i<lgBuff;i++){
				pS->seq[i+pS->lg]=buffer[i];
			}

			pS->lg+=lgBuff;
		}
		else{
			if(flag==1)
				break;
		}
	}
	return pS;
}



tySeqADN *LireFastaSimple(char *nomFi){
	
	FILE *pFi;
	tySeqADN *pS;
	pFi=fopen(nomFi, "rt");
	if(pFi==NULL){
		fprintf(stderr, "readFasta:: Can not open %s\n", nomFi);
		return NULL;
	}
	pS=LireUneSeqFasta(pFi);
	fclose(pFi);
	return pS;

}

int CompterNbSeq(char *nomFi){

	FILE *pFi;
	char buffer[MAX_BUFF];
	int nbSeq=0;

	pFi=fopen(nomFi, "rt");
	if(pFi==NULL){
		fprintf(stderr, "readFasta:: Can not open %s\n", nomFi);
		return -1;
	}
	while(fgets(buffer, MAX_BUFF, pFi)){
		if(buffer[0]=='>')
			nbSeq++;
	}
	fclose(pFi);

	return nbSeq;
}

/******************************/
tySeqADN **LireFastaMul(char *nomFi, int *nbSeq){

	FILE *pFi;
	tySeqADN **tpS=NULL;

	int i;

	*nbSeq=CompterNbSeq(nomFi);
	tpS=malloc(sizeof(tySeqADN*)*(*nbSeq));

	pFi=fopen(nomFi, "rt");
	if(pFi==NULL){
		fprintf(stderr, "readFasta:: Can not open %s\n", nomFi);
		return NULL;
	}
	for(i=0; i<*nbSeq;i++){
		tpS[i]=LireUneSeqFasta(pFi);
		assert(tpS[i]->lg >0);
	}


	return tpS;
}

void FreeTabSeq(tySeqADN **tpSeq, int nbSeq){
	int i;
	for (i=0;i<nbSeq;i++){
		FreeSeqADN(tpSeq[i]);
	}
	free(tpSeq);
}





