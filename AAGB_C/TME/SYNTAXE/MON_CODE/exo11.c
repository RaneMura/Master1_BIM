#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(){

    int n;
    printf("Nombre a tester -> ");
    scanf("%d",&n);

    printf("Liste des nombres premiers jusqu'a %d -> ",n);

    int i;
    int j;
    int prem = 2;

    for (j=2;j<n;j++){
        for(i=2;i<j;i++){
            if (j%i==0){
                //printf("breakpoint\n");
                break;
            }
            if(j%i!=0){
                //printf("not a breakpoint\n");
                //printf("passable %d\n",i);
            }
            prem = j;
           // printf("%d\n",prem);

        }
        if (prem == j){
            printf("%d ",prem);
        }

    }
    printf("\n");

    return 0;

}