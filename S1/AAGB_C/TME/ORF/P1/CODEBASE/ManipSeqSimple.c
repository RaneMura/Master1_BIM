#include <stdlib.h> 
#include <stdio.h> 
#include  <string.h> 

#include "ManipSeqSimple.h"
#include "codons.h"



char *NewSeq(int lg){

	return NULL;
}

char *ReallocSeq(char *seq, int lg){

	return NULL;
}
void FreeSeq(char *seq){

}


void AfficheSeq(char seq[], int lg){

}


void InitSeqAlea(char seq[], int lg){
}

float All_GC(char seq[], int lg, float *GC1, float *GC2, float *GC3){

	return 0;
}



char Nt_Complementaire(char nt){
	return 0;
}


int estStart(char *seq){
	return 0;
}

/*Les stop classiques sont TAA TAG et TGA mais pas de TGA pour M. genitalium*/
int estStop(char *seq){
	return 0;
}



/* Calcule le chi2 de conformité pour la composition en 3e base par rapport à une distribution
 non biaisée en 3e base, mais respectant le biais de GC*/
float calcChi2Conformite(char *seq, int lg, float GCGlobal ){
  	return 0;  
}



