
/* Standard libraries */
#include <stdio.h>      /* printf, scanf, NULL */
#include <stdlib.h>     /* calloc, exit, free */

/* GSL libraries */
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>

int main(int argc,char *argv[]){
    int i,x;
    int n=20;

    /* Set up GSL variables for random numbers, and the values for n_runs and i_startrun */
    gsl_rng_env_setup();


    for(i=0; i<10; i++){
	printf("%i\n",i);
    }
    
    return 0;
}
