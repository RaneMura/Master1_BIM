#include <stdio.h>

int main (){
    
    //fact while

    int entree;
    int i = 1;
    int fact = 1;

    printf("Factorielle while : valeur de calcul -> ");
    scanf("%d",&entree);

    while(i<=entree){
        fact*=i;
        i++;
    }

    printf("factwhile(%d) = %d\n",entree,fact);

    return 0;

}