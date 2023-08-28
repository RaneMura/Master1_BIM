#include <stdlib.h> 
#include <stdio.h> 
#include  <string.h> 
#include  <assert.h> 

#include "ManipSeqSimple.h"


char *NewSeq(int lg){

	char *s=NULL;
	s=malloc(lg*sizeof(char));
	if(s==NULL){
		fprintf(stderr, "NewSeq:: PB MALLOC, EXITING\n");
		exit(1);
	}

    return s;
}

char *ReallocSeq(char *seq, int new_lg){

	char *s=NULL;
	s=realloc(seq, new_lg*sizeof(char));
	if(s==NULL){
		fprintf(stderr, "ReallocSeq:: PB REALLOC, EXITING\n");
		exit(1);
	}
	return s;
}

void FreeSeq(char *seq){
	free(seq);

}

/*Fonctions de manipulation simple de sequence ADN sous forme de chaine de caracteres*/

/*Retourne un nombre entre 0 et 3 inclus*/
int NbEntre0Et3(){

    return rand()%3;
}

void AfficheSeq(char seq[], int lg){

	int i;
	for (i=0; i<lg; i++)
		fprintf(stdout, "%c", seq[i]);
	fprintf(stdout, "\n");
}



void InitSeqAlea(char seq[], int lg){
	int i, r;
	char base[]={'A', 'T', 'G', 'C'};
	
	for(i=0;i<lg;i++){
		r=NbEntre0Et3();
		seq[i]=base[r];
	}
}

float All_GC(char seq[], int lg, float *GC1, float *GC2, float *GC3){
	int i, GC=0;
	*GC1=*GC2=*GC3=0;
	
	for(i=0;i<lg; i++){
		if(seq[i]=='G' || seq[i]=='C'){
			GC++;
        
    		switch(i%3){
    			case 0: *GC1=*GC1+1; break;
    			case 1: *GC2=*GC2+1; break;
    			case 2: *GC3=*GC3+1; break;
    		  }
        }
    }
		
	*GC1=*GC1/lg;
	*GC2=*GC2/lg;
	*GC3=*GC3/lg;
	return (float)GC/lg;
}


char Nt_Complementaire(char nt){
	switch(nt){
		case 'A': return 'T';
		case 'T': return 'A';
		case 'G': return 'C';
		case 'C': return 'G';
		default: return 'X';
	}
    return 'X';
}


int estStart(char *seq){
	if(seq[0]=='A' && seq[1]=='T' && seq[2]=='G')
		return 1;
	else
		return 0;
}

/*Les stop classiques sont TAA TAG et TGA mais pas de TGA pour M. genitalium*/
int estStop(char *seq){
	if(seq[0]=='T' && 
			((seq[1]=='A' && (seq[2]=='A' || seq[2]=='G')) ||
			(seq[1]=='G' && seq[2]=='A')))
		return 1;
	else
		return 0;
}


char *BrinComplémentaire(char *seq, int lg){
    char *seq_c=NewSeq(lg);
    int i;
    for(i=0;i<lg;i++){
        seq_c[lg-i-1]=Nt_Complementaire(seq[i]);
    }
    return(seq_c);

}


/* Calcule le chi2 de conformité pour la composition en 3e base par rapport à une distribution
 non biaisée en 3e base, mais respectant le biais de GC*/
float calcChi2Conformite(char *seq, int lg, float GCGlobal ){
    
    
    float GC1=0, GC2=0,GC3=0,GCAttendu, Chi2, GCSeq, AT, ATTendu;
    
    /*tmp*/
    /*FILE *pFi;
    char nomFi[10]="";
    sprintf(nomFi, "%d.txt", numFi);

    pFi=fopen(nomFi, "a");*/
    /*Calcul des frequences de tous les codons, et du GC en 3e position*/
    /*Le dernier codon est un codon stop, on ne va pas jusque là*/
    GCSeq=All_GC(seq, lg, &GC1, &GC2, &GC3);
    GC1*=lg;
    GC2*=lg;
    GC3*=lg;

    AT=lg-(GC1+GC2+GC3);


    GCAttendu=GCSeq*lg/3.0;
    ATTendu=lg/3.0-GCAttendu;

    if(GCAttendu<5 || GC1<5 || GC2<5 || GC3<5 ||AT<5 || ATTendu<5){
        //fprintf(stderr, "calcChi2Conformite:: Calcul impossible car <5: GCAttendu %f GC1 %f GC2 %f GC3 %f AT %f ATTendu %f\n", GCAttendu, GC1, GC2, GC3, AT, ATTendu);
        return -1;
    }


    Chi2=(GC1-GCAttendu)*(GC1-GCAttendu)/GCAttendu+ 
        (GC2-GCAttendu)*(GC2-GCAttendu)/GCAttendu+ 
        (GC3-GCAttendu)*(GC3-GCAttendu)/GCAttendu +
        (lg/3.0-GC1-ATTendu)*(lg/3.0-GC1-ATTendu)/ATTendu+ 
        (lg/3.0-GC2-ATTendu)*(lg/3.0-GC2-ATTendu)/ATTendu+ 
        (lg/3.0-GC3-ATTendu)*(lg/3.0-GC3-ATTendu)/ATTendu; //+ (AT- ATTendu)*(AT- ATTendu)/ATTendu;
    
    //A priori pas bon: on n'est pas dans le cas du dé mais plutot dans le cas 3 personnes tirent à pile ou face.
    /*Chi2=(GC1-GCAttendu)*(GC1-GCAttendu)/GCAttendu+ 
        (GC2-GCAttendu)*(GC2-GCAttendu)/GCAttendu+ 
        (GC3-GCAttendu)*(GC3-GCAttendu)/GCAttendu ;*/
    //fprintf(stderr, " lg %d ATTendu %f GCAttendu %f GC1 %f GC2 %f GC3 %f chi2 %f\n", lg, ATTendu, GCAttendu, GC1, GC2, GC3, Chi2);
    //fprintf(stderr, " GCAttendu %f GC1+ GC2 + GC3 %f chi2 %f\n", GCAttendu*3, GC1+ GC2+ GC3, Chi2);

    if(Chi2<0){
        fprintf(stderr, "CHI2 négatif ??: %f somme de %f %f %f \n",Chi2, (GC1-GCAttendu)*(GC1-GCAttendu)/GCAttendu, (GC2-GCAttendu)*(GC2-GCAttendu)/GCAttendu, (GC3-GCAttendu)*(GC3-GCAttendu)/GCAttendu);
        fprintf(stderr, "ORF longueur %d \nEXITING...\n", lg);
        exit(1);
    }

    /*fprintf(pFi, " lg %d ATTendu %f GCAttendu %f GC1 %f GC2 %f GC3 %f chi2 %f\n", lg, ATTendu, GCAttendu, GC1, GC2, GC3, Chi2);
    fclose(pFi);*/

    return Chi2;
    
}


/********************** OLD*/

/*Pour une sequence, calculer la frequence de chaque codon et du GC en 3e position*/
/*A partir de ces frequénces, calculer l'ENC*/

/*Calcul de l'ENC*/
/*$$N_c=2+\frac{9}{F_2}+\frac{1}{F_3}+\frac{5}{F_4}+\frac{3}{F_2-6}$$*/
/*où $F_n$ est l'hétérozygotie moyenne attendue sur les codons dégénérés $n$ fois, que l'on
 calcule ainsi :
 $$F_n=\frac{1}{Q_n}\sum_{a=1}^{Q_n}\frac{n_a\sum_{j=1}^{n}p_j^2-1}{n_a-1}$$
 Dans cette équation $Q_n$ est le nombre d'acides aminés dégénérés $n$ fois, $n_a$ le nombre total de codons employés pour cet acide aminé, et $p_j$ la fréquence d'emploi du codon $j$ codant pour $a$ dans le gène (et non pas relativement à ses synonymes). */
/**************/
float calcENC(char seq[], int lg){
    
    int i, j, k, iSeq;
    int tNCodons[64]; /* nb de chaque codon dans cette orf*/
    int tAA[NBAA]; /* nb d'aa dans cette orfs, une case pour les stop au cas ou*/
    float tSumPj[NBAA]; /*somme des pj^2*/
    float F2=0, F3=0, F4=0, F6=0, ENC=0;
    float epsilon=0.0001;
    
    char codon[4];
    
    memset(tNCodons, 0, sizeof(int)*(64));
    memset(tAA, 0, sizeof(int)*(NBAA));
    //memset(tSumPj, 0, sizeof(float)*(NBAA));
    for(i=0;i<NBAA;i++) tSumPj[i]=epsilon;
    
    
    /*Calcul des fréquences de tous les codons, et du GC en 3e position*/
    /*Le dernier codon est un codon stop, on ne va pas jusque là*/
    for(iSeq=0; iSeq<lg; iSeq+=3){
        tNCodons[COD2IND(seq+iSeq)]++;
    }
    
    /*Calcul de l'ENC*/
    /*calcul des n_a/(n_a-1)*\sum_{j=1}{n}p_j^2-1 pour chaque aa*/
    /*POur chaque codon j, je fait la somme de pj pour l'aa pour lequel il code*/
    codon[3]='\0';
    for(i=0; i<4; i++){
        codon[0]=IND2NT(i);
        for(j=0;j<4;j++){
            codon[1]=IND2NT(j);
            for(k=0;k<4;k++){
                codon[2]=IND2NT(k);
                tAA[AA2IND(tCodon2AA[COD2IND(codon)])]+=tNCodons[COD2IND(codon)];
                tSumPj[AA2IND(tCodon2AA[COD2IND(codon)])]+=(float)tNCodons[COD2IND(codon)]/(lg/3-1)*(float)tNCodons[COD2IND(codon)]/(lg/3-1);
                //fprintf(stderr, "codon %s indice %d aa %c indice %d na %d Sumpj %f\n", codon, COD2IND(codon), tCodon2AA[COD2IND(codon)], AA2IND(tCodon2AA[COD2IND(codon)]), tAA[AA2IND(tCodon2AA[COD2IND(codon)])], tSumPj[AA2IND(tCodon2AA[COD2IND(codon)])] );
            }}}
    /* on soustrait 1 et multiple par n_a/(n_a-1)*/
    for(i=0; i<NBAA; i++){
        tSumPj[i]=((tSumPj[i]-1)*tAA[i])/(tAA[i]-1);
        fprintf(stderr, "AA %d %c nbAA %d Sumpj %f\n", i, IND2AA(i), tAA[i], tSumPj[i]);
    }
    F2 = 1/ (tAA[AA2IND('N')]+ tAA[AA2IND('D')]+ tAA[AA2IND('C')]+ tAA[AA2IND('Q')]+ tAA[AA2IND('E')]+ tAA[AA2IND('H')]+ tAA[AA2IND('K')]+ tAA[AA2IND('F')]+ tAA[AA2IND('Y')])*(tSumPj[AA2IND('N')]+ tSumPj[AA2IND('D')]+ tSumPj[AA2IND('C')]+ tSumPj[AA2IND('Q')]+ tSumPj[AA2IND('E')]+ tSumPj[AA2IND('H')]+ tSumPj[AA2IND('K')]+ tSumPj[AA2IND('F')]+ tSumPj[AA2IND('Y')]);
    F3=1/ tAA[AA2IND('I')]*tSumPj[AA2IND('I')];
    F4=  1/ (tAA[AA2IND('A')]+ tAA[AA2IND('G')]+ tAA[AA2IND('P')]+ tAA[AA2IND('T')])*(tSumPj[AA2IND('A')]+ tSumPj[AA2IND('G')]+ tSumPj[AA2IND('P')]+ tSumPj[AA2IND('T')]);
    F6=  1/ (tAA[AA2IND('R')]+ tAA[AA2IND('L')]+ tAA[AA2IND('S')])*(tSumPj[AA2IND('R')]+ tSumPj[AA2IND('L')]+ tSumPj[AA2IND('S')]);
    
    fprintf(stderr, "F2 %f F3 %f F4%f F6 %f\n", F2, F3, F4, F6);
    
    ENC=2+9/F2+1/F3+5/F4+3/F6;
    
    return ENC;
}

/***********************************************/

/*Calcul du % de GC en xe base*/
/******************************************/
int compteGC3en3(char *seq, int lgSeq){
    
    int iSeq;
    int GC=0;
    
    /*Calcul des frequences de tous les codons, et du GC en 3e position*/
    /*Le dernier codon est un codon stop, on ne va pas jusque là*/
    for(iSeq=0; iSeq<lgSeq-(2+3); iSeq+=3){
        if(seq[iSeq]=='C' || seq[iSeq]=='G')
            GC++;
    }
    /*  for(i=0; i<64; i++){
     freqCodons[i]/=(lgSeq/3-1);
     }*/
    return GC;
}


void ShuffleSeq(char seq[], int lg){
    int i, newi;
    char tmp;
    for(i=0; i<lg; i++){
        newi=rand()%lg;
        tmp=seq[i];
        seq[i]=seq[newi];
        seq[newi]=tmp;
    }
}


float GC(char seq[], int lg){
    int i, GC=0;
    for(i=0;i<lg; i++)
        if(seq[i]=='G' || seq[i]=='C')
            GC++;
    return (float)GC/lg;
}


void InitSeqAle_GCVar(char seq[], int lg, float GC){
    int i;
    float r;
    char base[]={'A', 'T', 'G', 'C'};
    
    for(i=0;i<lg;i++){
        r=rand()/(float)RAND_MAX;
        if (r<=GC){
            seq[i]=base[2+rand()%2];
        }
        else{
            seq[i]=base[rand()%2];
        }
    }
}




