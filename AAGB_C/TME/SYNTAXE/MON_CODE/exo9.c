#include <stdio.h>
#include <math.h>

int main (){

    // Boucle while : racine carree
    int a;
    float precision = 0.001;
    float x0 = 1.0;
    float x1 = 1.0;
    float tmp;

    printf("Racine carree : valeur d'entree -> ");
    scanf("%d",&a);


    while(fabs((x1-tmp)/tmp)>precision){
        tmp = x0;
        x1 = (x0+(a/x0))/2;
        x0 = x1;
        
    }

    printf("Racine carree de %d = %f\n",a,x1);

    return 0;

}


