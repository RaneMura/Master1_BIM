#include <stdio.h>

int main (){
    
    //fact do-while

    int entree;
    int i = 1;
    int fact = 1;

    printf("Factorielle do-while : valeur de calcul -> ");
    scanf("%d",&entree);

    do{
        fact*=i;
        i++;
    }while(i<=entree);

    printf("factdowhile(%d) = %d\n",entree,fact);

    return 0;

}