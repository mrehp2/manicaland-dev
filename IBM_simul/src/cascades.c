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


void assign_individual_VMMC_prevention_cascade(individual *indiv, int age, double p_use_VMMC[N_PREVENTIONBARRIER_GROUPS][2], int i_VMMC_intervention_running_flag){
    /* If under 15 then shouldn't get VMMC (VMMC in under-15 is carried out when people enter the model, so separate from this): */
    if (age<PREP_VMMC_MIN_AGE_PREVENTION_CASCADE)
	indiv->cascade_barriers.p_will_get_VMMC = 0;
    else if(age<=29)
	indiv->cascade_barriers.p_will_get_VMMC = p_use_VMMC[i_PREVENTIONBARRIER_YOUNG_M][i_VMMC_intervention_running_flag];
    else if(age<=VMMC_MAX_AGE_PREVENTION_CASCADE)
	indiv->cascade_barriers.p_will_get_VMMC = p_use_VMMC[i_PREVENTIONBARRIER_OLD_M][i_VMMC_intervention_running_flag];		    
    /* VMMC has an upper age limit: */
    else
	indiv->cascade_barriers.p_will_get_VMMC = 0;
}


void assign_individual_PrEP_prevention_cascade(individual *indiv, int age, int g, double p_use_PrEP[N_PREVENTIONBARRIER_GROUPS*N_GENDER][2], int i_PrEP_intervention_running_flag){

    /* If under 15 then shouldn't get PrEP: */
    if (age<PREP_VMMC_MIN_AGE_PREVENTION_CASCADE)
	indiv->cascade_barriers.p_will_use_PrEP = 0;	
    else{
	if (g==FEMALE){
	    if(age<=24)
		indiv->cascade_barriers.p_will_use_PrEP = p_use_PrEP[i_PREVENTIONBARRIER_YOUNG_F][i_PrEP_intervention_running_flag];	
	    else if(age<=PREP_MAX_AGE_PREVENTION_CASCADE)
		indiv->cascade_barriers.p_will_use_PrEP = p_use_PrEP[i_PREVENTIONBARRIER_OLD_F][i_PrEP_intervention_running_flag];
	    /* PrEP has an upper age limit: */
	    else
		indiv->cascade_barriers.p_will_use_PrEP = 0;
	}
	/* Male: */
	else{
	    if(age<=29)
		indiv->cascade_barriers.p_will_use_PrEP = p_use_PrEP[i_PREVENTIONBARRIER_YOUNG_M][i_PrEP_intervention_running_flag];	
	    else if(age<=PREP_MAX_AGE_PREVENTION_CASCADE)
		indiv->cascade_barriers.p_will_use_PrEP = p_use_PrEP[i_PREVENTIONBARRIER_OLD_M][i_PrEP_intervention_running_flag];
	    /* PrEP has an upper age limit: */		
	    else
		indiv->cascade_barriers.p_will_use_PrEP = 0;
	}
    }
}



void assign_individual_condom_prevention_cascade(individual *indiv, int age, int g, double p_use_cond_LT[N_PREVENTIONBARRIER_GROUPS*N_GENDER][2], double p_use_cond_casual[N_PREVENTIONBARRIER_GROUPS*N_GENDER][2], int i_condom_intervention_running_flag){
    
    if (g==FEMALE){
	if(age<=24){
	    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][i_condom_intervention_running_flag];
	    indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][i_condom_intervention_running_flag];
	}
	else{
	    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = p_use_cond_LT[i_PREVENTIONBARRIER_OLD_F][i_condom_intervention_running_flag];
	    indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = p_use_cond_casual[i_PREVENTIONBARRIER_OLD_F][i_condom_intervention_running_flag];

	}
    }
    /* Male: */
    else{
	if(age<=29){
	    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][i_condom_intervention_running_flag];
	    indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][i_condom_intervention_running_flag];
	}
	else{
	    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = p_use_cond_LT[i_PREVENTIONBARRIER_OLD_M][i_condom_intervention_running_flag];
	    indiv->cascade_barriers.p_want_to_use_condom_short_term_partner = p_use_cond_casual[i_PREVENTIONBARRIER_OLD_M][i_condom_intervention_running_flag];
	}
    }
}

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

    if(g==MALE)
	assign_individual_VMMC_prevention_cascade(indiv, age, barrier_params.p_use_VMMC, i_VMMC_intervention_running_flag);

    assign_individual_PrEP_prevention_cascade(indiv, age, g, barrier_params.p_use_PrEP, i_PrEP_intervention_running_flag);

    assign_individual_condom_prevention_cascade(indiv, age, g, barrier_params.p_use_cond_LT, barrier_params.p_use_cond_casual, i_condom_intervention_running_flag);

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




/* Goes through everyone, and calls function assign_individual_VMMC_cascade() to update their VMMC prevention cascade barriers in response to an intervention. 
 */
void prevention_cascade_intervention_VMMC(double t, patch_struct *patch, int p){

    int aa, ai, i;
    int number_per_age_group;
    int age; /* Current age in years. */
    
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    
    /* Store scenario for easier readability. */
    int intervention_scenario = patch[p].param->barrier_params.i_VMMC_barrier_intervention_flag;

    /* VMMC unlikely to ever be offered to people this age - this is just a check, although it would be straightforward to extend the code to include older people. */
    if(VMMC_MAX_AGE_PREVENTION_CASCADE>MAX_AGE){
	printf("Code issue - prevention_cascade_intervention_VMMC() currently not set up to deal with VMMC being offered to people aged >79 year old. Exiting\n");
	exit(1);
    }
    
    /* Go through all age-group-eligible men - modify if we only reach certain age groups etc (we assume that the intervention does not change the fact that these interventions are not available outside those age groups). */
    for(aa = (PREP_VMMC_MIN_AGE_PREVENTION_CASCADE-AGE_ADULT); aa < (VMMC_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){
	ai = patch[p].age_list->age_list_by_gender[MALE]->youngest_age_group_index + aa;            
	while(ai > (MAX_AGE - AGE_ADULT - 1))
	    ai = ai - (MAX_AGE - AGE_ADULT);
            
	number_per_age_group = patch[p].age_list->age_list_by_gender[MALE]->number_per_age_group[ai];

	
	for(i = 0; i < number_per_age_group; i++){
	    indiv = patch[p].age_list->age_list_by_gender[MALE]->age_group[ai][i];
	    age = (int) floor(t-indiv->DoB);
	    assign_individual_VMMC_prevention_cascade(indiv, age, patch[p].param->barrier_params.p_use_VMMC, intervention_scenario);
	}
	
    }
}


/* Goes through everyone, and calls function assign_individual_PrEP_cascade to update their PrEP prevention cascade barriers in response to an intervention. 
 */
void prevention_cascade_intervention_PrEP(double t, patch_struct *patch, int p){

    int aa, ai, g, i;
    int number_per_age_group;
    int age; /* Current age in years. */
    
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    
    /* Store scenario for easier readability. */
    int intervention_scenario = patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag;

    /* PrEP unlikely to ever be offered to people this age - this is just a check, although it would be straightforward to extend the code to include older people. */
    if(PREP_MAX_AGE_PREVENTION_CASCADE>MAX_AGE){
	printf("Code issue - prevention_cascade_intervention_PrEP() currently not set up to deal with PrEP being offered to people aged >79 year old\n");
	exit(1);
    }
	
    /* Go through all age-group-eligible people - modify if we only reach certain age groups etc (we assume that the intervention does not change the fact that these interventions are not available outside those age groups). */
    for(g = 0; g < N_GENDER; g++){    
	for(aa = (PREP_VMMC_MIN_AGE_PREVENTION_CASCADE-AGE_ADULT); aa < (PREP_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){
	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
	    while(ai > (MAX_AGE - AGE_ADULT - 1))
		ai = ai - (MAX_AGE - AGE_ADULT);
	
	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];

	
	    for(i = 0; i < number_per_age_group; i++){
		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
		age = (int) floor(t-indiv->DoB);
		assign_individual_PrEP_prevention_cascade(indiv, age, g, patch[p].param->barrier_params.p_use_PrEP, intervention_scenario);
	    }
	    
	}
    }
	
}


    


    
/* Not currently used (13/07/2021). 
***Note - need to repurpose function:
 - loop through population.
 - for each partnership, update the condom use
 - *** */
void prevention_cascade_intervention_condom(double t, patch_struct *patch, int p){
    /* Loop through the list of alive people via age_list.
       For each person, update their condom cascade barrier params.
       Then loop through again and look at partnerships for that person - update condom use if the id of the partner is < the id of that person. Note we need 2 loops as we can't guarantee that the age of the second person is less than that of the first (it is for new individuals, but not at the start of the simulation).
    */
    int aa, ai, g, i, i_partners;
    int number_per_age_group;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    individual *partner;
    long id;
    int n_partners;
    double duration_partnership;
    int age;

    /* Store scenario for easier readability. */
    int intervention_scenario = patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag;
    
    /* Go through everyone - modify if we only reach certain age groups etc. */
    for(g = 0; g < N_GENDER; g++){    
	for(aa = 0; aa < (MAX_AGE - AGE_ADULT); aa++){
	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
	    while(ai > (MAX_AGE - AGE_ADULT - 1))
		ai = ai - (MAX_AGE - AGE_ADULT);
            
	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
	    for(i = 0; i < number_per_age_group; i++){
		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
		age = (int) floor(t-indiv->DoB);
		assign_individual_condom_prevention_cascade(indiv,age,indiv->gender,patch[p].param->barrier_params.p_use_cond_LT,patch[p].param->barrier_params.p_use_cond_casual,intervention_scenario);
	    }
	}
	/* Now oldest age group: */
	number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
	for(i = 0; i < number_per_age_group; i++){
	    indiv = patch[p].age_list->age_list_by_gender[g]->oldest_age_group[i];
	    /* Probably could just use MAX_AGE rather than calculating age, but might generate a weird bug if we ever did change age dependency/MAX_AGE. */
	    age = (int) floor(t-indiv->DoB);
	    assign_individual_condom_prevention_cascade(indiv,age,indiv->gender,patch[p].param->barrier_params.p_use_cond_LT,patch[p].param->barrier_params.p_use_cond_casual,intervention_scenario);
	}

    }

    
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

		    /* Only update if they're not consistently using condoms already: */
		    if (indiv->cascade_barriers.use_condom_in_this_partnership[i_partners]==0){
			partner = indiv->partner_pairs[i_partners]->ptr[1-g];
			if (id< partner->id){

			    duration_partnership = indiv->partner_pairs[i_partners]->duration_in_time_steps *TIME_STEP;
			
			    get_partnership_condom_use(indiv, partner, t, duration_partnership);
			}
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
    
 
