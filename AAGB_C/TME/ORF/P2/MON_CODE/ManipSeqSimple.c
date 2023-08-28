#include <stdlib.h> 
#include <stdio.h> 
#include  <string.h>
#include <time.h>
#include <math.h>

#include "ManipSeqSimple.h"
#include "codons.h"



char *NewSeq(int lg){
	char *seq = (char *)malloc(lg*sizeof(char));
	if (seq==NULL){
		printf("Allocation BUG");
		return NULL;
	}
	return seq;
}

char *ReallocSeq(char *seq, int lg){
	char *seq2 = realloc(seq,lg*sizeof(char));
	if(!seq2){
		printf("Reallocation BUG");
	}
	return seq2;
}

void FreeSeq(char *seq){
	free(seq);
}


void AfficheSeq(char seq[], int lg){
	int i;
	for(i=0;i<lg;i++){
		printf("%c",seq[i]);	
	}
	printf("\n");	
}

void InitSeqAlea(char seq[], int lg){
	int i;
	for(i=0;i<lg;i++){
		int a = rand()%4;
		switch(a){
			case(0) : seq[i] = 'A'; break;
			case(1) : seq[i] = 'T'; break;
			case(2) : seq[i] = 'G'; break;
			case(3) : seq[i] = 'C'; break;
			default : a = rand()%4;
		}
	}
}

void InitSeqAleav2(char seq[], int lg){
	char nucl[] = {'A','T','G','C'};
	for(i=0;i<lg;i++){
		seq[i]=nucl[rand()%4];
	}

}

float All_GC(char seq[], int lg, float *GC1, float *GC2, float *GC3){
	

	*GC1=0;
	*GC2=0;
	*GC3=0;

	int GC_count=0;
	int i;
	
	for(i=0;i<lg;i++){
		if(seq[i]=='G'||seq[i]=='C'){
			GC_count+=1;
			int mod = i%3;
			switch(mod){
				case(0): *GC1+=1; break;
				case(1): *GC2+=1; break;
				case(2): *GC3+=1; break;
			}
		}
	}
	
	float GC0 = GC_count/(float)lg;
	*GC1/=(float)lg; 
	*GC2/=(float)lg; 
	*GC3/=(float)lg; 
	return GC0;
}

int estStart(char *seq){
		
	int i;
	char start[3] = {'A','T','G'};
	for(i=0;i<3;i++){
		if(seq[i]!=start[i]){
			return 0;
		}
	}
	return 1;
}


int estStartCorrection(char seq[]){
	return (seq[0]=='A'&&seq[1]=='T'&& seq[2]=='G');
}

/*Les stop classiques sont TAA TAG et TGA mais pas de TGA pour M. genitalium*/
int estStop(char *seq){
	
	switch(seq[0]){
		case('T'): switch(seq[1]){
				   		case('A'): switch(seq[2]){
										case('A'): return 1;
										case('G'): return 1;
										default : return 0;
									}
						case('G') : switch(seq[2]){
										case('A') : return 1;
										default : return 0;
									}		
						default : return 0;
					}
		default : return 0;
	}
	return 1;
}

int estStopCorrection(char seq[]){
	return (seq[0] = 'T' && ((seq[1]=='A' && (seq[2] =='A' || seq[2]=='G'))||(seq[1]=='G'&& seq[2]=='A')));
}

char Nt_Complementaire(char nt){
	char ntc;
	switch(nt){
			case('A') : ntc = 'T'; break;
			case('T') : ntc = 'A'; break;
			case('G') : ntc = 'C'; break;
			case('C') : ntc = 'G'; break;
			default : ntc = 'N';
		}
	return ntc;
}

char *BrinComplementaire(char *seq,int lg){
	char *seq_comp = NewSeq(lg);
	int  i;
	for(i = 0; i<lg;i++){
		seq_comp[i]=Nt_Complementaire(seq[i]);
	}
	return seq_comp;

}

/* Calcule le chi2 de conformité pour la composition en 3e base par rapport à une distribution
 non biaisée en 3e base, mais respectant le biais de GC*/
float calcChi2Conformite(char *seq, int lg){
  	
	
	float GC1=0.0;
	float GC2=0.0;
	float GC3=0.0;

	float tab[3]={GC1,GC2,GC3};
	float valtheo = All_GC(seq,lg,&tab[0],&tab[1],&tab[2])*lg;
	float valX2 = 0.0;

	int i = 0;
	for (i = 0;i <3;i++){
		float sub = ((tab[i]*lg)-valtheo)*((tab[i]*lg)-valtheo);
		valX2 += sub/valtheo;
	}
	if (valX2>5.99){
		printf("Le test de Chi2 montre qu'il n'y a PAS de biais au niveau du 3eme codon avec un seuil de 0.O5\n");
	}
	if (valX2<5.99){
		printf("Le test de Chi2 montre qu'il y a BIEN un biais au niveau du 3eme codon avec un seuil de 0.O5\n");
	}
	printf("GCGLOBAL : %f\n",valtheo/lg);
	printf("GCThéorique : %f\n",valtheo/(lg*3));
	printf("GC1 : %f\n",tab[0]);
	printf("GC2 : %f\n",tab[1]);
	printf("GC3 : %f\n",tab[2]);

	return valX2;  
}

float calcChi2Conformitev2(char *seq, int lg, float *GCGlobal,float *GC1, float *GC2,float *GC3){
	if (*GCGlobal<0){
		*GCGlobal = All_GC(seq,lg,GC1,GC2,GC3);
		}
	float Chi2;
	int Attendu = *GCGlobal*lg/3;
	Chi2 = (((*GC1*lg-Attendu)*(*GC1*lg-Attendu))/Attendu) + (((*GC2*lg-Attendu)*(*GC2*lg-Attendu))/Attendu) + (((*GC1*lg-Attendu)*(*GC1*lg-Attendu))/Attendu);

	if (Chi2>5.99){
		printf("Le test de Chi2 montre qu'il n'y a PAS de biais au niveau du 3eme codon avec un seuil de 0.O5\n");
	}
	if (Chi2<5.99){
		printf("Le test de Chi2 montre qu'il y a BIEN un biais au niveau du 3eme codon avec un seuil de 0.O5\n");
	}
	
	return Chi2;
}


void AlgoORF(int n){
	
	printf("\nSequence initiale de longueur %d:\n\n",n);
	char *nseq = NewSeq(n);
	InitSeqAlea(nseq,n);
	AfficheSeq(nseq,n);
	
	printf("\nSequence complementaire :\n\n");
	char *nseq_comp = BrinComplementaire(nseq,n);
	AfficheSeq(nseq_comp,n);
	printf("\n");
	
	char percentage = 37;
	float GC1,GC2,GC3,GC1_comp,GC2_comp,GC3_comp;
	float GC0 = All_GC(nseq,n,&GC1,&GC2,&GC3);
	float GC0_comp = All_GC(nseq_comp,n,&GC1_comp,&GC2_comp,&GC3_comp);	
	printf("Pourcentage de G-C :\n\tDans la sequence entiere -> %.2f%c\n\tEn premiere position -> %.2f%c\n\tEn seconde position -> %.2f%c\n\tEn troisieme position -> %.2f%c\n\n",GC0*100,percentage,GC1*100,percentage,GC2*100,percentage,GC3*100,percentage);
	printf("Pourcentage de G-C :\n\tDans la sequence complementaire -> %.2f%c\n\tEn premiere position -> %.2f%c\n\tEn seconde position -> %.2f%c\n\tEn troisieme position -> %.2f%c\n\n",GC0_comp*100,percentage,GC1_comp*100,percentage,GC2_comp*100,percentage,GC3_comp*100,percentage);

	int	nbstart = 0;
	int nbstart_comp = 0;
	int	nbstop = 0;
	int nbstop_comp = 0;

	int i;
	for(i = 0;i+2<n;i++){
		char *tSeq = NewSeq(3);
		char *tSeqcomp = NewSeq(3);

		tSeq[0] = nseq[i];
		tSeq[1] = nseq[i+1];
		tSeq[2] = nseq[i+2];

		tSeqcomp[0] = nseq_comp[i];
		tSeqcomp[1] = nseq_comp[i+1];
		tSeqcomp[2] = nseq_comp[i+2];
	
		nbstart+=estStart(tSeq);
		nbstart_comp+=estStart(tSeqcomp);
	
		nbstop+=estStop(tSeq);
		nbstop_comp+=estStop(tSeqcomp);

		FreeSeq(tSeq);
		FreeSeq(tSeqcomp);
	}

	printf("Nombre de codons dans la sequence initiale :\n\tStart -> %d\n\tStop -> %d\n\n",nbstart,nbstop);
	printf("Nombre de codons dans la sequence complementaire :\n\tStart -> %d\n\tStop -> %d\n\n",nbstart_comp,nbstop_comp);

	float chi2 = calcChi2Conformite(nseq,n);
	printf("Valeur de chi2 = %f\n\n",chi2);


	FreeSeq(nseq);
	FreeSeq(nseq_comp);

}



