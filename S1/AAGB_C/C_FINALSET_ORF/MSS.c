#include <stdlib.h> 
#include <stdio.h> 
#include  <string.h>
#include <time.h>
#include <math.h>

#include "ManipSeqSimple.h"

char *NewSeq(int lg){
    char *seq = (char *)calloc(lg, sizeof(char));
    if (seq == NULL){
        fprintf(stderr, "Erreur d'allocation");
        return NULL;
    }
    return seq;
}

char *ReallocSeq(char *seq, int lg){
    char *seq2 = realloc(seq, lg * sizeof(char));
    if(!seq2){
        fprintf(stderr, "Reallocation BUG");
    }
    return seq2;
}

void FreeSeq(char *seq){
	free(seq);
}

void AfficheSeq(char seq[], int lg){
    int i;
    for(i=0; i<lg; i++){
        putchar(seq[i]);
    }
    putchar('\n');
}

float All_GC(char seq[], int lg, float *GC0, float *GC1, float *GC2, float *GC3){
    int i;
    int GC_count = 0;

    static float GC[3] = {0.0, 0.0, 0.0};

    for(i=0; i<lg; i++){
        if(seq[i]=='G' || seq[i]=='C'){
            GC_count++;
            int mod = i % 3;
            GC[mod]++;
        }
    }

    *GC0 = GC[0] / (float)lg;
    *GC1 = GC[1] / (float)lg;
    *GC2 = GC[2] / (float)lg;
    *GC3 = GC[3] / (float)lg;

    return (float)GC_count / (float)lg;
}

int estStart(char seq[]){
    return (strncmp(seq, "ATG", 3) == 0);
}


int estStop(char seq[]){
    return (seq[0] == 'T' && (strncmp(seq+1, "AA", 2) == 0 || strncmp(seq+1, "AG", 2) == 0 || strncmp(seq+1, "GA", 2) == 0));
}


char Nt_Complementaire(char nt){
    static char ntc[256] = {0};
    if(ntc['A'] == 0){
        ntc['A'] = 'T';
        ntc['T'] = 'A';
        ntc['G'] = 'C';
        ntc['C'] = 'G';
    }
    return ntc[(unsigned char)nt];
}




