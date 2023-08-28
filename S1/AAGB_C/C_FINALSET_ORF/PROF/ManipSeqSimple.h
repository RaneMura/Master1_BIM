

#ifndef __MANIP_SEQ_SIMPLE__
#define __MANIP_SEQ_SIMPLE__

char *NewSeq(int lg); //malloc
char *ReallocSeq(char *seq, int new_lg);
void FreeSeq(char *seq);


void AfficheSeq(char seq[], int lg);
void InitSeqAlea(char seq[], int lg);
float All_GC(char seq[], int lg, float *GC1, float *GC2, float *GC3);

char Nt_Complementaire(char nt);
int estStart(char *seq);
int estStop(char *seq);

float calcChi2Conformite(char *seq, int lg, float GCGlobal );

char *BrinComplémentaire(char *seq, int lg);


void ShuffleSeq(char seq[], int lg);
void InitSeqAle_GCVar(char seq[], int lg, float GC);

#endif
