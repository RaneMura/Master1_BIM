#include <stdio.h>

int main(){
    char a;

    printf("Donnez un nucleotide : \n");
    scanf("%c",&a);

    switch(a){
        case('a'): printf("Nucleotide complementaire de %c -> t\n",a); break;
        case('t'): printf("Nucleotide complementaire de %c -> a\n",a); break;
        case('g'): printf("Nucleotide complementaire de %c -> c\n",a); break;
        case('c'): printf("Nucleotide complementaire de %c -> g\n",a); break;
        default : printf("Base invalide\n");
    }
    
    return 0;

}