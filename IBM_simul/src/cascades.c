/*  This file is part of the PopART IBM.

    The PopART IBM is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The PopART IBM is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with the PopART IBM.  If not, see <http://www.gnu.org/licenses/>.
 */


/* Manicaland HIV prevention cascade-related functions:
 */


//#include "hiv.h"
//#include "constants.h"
#include "cascades.h"
//#include "output.h"
//#include "utilities.h"
//#include "partnership.h"
//#include "interventions.h"
//#include "debug.h"
//#include "pc.h"


/* This function sets the probability of effectively using a method given the cascade barriers experienced by a person.
   Function is called in set_up_population() in init.c and create_new_individual() in demographics.c when MANICALAND_CASCADE==1.
   ***It will also be called when the person transitions age groups (i.e. reaches 15 and 25/30 for F/M. ***
   ***It will also be called if the barrier-removing intervention is called.*** 
   Note that the minimum age for the populations is 15 (e.g. 15-24 year old women are a priority age group for PrEP), so the probability of starting PrEP when first entering the population *should* be zero, and we reset it when the person turns 15. 
*/
void set_prevention_cascade_barriers(individual *indiv, double t, cascade_barrier_params barrier_params, int scenario_flag){
    int age = (int) floor(t-indiv->DoB);

    int g = indiv->gender;

    int i_VMMC_intervention_running_flag;
    int i_PrEP_intervention_running_flag;
    int i_condom_intervention_running_flag;
    
    if (t<barrier_params.t_start_prevention_cascade_intervention){
	i_VMMC_intervention_running_flag = 0;
	i_PrEP_intervention_running_flag = 0;
	i_condom_intervention_running_flag = 0;
    }
    else{
	i_VMMC_intervention_running_flag = barrier_params.i_VMMC_barrier_intervention_flag;
	i_PrEP_intervention_running_flag = barrier_params.i_PrEP_barrier_intervention_flag;
	i_condom_intervention_running_flag = barrier_params.i_condom_barrier_intervention_flag;
    }

    
    /* If under 15 then shouldn't get these (VMMC in under-15 is carried out when people enter the model, so separate from this): 
     Age 55+*/
    if (age<15){
	indiv->cascade_barriers.p_will_use_PrEP = 0;	
	indiv->cascade_barriers.p_will_get_VMMC = 0;
	/* Assume that condom use is the same as for people in the 15-X group (otherwise we end up with the weird effect that people can be sexually active but will not use a condom until age 15). */
	if(g==MALE){
	    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][i_condom_intervention_running_flag];
	    indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][i_condom_intervention_running_flag];
	}
	else{
	    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][i_condom_intervention_running_flag];
	    indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][i_condom_intervention_running_flag];
	}
    }
    
    else{
	if (g==FEMALE){
	    if(age<=24){
		indiv->cascade_barriers.p_will_use_PrEP = barrier_params.p_use_PrEP[i_PREVENTIONBARRIER_YOUNG_F][i_PrEP_intervention_running_flag];	
		indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][i_condom_intervention_running_flag];
		indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][i_condom_intervention_running_flag];
	    }
	    else{
		/* PrEP has an upper age limit: */
		if(age<(PREP_MAX_AGE_PREVENTION_CASCADE+1))
		    indiv->cascade_barriers.p_will_use_PrEP = barrier_params.p_use_PrEP[i_PREVENTIONBARRIER_OLD_F][i_PrEP_intervention_running_flag];
		else
		    /* Assume age > 55 don't use PrEP. */
		    indiv->cascade_barriers.p_will_use_PrEP = 0;
		indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_OLD_F][i_condom_intervention_running_flag];
		indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_OLD_F][i_condom_intervention_running_flag];
	    }
	}
	/* Male: */
	else{
	    if(age<=29){
		indiv->cascade_barriers.p_will_use_PrEP = barrier_params.p_use_PrEP[i_PREVENTIONBARRIER_YOUNG_M][i_PrEP_intervention_running_flag];	
		indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][i_condom_intervention_running_flag];
		indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][i_condom_intervention_running_flag];
		indiv->cascade_barriers.p_will_get_VMMC = barrier_params.p_use_VMMC[i_PREVENTIONBARRIER_YOUNG_M][i_VMMC_intervention_running_flag];
	    }
	    else{
		/* PrEP and VMMC have an upper age limit: */
		if(age<(PREP_MAX_AGE_PREVENTION_CASCADE+1))
		    indiv->cascade_barriers.p_will_use_PrEP = barrier_params.p_use_PrEP[i_PREVENTIONBARRIER_OLD_M][i_PrEP_intervention_running_flag];
		else
		    indiv->cascade_barriers.p_will_use_PrEP = 0;
		if(age<(VMMC_MAX_AGE_PREVENTION_CASCADE+1))
		    indiv->cascade_barriers.p_will_get_VMMC = barrier_params.p_use_VMMC[i_PREVENTIONBARRIER_OLD_M][i_VMMC_intervention_running_flag];		    
		else
		    indiv->cascade_barriers.p_will_get_VMMC = 0;
		indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_OLD_M][i_condom_intervention_running_flag];
		indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_OLD_M][i_condom_intervention_running_flag];
	    }
	}
    }
}



/* Function that at each timestep (or multiple of a timestep) goes through the male population (up to age VMMC_MAX_AGE_PREVENTION_CASCADE) using the age_groups list (men only).
   Function is called in simul.c when MANICALAND_CASCADE==1.
*/
void draw_VMMC_through_barriers(double t, patch_struct *patch, int p){
    int aa, ai, i;
    int number_per_age_group;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    double x;
    double p_will_get_VMMC_per_timestep;


    /* Really not expecting that we would *ever* want to model circumcision happening to 80 year olds... */
    if (VMMC_MAX_AGE_PREVENTION_CASCADE>79)
	printf("Need to modify this function to include oldest age group.\n");
    for(aa = 0; aa < (VMMC_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){
	ai = patch[p].age_list->age_list_by_gender[MALE]->youngest_age_group_index + aa;            
	while(ai > (MAX_AGE - AGE_ADULT - 1))
	    ai = ai - (MAX_AGE - AGE_ADULT);            
	number_per_age_group = patch[p].age_list->age_list_by_gender[MALE]->number_per_age_group[ai];
	/* Go through each person in the age list: */
	for(i = 0; i < number_per_age_group; i++){
	    indiv = patch[p].age_list->age_list_by_gender[MALE]->age_group[ai][i];

	    /* Only circumcise uncircumcised HIV- men (ignore TMC). */
	    if (indiv->circ==UNCIRC && indiv->HIV_status==UNINFECTED){
		p_will_get_VMMC_per_timestep = 1.0-pow(1.0-indiv->cascade_barriers.p_will_get_VMMC,TIME_STEP);
		x = gsl_rng_uniform (rng);
		/* indiv->cascade_barriers.p_will_get_VMMC is the per-timestep probability: */
		if(x <= p_will_get_VMMC_per_timestep){
		    indiv->circ = VMMC; /* Immediate VMMC (ignore healing period). */
		}
	    }
	}
    }
}




/* Function that at each timestep (or multiple of a timestep) goes through the population (up to age X_M, X_F):
   Function is called in simul.c when MANICALAND_CASCADE==1.
*/
void draw_PrEP_through_barriers(double t, patch_struct *patch, int p){
    int aa, ai, g, i;
    int number_per_age_group;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    double x;
    double p_will_use_PrEP_per_timestep;

    /* No reason why we would ever expect PrEP to be offered to very old people. */
    if (PREP_MAX_AGE_PREVENTION_CASCADE>79)
	printf("Need to modify this function to include oldest age group.\n");

    /* Allow PrEP for men and women here: */
    for(g = 0; g < N_GENDER; g++){    
	for(aa = 0; aa < (PREP_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){
	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
	    while(ai > (MAX_AGE - AGE_ADULT - 1))
		ai = ai - (MAX_AGE - AGE_ADULT);
            
	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
	    for(i = 0; i < number_per_age_group; i++){
		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
		if (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED){
		    /* Now convert to a per-timestep probability: */
		    p_will_use_PrEP_per_timestep = 1.0-pow(1.0-indiv->cascade_barriers.p_will_use_PrEP,TIME_STEP);
		    x = gsl_rng_uniform (rng);

		    if(x <= p_will_use_PrEP_per_timestep){
			start_PrEP_for_person(indiv, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, t);
			// PrEP status is set in start_PrEP_for_person(). Use below if we want to force all individuals to be adherent. 
			//indiv->PrEP_cascade_status = ONPREP_ADHERENT;
		    }
		}
	    }
	}
    }
}





       

/* This function returns the geometric mean of the individual-level preferences to generate a partner-level probability. 
   Make no assumptions about gender - so could be used for MSM in future. 
*/
double get_partner_cascade_probability_condom(individual *indiv1, individual *indiv2, double t, double duration_partnership){

    /* Individual-level preferences for using condom: */
    double p_use_condom1, p_use_condom2;
    /* Partner-level probability: */
    double p_use_condom;

    //p_use_condom1 = generate_individual_condom_preference(indiv1, t, duration_partnership, condom_cascade_scenario);
    if (duration_partnership<1.0){
	p_use_condom1 = indiv1->cascade_barriers.p_want_to_use_condom_short_term_partner;
	p_use_condom2 = indiv2->cascade_barriers.p_want_to_use_condom_short_term_partner;
    }
    else{
	p_use_condom1 = indiv1->cascade_barriers.p_want_to_use_condom_long_term_partner;
	p_use_condom2 = indiv2->cascade_barriers.p_want_to_use_condom_long_term_partner;
    }

    p_use_condom = sqrt(p_use_condom1*p_use_condom2);

    return p_use_condom;
}

/* Function uses individual-level condom barriers to determine if a partnership will use a condom (or not).
   Function called when a partnership is formed in new_partnership(), and also when there is an intervention to modify condom barriers in function intervention_condom_cascade(). */
void get_partnership_condom_use(individual *indiv1, individual *indiv2, double t, double duration_partnership){
    double p_use_condom, x;

    /* Works out the partnership probability of using a condom given the individual-level preferences for using a condom (takes the geometric means of them). */
    p_use_condom = get_partner_cascade_probability_condom(indiv1, indiv2, t, duration_partnership);

    /* Now draw a random number to see if they will use condoms: */
    x = gsl_rng_uniform (rng);
    if (x<p_use_condom){
	indiv1->cascade_barriers.use_condom_in_this_partnership[indiv1->n_partners-1] = 1;
	indiv2->cascade_barriers.use_condom_in_this_partnership[indiv2->n_partners-1] = 1;
    }
    else{
	indiv1->cascade_barriers.use_condom_in_this_partnership[indiv1->n_partners-1] = 0;
	indiv2->cascade_barriers.use_condom_in_this_partnership[indiv2->n_partners-1] = 0;
    }	
}


/* Not currently used (13/07/2021). 
***Note - need to repurpose function:
 - loop through population.
 - for each partnership, update the condom use
 - *** */
void intervention_condom_cascade(patch_struct *patch, int p, double t, int cascade_scenario){

    int condom_cascade_scenario = cascade_scenario%10;
    printf("condom_cascade_scenario=%i\n",condom_cascade_scenario);


    /* First update peoples individual cascade barriers (motivation, access, effective use). */
    //update_all_individual_condom_cascades(patch, p, t);
    /* Now loop through the list of alive people, and look at partnerships: */
    int aa, ai, g, i, i_partners;
    int number_per_age_group;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    individual *partner;
    long id;
    int n_partners;
    double duration_partnership;

    /* Go through everyone - modify if we only reach certain age groups etc. */
    for(g = 0; g < N_GENDER; g++){    
	for(aa = 0; aa < (MAX_AGE - AGE_ADULT); aa++){
	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
	    while(ai > (MAX_AGE - AGE_ADULT - 1))
		ai = ai - (MAX_AGE - AGE_ADULT);
            
	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
	    for(i = 0; i < number_per_age_group; i++){
		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
		id = indiv->id;
		n_partners = indiv->n_partners;
		/* Now check this person's partnerships: */
		for (i_partners=0; i_partners<n_partners; i_partners++){
		    partner = indiv->partner_pairs[i_partners]->ptr[1-g];
		    if (id< partner->id){
			duration_partnership = indiv->partner_pairs[i_partners]->duration_in_time_steps *TIME_STEP;
			get_partnership_condom_use(indiv, partner, t, duration_partnership);
			
		    }
		}
	    }
	}
	/* Now oldest age group: */
	number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
	for(i = 0; i < number_per_age_group; i++){
	    indiv = patch[p].age_list->age_list_by_gender[g]->oldest_age_group[i];
	    /* ***I don't know what this does! */
	    /* for(b=0;b<N_CASCADE_BARRIER_STEPS;b++){ */
	    /* 	indiv->cascade_barriers.condom_cascade_barriers[b] = 1;    */
	    /* } */
	}

    }
}



/* void update_all_individual_condom_cascades(patch_struct *patch, int p, double t){ */
/*     int aa, ai, g, i, b; */
/*     int number_per_age_group; */

/*     // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory)  */
/*     individual *indiv; */

/*     /\* Go through everyone - modify if we only reach certain age groups etc. *\/ */
/*     for(g = 0; g < N_GENDER; g++){     */
/* 	for(aa = 0; aa < (MAX_AGE - AGE_ADULT); aa++){ */
/* 	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;             */
/* 	    while(ai > (MAX_AGE - AGE_ADULT - 1)) */
/* 		ai = ai - (MAX_AGE - AGE_ADULT); */
            
/* 	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai]; */
/* 	    for(i = 0; i < number_per_age_group; i++){ */
/* 		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i]; */
/* 		for(b=0;b<N_CASCADE_BARRIER_STEPS;b++){ */
/* 		    indiv->cascade_barriers.condom_cascade_barriers[b] = 1;    */
/* 		} */
/* 	    } */
/* 	} */

/* 	/\* Now oldest age group: *\/ */
/* 	number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group; */
/* 	for(i = 0; i < number_per_age_group; i++){ */
/* 	    indiv = patch[p].age_list->age_list_by_gender[g]->oldest_age_group[i]; */
/* 	    for(b=0;b<N_CASCADE_BARRIER_STEPS;b++){ */
/* 		indiv->cascade_barriers.condom_cascade_barriers[b] = 1;    */
/* 	    } */
/* 	} */

/*     } */
/* } */



/* void update_all_individual_PrEP_cascades(patch_struct *patch, int p, double t){ */
/*     int aa, ai, g, i, b; */
/*     int number_per_age_group; */

/*     // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory)  */
/*     individual *indiv; */

/*     /\* Go through everyone - modify if we only reach certain age groups etc. *\/ */
/*     for(g = 0; g < N_GENDER; g++){     */
/* 	for(aa = 0; aa < (PREP_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){ */
/* 	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;             */
/* 	    while(ai > (MAX_AGE - AGE_ADULT - 1)) */
/* 		ai = ai - (MAX_AGE - AGE_ADULT); */
            
/* 	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai]; */
/* 	    for(i = 0; i < number_per_age_group; i++){ */
/* 		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i]; */
/* 		for(b=0;b<N_CASCADE_BARRIER_STEPS;b++){ */
/* 		    indiv->cascade_barriers.PrEP_cascade_barriers[b] = 1;    */
/* 		} */
/* 	    } */
/* 	} */
/*     } */
/* } */


/* void update_all_individual_VMMC_cascades(patch_struct *patch, int p, double t){ */
/*     int aa, ai, i, b; */
/*     int number_per_age_group; */

/*     // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory)  */
/*     individual *indiv; */

/*     /\* Go through all men - modify if we only reach certain age groups etc. *\/ */
/*     for(aa = 0; aa < (VMMC_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){ */
/* 	ai = patch[p].age_list->age_list_by_gender[MALE]->youngest_age_group_index + aa;             */
/* 	while(ai > (MAX_AGE - AGE_ADULT - 1)) */
/* 	    ai = ai - (MAX_AGE - AGE_ADULT); */
	
/* 	number_per_age_group = patch[p].age_list->age_list_by_gender[MALE]->number_per_age_group[ai]; */
/* 	for(i = 0; i < number_per_age_group; i++){ */
/* 	    indiv = patch[p].age_list->age_list_by_gender[MALE]->age_group[ai][i]; */
/* 	    for(b=0;b<N_CASCADE_BARRIER_STEPS;b++){ */
/* 		indiv->cascade_barriers.VMMC_cascade_barriers[b] = 1;    */
/* 	    } */
/* 	} */
/*     } */
/* } */
    
 
