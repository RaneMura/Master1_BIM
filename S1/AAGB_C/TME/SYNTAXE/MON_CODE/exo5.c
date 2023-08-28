#include <stdio.h>
#include <stdlib.h>

float convertir(float val, char dev){
    if (dev == 'f'){
        val/=6.55957;
    }
    if  (dev=='e'){
        val*=6.55957;
    }

    return val;
}


int main(){

    float val;
    char c1;

    printf("Veuillez saisir la devise de conversion :\n\t- e si votre montant est en euros\n\t- f si votre montant est en francs\nValeur entrée : ");
    scanf("%c",&c1);

    printf("Veuillez saisir le montant à convertir : ");
    scanf("%f",&val);

    if (c1=='e'){
        printf ("Montant initial = %f euros\nMontant après conversion : %f francs\n\n",val,convertir(val,c1));
    }

    if (c1=='f'){
        printf ("Montant initial = %f francs\nMontant après conversion : %f euros\n\n",val,convertir(val,c1));
    }

}


