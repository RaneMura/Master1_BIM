#include <stdio.h>

int main (){
    
    //fact for

    int entree;
    int i;
    int fact = 1;

    printf("Factorielle for : valeur de calcul -> ");
    scanf("%d",&entree);

    for(i=1;i<=entree;i++){
        fact*=i;
    }

    printf("factfor(%d) = %d\n",entree,fact);

    return 0;

}