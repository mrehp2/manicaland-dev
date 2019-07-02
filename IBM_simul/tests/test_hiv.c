#include <stdio.h>
#include "../src/hiv.h"
#include "test.h"

int main(void){
    int test_counter = 0;
    int pass_counter = 0;
    
    // Test the output from the get_spvl_cat() function
    test_counter++;
    if(assert_int_equal(get_spvl_cat(5.4), 3))
        pass_counter++;
    
    test_counter++;
    if(assert_int_equal(get_spvl_cat(4.9), 2))
        pass_counter++;

    test_counter++;
    if(assert_int_equal(get_spvl_cat(4.4), 1))
        pass_counter++;

    test_counter++;
    if(assert_int_equal(get_spvl_cat(3.9), 0))
        pass_counter++;

    // Need to set the random seed for this.  
    //test_counter++;
    //if(assert_int_equal(find_who_infected(), ))
    //    pass_counter++;
    
    
    //measured_cd4_cat() requires a random seed.  
    // Set up random seed
    gsl_rng_env_setup();
    TYPE_RNG = gsl_rng_default;
    rng = gsl_rng_alloc(TYPE_RNG);
    
    struct parameters{
        double cumulative_p_misclassify_cd4[NCD4][NCD4];
    };
    
    parameters param;
    int i, j;
    for(i = 0; i < NCD4; i++){
        for(j = 0; j < NCD4; j++){
            param.cumulative_p_misclassify_cd4[i][j] = 1.0;
        }
    }
    
    int k = measured_cd4_cat(&param, 4);
    printf("%d\n", k);
    
    k = measured_cd4_cat(&param, 3);
    printf("%d\n", k);
    
    k = measured_cd4_cat(&param, 2);
    printf("%d\n", k);
    
    k = measured_cd4_cat(&param, 1);
    printf("%d\n", k);
    
    for(i = 0; i < NCD4; i++){
        for(j = 0; j < NCD4; j++){
            param.cumulative_p_misclassify_cd4[i][j] = 0.0;
        }
    }
    
    k = measured_cd4_cat(&param, 4);
    printf("%d\n", k);
    
    k = measured_cd4_cat(&param, 3);
    printf("%d\n", k);
    
    k = measured_cd4_cat(&param, 2);
    printf("%d\n", k);
    
    k = measured_cd4_cat(&param, 1);
    printf("%d\n", k);
    
    // // Set up a mock individual structure with a CD4 category
    // struct individual{
    //     int cd4;
    // }
    // struct parameters{
    //     double COUNTRY_ART_START;
    // }
    // struct patch_struct{
    //     double CHIPS_START_YEAR[0];
    //     double CHIPS_START_TIMESTEP[0];
    //     int trial_arm;
    // }
    //
    // is_eligible_for_art(individual* indiv, parameters *param, double t, patch_struct *patch, int p)
    // art_cd4_eligibility_group() requires a param structure
    //is_eligible_for_art()
    
    printf("\nFinished a total of %d tests; %d failures\n", test_counter, test_counter - pass_counter);
    return 0;
}

