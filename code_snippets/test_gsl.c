/* Standard libraries */
#include <stdio.h>      /* printf, scanf, NULL */
#include <stdlib.h>     /* calloc, exit, free */
#include <math.h>

/* GSL libraries */
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>


const gsl_rng_type * TYPE_RNG;
gsl_rng * rng;


int main(int argc,char *argv[]){
    int i,x;
    int n=20;


    /* Set up GSL variables for random numbers, and the values for n_runs and i_startrun */
    gsl_rng_env_setup();
    /* Set up gsl seed: */
    TYPE_RNG = gsl_rng_default;
    rng = gsl_rng_alloc (TYPE_RNG);


    for(i=0; i<100; i++){
	x=gsl_rng_uniform_int(rng, n);
	printf("%i %i\n",i,x);
    }
    gsl_rng_free(rng);

    
    return 0;
}
