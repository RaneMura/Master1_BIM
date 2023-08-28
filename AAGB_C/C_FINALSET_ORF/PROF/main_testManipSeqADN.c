#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "ManipSeqSimple.h"
#include "ManipSeqADN.h"

#define SIZE_SEQ 10000


char numFi=1;



/************************************/
int main(){


	tySeqADN *pS=NULL, **tabCDS=NULL;//, *pS2;
	char *seqAlea=NULL;
	int nbCDS, nbCDSBiaises=0, i;
	float GC, GC1, GC2, GC3, chi2=0;

	srand(time(NULL));

	pS=LireFastaSimple("../NC_020075.fna");
 	GC=All_GC(pS->seq, pS->lg, &GC1, &GC2, &GC3);
	printf("Lu %d nt GC: %f\n", pS->lg, GC);

	tabCDS=LireFastaMul("../NC_020075.ffn", &nbCDS);

	printf("Lu %d CDS\n", nbCDS);

	//AfficheSeq(tabCDS[0]->seq, tabCDS[0]->lg);
	//AfficheSeq(pS->seq, pS->lg);

	//1
  	nbCDSBiaises=0;
	for(i=0;i<nbCDS; i++){
 		chi2=calcChi2Conformite(tabCDS[i]->seq, tabCDS[i]->lg, GC);
 		//printf("%6d %6d %6f\n", i, tabCDS[i]->lg, chi2);
 		if(chi2>5.99){
 			nbCDSBiaises++;
 		}
 	}
 	printf("%d/%d (%f) séquences biaisées\n", nbCDSBiaises, nbCDS, (float)nbCDSBiaises/nbCDS*100);
 	numFi++;

 	//2
  	nbCDSBiaises=0;
	for(i=0;i<nbCDS; i++){
		ShuffleSeq(tabCDS[i]->seq, tabCDS[i]->lg);
 		chi2=calcChi2Conformite(tabCDS[i]->seq, tabCDS[i]->lg, GC);
 		//printf("%6d %6d %6f\n", i, tabCDS[i]->lg, chi2);
 		if(chi2>5.99){
 			nbCDSBiaises++;
 		}
 	}
 	printf("%d/%d (%f) séquences biaisées si shuffle CDS\n", nbCDSBiaises, nbCDS, (float)nbCDSBiaises/nbCDS*100);
 	numFi++;

 	//3
 	nbCDSBiaises=0;
 	for(i=0;i<nbCDS; i++){
 		seqAlea=ReallocSeq(seqAlea, tabCDS[i]->lg);
 		//seqAlea=ReallocSeq(seqAlea, 10000);
 		InitSeqAlea(seqAlea, tabCDS[i]->lg);
 		//InitSeqAlea(seqAlea, 1000);
 		//chi2=calcChi2Conformite(seqAlea, 1000, 0.5);
 		chi2=calcChi2Conformite(seqAlea, tabCDS[i]->lg, GC);
 		//printf("%6d %6d %6f\n", i, tabCDS[i]->lg, chi2);
 		if(chi2>4.99){
 			nbCDSBiaises++;
 		}
 	}
 	printf("%d/%d (%f) séquences biaisées si aléatoire \n", nbCDSBiaises, nbCDS, (float)nbCDSBiaises/nbCDS*100);
 	numFi++;

 	//4
 	nbCDSBiaises=0;
 	for(i=0;i<nbCDS; i++){
 		seqAlea=ReallocSeq(seqAlea, tabCDS[i]->lg);
 		//seqAlea=ReallocSeq(seqAlea, 10000);
 		GC=All_GC(tabCDS[i]->seq, tabCDS[i]->lg, &GC1, &GC2, &GC3);
 		InitSeqAle_GCVar(seqAlea, tabCDS[i]->lg, GC);
 		//InitSeqAlea(seqAlea, 1000);
 		//chi2=calcChi2Conformite(seqAlea, 1000, 0.5);
 		chi2=calcChi2Conformite(seqAlea, tabCDS[i]->lg, GC);
 		//printf("%6d %6d %6f\n", i, tabCDS[i]->lg, chi2);
 		if(chi2>4.99){
 			nbCDSBiaises++;
 		}
 	}
 	printf("%d/%d (%f) séquences biaisées si aléatoire avec GC aléatoire aussi\n", nbCDSBiaises, nbCDS, (float)nbCDSBiaises/nbCDS*100);
 	numFi++;

 	//5
 	nbCDSBiaises=0;
 	for(i=0;i<nbCDS; i++){
 		int pos=rand()%(pS->lg-tabCDS[i]->lg);
 		chi2=calcChi2Conformite(pS->seq+pos, tabCDS[i]->lg, GC);
 		//printf("%6d %6d %6d %6f\n", i, tabCDS[i]->lg, pos, chi2);
 		if(chi2>4.99){
 			nbCDSBiaises++;
 		}
 	}
 	//Normal que ce soit biaisé: il y a du codant partout, et qu'on compte entre 1, 2 et 3 ou entre 2, 3 et 1, c'est tout autant biaisé.
 	printf("%d/%d (%f) séquences biaisées si position aléatoire\n", nbCDSBiaises, nbCDS, (float)nbCDSBiaises/nbCDS*100);
 	numFi++;

 /*	nbCDSBiaises=0;
 	for(i=0;i<pS->lg; i+=1000){
 		int lg=rand()%(pS->lg-i);
 		chi2=calcChi2Conformite(pS->seq+i, lg, GC);
 		//printf("%6d %6d %6f\n", i, tabCDS[i]->lg, chi2);
 		if(chi2>4.99){
 			nbCDSBiaises++;
 		}
 	}
 	printf("%d/%d (%f) séquences biaisées si lg  aléatoire, all seq\n", nbCDSBiaises, nbCDS, (float)nbCDSBiaises/nbCDS*100);

*/ 	free(seqAlea);
 	FreeTabSeq(tabCDS, nbCDS);
 	FreeSeqADN(pS);
	return 0;
}





