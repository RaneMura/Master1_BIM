#include <stdio.h>
#include <stdlib.h>

int main(){

    printf("Saisir un caractère : \n");

    char c1;
    scanf("%c",&c1);

    printf ("Caractère actuel :\n\t----> Caratère : %c\n\t----> Valeur ASCII %d\n\nCaractère précédènt :\n\t----> Caratère : %c\n\t----> Valeur ASCII %d\n\nCaractère suivant :\n\t----> Caratère : %c\n\t----> Valeur ASCII %d\n\n",c1,c1,c1-1,c1-1,c1+1,c1+1);

    char c2 = 127;
    printf("Valeur 127 avant incréméntation  : %d\n",c2);
    c2++;
    printf("Valeur 127 après incrémentation: %d\n\n",c2);

    return 0; 

}