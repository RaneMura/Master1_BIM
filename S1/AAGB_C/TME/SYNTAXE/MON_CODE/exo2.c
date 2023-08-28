#include <stdio.h>
#include <stdlib.h>

int main(){
    
    printf("Saisir un entier pour l'affichage des valeurs: \n");
    
    int i1;
    scanf("%d",&i1);

    printf("Affichage de l'entier demandé :\n\t---> au format entier : %d\n\t---> au format octal : %o\n\t---> au format héxadécimal : %X\n\n",i1,i1,i1);

    printf("Saisir un second entier diiférent de 0 : \n");

    int i2;
    scanf("%d",&i2);

    printf("Résultat de la division des deux entiers i1 par i2 = %f\n\n",i1/(float)i2);

    return 0;

}