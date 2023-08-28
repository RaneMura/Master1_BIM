#ifndef __ARBRE__
#define __ARBRE__

typedef struct _tyArbre{
    struct _tyArbre *pFG,*pFD; //fils gauche et droit
    char *seq; //pointeur vers le début de l'ORF
    int nbcodons; // nombre de codons dans l'ORF
    int complementaire; //0 si c'est sur le brin et 1 si c'est sur le brin complémentaire
}tyArbre;

tyArbre *Ajouter_ORF(tyArbre *pA, char *seq, int nbcodons,int complementaire);
tyArbre *Rechercher_ORF_Une_Phase(char *seq, int lg, int nbMinCodons,tyArbre *pA,int complementaire);
tyArbre *Rechercher_ORF(tySeqADN* pS, int nbMinCodons);

tyArbre *readFasta(char *nomFi,int nbMinCodons);
void Afficher_ORF(tyArbre *pA);

int nbORF(tyArbre *pA, int *ORFsens, int* ORFcomp);
int nbFeuilles(tyArbre *pA);
int profondeur(tyArbre *pA);
void freeArbre(tyArbre *pA);

#endif
