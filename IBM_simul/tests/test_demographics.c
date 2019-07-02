#include <stdio.h>
#include "../src/demographics.h"
#include "test.h"


/*
draw_sex_risk()
int get_age_index(double , double );
int get_age_indexv2(double , double , int);
int get_age_group(double , double , const int [], int);
int get_age_group_unpd(double , double );

*/

int main(void){
    int test_counter = 0;
    int pass_counter = 0;
    

    const int test_age_groups[3] = {1, 9, 11};
    // Test the output from the get_spvl_cat() function
    test_counter++;
    if(assert_int_equal(get_age_group(2027.1, 2029.1, test_age_groups, 3), 0))
        pass_counter++;
    
    test_counter++;
    if(assert_int_equal(get_age_group(2019.0, 2029.1, test_age_groups, 3), 1))
        pass_counter++;
    
    test_counter++;
    if(assert_int_equal(get_age_group(2000.0, 2029.1, test_age_groups, 3), 2))
        pass_counter++;
    
    // Test on the boundary between age categories
    test_counter++;
    if(assert_int_equal(get_age_group(2000.0, 2009.0, test_age_groups, 3), 0))
        pass_counter++;
    
    test_counter++;
    if(assert_int_equal(get_age_group(2000.51, 2011.51, test_age_groups, 3), 2))
        pass_counter++;

    printf("\nFinished a total of %d tests; %d failures\n", test_counter, test_counter - pass_counter);
    return 0;
}

