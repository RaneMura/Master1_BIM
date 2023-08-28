#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define MAXI 1000

//Q1
typedef struct _Atom{
    int resNum;
    char *resType;
    float CV;
    float x;       
    float y;
    float z;
}Atom;

//Q2
int nbAt(char *nomFi){

    FILE *pFi=NULL;
    pFi=fopen(nomFi, "r");

    if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier\n");
        return 0;
    }

    int nbl = 0;
    char buffer[MAXI];

    while(fgets(buffer,1000,pFi)){
        nbl++;
    }
    fclose(pFi);

    return nbl;
}

Atom* LireunCA(char *nomFi,int *nbl){



    FILE *pFi=NULL;
    pFi=fopen(nomFi, "r");
    if(pFi==NULL){
        printf ("Erreur a l ’ouverture du fichier\n");
        return NULL;
    }

    *nbl = nbAt(nomFi);
    Atom *tab = malloc(sizeof(Atom) * (*nbl));
    if(tab==NULL){
        printf ("Erreur a l ’ouverture du fichier\n");
        return NULL;
    }

    char buffer[MAXI];
    int i=0;
    while (fgets(buffer,MAXI,pFi) != NULL){
        int resNum;
        char resType[4];
        float x;
        float y;
        float z;
        sscanf(buffer, "%s %d %f %f %f",resType,&resNum,&x,&y,&z);

        tab[i].resType = malloc(4 * sizeof(char));
        if (tab[i].resType == NULL) {
            printf("Erreur\n");
            return NULL;
        }

        strcpy(tab[i].resType, resType);
        tab[i].resNum = resNum;
        tab[i].CV = 0.0;
        tab[i].x = x;
        tab[i].y = y;
        tab[i].z = z;
        i++;
    }

    fclose(pFi);

    return tab;
}


void AfficheAt(Atom* tab, int nbl){

    for(int i = 0; i<nbl;i++){
         printf("Atom %d: resNum=%d resType=%s CV=%f x=%f y=%f z=%f\n", i, tab[i].resNum, tab[i].resType,tab[i].CV, tab[i].x, tab[i].y, tab[i].z);
    }
}

void freeAt(Atom at){
    free(at.resType);
}

//Q3

float CalculerDistance(Atom A1, Atom A2){
    float i =sqrt(pow(A2.x-A1.x,2) + pow(A2.y-A1.y,2)+ pow(A2.z-A1.z,2)); 
    return i;
}

//-lm a la fin pour la compliation

//Q4

Atom *TrouverAtomeAutour(float dist, Atom* tabInit, Atom atomRef, int nba, int *trouve){
    
    Atom *tabn = malloc(sizeof(Atom)*nba);
    int tro = 0;

    for(int i =0;i<nba;i++){

        if (CalculerDistance(atomRef,tabInit[i])<dist) {
            tabn[tro]=tabInit[i];
            tro++;
        }
    }
    *trouve = tro;
    return tabn;

}

//Q5

float CalculerCVunAtome(Atom atomRef, Atom * lesAtomes, int nbca, float dist){
    int trouve = 0;
    Atom *aut = TrouverAtomeAutour(dist,lesAtomes,atomRef,nbca, &trouve);

    float deno = 0.0;
    float x = 0.0;
    float y = 0.0;
    float z = 0.0;



    for (int i=0 ; i<trouve;i++){
        x += aut[i].x - atomRef.x; 
        y += aut[i].y - atomRef.y;
        z += aut[i].z - atomRef.z;

        deno += CalculerDistance(atomRef,aut[i]); 

    }
    printf("x : %f\n",x);
    printf("y : %f\n",y);
    printf("z : %f\n",z);

    
    float num =sqrt(pow(x-atomRef.x,2) + pow(y-atomRef.y,2)+ pow(z-atomRef.z,2));
    printf("%f\n",num);
    printf("%f\n",deno);
    return 1-(num/deno);
}

//-g avant le o
//gdb ./ficher
//run, up

int main(){
    
    int nba = 0; 
    Atom *tab = LireunCA("CAsimples.txt",&nba);
    
    AfficheAt(tab,nba);
    printf("dist01 = %f\n",CalculerDistance(tab[0],tab[1]));
    printf("dist02 = %f\n",CalculerDistance(tab[0],tab[2]));
    printf("dist12 = %f\n",CalculerDistance(tab[1],tab[2]));

    int trouve = 0;
    Atom *tabaut = TrouverAtomeAutour(7,tab,tab[1],nba,&trouve);
    AfficheAt(tabaut,trouve);

    tab[0].CV = CalculerCVunAtome(tab[0],tab,nba,5.0);
    tab[1].CV = CalculerCVunAtome(tab[1],tab,nba,5.0);
    tab[2].CV = CalculerCVunAtome(tab[2],tab,nba,5.0);

    printf("CV ATOME 0 : %f\n",tab[0].CV);
    printf("CV ATOME 1 : %f\n",tab[1].CV);
    printf("CV ATOME 2 : %f\n",tab[2].CV);

    free(tab);
    free(tabaut);

    return 0;
}