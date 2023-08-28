#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "Rain.h"


int main()
{

    tyCase t[6] = {{1,0},{2,0},{1,0},{1,0},{3,0},{2,0}};
    printf("%d\n",t[0].barre);
    
    int som_tab_init = sommeTab(t,6);
    printf("Quantité d'eau retenue initiale = %d\n", som_tab_init);

    int maxibar = maximumBarreTab(t,6);
    printf("Indice avec la taille de barre maximale : %d\n",maxibar);
 

    //Problème avec l'algo dans fillWater  : oublié de calculer avec les maxima locaux.

    fillWater(t,6);

    afficheRainWatter(t,6);

    //int nbl = compter_lignes("unTab.txt");
    //printf("Nombre de lignes dans la séquence : %d\n",nbl);

    //int *p_nbVal = 0;
    //tyCase *tc = lire_tableau("unTab.txt",p_nbVal);
    
    //afficheRainWatter(tc,6);

    //free(tc);
    
    return 0;
}