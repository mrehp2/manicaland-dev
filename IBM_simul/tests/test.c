#include "test.h"
#include<stdio.h>

int assert_int_equal(int observed, int expected){
    if(observed == expected){
        printf(".");
        return 1;
    }else{
        printf("x %s %d", __FUNCTION__, __LINE__);
        return 0;
    }
}

