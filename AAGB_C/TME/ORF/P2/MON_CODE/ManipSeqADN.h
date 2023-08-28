
#ifndef __MANIP_SEQ_ADN__
#define __MANIP_SEQ_ADN__

typedef struct {
	char *seq;
	int lg;
	float GC;
} tySeqADN;


tySeqADN *readFasta(char *nomFi);
tySeqADN* complementaire(tySeqADN *pS);
void freeSeqADN(tySeqADN *pS);
tySeqADN* newSeqADN();


#endif
