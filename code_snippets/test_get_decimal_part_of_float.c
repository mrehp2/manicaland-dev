#include<stdio.h>
#include<math.h>

#define SWITCH 0
#define BIGNUM 100000000
int main () {
    double x, fractpart, intpart;
    int i;
    x = 8.123456;

    if(SWITCH==0)
	for(i=0; i<BIGNUM; i++)
	    fractpart = (int) (modf(x, &intpart)*48);
    else
	for(i=0; i<BIGNUM; i++)
	    fractpart = (int) floor((x-floor(x))*48);
    //printf("Integral part = %lf\n", intpart);
   printf("Fraction Part = %lf \n", fractpart);
   
   return(0);
}
