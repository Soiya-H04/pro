#include <stdio.h>
#include <stdlib.h> 
#include <time.h>

int main()
{
    srand(time(NULL));
    int n = rand();
    printf("%d\n", n);
    printf("RAND_MAX: %d\n", RAND_MAX);

    double random_number = (double)rand() / RAND_MAX;
    printf("Random number between 0 and 1: %.6f\n", random_number);

    return 0;
}