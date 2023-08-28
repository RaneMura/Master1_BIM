#include <stdio.h>
#include <stdlib.h>

int main(){
    
    float f1 = 0.1;
    float f2 = 0.1;

    int i1 = 2;
    int i2 = 2;

    //Comparaison q1

    if(f1 + f2 == 0.2) {
        printf("Les deux floats sont égaux\n\n");
    }
    else{
        printf(" Les deux floats diffèrent\n\n");
    }

    //Comparaison q2

    if(i1 + i2 == 4) {
        printf("Les deux entiers sont égaux\n\n");
    }
    else{
        printf(" Les deux entiers diffèrent\n\n");
    }

    //Comparasion q3
    if(f1 - f2 < 0.000001) {
        printf("Les deux floats sont égaux\n\n");
    }
    else{
        printf(" Les deux floats diffèrent\n\n");
    }

    return 0;

}