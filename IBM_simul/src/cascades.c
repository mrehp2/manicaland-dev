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



/* Functions assign the probability of getting VMMC / PrEP (2nd function) / condom preferences (3rd function) based on characteristics (age, sex) as well as whether there's an intervention to remove barriers and increase usage at that time. */

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



/* Function that at each timestep (or multiple of a timestep) goes through the male population (up to age VMMC_MAX_AGE_PREVENTION_CASCADE) using the age_groups list (men only) to decide who gets VMMC given their individual probabilities (determined implicitly by cascade barriers).
   Function is called in simul.c when MANICALAND_CASCADE==1.
*/
void sweep_pop_for_VMMC_per_timestep_given_barriers(double t, patch_struct *patch, int p){
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




/* Function that at each timestep (or multiple of a timestep) goes through the population (up to age X_M, X_F) to decide who gets PrEP given their individual probabilities (determined implicitly by cascade barriers).
   Function is called in simul.c when MANICALAND_CASCADE==1.
*/
void sweep_pop_for_PrEP_per_timestep_given_barriers(double t, patch_struct *patch, int p){
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
double calculate_partnership_condom_cascade_probability(individual *indiv1, individual *indiv2, double t, double duration_partnership){

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
    p_use_condom = calculate_partnership_condom_cascade_probability(indiv1, indiv2, t, duration_partnership);

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




/* This function represents an intervention that increases the probability that an individual will get VMMC from time t onwards (by reducing barriers).
   Function goes through everyone (using age_list), and calls function assign_individual_VMMC_cascade() to update their VMMC prevention cascade barriers in response to the intervention. 
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


/* This function represents an intervention that increases the probability that an individual will get PrEP from time t onwards (by reducing barriers).
   Function goes through everyone (using age group), and calls function assign_individual_PrEP_cascade to update their PrEP prevention cascade barriers in response to the intervention. 
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




/* Function called when a condom barrier prevention intervention occurs, potentially changing condom use in existing partnerships (*starting condom use in partnership where condoms were not used before*).
   Function called by ******. */
void update_partnership_condom_use_in_response_to_intervention(individual *indiv1, individual *indiv2, cascade_barrier_params barrier_params, double t, double duration_partnership){
    double p_use_condom_partnerM_preintervention;
    double p_use_condom_partnerM_postintervention;
    double p_use_condom_partnerF_preintervention;
    double p_use_condom_partnerF_postintervention;
    
    double change_in_p_use_condom; /* We want to calculate what the extra probability of using a condom is; */
    double x;  /* RV to see if condom is used or not. */

    int i_partner1, i_partner2; /* Indices for use_condom_in_this_partnership[] array. */ 
    int ageM, ageF; /* Ages of the male and female partner. */
    int g1 = indiv1->gender; /* Sex of partner 1. */
    long check_id;
    
    if(g1==MALE){
	ageM = (int) floor(t-indiv1->DoB);
	ageF = (int) floor(t-indiv2->DoB);
    }
    else{	
	ageM = (int) floor(t-indiv1->DoB);
	ageF = (int) floor(t-indiv2->DoB);
    }

    
    if (duration_partnership<1.0){
	if(ageM<=29){
	    p_use_condom_partnerM_preintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][0];
	    p_use_condom_partnerM_postintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][1];
	}
	else{
	    p_use_condom_partnerM_preintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][0];
	    p_use_condom_partnerM_postintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_M][1];
	}

	if(ageF<=24){
	    p_use_condom_partnerF_preintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][0];
	    p_use_condom_partnerF_postintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][1];
	}
	else{
	    p_use_condom_partnerF_preintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][0];
	    p_use_condom_partnerF_postintervention = barrier_params.p_use_cond_casual[i_PREVENTIONBARRIER_YOUNG_F][1];
	}
    }
    /* Long-term partnership: */
    else{
	if(ageM<=29){
	    p_use_condom_partnerM_preintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][0];
	    p_use_condom_partnerM_postintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][1];
	}
	else{
	    p_use_condom_partnerM_preintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][0];
	    p_use_condom_partnerM_postintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_M][1];
	}

	if(ageF<=24){
	    p_use_condom_partnerF_preintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][0];
	    p_use_condom_partnerF_postintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][1];
	}
	else{
	    p_use_condom_partnerF_preintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][0];
	    p_use_condom_partnerF_postintervention = barrier_params.p_use_cond_LT[i_PREVENTIONBARRIER_YOUNG_F][1];
	}
    }

    /* Look at change in probability: */
    change_in_p_use_condom = sqrt(p_use_condom_partnerM_postintervention*p_use_condom_partnerF_postintervention) - sqrt(p_use_condom_partnerM_preintervention*p_use_condom_partnerF_preintervention);
    if (change_in_p_use_condom<0 || change_in_p_use_condom>1){
	printf("Error: change in probability of using condom from intervention = %6.4lf. Exiting\n",change_in_p_use_condom);
	exit(1);
    }
    
    /* Now draw a random number to see if they will use condoms: */
    x = gsl_rng_uniform (rng);
    if (x<change_in_p_use_condom){
	/* Need to find the array indices for these two (the indices for use_condom_in_this_partnership[] and partner_pairs[] are set up to be the same): */
	i_partner1 = 0;
	while(1){
	    check_id = indiv1->partner_pairs[i_partner1]->ptr[1-g1]->id;
	    if(check_id==indiv2->id)
		break;
	    else
		i_partner1++;
	    if(i_partner1>=indiv1->n_partners){
		printf("Error - run out of partners for partner 1 in update_partnership_condom_use_in_response_to_intervention(). Exiting\n");
		exit(1);
	    }
	}
	i_partner2 = 0;
	while(1){
	    check_id = indiv2->partner_pairs[i_partner2]->ptr[g1]->id;
	    if(check_id==indiv1->id)
		break;
	    else
		i_partner2++;
	    if(i_partner2>=indiv2->n_partners){
		printf("Error - run out of partners for partner 2 in update_partnership_condom_use_in_response_to_intervention(). Exiting\n");
		exit(1);
	    }
	}

	/* Check that condom use matches: */
	if(indiv1->cascade_barriers.use_condom_in_this_partnership[i_partner1]!=0 || indiv2->cascade_barriers.use_condom_in_this_partnership[i_partner2]!=0){
	    printf("Error in update_partnership_condom_use_in_response_to_intervention() - condom use in partners 1+2 not equal to zero prior to intervention. Exiting\n");
	    exit(1);
	}
	
	indiv1->cascade_barriers.use_condom_in_this_partnership[i_partner1] = 1;
	indiv2->cascade_barriers.use_condom_in_this_partnership[i_partner2] = 1;
    }

}




    
/* Function corresponds to an intervention that increases each individual's preference for using a condom (by reducing barriers).
   Thus any new partnerships will have a higher probability of using a condom.
   In addition this function increases the probability of using a condom for existing partnerhips.
   ***Right now, if a partnerships is using a condom, then they will continue to do so. If not, then there is a probability that they will start to use it. 
   
   
   Function loops through the list of alive people via age_list *TWICE*.
   Firstly, loop through the list of alive people. For each person, update their individual condom cascade barrier params.
   Then, loop through again and look at partnerships for each person - update condom use if the id of the partner is < the id of that person. 
   Note we need 2 loops as we can't guarantee that the age of the second person is less than that of the first (it is for new individuals, but not at the start of the simulation). */
void prevention_cascade_intervention_condom(double t, patch_struct *patch, int p){
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
    
    /* First - go through everyone, and alter their individual preference for condoms.
      */
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
			    update_partnership_condom_use_in_response_to_intervention(indiv, partner, patch[p].param->barrier_params, t, duration_partnership);				    //get_partnership_condom_use(indiv, partner, t, duration_partnership);
			}
		    }		    

		}
	    }
	}
	/* Now oldest age group: */
	number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
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
			update_partnership_condom_use_in_response_to_intervention(indiv, partner, patch[p].param->barrier_params, t, duration_partnership);				//get_partnership_condom_use(indiv, partner, t, duration_partnership);
		    }		    

		}
	    }
	}

    }
}


/* Carried out at each timestep to check for people passing age thresholds related to PrEP prevention cascade barriers.
   Function uses age_list to get birth year cohorts, then birthday_timestep to check if it's their birthday in that timestep. */
void update_individual_PrEPbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p){

    int aa, ai, g, i;
    int number_per_age_group;
    int age;
    
    int intervention_scenario = patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    double age_check;
    
    /* Go through everyone - modify if we only reach certain age groups etc. */
    for(g = 0; g < N_GENDER; g++){
	aa = PREP_VMMC_MIN_AGE_PREVENTION_CASCADE - AGE_ADULT;
	ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
	while(ai > (MAX_AGE - AGE_ADULT - 1))
	    ai = ai - (MAX_AGE - AGE_ADULT);
            
	number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
	for(i = 0; i < number_per_age_group; i++){
	    indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
	    if(indiv->birthday_timestep==t_step){
		age = (int) floor(t-indiv->DoB);
		age_check = t-indiv->DoB;
		printf("At t=%lf tstep=%i DoB=%lf birthday_step=%i age=%lf\n",t,t_step,indiv->DoB,indiv->birthday_timestep,age_check);
		assign_individual_PrEP_prevention_cascade(indiv, age, indiv->gender, patch[p].param->barrier_params.p_use_PrEP, intervention_scenario);
	    }
	}

    }
}
