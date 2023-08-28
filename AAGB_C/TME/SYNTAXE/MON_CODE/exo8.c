#include <stdio.h>

int main (){

    int i,j;
    
    printf("Tables de multiplication de 1 a 10\n\n");
    for(i=1;i<=10;i++){
        printf("\tTable de %d\n\n",i);
        for(j=1;j<=10;j++){
            printf("\t%d * %d = %d\n",i,j,i*j);
        }
        printf("\n");
    }
}