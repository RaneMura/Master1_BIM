#include <stdio.h>

int main (){
    
    int a,b;

    printf("Entrez une valeur pour a\n");
    scanf("%d",&a);

    printf("Entrez une valeur pour b\n");
    scanf("%d",&b);

    if (a>b)
        {printf("a est plus grand que b\n");}

    else
        {printf("b est au moins aussi grand que a\n");}

    return 0;

}