/* Contains MIHPSA-specific functions (excluding outputs): */

/************************************************************************/
/******************************* Includes  ******************************/
/************************************************************************/

#include "mihpsa.h"
#include "constants.h"
#include "prevention_cascades.h"


/* Function finds the scale factor needed to scale the simulated population (adults + children) to the actual population at a given time. */
double find_population_scale(patch_struct *patch, int p, double real_population){
    
    double npop_children=0;
    double npop_adult = 0;
    int g,aa,ai;
    
    for(g = 0; g < N_GENDER; g++){
        for(aa = 0; aa < (MAX_AGE-AGE_ADULT); aa++){
            ai = aa + patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index;
            while (ai>(MAX_AGE-AGE_ADULT-1)){
                ai = ai - (MAX_AGE-AGE_ADULT);
            }
            npop_adult += patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
        }
        npop_adult += patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
    }

    printf("In find_pop_scale, npop_adult=%lf\n",npop_adult);
    
    for(int j_child=0; j_child<((AGE_ADULT+1)*N_TIME_STEP_PER_YEAR-1); j_child++)
	npop_children += patch[p].child_population[0].n_child[j_child] + patch[p].child_population[1].n_child[j_child] + patch[p].child_population[2].n_child[j_child];


    double npop_model = npop_children+npop_adult;
    
    printf("In find_pop_scale, npop_model=%lf\n",npop_model);

    double scale = real_population/npop_model;

    return scale;
}




/* Function counts number of people aged 15+ at a given time, to allow rescaling of population proportions to keep total numbers fixed (e.g. number of HIV tests). */
double count_15plus_scale(patch_struct *patch, int p){
    
    double npop_adult = 0;
    int g,aa,ai;
    
    for(g = 0; g < N_GENDER; g++){
        for(aa = (15-AGE_ADULT); aa < (MAX_AGE-AGE_ADULT); aa++){
            ai = aa + patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index;
            while (ai>(MAX_AGE-AGE_ADULT-1)){
                ai = ai - (MAX_AGE-AGE_ADULT);
            }
            npop_adult += patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
        }
        npop_adult += patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
    }
    return npop_adult;
}



void count_adult_pop_by_gender(patch_struct *patch, int p, double *N_m, double *N_f){
    
    int aa,ai;
    /* Set counters to zero: */
    *N_m = 0;
    *N_f = 0;
    
    for(aa = 0; aa < (MAX_AGE-AGE_ADULT); aa++){
	/* First count for men: */
	ai = aa + patch[p].age_list->age_list_by_gender[MALE]->youngest_age_group_index;
	while (ai>(MAX_AGE-AGE_ADULT-1)){
	    ai = ai - (MAX_AGE-AGE_ADULT);
	}
	*N_m += patch[p].age_list->age_list_by_gender[MALE]->number_per_age_group[ai];

	/* Now for women: */
	ai = aa + patch[p].age_list->age_list_by_gender[FEMALE]->youngest_age_group_index;
	while (ai>(MAX_AGE-AGE_ADULT-1)){
	    ai = ai - (MAX_AGE-AGE_ADULT);
	}
	*N_f += patch[p].age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai];

    }
    /* Add in oldest age group: */
    N_m += patch[p].age_list->age_list_by_gender[MALE]->number_oldest_age_group;
    N_f += patch[p].age_list->age_list_by_gender[FEMALE]->number_oldest_age_group;
}


void MIHPSA_determine_PrEP_scenario(double t, patch_struct *patch, int p){
    /* Until 2023, use default oral PrEP coverage: */
    if(t<2023.0){
	sweep_pop_for_PrEP_per_timestep_given_barriers(t, patch, p);
    }
    else{
	if(patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CAPPEDORALPREP){
	    /* Run a version of the code that fixes PrEP coverage to be 37,144 AGYW 15-24 at risk (FSW or non-regular partner) from 2023 onwards. */
	    if(t==2024)
		printf("running MIHPSA scenario where oral PrEP is available for 15-24 at risk women, but capped, from 2023 onwards\n");
	    MIHPSA_sweep_pop_for_PrEP_per_timestep(t, patch, p);
	}

	else if((patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_CURRENTORALPREP)){
	    sweep_pop_for_PrEP_per_timestep_given_barriers(t, patch, p);
	}
	else if((patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023==MIHPSA_NOORALPREP)){
	    if(t==2023.0)
		printf("MIHPSA minimal or essential scenario without oral PrEP\n");
	}else{
	    if(t>2023){
		printf("Unknown MIHPSA scenario %i - exiting\n",MIHPSA_SCENARIO_FLAG);
		exit(1);
	    }
	}
    }
}




/*  Removal of CUPP activities increases multiple partners (by ~3%). To match other (compartmental) models we assume that this is immediate. However for simplicity we do not change existing partnerships. */
void mihpsa_minimalscenario_increasemulitplepartners(double t, patch_struct *patch){
    /* In minimal scenario for MIHPSA we switch off CUPP + SBCC from 2023 onwards: */
    if(t==2023){
	printf("Modifying number of partners for MIHPSA minimal scenario\n");
	//for(int r_temp=MEDIUM; r_temp<=HIGH; r_temp++)
	for(int r_temp=LOW; r_temp<=HIGH; r_temp++)
	    patch[0].param->relative_number_partnerships_per_risk[r_temp] = patch[0].param->relative_number_partnerships_per_risk[r_temp]*patch[0].param->MIHPSA_params.increase_in_npartners_without_CUPP;
    }
    
}




/* Version of prevention_cascade_intervention_condom() that *reduces* condom use when moving to the minimal scenarion (instead of increasing it in response to an intervention)
   This function decreases the probability of using a condom for existing partnerhips.
   Function loops through the list of alive people via age_list, looking at partnerships for each person - update condom use if the id of the partner is < the id of that person. 
   Note we need 2 loops as we can't guarantee that the age of the second person is less than that of the first (it is for new individuals, but not at the start of the simulation). */
void MIHPSA_sweep_through_condomusepartnerships_reduce_forcondomuse_minimalscenario(patch_struct *patch, int p, double t){
    int aa, ai, g, i, i_partners;
    int number_per_age_group;

    // Pointer to the individual (so no need to malloc as pointing at pre-allocated memory) 
    individual *indiv;
    individual *partner;
    long id;
    int n_partners;
    double duration_partnership;

    printf("Reducing condom use in exisiing partnerships for MIHPSA minimal scenario\n");

    
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

		    /* Only update if they're currently consistently using condoms: */
		    if (indiv->cascade_barriers.use_condom_in_this_partnership[i_partners]==USECOND){
			partner = indiv->partner_pairs[i_partners]->ptr[1-g];
			if (id< partner->id){
			    duration_partnership = indiv->partner_pairs[i_partners]->duration_in_time_steps *TIME_STEP;
			    MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse(indiv, partner, duration_partnership, patch[p].param, t);
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

		/* Only update if they're currently consistently using condoms: */
		if (indiv->cascade_barriers.use_condom_in_this_partnership[i_partners]==USECOND){
		    partner = indiv->partner_pairs[i_partners]->ptr[1-g];
		    if (id< partner->id){
			duration_partnership = indiv->partner_pairs[i_partners]->duration_in_time_steps *TIME_STEP;
			MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse(indiv, partner, duration_partnership, patch[p].param, t);
		    }		    

		}
	    }
	}

    }
}


/* Function called for MIHPSA minimal scenario, potentially changing condom use in existing partnerships (*stopping condom use in partnership where condoms were used before*).
   Function is a version of update_partnership_condom_use_in_response_to_intervention() which stops (rather than starts) condom use. */
void MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse(individual *indiv1, individual *indiv2, double duration_partnership, parameters *param, double t){


    


    
	
    double x;  /* RV to see if condom is used or not. */

    double change_in_p_use_condom; /* This is the change in probability. */
    double new_cond_propensity_partner1;
    double new_cond_propensity_partner2;
    double original_cond_propensity_partner1;
    double original_cond_propensity_partner2;
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
	original_cond_propensity_partner1 = param->barrier_params.p_use_cond_casual[index_HIV_prevention_cascade_condom(ageF,FEMALE)];
	original_cond_propensity_partner2 = param->barrier_params.p_use_cond_casual[index_HIV_prevention_cascade_condom(ageM,MALE)];
	new_cond_propensity_partner1 = MIHPSA_new_condomuse_when_CUPP_switchedoff(original_cond_propensity_partner1,param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_nonreg);
	new_cond_propensity_partner2 = MIHPSA_new_condomuse_when_CUPP_switchedoff(original_cond_propensity_partner2,param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_nonreg);
    }
    /* Long-term partnership: */
    else{
	original_cond_propensity_partner1 = param->barrier_params.p_use_cond_LT[index_HIV_prevention_cascade_condom(ageF,FEMALE)];
	original_cond_propensity_partner2 = param->barrier_params.p_use_cond_LT[index_HIV_prevention_cascade_condom(ageM,MALE)];
	new_cond_propensity_partner1 = MIHPSA_new_condomuse_when_CUPP_switchedoff(original_cond_propensity_partner1,param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_LT);
	new_cond_propensity_partner2 = MIHPSA_new_condomuse_when_CUPP_switchedoff(original_cond_propensity_partner2,param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_LT);
    }
    
    /* Calculate the new and original probabilities of using a condom in this partnership given the above propensities, and find the difference. */
    //change_in_p_use_condom =  sqrt(original_cond_propensity_partner1*original_cond_propensity_partner2) - sqrt(new_cond_propensity_partner1*new_cond_propensity_partner2);
    change_in_p_use_condom =  1.0 - sqrt(new_cond_propensity_partner1*new_cond_propensity_partner2) / sqrt(original_cond_propensity_partner1*original_cond_propensity_partner2);
    
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
		printf("Error - run out of partners for partner 1 in MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse(). Exiting\n");
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
		printf("Error - run out of partners for partner 2 in MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse(). Exiting\n");
		printf("%li %li %li\n",indiv1->id,check_id,indiv2->id);
		exit(1);
	    }
	}

	/* Check that condom use matches: */
	if(indiv1->cascade_barriers.use_condom_in_this_partnership[i_partner1]!=USECOND || indiv2->cascade_barriers.use_condom_in_this_partnership[i_partner2]!=USECOND){
	    printf("Error in MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse() - condom use in partners 1+2 not equal to zero prior to intervention. Exiting\n");
	    exit(1);
	}

	/* Now set condom use in partnership to be 'don't use condom': */
	indiv1->cascade_barriers.use_condom_in_this_partnership[i_partner1] = NOCOND;
	indiv2->cascade_barriers.use_condom_in_this_partnership[i_partner2] = NOCOND;
    }

}


double MIHPSA_new_condomuse_when_CUPP_switchedoff(double original_condomuse, double decreasein_nonuse_with_CUPPon){
    return (1 - (1-original_condomuse)/decreasein_nonuse_with_CUPPon);
}


void initialise_MIHPSA_flags(patch_struct *patch, int p){
    if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_CUPP ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_AGYW_ORALPREP)
	patch[p].param->MIHPSA_params.FLAGS.remove_SBCC=1;
    else if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_SBCC ||
	    MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO ||
	    MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO_PLUS_AGYW_ORALPREP ||
	    MIHPSA_SCENARIO_FLAG==MIHPSA_STATUSQUO_SCENARIO)
	patch[p].param->MIHPSA_params.FLAGS.remove_SBCC=0;
    else{
	printf("Error - unknown MIHPSA scenario in initialise_MIHPSA_flags() for SBCC - exiting\n");
	fflush(stdout);
	exit(1);
    }
	

    if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_SBCC ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_AGYW_ORALPREP)
	patch[p].param->MIHPSA_params.FLAGS.remove_CUPP=1;
    else if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_CUPP ||
	    MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO ||
	    MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO_PLUS_AGYW_ORALPREP ||
	    MIHPSA_SCENARIO_FLAG==MIHPSA_STATUSQUO_SCENARIO)
	patch[p].param->MIHPSA_params.FLAGS.remove_CUPP=0;
    else{
	printf("Error - unknown MIHPSA scenario in initialise_MIHPSA_flags() for CUPP - exiting\n");
	fflush(stdout);
	exit(1);
    }
    
    if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_SBCC ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_CUPP ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_AGYW_ORALPREP ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO_PLUS_AGYW_ORALPREP
       )
	patch[p].param->MIHPSA_params.FLAGS.remove_VMMC_from2023 = 1;
    else if(MIHPSA_SCENARIO_FLAG==MIHPSA_STATUSQUO_SCENARIO)
	patch[p].param->MIHPSA_params.FLAGS.remove_VMMC_from2023 = 0;
    else{
	printf("Error - unknown MIHPSA scenario in initialise_MIHPSA_flags() for VMMC - exiting\n");
	fflush(stdout);
	exit(1);
    }


    if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_SBCC ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_CUPP ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_AGYW_ORALPREP)
	patch[p].param->MIHPSA_params.FLAGS.only_ANC_PD_symptomatic_testing_from2023 = 1;
    else if(MIHPSA_SCENARIO_FLAG==MIHPSA_STATUSQUO_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO ||
       MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO_PLUS_AGYW_ORALPREP)
	patch[p].param->MIHPSA_params.FLAGS.only_ANC_PD_symptomatic_testing_from2023 = 0;
    else{
	printf("Error - unknown MIHPSA scenario in initialise_MIHPSA_flags() for HIV testing - exiting\n");
	fflush(stdout);
	exit(1);
    }
    
    /* Under essential, and all minimal, scenarios no oral PrEP from 2023 (unless specified): */
    if(MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO || MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_SBCC || MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_CUPP || MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO)
	patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023 = MIHPSA_NOORALPREP;
    /* Under MIHPSA_ESSENTIAL_SCENARIO_PLUS_AGYW_ORALPREP scenario, oral PrEP coverage is fixed to be 37,144 AGYW 15-24 at risk (FSW or non-regular partner) from 2023 onwards. */
    else if(MIHPSA_SCENARIO_FLAG==MIHPSA_ESSENTIAL_SCENARIO_PLUS_AGYW_ORALPREP || MIHPSA_SCENARIO_FLAG==MIHPSA_MINIMAL_SCENARIO_PLUS_AGYW_ORALPREP)
	patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023 = MIHPSA_CAPPEDORALPREP;
    else if(MIHPSA_SCENARIO_FLAG==MIHPSA_STATUSQUO_SCENARIO)
	patch[p].param->MIHPSA_params.FLAGS.MIHPSA_oralPrEP_from2023 = MIHPSA_CURRENTORALPREP;
    else{
	printf("Error - unknown MIHPSA scenario in initialise_MIHPSA_flags() for oral PrEP - exiting\n");
	fflush(stdout);
	exit(1);
    }
}

void fix_MIHPSA_parameters(patch_struct *patch, int p){
    printf("**Fixing MIHPSA parameters in 2023\n");
    //double x;

    //x = gsl_rng_uniform (rng);

    /* See Dropbox/projects/MIHPSA_Zimabwe2021/Phase2/Outputs_Dec2023/PopART-IBM_modelling_minimal_scenario.pptx for more details on parameters below. */
    
    if(patch[p].param->MIHPSA_params.FLAGS.remove_CUPP==1){
	/* Mass media 0-6% change in number of people with multiple partners. */
	patch[p].param->MIHPSA_params.increase_in_npartners_without_CUPP = 1.07;

	/* CUPP Mass media 17% change in condom non-use for stable partnerships. */
	patch[p].param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_LT = 0.83;
	/* CUPP Mass media 3-20% change in condom non-use for multiple partnerships. We assume that most "multiple" partnerships are non-regular. */
	patch[p].param->MIHPSA_params.decreasein_condomnonuse_dueto_CUPPon_nonreg = 0.885;
    }

    if(patch[p].param->MIHPSA_params.FLAGS.remove_SBCC==1){

	/* SBCC (Sista2Sista and DREAMS) give 9840+22062 HIV tests respectively in AGYW 10-24. Assume all tests are in 14-24. In 2022 PopART_IBM has approximately 600,000 tests (scaled to national pop) in AGYW 14-24.
	   Reduction of (9840+22062)/600000 = 5.3% of HIV tests in AGYW 14-24 annually due to SBCC. */
	patch[p].param->MIHPSA_params.change_in_AGYW14to24_HIVtesting_dueto_SBCC = 0.947;
    }

}


