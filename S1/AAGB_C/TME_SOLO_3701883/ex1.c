/* Ce programme calcule et affiche le PGCD ou plus grand  diviseur commun des valeurs N1 et N2 */

#include <stdio.h>

#define N1 128
#define N2 135

int pgcd(int nb1, int nb2) {
  while (nb1 != nb2) {
     if (nb1 > nb2) {
        nb1 = nb1 - nb2;
     } 
     else {
        nb2 = nb2 - nb1;
     }
  }
  
  return nb1;
}

int main() {
   
   /* Affichage */
   printf("Le PGCD de %d et de %d vaut %d\n", N1, N2, pgcd(N1,N2));
   
   return 0;
}
