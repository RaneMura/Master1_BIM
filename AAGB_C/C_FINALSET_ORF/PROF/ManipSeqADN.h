

#ifndef __MANIP_SEQ_ADN__
#define __MANIP_SEQ_ADN__

typedef struct {
	char *seq;
	char *seqComp;
	int lg;
	float GC;
} tySeqADN;


tySeqADN **LireFastaMul(char *nomFi, int *nbSeq);
int CompterNbSeq(char *nomFi);
tySeqADN *LireFastaSimple(char *nomFi);
tySeqADN *LireUneSeqFasta(FILE *pFi);



void Complementaire(tySeqADN *pS);
tySeqADN* FreeSeqADN(tySeqADN *pS);
tySeqADN* NewSeqADN();

void FreeTabSeq(tySeqADN **tpSeq, int nbSeq);


#endif
