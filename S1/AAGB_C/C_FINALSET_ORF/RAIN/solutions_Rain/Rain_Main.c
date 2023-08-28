#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "Rain.h"

#define N 6 

int main(int argc, char **argv)
{

   int n=N;
    tyCase *tEau;
	tyCase tEau2[N] = {{1,0}, {2,0}, {1,0}, {1,0}, {3,0}, {2,0}};
	n=N;
	afficheRainWatter(tEau2, n);
	printf("Plus grande barre en : %d\n", maximumBarreTab(tEau2, n));
	fillWater(tEau2,n);
	printf("Quantité d'eau stockée: %d\n", sommeTab(tEau2, n));
	afficheRainWatter(tEau2, n);


	if(argc<2){
		fprintf(stderr, "%s:: not enough arguments", argv[0]);
		fprintf(stderr, "USAGE %s <input file>", argv[0]);
		exit(1);
	}

	tEau=lire_tableau(argv[1],  &n);
	afficheRainWatter(tEau, n);
	fillWater(tEau,n);
	printf("Quantité d'eau stockée: %d\n", sommeTab(tEau, n));
	afficheRainWatter(tEau, n);

    return 0;
}