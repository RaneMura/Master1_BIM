#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(){

    int n1,n2;
    printf("Calcul de PGCD\nValeur de n1 -> ");
    scanf("%d",&n1);
    
    printf("\nValeur de n2 -> ");
    scanf("%d",&n2);

    while (n1!=n2){
        if (n1>n2){
            n1=n1-n2;
        }
        else{
            n2=n2-n1;
        }
    }

    printf("n1 = %d\tn2 = %d\n",n1,n2);
    return 0;
}