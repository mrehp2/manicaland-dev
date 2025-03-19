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
#include "prevention_cascades.h"
#include "mihpsa.h"
#include "structures.h"
//#include "output.h"
//#include "utilities.h"
//#include "partnership.h"
//#include "interventions.h"
//#include "debug.h"
//#include "pc.h"






/* Function converts individual-level characteristics into an index for barrier_params parameter arrays (p_use_PrEP).
   Current characteristics are age, sex, number of partners (if this is zero, then never had sex - so variable is called ever_have_sex here, and should be treated as boolean).
*/
int index_HIV_prevention_cascade_PrEP(int age, int g, int ever_had_sex){
    /* Put female first as more efficient: */

    
    
    if(g==FEMALE){
	if(ever_had_sex==0)
	    return i_PrEP_PREVENTIONBARRIER_NEVERSEX_F;
	else if(age<PREP_VMMC_MIN_AGE_PREVENTION_CASCADE)
	    return i_PrEP_PREVENTIONBARRIER_TOO_YOUNG_F;
	else if(age<=24)
	    return i_PrEP_PREVENTIONBARRIER_YOUNG_F;
	else if(age<=PREP_MAX_AGE_PREVENTION_CASCADE)
	    return i_PrEP_PREVENTIONBARRIER_OLD_F;
	else
	    return i_PrEP_PREVENTIONBARRIER_TOO_OLD_F;
    }
    else if(g==MALE){
	if(ever_had_sex==0)
	    return i_PrEP_PREVENTIONBARRIER_NEVERSEX_M;
	else if(age<PREP_VMMC_MIN_AGE_PREVENTION_CASCADE)
	    return i_PrEP_PREVENTIONBARRIER_TOO_YOUNG_M;
	else if(age<=29)
	    return i_PrEP_PREVENTIONBARRIER_YOUNG_M;
	else if(age<=PREP_MAX_AGE_PREVENTION_CASCADE)
	    return i_PrEP_PREVENTIONBARRIER_OLD_M;
	else
	    return i_PrEP_PREVENTIONBARRIER_TOO_OLD_M;
    }
    else{
	/* Should never get here: */
	printf("Error: Unexpected age/sex combination in index_HIV_prevention_cascade_PrEP(). Exiting\n");
	exit(1);
    }

}


/* Function converts individual-level characteristics into an index for barrier_params parameter arrays (p_use_VMMC).
   Current characteristics are age, number of partners (if this is zero, then never had sex - so variable is called ever_have_sex here, and should be treated as boolean).
*/
int index_HIV_prevention_cascade_VMMC(int age, int ever_had_sex, double t){

    if((MIHPSA_MODULE==0) || (t<2021)){
	if(ever_had_sex==0)
	    return i_VMMC_PREVENTIONBARRIER_NEVERSEX_M;
	else if(age<PREP_VMMC_MIN_AGE_PREVENTION_CASCADE)
	    return i_VMMC_PREVENTIONBARRIER_TOO_YOUNG_M;
	else if(age<=29)
	    return i_VMMC_PREVENTIONBARRIER_YOUNG_M;
	else if(age<=VMMC_MAX_AGE_PREVENTION_CASCADE)
	    return i_VMMC_PREVENTIONBARRIER_OLD_M;
	else
	    return i_VMMC_PREVENTIONBARRIER_TOO_OLD_M;
    }
    else{
	/* For MIHPSA, allow VMMC for people who've never had sex: */
        if(age<PREP_VMMC_MIN_AGE_PREVENTION_CASCADE)
	    return i_VMMC_PREVENTIONBARRIER_TOO_YOUNG_M;
	else if(age<=29)
	    return i_VMMC_PREVENTIONBARRIER_YOUNG_M;
	else if(age<=VMMC_MAX_AGE_PREVENTION_CASCADE)
	    return i_VMMC_PREVENTIONBARRIER_OLD_M;
	else
	    return i_VMMC_PREVENTIONBARRIER_TOO_OLD_M;
    }	
    /* Should never get here: */
    printf("Error: Unexpected age in index_HIV_prevention_cascade_VMMC(). Exiting\n");
    exit(1);

}



/* Function converts individual-level characteristics into an index for condom-related barrier_params parameter arrays (barrier_params.p_use_cond_casual and barrier_params.p_use_cond_LT.).
   Current characteristics are age, sex.
*/
int index_HIV_prevention_cascade_condom(int age, int g){
    if(g==MALE){
	if(age<=29)
	    return i_COND_PREVENTIONBARRIER_YOUNG_M;
	else
	    return i_COND_PREVENTIONBARRIER_OLD_M;
    }
    else if(g==FEMALE){
	if(age<=24)
	    return i_COND_PREVENTIONBARRIER_YOUNG_F;
	else
	    return i_COND_PREVENTIONBARRIER_OLD_F;
    }

    else{
	/* Should never get here: */
	printf("Error: Unexpected age/sex combination in index_HIV_prevention_cascade_condom(). Exiting\n");
	exit(1);
    }

}



/* Functions assign the probability of getting PrEP / VMMC / condom preferences
   based on characteristics (currently age, sex) as well as whether there's an intervention to remove barriers and increase usage at that time. */
void assign_individual_PrEP_prevention_cascade(double t, individual *indiv, cascade_barrier_params *barrier_params, int i_PrEP_intervention_running_flag){
    int age = (int) floor(t-indiv->DoB);
    int g = indiv->gender;
    if(indiv->id==FOLLOW_INDIVIDUAL){
	printf("Modifying PrEP probability for id=%li at t=%lf.\n",indiv->id,t);
	printf("Age=%i gender=%i n_partners=%li\n",age,g,indiv->n_lifetime_partners);
    }
    indiv->cascade_barriers.p_will_use_PrEP = barrier_params->p_use_PrEP[index_HIV_prevention_cascade_PrEP(age,g,indiv->n_lifetime_partners)][i_PrEP_intervention_running_flag];
    if(indiv->id==FOLLOW_INDIVIDUAL)
	printf("Following change, PrEP probability is now %lf\n",indiv->cascade_barriers.p_will_use_PrEP);
}

/* Need to pass a pointer to barrier_params as otherwise we create a local copy of barrier_params (and then assigning p_will_get_VMMC to that address fails, as the address is freed once we return from the function). */
void assign_individual_VMMC_prevention_cascade(double t, individual *indiv, cascade_barrier_params *barrier_params){

    int age = (int) floor(t-indiv->DoB);
    indiv->cascade_barriers.p_will_get_VMMC = &(barrier_params->p_use_VMMC[index_HIV_prevention_cascade_VMMC(age,indiv->n_lifetime_partners,t)]);
    //printf("id=%li %lf %lf\n",indiv->id,barrier_params->p_use_VMMC[index_HIV_prevention_cascade_VMMC(age,indiv->n_lifetime_partners,t)],*(indiv->cascade_barriers.p_will_get_VMMC));

}

void assign_individual_condom_prevention_cascade(double t, individual *indiv, cascade_barrier_params *barrier_params){
    int age = (int) floor(t-indiv->DoB);
    int g = indiv->gender;
    
    indiv->cascade_barriers.p_want_to_use_condom_long_term_partner = &(barrier_params->p_use_cond_LT[index_HIV_prevention_cascade_condom(age,g)]);
    indiv->cascade_barriers.p_want_to_use_condom_casual_partner = &(barrier_params->p_use_cond_casual[index_HIV_prevention_cascade_condom(age,g)]);
}



/* This function sets the probability of effectively using a method given the cascade barriers experienced by a person, depending on their age, sex, and other individual covariates.
   Function is called in set_up_population() in init.c and create_new_individual() in demographics.c when MANICALAND_CASCADE==1.
*/
void set_prevention_cascade_barriers(individual *indiv, double t, cascade_barrier_params *barrier_params, int scenario_flag){

    int i_PrEP_intervention_running_flag;
    
    if (t<barrier_params->t_start_prevention_cascade_intervention){
	i_PrEP_intervention_running_flag = 0;
    }
    else{
	i_PrEP_intervention_running_flag = barrier_params->i_PrEP_barrier_intervention_flag;
    }

    /* if(t>2007){ */
    /* 	printf("Exiting1\n"); */
    /* 	exit(1); */
    /* } */
    
    if(indiv->gender==MALE)
	assign_individual_VMMC_prevention_cascade(t, indiv, barrier_params);

    
    if(indiv->id==FOLLOW_INDIVIDUAL)
	printf("Modifying PrEP HIV prevention cascade probability in set_preventon_cascade_barriers() at time t=%lf for id=%li age%i\n",t,indiv->id,(int) floor(t-indiv->DoB));
    
    assign_individual_PrEP_prevention_cascade(t, indiv, barrier_params, i_PrEP_intervention_running_flag);

    /* No need to specify if condom intervention is running, because that is dealt with in p_use_condom_casual/LT[], which is updated at each timestep. */
    assign_individual_condom_prevention_cascade(t, indiv, barrier_params);

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

    /* For certain MIHPSA scenarios, VMMC is switched off from 2023 onwards: */
    if((t>=2023.0) && (patch[p].param->MIHPSA_params.FLAGS.remove_VMMC_from2023==1))
	return;


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
		if(*(indiv->cascade_barriers.p_will_get_VMMC)>0){
		    p_will_get_VMMC_per_timestep = 1.0-pow(1.0-*(indiv->cascade_barriers.p_will_get_VMMC),TIME_STEP);
		    x = gsl_rng_uniform (rng);
		    /* indiv->cascade_barriers.p_will_get_VMMC is the per-timestep probability: */
		    if(x <= p_will_get_VMMC_per_timestep){
			indiv->circ = VMMC; /* Immediate VMMC (ignore healing period). */
			int age = floor(t - indiv->DoB);
			if(age>=15 && age <=49)
			    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_VMMC_15to49++;
		    }
		}
	    }
	}
    }
}




/* Function that at each timestep (or multiple of a timestep) goes through the population (up to age X_M, X_F) to decide who gets PrEP given their individual probabilities (determined implicitly by cascade barriers).
   Function is called in simul.c when MANICALAND_CASCADE==1.
*/
void sweep_pop_for_PrEP_per_timestep_given_barriers(double t, patch_struct *patch, int p, debug_struct *debug){
    int aa, ai, g, i;
    int number_per_age_group;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    double x;
    double p_will_use_PrEP_per_timestep;
    if((t-floor(t)<0.01))
       printf("Using sweep_pop_for_PrEP_per_timestep_given_barriers() to determine PrEP initiation at t=%6.4lf\n",t);
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
		    if(indiv->cascade_barriers.p_will_use_PrEP>0){
			/* Now convert to a per-timestep probability: */
			p_will_use_PrEP_per_timestep = 1.0-pow(1.0-indiv->cascade_barriers.p_will_use_PrEP,TIME_STEP);
			x = gsl_rng_uniform (rng);

			if(x <= p_will_use_PrEP_per_timestep){
			    start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PREPTYPE_DAILYORALPREP, REASON_START_PREP_BACKGROUND);
			// PrEP status is set in start_PrEP_for_person(). Use below if we want to force all individuals to be adherent. 
			//indiv->PrEP_cascade_status = ONPREP_ADHERENT;
			}
		    }
		}
	    }
	}
    }
}




/////////////////////////////
/* Version of sweep_pop_for_PrEP_per_timestep_given_barriers()  that at each timestep (or multiple of a timestep) goes through the population (up to age X_M, X_F) to decide who gets PrEP.  For older individuals, this remains given their individual probabilities (determined implicitly by cascade barriers).
   Function is called in mihpsa.c by MIHPSA_determine_PrEP_scenario() when MANICALAND_CASCADE==1 and one of the following:
    - patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDORALPREP_AGYW || patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDDAPIVIRINERINGPREP_AGYW || patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDCABLAPREP_AGYW 
   (i.e. MIHPSA scenarios where PrEP is only available for AGYW, and only for a capped number. Only specified type of PrEP now available).
   Original intention was to have a coverage of 37,144 in 15-24 year old women. Based on the call 2 Aug 2023 (MIHPSA Zimbabwe call 2Aug2023_withNotes.pptx) we decided to reduce coverage so that the number of 15-24 y.o. women using PrEP in the past quarter is ~50,000 (it is ~125,000 with a coverage of 37,144 - so divide original coverage by 2.5).
   16 June 2024: Adding in HIV test as part of starting PrEP. */
void MIHPSA_sweep_pop_for_PrEP_per_timestep(double t, patch_struct *patch, int p, debug_struct *debug){
    int aa, ai, g, i;
    int number_per_age_group;
    int i_partner;
    //int partnership_duration; /* Duration (in timesteps) of partnership. */
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    double x;
    double p_will_use_PrEP_per_timestep;


    int PrEP_type;
    if (patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDORALPREP_AGYW)
	PrEP_type = PREPTYPE_DAILYORALPREP;
    else if (patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDDAPIVIRINERINGPREP_AGYW)
	PrEP_type = PREPTYPE_DAPIVIRINERINGPREP;
    else if (patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDCABLAPREP_AGYW)
	PrEP_type = PREPTYPE_CABLAPREP;
    else{
	printf("Error: unknown PrEP scenario in MIHPSA_sweep_pop_for_PrEP_per_timestep(). Exiting\n");
	fflush(stdout);
	exit(1);
    }
    
    //printf("Using MIHPSA_sweep_pop_for_PrEP_per_timestep_given_barriers() to determine PrEP initiation at t=%6.4lf\n",t);
    /* No reason why we would ever expect PrEP to be offered to very old people. */
    if (PREP_MAX_AGE_PREVENTION_CASCADE>79)
	printf("Need to modify this function to include oldest age group.\n");

    /* I calculate this from UNPD WPP. Output comes from get_mihpsa_project_outputs_phase2_v1.py. */
    double population_15plus_in2021 = 8773997.323;
    double scale_factor = patch[p].param->mihpsa_population_scale/population_15plus_in2021;

    /* When HIV_TEST_WHEN_ON_PrEP==1 we make people test before starting ART. In that case we would include some HIV+ unaware as potential PrEP initates (i.e. they get put in the MIHPSA_intervention_sample samples) - though in the case of a positive test they do not start ART, which is sorted in start_PrEP_for_person(). scale_factor_accountingfor_recruitmentofHIVposunware is the adjustment to make sure we start the right number of people on PrEP. Basically this means we keep trying to put people on PrEP until we reach our target of people on PrEP (so it's not really god-mode - though the way it is implemented in the code might seem that way - in reality we are just making an adjustment for knowledge that will be accrued by the time the person starts PrEP). */
    
    double fudge_factor_lower_coverage = 0.4; /* Factor introduced post 2 Aug 2023 to reduce PrEP to match other models (I previously hit new initiations and active PrEP in the past quarter, but was much higher on number of 15-24 who used PrEP in the past quarter - ie turnover too high). */
    int TARGET_n_AGYW_onPrEP;
    double temp_n_target;

    /* This is deterined by HIV_TEST_WHEN_ON_PrEP. If HIV_TEST_WHEN_ON_PrEP=0 or HIV_TEST_WHEN_ON_PrEP=2, then we assume everyone starting PrEP has already been filtered out (so no HIV testing). If HIV_TEST_WHEN_ON_PrEP=1 then we make them all do a screenign test. In that case we only exclude KNOWN HIV+. */
    double able_to_go_to_start_PrEP_for_person_function;
    
    int i_temp;
    if(t-floor(t)<0.001)
	printf("Calling MIHPSA_sweep_pop_for_PrEP_per_timestep at t=%lf\n",t);
    /* Fudge factor to adjust for the fact that what we want is the number of people continuously on PrEP, not the total number of people on PrEP. */
    //temp_n_target = temp_n_target * 3.0;

    for(i=0; i<MIHPSA_INTERVENTION_SAMPLE_MAX_ARRAY_SIZE; i++){
	patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_primarypop[i] = NULL;
        patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_othereligibles[i] = NULL;
	//patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible[i] = NULL;
    }
    
    if(t<2024)
	/* Arbitrarily chosen baseline (~ population already on PrEP in 2023). */
	//temp_n_target = (t-2023)*11594 + (2024-t)*5000;
	//temp_n_target = (t-2023)*36000 + (2024-t)*20000;
	//temp_n_target = (t-2023)*38000 + (2024-t)*22000;
	temp_n_target = (t-2023)*38000 + (2024-t)*21500;
    else if(t<2025)
	//temp_n_target = (t-2024)*22544 + (2025-t)*11594;
	//temp_n_target = (t-2024)*48000 + (2025-t)*36000;
	temp_n_target = (t-2024)*47000 + (2025-t)*38000;
    else if(t<2026)
	//temp_n_target = (t-2025)*33436 + (2026-t)*22544;
	//temp_n_target = (t-2025)*90000 + (2026-t)*48000;
	//temp_n_target = (t-2025)*88000 + (2026-t)*47000;
	temp_n_target = (t-2025)*87000 + (2026-t)*47000;
    //else if(t<2027)
	//temp_n_target = (t-2026)*42431 + (2027-t)*33436;
	//temp_n_target = 75000;
	//temp_n_target = 88000;
    else
	//temp_n_target = 42431;
	//temp_n_target = 90000;
	temp_n_target = 87000;

    /* This is the number of people (scaled to the IBM population) to start PrEP (assuming we have enough eligibles). 
       Note that we cap the % of eligibles we can reach at MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP (currently 90%). */
    TARGET_n_AGYW_onPrEP = (int) floor(temp_n_target*scale_factor*fudge_factor_lower_coverage);

    //printf("Scale factor=%lf target=%i\n",scale_factor, TARGET_n_AGYW_onPrEP);
    /* Count number of AGYW already on (any type of) PrEP: */
    int n_AGYW_already_onPrEP = 0;


    int i_potential_prep_initiates_primarypop = 0;
    int i_potential_prep_initiates_othereligible = 0;

    /* Boolean for whether the person in "elevated risk" pop (0=n, 1=y). */
    int in_primarypop = 0;
    
    ////////////////
    /* PrEP for 15-24 year old women in a high (non-regular partner)/very high (key pop) risk group:  */
    for(aa = 0; aa < (26 - AGE_ADULT); aa++){
	ai = patch[p].age_list->age_list_by_gender[FEMALE]->youngest_age_group_index + aa;            
	while(ai > (MAX_AGE - AGE_ADULT - 1))
	    ai = ai - (MAX_AGE - AGE_ADULT);
	
	number_per_age_group = patch[p].age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai];
	for(i = 0; i < number_per_age_group; i++){
	    indiv = patch[p].age_list->age_list_by_gender[FEMALE]->age_group[ai][i];
	    /* Ignore anyone <15 or >24: */
	    if((floor(t-indiv->DoB)>=15) && (floor(t-indiv->DoB)<25)){
		//if (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED){
		if(HIV_TEST_WHEN_ON_PrEP==1)
		    /* Assume never tested HIV+ (so both HIV- and unaware HIV+ can go to start_PrEP_for_person() where they will be tested): */
		    able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->ART_status==ARTNEG)?1:0;
		else
		    /* Assume HIV testing happens elsewhere or is badly applied somehow. */
		    able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED)?1:0;
		
		if (able_to_go_to_start_PrEP_for_person_function){	    
		    in_primarypop = 0;
		    /* Primary population = at least 1 non-reg partner. */
		    for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){
			if((indiv->partner_pairs[i_partner]->duration_in_time_steps)<N_TIME_STEP_PER_YEAR){
			    in_primarypop = 1;
			    break;
			}
		    }
		    if(in_primarypop==1){
			patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop[i_potential_prep_initiates_primarypop] = indiv;
			i_potential_prep_initiates_primarypop++;
			if((indiv->id)==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH)
			    printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep() at t=%lf indiv=%li is a potential primary PrEP initiate (step 1) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status);
		    }
		    else if((indiv->n_partners)>1){
			/* Not in primary pop but has multiple partners: */
			patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible[i_potential_prep_initiates_othereligible] = indiv;
			i_potential_prep_initiates_othereligible++;
			if((indiv->id)==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH)
			    printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep() at t=%lf indiv=%li is a potential other PrEP initiate (step 1) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status);
		    }

		    /* /\* Loop through all partners to determine if at high risk. *\/ */
		    /* partnership_duration=1000; /\* Set to dummy value. *\/ */
		    /* i_partner=0; */
		    /* while(i_partner<(indiv->n_partners) && (partnership_duration>=N_TIME_STEP_PER_YEAR)){ */
		    /* 	partnership_duration = indiv->partner_pairs[i_partner]->duration_in_time_steps; */
		    /* 	/\* If this is a non-regular partner, update counters (and add to potential PrEP initiates). *\/ */
		    /* 	if(partnership_duration<N_TIME_STEP_PER_YEAR){ */
		    /* 	    potential_prep_initiates_pointers[i_potential_prep_initiates] = indiv; */
		    /* 	    i_potential_prep_initiates += 1; */
		    /* 	    if(indiv->id==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH) */
		    /* 		printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep() at t=%lf indiv=%li is a potential PrEP initiate with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status); */

		    /* 	} */
		    /* 	i_partner++; */
		    /* } */
		}else if(indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT || indiv->PrEP_cascade_status==ONPREP_ADHERENT || indiv->PrEP_cascade_status==ONDAPIVIRINERING_PREP || indiv->PrEP_cascade_status==ONCABLA_PREP)
		    n_AGYW_already_onPrEP += 1;
		
	    }
	}
    }
    /* if(t>2048){ */
    /* 	printf(">>>t=%6.4lf samplepop=%i otherpop sample IDs: ",t,i_potential_prep_initiates_othereligible); */
    /* 	for(int z_temp=0; z_temp<i_potential_prep_initiates_othereligible; z_temp++) */
    /* 	    printf("%li ",patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible[z_temp]->id); */
    /* 	printf("\n"); */
    /* } */
    
    
    int n_AGYW_to_initiate_PrEP = TARGET_n_AGYW_onPrEP-n_AGYW_already_onPrEP;
    int n_AGYW_to_initiate_PrEP_othereligiblepop;
    
    /* We prioritise the "target" population (currently 15-24 with non-regular partner). Only MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP proportion of the target pop can be initated on PrEP (so we're not perfect).
     Remainder comes from the other pops:*/
    int n_AGYW_to_initiate_PrEP_primarypop;
    if (n_AGYW_to_initiate_PrEP>0){
	if(n_AGYW_to_initiate_PrEP<=i_potential_prep_initiates_primarypop*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP)
	    n_AGYW_to_initiate_PrEP_primarypop = n_AGYW_to_initiate_PrEP;
	else
	    n_AGYW_to_initiate_PrEP_primarypop = (int) floor(i_potential_prep_initiates_primarypop*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP);

	//printf("Initiating %i out of %i in primary pop\n",n_AGYW_to_initiate_PrEP_primarypop,i_potential_prep_initiates_primarypop);
	if(n_AGYW_to_initiate_PrEP_primarypop>0)
	    gsl_ran_choose(rng, patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_primarypop,
			   n_AGYW_to_initiate_PrEP_primarypop,
			   patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop,
			   i_potential_prep_initiates_primarypop, sizeof(individual *));
	for(i_temp=0; i_temp<n_AGYW_to_initiate_PrEP_primarypop; i_temp++){
	    indiv = patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_primarypop[i_temp];
	    if(indiv->id==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH)
		printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep() at t=%lf indiv=%li is a primary pop PrEP initiate with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status);
	    
	    start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PrEP_type, REASON_START_PREP_AGYWINTERVENTION);
	}


	/* Now look for remainder: */
	n_AGYW_to_initiate_PrEP_othereligiblepop = n_AGYW_to_initiate_PrEP - n_AGYW_to_initiate_PrEP_primarypop;

	//printf("At t=%6.4lf, primary population left=%i n_added=%i Remainder n=%i\n",t,i_potential_prep_initiates_primarypop,n_AGYW_to_initiate_PrEP_primarypop,n_AGYW_to_initiate_PrEP_othereligiblepop);


	if(n_AGYW_to_initiate_PrEP_othereligiblepop>(i_potential_prep_initiates_othereligible*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP))
	    /* Cap the number of new initates if needed: */
	    n_AGYW_to_initiate_PrEP_othereligiblepop = (int) floor(i_potential_prep_initiates_othereligible*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP);

	if(n_AGYW_to_initiate_PrEP_othereligiblepop>0)
	    gsl_ran_choose(rng, patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_othereligibles, n_AGYW_to_initiate_PrEP_othereligiblepop,
			   patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible,
			   i_potential_prep_initiates_othereligible, sizeof(individual *));
    
	for(i_temp=0; i_temp<n_AGYW_to_initiate_PrEP_othereligiblepop; i_temp++){
	    indiv = patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_othereligibles[i_temp];
	    if(indiv->id==FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH)
		printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep() at t=%lf indiv=%li is a other eligible pop PrEP initiate (step 2) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status);
	    start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PrEP_type, REASON_START_PREP_AGYWINTERVENTION);
	}
    }
	    //printf("Age = %i sex=%i\n",(int) floor(t-new_prep_initiates_pointers[i_temp]->DoB), new_prep_initiates_pointers[i_temp]->gender);
    /*	    if((new_prep_initiates_pointers[i_temp]->id==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH))
		printf("Initiating PrEP in MIHPSA_sweep_pop_for_PrEP_per_timestep() for %li at t=%6.4lf\n",new_prep_initiates_pointers[i_temp]->id,t);
	    start_PrEP_for_person(new_prep_initiates_pointers[i_temp], patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t);
	}
    */

    //printf("MIHPSA_sweep_pop_for_PrEP_per_timestep() t=%6.4lf target=%i n_to_initate=%i\n",t,TARGET_n_AGYW_onPrEP,n_AGYW_to_initiate_PrEP);
    
    
    
    /* start_PrEP_for_person(indiv, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t); */
    /* Use the line below if we want to force people to be fully adherent: */
    //indiv->PrEP_cascade_status = ONPREP_ADHERENT;





    /* Allow PrEP for men and women here (deal with 15-24 year old women separately): */
    int MIN_PREP_AGE;
    if(patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CURRENTORALPREP){
	for(g = 0; g < N_GENDER; g++){
	    MIN_PREP_AGE = (g==MALE)?0:(24-AGE_ADULT);
	    for(aa = MIN_PREP_AGE; aa < (PREP_MAX_AGE_PREVENTION_CASCADE - AGE_ADULT); aa++){
		ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
		while(ai > (MAX_AGE - AGE_ADULT - 1))
		    ai = ai - (MAX_AGE - AGE_ADULT);
            
		number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
		for(i = 0; i < number_per_age_group; i++){
		    indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
		    if((g==MALE) || (floor(t-indiv->DoB)>=25.0)){
			/* if(i%50==0) */
			/* 	printf("g=%i V2Age=%i\n",g, (int) floor(t-indiv->DoB)); */

			//if (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED){
			/* Here we generate a boolean variable about whether the person meets the eligibility conditions for this scenario: */
			if(HIV_TEST_WHEN_ON_PrEP==1)
			    /* Assume never tested HIV+ (so both HIV- and unaware HIV+ can go to start_PrEP_for_person() where they will be tested): */
			    able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->ART_status==ARTNEG)?1:0;
			else
			    /* Assume HIV testing happens elsewhere or is badly applied somehow. */
			    able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED)?1:0;
			if (able_to_go_to_start_PrEP_for_person_function){	    
			    if(indiv->cascade_barriers.p_will_use_PrEP>0){
				/* Now convert to a per-timestep probability: */
				p_will_use_PrEP_per_timestep = 1.0-pow(1.0-indiv->cascade_barriers.p_will_use_PrEP,TIME_STEP);
				x = gsl_rng_uniform (rng);

				if(x <= p_will_use_PrEP_per_timestep){
				    if((indiv->id==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH))
					printf("***Initiating PrEP in MIHPSA_sweep_pop_for_PrEP_per_timestep() v3 for %li at t=%6.4lf\n",indiv->id,t);
				
				    start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PrEP_type, REASON_START_PREP_BACKGROUND);
				    // PrEP status is set in start_PrEP_for_person(). Use below if we want to force all individuals to be adherent. 
				    //indiv->PrEP_cascade_status = ONPREP_ADHERENT;
				}
			    }
			}
		    }
		}
	    }
	}
    }



    /////////////////////////////////////////////////////////////////////
    /* Testing: */
    /* int a_inprimarypop_notonprep = 0; */
    /* int a_inprimarypop_onprep = 0; */
    /* int a_notinprimarypop_notonprep =0; */
    /* int a_notinprimarypop_onprep =0; */
    
    /* for(aa = 0; aa < (26 - AGE_ADULT); aa++){ */
    /* 	ai = patch[p].age_list->age_list_by_gender[FEMALE]->youngest_age_group_index + aa;             */
    /* 	while(ai > (MAX_AGE - AGE_ADULT - 1)) */
    /* 	    ai = ai - (MAX_AGE - AGE_ADULT); */
	
    /* 	number_per_age_group = patch[p].age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai]; */
    /* 	for(i = 0; i < number_per_age_group; i++){ */
    /* 	    indiv = patch[p].age_list->age_list_by_gender[FEMALE]->age_group[ai][i]; */
    /* 	    /\* Ignore anyone <15 or >24: *\/ */
    /* 	    if((floor(t-indiv->DoB)>=15) && (floor(t-indiv->DoB)<25)){ */
    /* 		if (indiv->HIV_status==UNINFECTED){ */
    /* 		    in_primarypop = 0; */
    /* 		    /\* Primary population = at least 1 non-reg partner. *\/ */
    /* 		    for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){ */
    /* 			if((indiv->partner_pairs[i_partner]->duration_in_time_steps<N_TIME_STEP_PER_YEAR)){ */
    /* 			    in_primarypop = 1; */
    /* 			    break; */
    /* 			} */
    /* 		    } */
    /* 		    if(in_primarypop==1){ */
    /* 			if(indiv->PrEP_cascade_status==NOTONPREP) */
    /* 			    a_inprimarypop_notonprep++; */
    /* 			else */
    /* 			    a_inprimarypop_onprep++; */
    /* 		    }else if((indiv->n_partners)>1){	 */
    /* 			if(indiv->PrEP_cascade_status==NOTONPREP) */
    /* 			    a_notinprimarypop_notonprep++; */
    /* 			else */
    /* 			    a_notinprimarypop_onprep++; */
    /* 		    } */
    /* 		} */
    /* 	    } */
    /* 	} */
    /* } */
    /* printf("At t=%6.4lf primary pop PrEP=%i not prep=%i; otherpop PrEP=%i not prep=%i\n",t,a_inprimarypop_onprep,a_inprimarypop_notonprep, a_notinprimarypop_onprep,a_notinprimarypop_notonprep); */


    ////////////////////////////////////////////////////////////////////

}


/*  */
void MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD(double t, patch_struct *patch, int p, debug_struct *debug){
    int aa, ai, g, i;
    int number_per_age_group;
    int i_partner;
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory), and any partner:
    individual *indiv, *partner;


    int PrEP_type;
    if (patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDORALPREP_SD)
	PrEP_type = PREPTYPE_DAILYORALPREP;
    else if (patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDDAPIVIRINERINGPREP_SD)
	PrEP_type = PREPTYPE_DAPIVIRINERINGPREP;
    else if (patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDCABLAPREP_SD)
	PrEP_type = PREPTYPE_CABLAPREP;
    else{
	printf("Error: unknown PrEP scenario in MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD(). Exiting\n");
	fflush(stdout);
	exit(1);
    }
    
    //printf("Using MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD_forcapped_SD() to determine PrEP initiation at t=%6.4lf\n",t);
    /* No reason why we would ever expect PrEP to be offered to very old people. */
    if (PREP_MAX_AGE_PREVENTION_CASCADE>79)
	printf("Need to modify this function to include oldest age group.\n");

    /* I calculate this from UNPD WPP. Output comes from get_mihpsa_project_outputs_phase2_v1.py. */
    double population_15plus_in2021 = 8773997.323;
    double scale_factor = patch[p].param->mihpsa_population_scale/population_15plus_in2021;

    /* When HIV_TEST_WHEN_ON_PrEP==1 we make people test before starting ART. In that case we would include some HIV+ unaware as potential PrEP initates (i.e. they get put in the MIHPSA_intervention_sample samples) - though in the case of a positive test they do not start ART, which is sorted in start_PrEP_for_person(). scale_factor_accountingfor_recruitmentofHIVposunware is the adjustment to make sure we start the right number of people on PrEP. Basically this means we keep trying to put people on PrEP until we reach our target of people on PrEP (so it's not really god-mode - though the way it is implemented in the code might seem that way - in reality we are just making an adjustment for knowledge that will be accrued by the time the person starts PrEP). */
    //int temp_n_HIVposunware_primarypop;
    //int temp_n_HIVposunware_othereligibles;
    //double scale_factor_accountingfor_recruitmentofHIVposunware_primarypop;
    //double scale_factor_accountingfor_recruitmentofHIVposunware_othereligibles;
    
    double fudge_factor_lower_coverage = 1.0; /* Factor introduced post 2 Aug 2023 to reduce PrEP to match other models (I previously hit new initiations and active PrEP in the past quarter, but was much higher on number of 15-24 who used PrEP in the past quarter - ie turnover too high). 
					       was 0.4 */
    int TARGET_n_onPrEP;
    double temp_n_target;

    /* This is deterined by HIV_TEST_WHEN_ON_PrEP. If HIV_TEST_WHEN_ON_PrEP=0 or HIV_TEST_WHEN_ON_PrEP=2, then we assume everyone starting PrEP has already been filtered out (so no HIV testing). If HIV_TEST_WHEN_ON_PrEP=1 then we make them all do a screenign test. In that case we only exclude KNOWN HIV+. */
    int able_to_go_to_start_PrEP_for_person_function;

    /* Fudge factor to adjust for the fact that what we want is the number of people continuously on PrEP, not the total number of people on PrEP. */
    //temp_n_target = temp_n_target * 3.0;

    for(i=0; i<MIHPSA_INTERVENTION_SAMPLE_MAX_ARRAY_SIZE; i++)
	patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop[i] = NULL;

    
    if(t<2024)
	/* Arbitrarily chosen baseline (~ population already on PrEP in 2023). */
	temp_n_target = (t-2023)*3000 + (2024-t)*1000;
    else if(t<2025)
	temp_n_target = (t-2024)*500 + (2025-t)*3000;
    else if(t<2026)
	//temp_n_target = (t-2025)*88000 + (2026-t)*47000;
	temp_n_target = (t-2025)*500 + (2026-t)*7000;
    else
	temp_n_target = 7000;

    /* This is the number of people (scaled to the IBM population) to start PrEP (assuming we have enough eligibles). 
       Note that we cap the % of eligibles we can reach at MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP (currently 90%). */
    TARGET_n_onPrEP = (int) floor(temp_n_target*scale_factor*fudge_factor_lower_coverage);

    //printf("Scale factor=%lf target=%i\n",scale_factor, TARGET_n_onPrEP);
    /* Count number already on (any type of) PrEP: */
    int n_already_onPrEP = 0;

    int i_potential_prep_initiates_primarypop = 0;

    
    ////////////////
    /* PrEP for individuals in a serodiscordant partnership, where the (known) positive partner if off ART or on ART but not suppressed.
       NOTE - we start with the HIV+ partner (of the opposite gender) as we assume that we are contact-tracing HIV-negative partners.
       Create a list of all their HIV-negative or not known HIV+ partners (ie has some HIV+ partners). 
       Make list unique (sort)
       Rearrange list randomly
       Go through list sequentially until reach coverage (assuming some won't test - so stop at say 90% of the list length if only 90% test)
       For simplicity, cap age of HIV+ partner at age 64:  */


    /* for(aa = 0; aa < (64 - AGE_ADULT); aa++){ */
    /* 	ai = patch[p].age_list->age_list_by_gender[1-g]->youngest_age_group_index + aa; */
    /* 	while(ai > (MAX_AGE - AGE_ADULT - 1)) */
    /* 	    ai = ai - (MAX_AGE - AGE_ADULT); */
	
    /* 	number_per_age_group = patch[p].age_list->age_list_by_gender[1-g]->number_per_age_group[ai]; */
    /* 	for(i = 0; i < number_per_age_group; i++){ */
    /* 	    indiv = patch[p].age_list->age_list_by_gender[1-g]->age_group[ai][i]; */
    /* 	    /\* Check if they have any SD partners: *\/ */
    /* 	    if(indiv->n_partners>0){ */
    /* 		/\* Check if the HIV+ partner meets criteria: *\/ */
    /* 		for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){ */
    /* 		    if(indiv->partner_pairs[i_partner]->ptr[g]->ART_status==ARTNEG){ */
    /* 			/\* Store this person as a potential PrEP initiate (subject to HIV testing). Note that we deal with duplicates later on. *\/ */
    /* 			patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop[i_potential_prep_initiates_primarypop] = indiv; */
    /* 			i_potential_prep_initiates_primarypop++; */
    /* 			if(i_potential_prep_initiates_primarypop>=MIHPSA_INTERVENTION_SAMPLE_MAX_ARRAY_SIZE){ */
    /* 			    printf("Error - need to adjust MIHPSA_INTERVENTION_SAMPLE_MAX_ARRAY_SIZE in MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() as run out of memory. aa=%i Exiting\n", aa); */
    /* 			    fflush(stdout); */
    /* 			    exit(1); */
    /* 			} */
    /* 		    } */
    /* 		} */
    /* 	    } */
    /* 	} */
    /* } */


    /* Age 15+ adults (women only for dapivirine ring, both men and women otherwise). */

    /* This bit allows us to loop over only the necessary genders for the given PrEP type: */
    int start_g;
    if(PrEP_type==PREPTYPE_DAPIVIRINERINGPREP)
	start_g = FEMALE;
    else if(PrEP_type==PREPTYPE_DAILYORALPREP || PrEP_type==PREPTYPE_CABLAPREP)
	start_g = MALE;
    else{
	printf("Unknown PrEP type in MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD(). Exiting\n");
	fflush(stdout);
	exit(1);
    }

    /* Check if this person has a partner living with HIV who meets the criteria: */
    int has_eligible_positive_partner;

    /* Aged 15+ */
    for(g=start_g; g<=FEMALE; g++){
	for(aa = (15-AGE_ADULT); aa < (MAX_AGE-AGE_ADULT); aa++){
	    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;
	    while(ai > (MAX_AGE - AGE_ADULT - 1))
		ai = ai - (MAX_AGE - AGE_ADULT);
	
	    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
	    for(i = 0; i < number_per_age_group; i++){
		indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
		/* Either HIV- or unaware HIV+: */
		if(indiv->ART_status==ARTNEG){
		    /* Check if they have any partners as follows:
		       If HIV- then they need to have at least one HIV+ partner (and then we check if that partner meets criteria of not being VS)
		       If HIV+ (note we already checked they're unaware of status) then we just go through their partners to see if any meets the criteria because for HIV+ people n_HIVpos_partners is not properly tracked. */
		    has_eligible_positive_partner = 0;
		    if(((indiv->HIV_status==UNINFECTED) && (indiv->n_HIVpos_partners>0)) || (indiv->HIV_status>UNINFECTED)){
			/* Check if they have any HIV+ partner meeting criteria: */
			for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){
			    partner = indiv->partner_pairs[i_partner]->ptr[1-g];
			    if(partner->ART_status==ARTNAIVE || partner->ART_status==EARLYART || partner->ART_status==LTART_VU || partner->ART_status==ARTDROPOUT || partner->ART_status==CASCADEDROPOUT){

				has_eligible_positive_partner = 1;
				break;
			    }
			}

			if(has_eligible_positive_partner==1){
			    if(HIV_TEST_WHEN_ON_PrEP==1)
				/* Assume never tested HIV+ (so both HIV- and unaware HIV+ can go to start_PrEP_for_person() where they will be tested): */
				able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->ART_status==ARTNEG)?1:0;
			    else
				/* Assume HIV testing happens elsewhere or is badly applied somehow. */
				able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED)?1:0;
			
			    if(able_to_go_to_start_PrEP_for_person_function==1){
				if(indiv->id==FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH)
				    printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() at t=%lf indiv=%li is able to start PrEP with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status);
			    
				/* Store this person (indiv) as a potential PrEP initiate (subject to HIV testing). Note that we deal with duplicates later on. */
				patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop[i_potential_prep_initiates_primarypop] = indiv;
				i_potential_prep_initiates_primarypop++;
				if(i_potential_prep_initiates_primarypop>=MIHPSA_INTERVENTION_SAMPLE_MAX_ARRAY_SIZE){
				    printf("Error - need to adjust MIHPSA_INTERVENTION_SAMPLE_MAX_ARRAY_SIZE in MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() as run out of memory. aa=%i Exiting\n", aa);
				    fflush(stdout);
				    exit(1);
				}
			    }
			    /* If not able to go on PrEP (but meets other criteria) check if already on ART: */
			    else if(indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT || indiv->PrEP_cascade_status==ONPREP_ADHERENT || indiv->PrEP_cascade_status==ONDAPIVIRINERING_PREP || indiv->PrEP_cascade_status==ONCABLA_PREP){
				n_already_onPrEP++;
			    }
			}
		    }
		}
	    }
	}
    }

    if(t-floor(t)<0.001){
	printf("Calling MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD at t=%lf\n",t);
	printf("Number of potential initates = %i Number already on PrEP = %i\n", i_potential_prep_initiates_primarypop,n_already_onPrEP);
    }

    if(i_potential_prep_initiates_primarypop>0)
	gsl_ran_shuffle(rng, patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop, i_potential_prep_initiates_primarypop, sizeof(individual *));

    int n_to_initiate_PrEP = TARGET_n_onPrEP-n_already_onPrEP;
    if (n_to_initiate_PrEP>0){
	if(n_to_initiate_PrEP>i_potential_prep_initiates_primarypop*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP)
	    n_to_initiate_PrEP = (int) floor(i_potential_prep_initiates_primarypop*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP);
    }

    /* printf("n_to_initiate_PrEP=%i\n",n_to_initiate_PrEP); */
    /* fflush(stdout); */
    
    for(i=0; i<n_to_initiate_PrEP; i++){
	indiv = patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop[i];
	if(indiv->id==FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH)
	    printf("$$$$$$$$$$$$$$In MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() at t=%lf indiv=%li is a other eligible pop PrEP initiate (step 2) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status);
	start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PrEP_type, REASON_START_PREP_SDPARTNERINTERVENTION);
    }


    
    /* 		if(HIV_TEST_WHEN_ON_PrEP==1) */
    /* 		    /\* Assume never tested HIV+ (so both HIV- and unaware HIV+ can go to start_PrEP_for_person() where they will be tested): *\/ */
    /* 		    able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->ART_status==ARTNEG)?1:0; */
    /* 		else */
    /* 		    /\* Assume HIV testing happens elsewhere or is badly applied somehow. *\/ */
    /* 		    able_to_go_to_start_PrEP_for_person_function = (indiv->PrEP_cascade_status==NOTONPREP && indiv->HIV_status==UNINFECTED)?1:0; */
		
    /* 		if (able_to_go_to_start_PrEP_for_person_function){	     */
    /* 		    in_primarypop = 0; */
    /* 		    /\* Primary population = at least 1 non-reg partner. *\/ */
    /* 		    for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){ */
    /* 			if((indiv->partner_pairs[i_partner]->duration_in_time_steps)<N_TIME_STEP_PER_YEAR){ */
    /* 			    in_primarypop = 1; */
    /* 			    break; */
    /* 			} */
    /* 		    } */
    /* 		    if(in_primarypop==1){ */
    /* 			patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop[i_potential_prep_initiates_primarypop] = indiv; */
    /* 			i_potential_prep_initiates_primarypop++; */
    /* 			if((indiv->id)==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH) */
    /* 			    printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() at t=%lf indiv=%li is a potential primary PrEP initiate (step 1) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status); */
    /* 		    } */
    /* 		    else if((indiv->n_partners)>1){ */
    /* 			/\* Not in primary pop but has multiple partners: *\/ */
    /* 			patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible[i_potential_prep_initiates_othereligible] = indiv; */
    /* 			i_potential_prep_initiates_othereligible++; */
    /* 			if((indiv->id)==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH) */
    /* 			    printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() at t=%lf indiv=%li is a potential other PrEP initiate (step 1) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status); */
    /* 		    } */

    /* 		}else if(indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT || indiv->PrEP_cascade_status==ONPREP_ADHERENT || indiv->PrEP_cascade_status==ONDAPIVIRINERING_PREP || indiv->PrEP_cascade_status==ONCABLA_PREP) */
    /* 		    n_already_onPrEP += 1; */
		
    /* 	    } */
    /* 	} */
    /* } */
    /* /\* if(t>2048){ *\/ */
    /* /\* 	printf(">>>t=%6.4lf samplepop=%i otherpop sample IDs: ",t,i_potential_prep_initiates_othereligible); *\/ */
    /* /\* 	for(int z_temp=0; z_temp<i_potential_prep_initiates_othereligible; z_temp++) *\/ */
    /* /\* 	    printf("%li ",patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible[z_temp]->id); *\/ */
    /* /\* 	printf("\n"); *\/ */
    /* /\* } *\/ */
    
    
    /* int n_to_initiate_PrEP = TARGET_n_onPrEP-n_already_onPrEP; */
    /* int n_to_initiate_PrEP_othereligiblepop; */
    
    /* /\* We prioritise the "target" population (currently 15-24 with non-regular partner). Only MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP proportion of the target pop can be initated on PrEP (so we're not perfect). */
    /*  Remainder comes from the other pops:*\/ */
    /* int n_to_initiate_PrEP_primarypop; */
    /* if (n_to_initiate_PrEP>0){ */
    /* 	if(n_to_initiate_PrEP<=i_potential_prep_initiates_primarypop*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP) */
    /* 	    n_to_initiate_PrEP_primarypop = n_to_initiate_PrEP; */
    /* 	else */
    /* 	    n_to_initiate_PrEP_primarypop = (int) floor(i_potential_prep_initiates_primarypop*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP); */

    /* 	//printf("Initiating %i out of %i in primary pop\n",n_to_initiate_PrEP_primarypop,i_potential_prep_initiates_primarypop); */
    /* 	gsl_ran_choose(rng, patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_primarypop, */
    /* 		       n_to_initiate_PrEP_primarypop, */
    /* 		       patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_primarypop, */
    /* 		       i_potential_prep_initiates_primarypop, sizeof(individual *)); */
    /* 	for(i_temp=0; i_temp<n_to_initiate_PrEP_primarypop; i_temp++){ */
    /* 	    indiv = patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_primarypop[i_temp]; */
    /* 	    if(indiv->id==FOLLOW_INDIVIDUAL  && p==FOLLOW_PATCH) */
    /* 		printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() at t=%lf indiv=%li is a primary pop PrEP initiate with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status); */
	    
    /* 	    start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PrEP_type); */
    /* 	} */


    /* 	/\* Now look for remainder: *\/ */
    /* 	n_to_initiate_PrEP_othereligiblepop = n_to_initiate_PrEP - n_to_initiate_PrEP_primarypop; */

    /* 	//printf("At t=%6.4lf, primary population left=%i n_added=%i Remainder n=%i\n",t,i_potential_prep_initiates_primarypop,n_to_initiate_PrEP_primarypop,n_to_initiate_PrEP_othereligiblepop); */


    /* 	if(n_to_initiate_PrEP_othereligiblepop>(i_potential_prep_initiates_othereligible*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP)) */
    /* 	    /\* Cap the number of new initates if needed: *\/ */
    /* 	    n_to_initiate_PrEP_othereligiblepop = (int) floor(i_potential_prep_initiates_othereligible*MIHPSA_PREP_TARGET_COVERAGE_PRIMARY_POP); */

    /* 	gsl_ran_choose(rng, patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_othereligibles, n_to_initiate_PrEP_othereligiblepop, */
    /* 		       patch[p].MIHPSA_intervention_sample->potential_prep_initiates_pointers_othereligible, */
    /* 		       i_potential_prep_initiates_othereligible, sizeof(individual *)); */
    
    /* 	for(i_temp=0; i_temp<n_to_initiate_PrEP_othereligiblepop; i_temp++){ */
    /* 	    indiv = patch[p].MIHPSA_intervention_sample->new_prep_initiates_pointers_othereligibles[i_temp]; */
    /* 	    if(indiv->id==FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH) */
    /* 		printf("In MIHPSA_sweep_pop_for_PrEP_per_timestep_forcapped_SD() at t=%lf indiv=%li is a other eligible pop PrEP initiate (step 2) with HIV=%i PrEP=%i\n",t,indiv->id,indiv->HIV_status,indiv->PrEP_cascade_status); */
    /* 	    start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PrEP_type); */
    /* 	} */
    /* } */


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
	p_use_condom1 = *(indiv1->cascade_barriers.p_want_to_use_condom_casual_partner);
	p_use_condom2 = *(indiv2->cascade_barriers.p_want_to_use_condom_casual_partner);
    }
    else{
	p_use_condom1 = *(indiv1->cascade_barriers.p_want_to_use_condom_long_term_partner);
	p_use_condom2 = *(indiv2->cascade_barriers.p_want_to_use_condom_long_term_partner);
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
	indiv1->cascade_barriers.use_condom_in_this_partnership[indiv1->n_partners-1] = USECOND;
	indiv2->cascade_barriers.use_condom_in_this_partnership[indiv2->n_partners-1] = USECOND;
    }
    else{
	indiv1->cascade_barriers.use_condom_in_this_partnership[indiv1->n_partners-1] = NOCOND;
	indiv2->cascade_barriers.use_condom_in_this_partnership[indiv2->n_partners-1] = NOCOND;
    }	
}




/* This function represents an intervention that increases the probability that an individual will get VMMC from time t onwards (by reducing barriers).
   Function goes through everyone (using age_list), and calls function assign_individual_VMMC_cascade() to update their VMMC prevention cascade barriers in response to the intervention. 
 */
void prevention_cascade_intervention_VMMC(double t, patch_struct *patch, int p){

    int aa, ai, i;
    int number_per_age_group;
    
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    

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
	    assign_individual_VMMC_prevention_cascade(t, indiv, &(patch[p].param->barrier_params));
	}
	
    }
}


/* This function represents an intervention that increases the probability that an individual will get PrEP from time t onwards (by reducing barriers).
   Function goes through everyone (using age group), and calls function assign_individual_PrEP_cascade to update their PrEP prevention cascade barriers in response to the intervention. 
 */
void prevention_cascade_intervention_PrEP(double t, patch_struct *patch, int p){

    int aa, ai, g, i;
    int number_per_age_group;
    
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
		assign_individual_PrEP_prevention_cascade(t, indiv, &(patch[p].param->barrier_params), intervention_scenario);
	    }
	    
	}
    }
	
}




void generate_intervention_increase_in_partnership_condom_use_lookuptable(cascade_barrier_params *barrier_params){

    /* Index over M/F prevention barrier groups: */
    int i_cond_preventionbarrier_group_M,i_cond_preventionbarrier_group_F;

    for(i_cond_preventionbarrier_group_M=0; i_cond_preventionbarrier_group_M<N_COND_PREVENTIONBARRIER_GROUPS_M; i_cond_preventionbarrier_group_M++)
	for(i_cond_preventionbarrier_group_F=0; i_cond_preventionbarrier_group_F<N_COND_PREVENTIONBARRIER_GROUPS_F; i_cond_preventionbarrier_group_F++){

	    barrier_params->change_in_p_use_condom_casual[i_cond_preventionbarrier_group_M][i_cond_preventionbarrier_group_F] =
		sqrt(barrier_params->p_use_cond_casual_present[i_cond_preventionbarrier_group_M][1]*barrier_params->p_use_cond_casual_present[N_COND_PREVENTIONBARRIER_GROUPS_M+i_cond_preventionbarrier_group_F][1]) - 
		sqrt(barrier_params->p_use_cond_casual_present[i_cond_preventionbarrier_group_M][0]*barrier_params->p_use_cond_casual_present[N_COND_PREVENTIONBARRIER_GROUPS_M+i_cond_preventionbarrier_group_F][0]);
    

	    barrier_params->change_in_p_use_condom_LT[i_cond_preventionbarrier_group_M][i_cond_preventionbarrier_group_F] =
		sqrt(barrier_params->p_use_cond_LT_present[i_cond_preventionbarrier_group_M][1]*barrier_params->p_use_cond_LT_present[N_COND_PREVENTIONBARRIER_GROUPS_M+i_cond_preventionbarrier_group_F][1]) - 
		sqrt(barrier_params->p_use_cond_LT_present[i_cond_preventionbarrier_group_M][0]*barrier_params->p_use_cond_LT_present[N_COND_PREVENTIONBARRIER_GROUPS_M+i_cond_preventionbarrier_group_F][0]);
	}    


}





/* Function called when a condom barrier prevention intervention occurs, potentially changing condom use in existing partnerships (*starting condom use in partnership where condoms were not used before*).
   Function called by ******. */
void update_partnership_condom_use_in_response_to_intervention(individual *indiv1, individual *indiv2, cascade_barrier_params barrier_params, double t, double duration_partnership){
    
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


    

    /* Look at change in probability: */    
    if (duration_partnership<1.0){
	change_in_p_use_condom = barrier_params.change_in_p_use_condom_casual[index_HIV_prevention_cascade_condom(ageM,MALE)][index_HIV_prevention_cascade_condom(ageF,FEMALE)-N_COND_PREVENTIONBARRIER_GROUPS_M];
    }
    /* Long-term partnership: */
    else{
	change_in_p_use_condom = barrier_params.change_in_p_use_condom_LT[index_HIV_prevention_cascade_condom(ageM,MALE)][index_HIV_prevention_cascade_condom(ageF,FEMALE)-N_COND_PREVENTIONBARRIER_GROUPS_M];

    }

    
    
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
		printf("%li %li %li\n",indiv1->id,check_id,indiv2->id);
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
		printf("%li %li %li\n",indiv1->id,check_id,indiv2->id);
		exit(1);
	    }
	}

	/* Check that condom use matches: */
	if(indiv1->cascade_barriers.use_condom_in_this_partnership[i_partner1]!=NOCOND || indiv2->cascade_barriers.use_condom_in_this_partnership[i_partner2]!=NOCOND){
	    printf("Error in update_partnership_condom_use_in_response_to_intervention() - condom use in partners 1+2 not equal to zero prior to intervention. Exiting\n");
	    exit(1);
	}

	/* Now set condom use in partnership to be 'use condom': */
	indiv1->cascade_barriers.use_condom_in_this_partnership[i_partner1] = USECOND;
	indiv2->cascade_barriers.use_condom_in_this_partnership[i_partner2] = USECOND;
    }

}




    
/* Function corresponds to an intervention that increases each individual's preference for using a condom (by reducing barriers).
   This function increases the probability of using a condom for existing partnerhips.
   ***Right now, if a partnerships is using a condom, then they will continue to do so. If not, then there is a probability that they will start to use it. 
   
   
   Function loops through the list of alive people via age_list, looking at partnerships for each person - update condom use if the id of the partner is < the id of that person. 
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

    /* Store scenario for easier readability. */
    int intervention_scenario = patch[p].param->barrier_params.i_condom_barrier_intervention_flag;
    printf("Condom intervention scenario = %i\n",intervention_scenario);

    /* Note - it is *wrong* to call this function if there is no condom intervention, as the second part of the function calls update_partnership_condom_use_in_response_to_intervention(). That function redraws condom use in partnerships where condoms are not already used - so increases condom use in the absence of an intervention. Hence this return statement is a safety catch: */
    if(intervention_scenario==0){
	printf("Should not be in function prevention_cascade_intervention_condom() when patch[p].param->barrier_params.i_condom_barrier_intervention_flag is 0. Please check what's happening.\n");
	return;
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
		    if (indiv->cascade_barriers.use_condom_in_this_partnership[i_partners]==NOCOND){
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
	    indiv = patch[p].age_list->age_list_by_gender[g]->oldest_age_group[i];
	    id = indiv->id;
	    n_partners = indiv->n_partners;
	    /* Now check this person's partnerships: */
	    for (i_partners=0; i_partners<n_partners; i_partners++){

		/* Only update if they're not consistently using condoms already: */
		if (indiv->cascade_barriers.use_condom_in_this_partnership[i_partners]==NOCOND){
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



void update_specific_age_VMMCbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p, int age_to_update){


    int aa, ai, i;
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;

    int number_per_age_group;
    /* Subtract 1 because the age_list cohort 'age a' is 'people who are aged a at the start of the year (so would be age a+1 on their birthday during the year)' . */
    aa = (age_to_update-1) - AGE_ADULT;
    ai = patch[p].age_list->age_list_by_gender[MALE]->youngest_age_group_index + aa;            
    while(ai > (MAX_AGE - AGE_ADULT - 1))
	ai = ai - (MAX_AGE - AGE_ADULT);
            
    number_per_age_group = patch[p].age_list->age_list_by_gender[MALE]->number_per_age_group[ai];
    for(i = 0; i < number_per_age_group; i++){
	indiv = patch[p].age_list->age_list_by_gender[MALE]->age_group[ai][i];
	if(indiv->birthday_timestep==t_step){
	    if(indiv->id==FOLLOW_INDIVIDUAL)
		printf("Modifying VMMC HIV prevention cascade probability due to birthday at time t=%lf for id=%li age%i\n",t,indiv->id,(int) floor(t-indiv->DoB));
	    assign_individual_VMMC_prevention_cascade(t, indiv, &(patch[p].param->barrier_params));
	}
    }
}

/* Carried out at each timestep to check for people passing age thresholds related to VMMC prevention cascade barriers.
   Function uses age_list to get birth year cohorts, then birthday_timestep to check if it's their birthday in that timestep. */
void update_VMMCbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p){
    /* Note that this is a little more complicated.
       age_list is the list of people whose birthdays lie between YYYY+TIME_STEP and (YYYY+1). So we split this up correspondingly.
    */
    int offset=(t_step==0)?1:0;
    
    /* Go through 15 year old men. */
    update_specific_age_VMMCbarriers_from_ageing(t, t_step, patch, p, PREP_VMMC_MIN_AGE_PREVENTION_CASCADE+offset);
    /* Now 30 year old men: */
    update_specific_age_VMMCbarriers_from_ageing(t, t_step, patch, p, 30+offset);
    /* Now 56 year old men (the +1 is to make it 56): */
    update_specific_age_VMMCbarriers_from_ageing(t, t_step, patch, p, VMMC_MAX_AGE_PREVENTION_CASCADE+1+offset);

}


void update_specific_age_PrEPbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p, int age_to_update, int g){

    int intervention_scenario = (t<patch[p].param->barrier_params.t_start_prevention_cascade_intervention) ? 0:patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag;

    int aa, ai, i;
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;

    int number_per_age_group;
    /* Subtract 1 because the age_list cohort 'age a' is 'people who are aged a at the start of the year (so would be age a+1 on their birthday during the year)' . */
    aa = (age_to_update-1) - AGE_ADULT;
    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
    while(ai > (MAX_AGE - AGE_ADULT - 1))
	ai = ai - (MAX_AGE - AGE_ADULT);
            
    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
    for(i = 0; i < number_per_age_group; i++){

	if(t==2019 && g==MALE && age_to_update==15)
	    printf("ZZAai=%i i=%i\n",ai,i);
	
	indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
	
	if(indiv->birthday_timestep==t_step){
	    
	    if(indiv->id==FOLLOW_INDIVIDUAL)
		printf("Modifying PrEP HIV prevention cascade probability due to birthday at time t=%lf for id=%li age%i\n",t,indiv->id,(int) floor(t-indiv->DoB));
		
	    assign_individual_PrEP_prevention_cascade(t, indiv, &(patch[p].param->barrier_params), intervention_scenario);
	    
	}
    }
}

/* Carried out at each timestep to check for people passing age thresholds related to PrEP prevention cascade barriers.
   Function uses age_list to get birth year cohorts, then birthday_timestep to check if it's their birthday in that timestep. */
void update_PrEPbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p){
    int g;

    /* Note that this is a little more complicated.
       age_list is the list of people whose birthdays lie between YYYY+TIME_STEP and (YYYY+1). So we split this up correspondingly.
    */
    int offset=(t_step==0)?1:0;
    

    
    /* Go through everyone - modify if we only reach certain age groups etc. */

    /* Firstly 15 year old men+women: */
    for(g = 0; g < N_GENDER; g++){
	update_specific_age_PrEPbarriers_from_ageing(t, t_step, patch, p, PREP_VMMC_MIN_AGE_PREVENTION_CASCADE+offset, g);
    }

    /* Now 25 year old women: */
    update_specific_age_PrEPbarriers_from_ageing(t, t_step, patch, p, 25+offset, FEMALE);

    /* Now 30 year old men: */
    update_specific_age_PrEPbarriers_from_ageing(t, t_step, patch, p, 30+offset, MALE);

    /* Now 56 year old men+women (the +1 is to make it 56): */
    for(g = 0; g < N_GENDER; g++)
	update_specific_age_PrEPbarriers_from_ageing(t, t_step, patch, p, PREP_MAX_AGE_PREVENTION_CASCADE+1+offset, g);

}




void update_specific_age_condombarriers_from_ageing(double t, int t_step, patch_struct *patch, int p, int age_to_update, int g){


    int aa, ai, i;
    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;

    int number_per_age_group;
    /* Subtract 1 because the age_list cohort 'age a' is 'people who are aged a at the start of the year (so would be age a+1 on their birthday during the year)' . */
    aa = (age_to_update-1) - AGE_ADULT;
    ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;            
    while(ai > (MAX_AGE - AGE_ADULT - 1))
	ai = ai - (MAX_AGE - AGE_ADULT);
            
    number_per_age_group = patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
    for(i = 0; i < number_per_age_group; i++){
	indiv = patch[p].age_list->age_list_by_gender[g]->age_group[ai][i];
	if(indiv->birthday_timestep==t_step){
	    /* Assumption - condom use in *existing* partnerships does not change when people pass this age threshold. We therefore do not need an equivalent function to update_partnership_condom_use_in_response_to_intervention(). */
	    assign_individual_condom_prevention_cascade(t, indiv, &(patch[p].param->barrier_params));
	}
    }
}

/* Carried out at each timestep to check for people passing age thresholds related to condom prevention cascade barriers.
   Function uses age_list to get birth year cohorts, then birthday_timestep to check if it's their birthday in that timestep. */
void update_condombarriers_from_ageing(double t, int t_step, patch_struct *patch, int p){
    
    /* Go through everyone - modify if we only reach certain age groups etc: */

    /* Note that this is a little more complicated.
       age_list is the list of people whose birthdays lie between YYYY+TIME_STEP and (YYYY+1). So we split this up correspondingly.
    */
    int offset=(t_step==0)?1:0;
    

    
    /* Go through everyone - modify if we only reach certain age groups etc. */

 
    /* 25 year old women: */
    update_specific_age_condombarriers_from_ageing(t, t_step, patch, p, 25+offset, FEMALE);

    /* Now 30 year old men: */
    update_specific_age_condombarriers_from_ageing(t, t_step, patch, p, 30+offset, MALE);

}


void update_VMMCrates(int t, parameters *param, double *adjustment_to_rate){
    if(MIHPSA_MODULE==1)
	update_VMMCrates_MIHPSA(t, param, adjustment_to_rate);
    else
	update_VMMCrates_Manicaland(t, param, adjustment_to_rate);
}



void get_VMMC_rate_adjustment_foralreadycirc_hivpos(double t, patch_struct *patch, int p, double adjustment_to_rate[2]){
    int age;
    long n_id;

    individual *indiv; /* Pointer used to make code more readable - points to already allocated memory so no need to malloc. */

    /* The '2' is the number of (male) prevention cascade priority populations that are eligible for VMMC (15-29 and 30-54 yer old men who have ever had sex). */
    int n_men_in_prevention_group[2] = {0,0};
    int n_men_eligble_vmmc_in_prevention_group[2] = {0,0};

    int i_prevention_group;

    /* Loop through the alive population. */
    for (n_id = 0; n_id < patch[p].id_counter; n_id++){
	indiv = &patch[p].individual_population[n_id];
	/* Only for male: */
	if(indiv->gender==MALE){

	    /* Check that the person is not dead: */
	    if (indiv->cd4!=DEAD){
		age = (int) floor(t - indiv->DoB);
		
		if(age>=15 && age<=54){

		    /* Restrict to men who have ever had sex: */
		    if(indiv->n_lifetime_partners>0){
			
			i_prevention_group = (age<30)? 0:1;
			n_men_in_prevention_group[i_prevention_group]++;
			if(indiv->HIV_status==UNINFECTED && indiv->circ==UNCIRC)
			    n_men_eligble_vmmc_in_prevention_group[i_prevention_group]++;
		    }
		}
	    }
	}

    }

    for(i_prevention_group=0; i_prevention_group<2; i_prevention_group++){
	adjustment_to_rate[i_prevention_group] = n_men_in_prevention_group[i_prevention_group]/((n_men_eligble_vmmc_in_prevention_group[i_prevention_group]>0 ? n_men_eligble_vmmc_in_prevention_group[i_prevention_group]:1e-10));
	//printf("In function adjustment_to_rate[%i]=%lf\n",i_prevention_group, adjustment_to_rate[i_prevention_group]);
    }
    
}


/* Function allows VMMC rates to vary each year - for Manicaland. */
void update_VMMCrates_Manicaland(int t, parameters *param, double *adjustment_to_rate){

    /* Based on analysis of national DHIS2 data to get relative number of 2013-2018 VMMC operations compared to 2019. Data came from MIHPSA project, but is in tile C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\VMMC\Model_VMMC_uptake_FINAL.xlsx 'Louisa prevention cascade' tab. */
    double VMMC_relativerate_2013_2018[6] = {0.317,0.531,0.641,0.661,0.769,0.953};
    
    int i_vmmc_preventionbarrier_group;

    int i_adjustment;

    
    int intervention_scenario;    /* Stores scenario for easier readability. */
    if(t>=param->barrier_params.t_start_prevention_cascade_intervention){
        intervention_scenario = param->barrier_params.i_VMMC_barrier_intervention_flag;
	
    }
    else{
	intervention_scenario = 0; /* pre-intervention. */
    }


    /* We set these to be zero: */
    param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_TOO_YOUNG_M] = 0;
    param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_TOO_OLD_M] = 0;
    param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_NEVERSEX_M] = 0;

    
    if(t<2013){
	for(i_vmmc_preventionbarrier_group=i_VMMC_PREVENTIONBARRIER_YOUNG_M; i_vmmc_preventionbarrier_group<=i_VMMC_PREVENTIONBARRIER_OLD_M; i_vmmc_preventionbarrier_group++)
	    param->barrier_params.p_use_VMMC[i_vmmc_preventionbarrier_group] = 0; 
    }
    else{
	/* Once VMMC starts we need to adjust for % of men in given VMMC prevention barrier group who can get VMMC (i.e. HIV- and not already circumcised). */
	//for(i_adjustment=0;i_adjustment<2;i_adjustment++)
	//printf("Outside function adjustment_to_rate[%i]=%lf\n",i_adjustment,adjustment_to_rate[i_adjustment]);
	
	if(t>=2019){
	    for(i_vmmc_preventionbarrier_group=i_VMMC_PREVENTIONBARRIER_YOUNG_M; i_vmmc_preventionbarrier_group<=i_VMMC_PREVENTIONBARRIER_OLD_M; i_vmmc_preventionbarrier_group++){
		i_adjustment = i_vmmc_preventionbarrier_group-i_VMMC_PREVENTIONBARRIER_YOUNG_M;
		param->barrier_params.p_use_VMMC[i_vmmc_preventionbarrier_group] = param->barrier_params.p_use_VMMC_present[i_vmmc_preventionbarrier_group][intervention_scenario]*adjustment_to_rate[i_adjustment]; /* Note -we ignore COVID-19 here (so use last pre-covid value). */
	    }
	}
    
	else{
	    int i_year = (int) t-2013;
	    for(i_vmmc_preventionbarrier_group=i_VMMC_PREVENTIONBARRIER_YOUNG_M; i_vmmc_preventionbarrier_group<=i_VMMC_PREVENTIONBARRIER_OLD_M; i_vmmc_preventionbarrier_group++){
		i_adjustment = i_vmmc_preventionbarrier_group-i_VMMC_PREVENTIONBARRIER_YOUNG_M;
		param->barrier_params.p_use_VMMC[i_vmmc_preventionbarrier_group] = VMMC_relativerate_2013_2018[i_year] * param->barrier_params.p_use_VMMC_present[i_vmmc_preventionbarrier_group][intervention_scenario]*adjustment_to_rate[i_adjustment]; /* Note -we ignore COVID-19 here (so use last pre-covid value). */
	    }
	}
    }


    // Checked that this works:
    //printf("p_use_VMMC at t=%i: %lf %lf\n",t,param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M],param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M]);

    return;


}


/* Function allows VMMC rates to vary each year. 
   Designed for MIHPSA project, but can take into account the fact that VMMC uptake has been quite non-linear. */
void update_VMMCrates_MIHPSA(int t, parameters *param, double *adjustment_to_rate){

    /* We have data for 12 years from C:\Users\mpickles\Dropbox (SPH Imperial College)\projects\MIHPSA_Zimabwe2021\Copy of HIVcalibrationData_Zimbabwe.xlsx. */
    double VMMCrate_young[12] = {0.0005,0.0021,0.0063,0.0095,0.0157,0.0287,0.0392,0.0430,0.0467,0.0556,0.0623,0.0397};
    double VMMCrate_old[12] = {0.0005,0.0021,0.0063,0.0095,0.0157,0.0287,0.0392,0.0430,0.0467,0.0556,0.0623,0.0397};

    /* We set these to be zero: */
    param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_TOO_YOUNG_M] = 0;
    param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_TOO_OLD_M] = 0;
    param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_NEVERSEX_M] = 0;

    if(t>2021){
	//param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[10]*adjustment_to_rate[0]; /* Use 2018-19 pre-COVID value. */
	//param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[10]*adjustment_to_rate[1]; /* Use 2018-19 pre-COVID value. */
	double reach_eightypercent_rate = 0.026;
	//printf("Adjustment = %lf %lf\n",adjustment_to_rate[0],adjustment_to_rate[1]);
	//param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = reach_eightypercent_rate*adjustment_to_rate[0]; /* Use 2018-19 pre-COVID value. */
	//param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = reach_eightypercent_rate*adjustment_to_rate[1]; /* Use 2018-19 pre-COVID value. */
	param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = reach_eightypercent_rate*2.0*adjustment_to_rate[0]; /* Use 2018-19 pre-COVID value. */
	param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = reach_eightypercent_rate*adjustment_to_rate[1]; /* Use 2018-19 pre-COVID value. */
    }
    else if(t<2010){
	param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = 0;
	param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = 0;
    }

    else{
	switch(t)
	    {
	    case 2010:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[0]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[0]*adjustment_to_rate[1];
		break;
	    case 2011:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[1]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[1]*adjustment_to_rate[1];
		break;
	    case 2012:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[2]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[2]*adjustment_to_rate[1];
		break;
	    case 2013:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[3]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[3]*adjustment_to_rate[1];
		break;
	    case 2014:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[4]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[4]*adjustment_to_rate[1];
		break;
	    case 2015:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[5]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[5]*adjustment_to_rate[1];
		break;
	    case 2016:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[6]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[6]*adjustment_to_rate[1];
		break;
	    case 2017:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[7]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[7]*adjustment_to_rate[1];
		break;
	    case 2018:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[8]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[8]*adjustment_to_rate[1];
		break;
	    case 2019:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[9]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[9]*adjustment_to_rate[1];
		break;
	    case 2020:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[10]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[10]*adjustment_to_rate[1];
		break;
	    case 2021:
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M] = VMMCrate_young[11]*adjustment_to_rate[0];
		param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M] = VMMCrate_old[11]*adjustment_to_rate[1];
		break;
	    default:
		printf("Default ");
	    }
    }
    // Checked that this works:
    //printf("p_use_VMMC at t=%i: %lf %lf\n",t,param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_YOUNG_M],param->barrier_params.p_use_VMMC[i_VMMC_PREVENTIONBARRIER_OLD_M]);

    return;


}


/* Function allows condom rates to vary each year.
   Designed for MIHPSA project, but can be used elsewhere. */
void update_condomrates(double t, parameters *param){
    if(MIHPSA_MODULE==1)
	update_condomrates_MIHPSA(t, param);
    else
	update_condomrates_Manicaland(t, param);
}





/* Function allows condom rates to vary each year. 
   Designed for MIHPSA project, but can be used elsewhere. */
void update_condomrates_MIHPSA(double t, parameters *param){

    double cond_1989 = 0.05; /* Assumed condom use rate in 1989. */

    int intervention_scenario;    /* Stores scenario for easier readability. */
    if(t>=param->barrier_params.t_start_prevention_cascade_intervention){
        intervention_scenario = param->barrier_params.i_condom_barrier_intervention_flag;
	
    }
    else{
	intervention_scenario = 0; /* pre-intervention. */
    }

    /* Based on analysis of data for MIHPSA (see C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\Condom_use_analysis.xlsx, sheet "MIHPSA info"). 
       There is an increase in recorded distributed condoms per person between 2010 and 2018. It dips in 2019/20 in response to covid-19, which we ignore and assume 2018 value continues. We fit a regression to the 'per-person' condom via Excel. 
       We don't have distribution data for pre-2010. HOWEVER, the Manicaland R1-R5 analyses suggest that condom use was fairly constant during this time - so let's have it as a slow decline to some constant value that represents pre-HIV contraception use. 
       There's a paper that puts condom use at last act among men to be 5% in 1989, so let's take that as baseline. */

    int i_cond_preventionbarrier_group;

    /* Before 1989, assume that condom use is 5%: */
    if(t<1989){
	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = cond_1989;
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = cond_1989;
	}

    }
    else if(t>=2018){
	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = param->barrier_params.p_use_cond_casual_present[i_cond_preventionbarrier_group][intervention_scenario];
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = param->barrier_params.p_use_cond_LT_present[i_cond_preventionbarrier_group][intervention_scenario];
	}
	/* For MIHPSA minimal scenarios when CUPP is removed from 2023 onwards,  we need to decrease condom use in 2023: */
	if((param->MIHPSA_params.FLAGS.remove_CUPP==1) && (t>=2023)){
	    // 
	    //if(t==2023){
	    //MIHPSA_sweep_through_condomusepartnerships_reduce_forcondomuse_minimalscenario(patch, p, double change_in_condomuse_LT, double change_in_condomuse_nonreg);
	    //printf("*** Adjust minimal scenario condom use for young women\n");
	    for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
		//param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] *= 0.9;
		param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = MIHPSA_new_condomuse_when_CUPP_switchedoff(param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group], param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_nonreg);

		
		param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = MIHPSA_new_condomuse_when_CUPP_switchedoff(param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group], param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_LT);
		
		//param->barrier_params.p_use_cond_casual[i_COND_PREVENTIONBARRIER_YOUNG_F] = param->barrier_params.p_use_cond_casual_present[i_COND_PREVENTIONBARRIER_YOUNG_F][intervention_scenario] * 0.5;
	    }
	}
    }
	    
    else if(t>=2010 && t<2018){
	/* Based off excel file C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\Condom_use_analysis.xlsx "MIHPSA info" sheet. */
	double f = (0.8433*(t-2009)+8.665)/16.2547;

	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = f*param->barrier_params.p_use_cond_casual_present[i_cond_preventionbarrier_group][0];
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = f*param->barrier_params.p_use_cond_LT_present[i_cond_preventionbarrier_group][0];
	}
    }
    /* t=1989-2009: */
    else if(t>=1989 && t<2010){
	/* This is the fraction of 2018's condom use which is used in 2010.
	   e.g. if condom use was 80% in 2018, then it would be f_2010*80% in 2010. */
	double f_2010 = 9.5083/16.2547; /* Calculated in Condom_use_analysis.xlsx "MIHPSA info" sheet. */
	double delta_t = (t-1989.0)/(2010-1989);
	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = cond_1989 + delta_t * (f_2010*param->barrier_params.p_use_cond_casual_present[i_cond_preventionbarrier_group][0] - cond_1989);
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = cond_1989 + delta_t * (f_2010*param->barrier_params.p_use_cond_LT_present[i_cond_preventionbarrier_group][0] - cond_1989);
	}

    }
    else{
	printf("Error - time %6.4lf is not included in the if statement in update_condomrates(). Exiting\n",t);
	exit(1);
    }

    /* printf("At t=%6.4lf, p_use_cond_casual= %lf %lf %lf %lf; p_use_cond_LT= %lf %lf %lf %lf\n",t, */
    /* 	   param->barrier_params.p_use_cond_casual[0], */
    /* 	   param->barrier_params.p_use_cond_casual[1], */
    /* 	   param->barrier_params.p_use_cond_casual[2], */
    /* 	   param->barrier_params.p_use_cond_casual[3], */
    /* 	   param->barrier_params.p_use_cond_LT[0], */
    /* 	   param->barrier_params.p_use_cond_LT[1], */
    /* 	   param->barrier_params.p_use_cond_LT[2], */
    /* 	   param->barrier_params.p_use_cond_LT[3]); */

}



/* Function allows condom rates to vary each year. 
   Version for Manicaland. */
void update_condomrates_Manicaland(double t, parameters *param){

    double cond_1989 = 0.05; /* Assumed condom use rate in 1989. */

    int intervention_scenario;    /* Stores scenario for easier readability. */
    if(t>=param->barrier_params.t_start_prevention_cascade_intervention){
        intervention_scenario = param->barrier_params.i_condom_barrier_intervention_flag;
	
    }
    else{
	intervention_scenario = 0; /* pre-intervention. */
    }

    /* Based on analysis of data for MIHPSA (see C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\Condom_use_analysis.xlsx, sheet "Model decisions Manicaland"). 
       There's a paper that puts condom use at last act among men to be 5% in 1989, so let's take that as baseline. */

    int i_cond_preventionbarrier_group;

    /* Before 1995, assume that condom use is 5% (Mbizvo and Adamchak, Central African Journal of Medicine 1989 - see Dropbox/Manicaland/Model/CondomUse). 1995 chosen fairly arbitrarily - condom use had already reached R1 levels by 1999, so need to increase beforehand.  */
    if(t<1995){
	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = cond_1989;
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = cond_1989;
	}

    }
    else if(t>=2012){
	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = param->barrier_params.p_use_cond_casual_present[i_cond_preventionbarrier_group][intervention_scenario];
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = param->barrier_params.p_use_cond_LT_present[i_cond_preventionbarrier_group][intervention_scenario];
	}
    }

    else if(t>=1995 && t<2012){
	/* Based off excel file C:\Users\mpickles\Dropbox (SPH Imperial College)\Manicaland\Model\Condom_use_analysis.xlsx "Model decisions Manicaland" sheet. 
	 Roguhly speaking CCU was only 70% of the R6-7 value in R1-5. */
	double f = 0.7;
	for(i_cond_preventionbarrier_group=0; i_cond_preventionbarrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_cond_preventionbarrier_group++){
	    param->barrier_params.p_use_cond_casual[i_cond_preventionbarrier_group] = f*param->barrier_params.p_use_cond_casual_present[i_cond_preventionbarrier_group][0];
	    param->barrier_params.p_use_cond_LT[i_cond_preventionbarrier_group] = f*param->barrier_params.p_use_cond_LT_present[i_cond_preventionbarrier_group][0];
	}
    }
    else{
	printf("Error - time %6.4lf is not included in the if statement in update_condomrates(). Exiting\n",t);
	exit(1);
    }

    /* printf("At t=%6.4lf, p_use_cond_casual= %lf %lf %lf %lf; p_use_cond_LT= %lf %lf %lf %lf\n",t, */
    /* 	   param->barrier_params.p_use_cond_casual[0], */
    /* 	   param->barrier_params.p_use_cond_casual[1], */
    /* 	   param->barrier_params.p_use_cond_casual[2], */
    /* 	   param->barrier_params.p_use_cond_casual[3], */
    /* 	   param->barrier_params.p_use_cond_LT[0], */
    /* 	   param->barrier_params.p_use_cond_LT[1], */
    /* 	   param->barrier_params.p_use_cond_LT[2], */
    /* 	   param->barrier_params.p_use_cond_LT[3]); */

}
 


 
