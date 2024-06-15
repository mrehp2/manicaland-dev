/* Outputs for MIHPSA Zimbabwe project (October 2021). 
 */

#include "mihpsa_output.h"

/* Functions: 
int get_MIHPSA_condom_use_last_act(individual *indiv)
void store_annual_outputs_MIHPSA(patch_struct *patch, int p, output_struct *output, double t)
void write_MIHPSA_outputs(file_struct *file_data_store, output_struct *output, int p)

*/

/* Function to approximate 'condom use at last sex act'. */
int get_MIHPSA_condom_use_last_act(individual *indiv){

    int i_partners;
    int n_partners_use_cond = 0;
    /* Check this person's partnerships: */
    for (i_partners=0; i_partners<(indiv->n_partners); i_partners++)
	n_partners_use_cond += indiv->cascade_barriers.use_condom_in_this_partnership[i_partners];

    double p_use_cond = n_partners_use_cond/(1.0*indiv->n_partners);
    double x = gsl_rng_uniform (rng);
    if (x<p_use_cond)
	return 1;
    else
	return 0;
}

void store_annual_outputs_MIHPSA(patch_struct *patch, int p, output_struct *output, double t){
    /* Stores annual data (HIV prevalence, ART coverage, HIV incidence, new infections, number on ART, AIDS deaths, total deaths, number of HIV tests, test yield, % circ (either VMMC or TMC), viral suppression, condom use at last sex)
    for a single patch (patch `p`) in the output structure `output`.  
    
    This function populates a range of string variables (e.g. `temp_string`) with output summaries
    from the different patches.  These strings are then added to the structure `output` which 
    is used within functions which write to file.  Output is only generated for a single year *on July 1*.  

    */
    
    int age,g;
    long n_id;
    int i_partner; /* Index for serodiscordant partner. */
    int art; /* ART status. */
    int art_partner; /* ART status of (serodiscordant) partner. */

    //int partnership_duration; /* Length of partnership (in timesteps). Proxy for casual partnership. */
    
    individual *indiv; /* Pointer used to make code more readable - points to already allocated memory so no need to malloc. */

    long npop_bysex_15to49[N_GENDER]={0,0}; /* Population aged 15-49. */
    long npop_bysex_younger[N_GENDER]={0,0}; /* Population aged (15-24F, 15-29M - Manicaland), (15-24M+F MIHPSA). */
    long npop_bysex_older[N_GENDER]={0,0}; /* Population aged (25-54F, 30-54M Manicaland), (25-49 MIHPSA). */
    long npop_bysex_15plus[N_GENDER]={0,0}; /* Population aged 15+. */




    long npositive_bysex_15to49[N_GENDER]={0,0}; /* No. of HIV+ aged 15-49. */
    long npositive_bysex_younger[N_GENDER]={0,0}; /* No. of HIV+ in younger group. */
    long npositive_bysex_older[N_GENDER]={0,0}; /* No. of HIV+ in older group. */
    long npositive_bysex_15plus[N_GENDER]={0,0}; /* Number of HIV+ aged 15+. */


    
    long naware_bysex_younger[N_GENDER]={0,0}; 
    long naware_bysex_older[N_GENDER]={0,0}; 
    long naware_bysex_15plus[N_GENDER]={0,0}; /* Number of HIV+ diagnosed aged 15+. */


    long nonART_bysex_younger[N_GENDER]={0,0}; 
    long nonART_bysex_older[N_GENDER]={0,0}; 

    long N_VS_bysex_younger[N_GENDER]={0,0}; 
    long N_VS_bysex_older[N_GENDER]={0,0}; 
    
    long nARTexperienced_bysex_15plus[N_GENDER]={0,0}; 
    long nARTexperienced_bysex_younger[N_GENDER]={0,0}; 
    long nARTexperienced_bysex_older[N_GENDER]={0,0}; 

    /* Number of people 15+ years old living with HIV, not on treatment, by CD4 category: */
    long n_notonART_byCD4_15plus[NCD4]={0,0,0,0};


    /* N people 15+ living with HIV, asymptomatic, undiagnosed
       N people 15+ living with HIV, asymptomatic, diagnosed not ART
       N people 15+ living with HIV, asymptomatic, diagnosed on ART
       N people 15+ living with HIV, symptomatic, AIDS
       Note - we assume "N PLHIV 15+, symptomatic, AIDS"=0 - ie CD4<200 means symptomatic.
    */
    long n_hivasympt_undiag_15plus = 0;
    long n_hivasympt_diag_notART = 0;
    long n_hivasympt_diag_ART = 0;
    long n_hivsympt_AIDS = 0;

    /* Number 15+ years old who ever had sex (i.e. sexually active). */
    long n_eversex_15plus[N_GENDER] = {0,0};
    long N_women_sexuallyactive_15to24 = 0;
    
    long n_usedcondomlastact_15plus[N_GENDER] = {0,0};
    long N_women_usecondomlastact_15to24 = 0;
    /* Counters to validate MIHPSA minimal scenario (reduction in condom use):
       “Stable couples” would be assumed to be long-term couples (lasting >1 year)
       “People with multiple partners” - Condom use is not determined by having multiple partners – so planning to use non—regular partnerships (lasting <1 year) instead.
 */
    long N_longtermpartnerships = 0;
    long N_longtermpartnerships_condomused = 0;
    long N_nonregularpartnerships = 0;
    long N_nonregularpartnerships_condomused = 0;
    long N_concurrentpartnerships_condomused = 0;
    long N_concurrentpartnerships = 0;

    
    /* Counts women eligible for PrEP (MIHPSA definition=with Non-regular sexual partner(s) or from key populations. I'm using partnership < 1 year = non-regular as this is where condom use changes). */
    long n_women_at_elevatedrisk_15to24 = 0;
    int in_primarypop; // Boolean for the person is in the primary population.
    /* Counts those eligible women who are on PrEP (adherent or semiadherent). */
    long n_women_at_elevatedrisk_andonoralPrEP_15to24 = 0;

    long n_women_used_oralPrEP_lastQ_15to24 = 0;
    long n_women_active_oralPrEP_lastQ_15to24 = 0;
    long n_women_ever_oralPrEP_15to24 = 0;
    long n_women_used_dapivirinering_lastQ_15to24 = 0;
    long n_women_active_dapivirinering_lastQ_15to24 = 0;
    long n_women_used_injectablePrEP_lastQ_15to24 = 0;
    long n_women_active_injectablePrEP_lastQ_15to24 = 0;

    /* Counters for women with SD partners: */
    long n_women_used_oralPrEP_lastQ_15plus_sdpartner = 0;
    long n_women_active_oralPrEP_lastQ_15plus_sdpartner = 0;
    long n_women_ever_oralPrEP_15plus_sdpartner = 0;
    long n_women_used_dapivirinering_lastQ_15plus_sdpartner = 0;
    long n_women_active_dapivirinering_lastQ_15plus_sdpartner = 0;
    long n_women_used_injectablePrEP_lastQ_15plus_sdpartner = 0;
    long n_women_active_injectablePrEP_lastQ_15plus_sdpartner = 0;
    
    int UPPER_AGE_LIM_YOUNG[N_GENDER];
    int UPPER_AGE_LIM_OLD[N_GENDER];
    
    if(MIHPSA_MODULE==1){
	UPPER_AGE_LIM_YOUNG[MALE] = 24; 
	UPPER_AGE_LIM_YOUNG[FEMALE] = 24; 
	UPPER_AGE_LIM_OLD[MALE] = 49;
	UPPER_AGE_LIM_OLD[FEMALE] = 49;
    }
    else{
	UPPER_AGE_LIM_YOUNG[MALE] = 29; 
	UPPER_AGE_LIM_YOUNG[FEMALE] = 24; 
	UPPER_AGE_LIM_OLD[MALE] = 54;
	UPPER_AGE_LIM_OLD[FEMALE] = 54;
    }
    long N_men_MC_15to49 = 0; /* Number of men aged 15-49 circumcised (VMMC or TMC). */

    
    long N_onART_bysex_15plus[N_GENDER]={0,0}; /* Number on ART aged 15+. */
    long N_VS_bysex_15plus[N_GENDER]={0,0}; /* Number virally suppressed aged 15+. */


    long npop_children_under15 = 0;
    long npositive_children_under15 = 0;
    long naware_children_under15 = 0;


    /* New outputs 28/04/2023:
       Number of HIV-negative adults/females 15+ years old in a sero-discordant relationship (whom partner is not on ART).  */
    long N_HIVneg_15plus_in_SD_partnership[N_GENDER]={0,0}; 
    long N_HIVneg_15plus_in_SD_partnership_noART[N_GENDER]={0,0}; 

    /* Counters for multiple partners and concurrent partners: */
    long n_concurrent_partnerships_15to49 = 0;
    long n_multiple_partnerships_lastyear_15to49 = 0;
    int temp_npartners_thisyear;



    int j_child;
    for(j_child=0; j_child<((AGE_ADULT+1)*N_TIME_STEP_PER_YEAR-1); j_child++){
	npop_children_under15 += patch[p].child_population[0].n_child[j_child] + patch[p].child_population[1].n_child[j_child] + patch[p].child_population[2].n_child[j_child];
	npositive_children_under15 += patch[p].child_population[1].n_child[j_child] + patch[p].child_population[2].n_child[j_child];
	naware_children_under15 += patch[p].child_population[2].n_child[j_child];
    }
    //int current_cd4_guidelines = art_cd4_eligibility_group(patch[p].param, t);


    /* Temporary stores of data from current year. */
    char temp_string[10000];
    char temp_string2[10000];
    /* Temporary store for single variable which gets strcat'd into temp_string. */

    /* Loop through the alive population. */
    for (n_id = 0; n_id < patch[p].id_counter; n_id++){
	indiv = &patch[p].individual_population[n_id];
        /* Check that the person is not dead: */
        if (indiv->cd4!=DEAD){

	    age = (int) floor(t - indiv->DoB);
	    g = indiv->gender;

	    /* 15-49 outputs: */
	    if(age>=15 && age<=49){
		npop_bysex_15to49[g]++;
		if(indiv->HIV_status>UNINFECTED){
		    npositive_bysex_15to49[g]++;
		}
		/* Now if circumcised (including healing): */
		if (g==MALE){
		    if((indiv->circ == VMMC) || (indiv->circ == VMMC_HEALING) || (indiv->circ == TRADITIONAL_MC))
			N_men_MC_15to49++;
		}
		if(indiv->n_partners>1)
		    n_concurrent_partnerships_15to49++;
		
		/* n_partnersminusoneyear counts the number of partners that someone has had at the start of the current year. Thus n_partnersminusoneyear + n_lifetime_partners-n_lifetimeminusoneyear_partners gives the number of partners in the most recent years (existing + new)*/
		temp_npartners_thisyear = indiv->n_partnersminusoneyear + indiv->n_lifetime_partners - indiv->n_lifetimeminusoneyear_partners;

		if(temp_npartners_thisyear>1)
		    n_multiple_partnerships_lastyear_15to49++;
	    }
	    
	    /* Specialist outputs: */
	    if(age>=15 && age<=UPPER_AGE_LIM_YOUNG[g]){
		npop_bysex_younger[g]++;
	    }
	    else if(age>UPPER_AGE_LIM_YOUNG[g] && age<=UPPER_AGE_LIM_OLD[g]){
		npop_bysex_older[g]++;
	    }
	    if(indiv->HIV_status>UNINFECTED){
		if(age>=15 && age<=UPPER_AGE_LIM_YOUNG[g]){
		    npositive_bysex_younger[g]++;
		}
		else if(age>UPPER_AGE_LIM_YOUNG[g] && age<=UPPER_AGE_LIM_OLD[g]){
		    npositive_bysex_older[g]++;
		}
	    }

    	    
	    /* Now outputs aged 15+ */
	    if(age>=15){
		npop_bysex_15plus[g]++;
		if(indiv->n_lifetime_partners>0){
		    n_eversex_15plus[g]++;
		    n_usedcondomlastact_15plus[g] += get_MIHPSA_condom_use_last_act(indiv);
		}
		if(indiv->HIV_status>UNINFECTED){
		    npositive_bysex_15plus[g]++;
		    art = indiv->ART_status;
		    /* Aware of status: */
		    if((art==ARTNAIVE) || (art==EARLYART) || (art==LTART_VS) || (art==LTART_VU) || (art==ARTDROPOUT) || (art==CASCADEDROPOUT)){
			if(age>=15 && age<=UPPER_AGE_LIM_YOUNG[g]){
			    naware_bysex_younger[g]++;
			}
			else if(age>UPPER_AGE_LIM_YOUNG[g] && age<=UPPER_AGE_LIM_OLD[g]){	
			    naware_bysex_older[g]++;
			}
			naware_bysex_15plus[g]++;

			/* ART experienced: */
			if((art==EARLYART) || (art==LTART_VS) || (art==LTART_VU) || (art==ARTDROPOUT) || (art==CASCADEDROPOUT)){
			    if(age>=15 && age<=UPPER_AGE_LIM_YOUNG[g]){
				nARTexperienced_bysex_younger[g]++;
			    }
			    else if(age>UPPER_AGE_LIM_YOUNG[g] && age<=UPPER_AGE_LIM_OLD[g]){	
				nARTexperienced_bysex_older[g]++;
			    }
			    nARTexperienced_bysex_15plus[g]++;
			}
			/* On ART: */
			if((art==EARLYART) || (art==LTART_VS) || (art==LTART_VU)){
			    if(age>=15 && age<=UPPER_AGE_LIM_YOUNG[g]){
				nonART_bysex_younger[g]++;
				/* Now virally suppressed: */
				if(art==LTART_VS)
				    N_VS_bysex_younger[g]++;
			    }
			    else if(age>UPPER_AGE_LIM_YOUNG[g] && age<=UPPER_AGE_LIM_OLD[g]){	
				nonART_bysex_older[g]++;
				/* Now virally suppressed: */
				if(art==LTART_VS)
				    N_VS_bysex_older[g]++;
			    }
			    N_onART_bysex_15plus[g]++;
			    /* Now virally suppressed: */
			    if(art==LTART_VS)
			        N_VS_bysex_15plus[g]++;
			}
		    }

		    /* Not on treatment: */
		    if((art==ARTNEG) || (art==ARTNAIVE) || (art==ARTDROPOUT) || (art==CASCADEDROPOUT))
			/* Number of people 15+ years old living with HIV, not on treatment by CD4: */
			n_notonART_byCD4_15plus[indiv->cd4]++;

		    /* Number of PLHIV 15+, asymptomatic, undiagnosed (cd4=3 is CD4<200). */
		    if(indiv->cd4<3){
			if(art==ARTNEG)
			    n_hivasympt_undiag_15plus++;
			/* Number of PLHIV 15+, asymptomatic, diagnosed not on ART. */
			else if((art==ARTNAIVE) || (art==ARTDROPOUT) || (art==CASCADEDROPOUT))
			    n_hivasympt_diag_notART++;
			/* Number of PLHIV 15+, asymptomatic, diagnosed not on ART. */
			else if((art==EARLYART) || (art==LTART_VS) || (art==LTART_VU))
			    n_hivasympt_diag_ART++;
		    }else{
			/* Number of PLHIV 15+, symptomatic, AIDS. */
			n_hivsympt_AIDS++;
		    }
		    
		}
		/* HIV- people 15+: */
		else{
		    if(indiv->n_HIVpos_partners>0){
			N_HIVneg_15plus_in_SD_partnership[g]++;
			for(i_partner=0; i_partner<(indiv->n_HIVpos_partners); i_partner++){
			    art_partner = indiv->partner_pairs_HIVpos[i_partner]->ptr[1-g]->ART_status;
			    if(art_partner==ARTNEG || art_partner==ARTNAIVE || art_partner==ARTDROPOUT || art_partner==CASCADEDROPOUT){
				N_HIVneg_15plus_in_SD_partnership_noART[g]++;
				break; /* Exit for loop as found non-ART. */
			    }

			}
		    }
		}
	    }

	    /* Start getting outputs for kids <15 - note that we need to add in extras from the child part of the code: */
	    else{
		npop_children_under15++;    
		if(indiv->HIV_status>UNINFECTED){
		    npositive_children_under15++;
		    art = indiv->ART_status;
		    /* Aware of status: */
		    if((art==ARTNAIVE) || (art==EARLYART) || (art==LTART_VS) || (art==LTART_VU) || (art==ARTDROPOUT) || (art==CASCADEDROPOUT)){
    			naware_children_under15++;

		    }
		}
	    }



	    if(g==FEMALE && age>=15 && age<=24){
		/* Count number in "primary (or elevated risk)" pop: */
		if(indiv->HIV_status==UNINFECTED){
		    in_primarypop = 0;
		    /* Primary population = at least 1 non-reg partner. */
		    for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){
			if((indiv->partner_pairs[i_partner]->duration_in_time_steps<N_TIME_STEP_PER_YEAR)){
			    in_primarypop = 1;
			    break;
			}
		    }
		    /* Need to make sure at least 1 partner (otherwise the indiv->partner_pairs[0] causes a segmentation fault). */
		    if(in_primarypop==1){
			n_women_at_elevatedrisk_15to24++;
			if((indiv->PrEP_cascade_status==ONPREP_ADHERENT) || (indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT)){
			    n_women_at_elevatedrisk_andonoralPrEP_15to24++;
			}
		    }
		}

		
		/* If they are currently on PrEP, or stopped PrEP in the last quarter (note - we first have to test if they have ever started PrEP): */
		if(indiv->date_most_recent_oralPrEP_initiation<=t){
		    /* Have ever initated oral PrEP: */
		    n_women_ever_oralPrEP_15to24++;
		    if((indiv->PrEP_cascade_status==ONPREP_ADHERENT) || (indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT) || (t-(indiv->date_most_recent_oralPrEP_stoppage)<=0.25))
			n_women_used_oralPrEP_lastQ_15to24++;
		    /* If they are have been on PrEP throughout the last quarter: */
		    if(((indiv->PrEP_cascade_status==ONPREP_ADHERENT) || (indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT)) && (t-(indiv->date_most_recent_oralPrEP_initiation)>=0.25))
			n_women_active_oralPrEP_lastQ_15to24++;
		}
	    
		
		/* /\* Loop through all partners. *\/ */
		/* for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){ */
		/*     partnership_duration = indiv->partner_pairs[i_partner]->duration_in_time_steps; */
		/*     if(partnership_duration<N_TIME_STEP_PER_YEAR){ */
		/* 	n_women_at_elevatedrisk_15to24++; */
		/* 	if((indiv->PrEP_cascade_status==ONPREP_ADHERENT) || (indiv->PrEP_cascade_status==ONPREP_SEMIADHERENT)){ */
		/* 	    n_women_at_elevatedrisk_andonoralPrEP_15to24++; */
		/* 	} */
		/* 	break; /\* Exit for loop as at elevated risk. *\/ */
		/*     } */
		/* } */
		
		if(indiv->n_lifetime_partners>0){
		   N_women_sexuallyactive_15to24++;
		   /* Function that approximates a woman's condom use at last act based on partners and condom use at present, and returns 1 if condom was used, 0 if not: */
		   N_women_usecondomlastact_15to24 += get_MIHPSA_condom_use_last_act(indiv);
		}
	    }


	    /* Get output to validate MIHPSA minimal scenario regarding reduction in condom use. */
	    for(i_partner=0; i_partner<(indiv->n_partners); i_partner++){
		if((indiv->partner_pairs[i_partner]->duration_in_time_steps<N_TIME_STEP_PER_YEAR)){
		    N_nonregularpartnerships++;
		    N_nonregularpartnerships_condomused += indiv->cascade_barriers.use_condom_in_this_partnership[i_partner];
		}else{
		    N_longtermpartnerships++;
		    N_longtermpartnerships_condomused += indiv->cascade_barriers.use_condom_in_this_partnership[i_partner];
		}
		if((indiv->n_partners)>1){
		    N_concurrentpartnerships++;
		    N_concurrentpartnerships_condomused += indiv->cascade_barriers.use_condom_in_this_partnership[i_partner];
		}
	    }
	    
	}
    }
    		    


    sprintf(temp_string, "%i,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,",
	    (int) floor(t),npop_bysex_15to49[MALE],npop_bysex_15to49[FEMALE],
	    npop_bysex_younger[MALE],npop_bysex_younger[FEMALE],
	    npop_bysex_older[MALE],npop_bysex_older[FEMALE],
	    npositive_bysex_15to49[MALE],npositive_bysex_15to49[FEMALE],
	    npositive_bysex_younger[MALE],npositive_bysex_younger[FEMALE],
	    npositive_bysex_older[MALE],npositive_bysex_older[FEMALE],
	    N_men_MC_15to49);



    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,%li,",N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24);
	strcat(temp_string, temp_string2);
    }
	
    sprintf(temp_string2, "%li,%li,",npop_bysex_15plus[MALE],npop_bysex_15plus[FEMALE]);
    strcat(temp_string, temp_string2);
 


    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,",npop_children_under15);
	strcat(temp_string, temp_string2);
    }

    sprintf(temp_string2, "%li,%li,",npositive_bysex_15plus[MALE],npositive_bysex_15plus[FEMALE]);
    strcat(temp_string, temp_string2);

    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,",npositive_children_under15);
	strcat(temp_string, temp_string2);
    }

    sprintf(temp_string2, "%li,%li,",naware_bysex_15plus[MALE],naware_bysex_15plus[FEMALE]);
    strcat(temp_string, temp_string2);

    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,",naware_children_under15);
	strcat(temp_string, temp_string2);
    }
    else{
	sprintf(temp_string2, "%li,%li,%li,%li,",
		naware_bysex_younger[MALE],naware_bysex_younger[FEMALE],
		naware_bysex_older[MALE],naware_bysex_older[FEMALE]);
	strcat(temp_string, temp_string2);
    }


    sprintf(temp_string2, "%li,%li,%li,%li,",
	    N_onART_bysex_15plus[MALE],N_onART_bysex_15plus[FEMALE],
	    N_VS_bysex_15plus[MALE],N_VS_bysex_15plus[FEMALE]);
    strcat(temp_string, temp_string2);


    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,%li,",patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_20_59[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_20_59[FEMALE]);
	strcat(temp_string, temp_string2);
    }
    else{
	sprintf(temp_string2, "%li,%li,%li,%li,",
		nonART_bysex_younger[MALE],nonART_bysex_younger[FEMALE],
		nonART_bysex_older[MALE],nonART_bysex_older[FEMALE]);
	strcat(temp_string, temp_string2);
    }

    sprintf(temp_string2, "%li,%li,",
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_15plus[FEMALE]);
    strcat(temp_string, temp_string2);



    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,",patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_children_under15);
	strcat(temp_string, temp_string2);
    }
    

    sprintf(temp_string2, "%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,",
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15plus[FEMALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15to24F,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15to24[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_25to49[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15to24[FEMALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_25to49[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus[MALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15to24F,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_VMMC_15to49,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_ARTinitiations_15plus,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_ARTreinitiations_15plus,
	    nARTexperienced_bysex_15plus[MALE],nARTexperienced_bysex_15plus[FEMALE],
	    nARTexperienced_bysex_younger[MALE],nARTexperienced_bysex_younger[FEMALE],
	    nARTexperienced_bysex_older[MALE],nARTexperienced_bysex_older[FEMALE],
	    n_women_at_elevatedrisk_15to24,n_women_at_elevatedrisk_andonoralPrEP_15to24,
	    N_VS_bysex_younger[MALE],N_VS_bysex_younger[FEMALE],
	    N_VS_bysex_older[MALE],N_VS_bysex_older[FEMALE],
	    n_women_used_oralPrEP_lastQ_15to24,
	    n_women_active_oralPrEP_lastQ_15to24,
	    n_women_ever_oralPrEP_15to24,
	    n_women_used_dapivirinering_lastQ_15to24,
	    n_women_active_dapivirinering_lastQ_15to24,
	    n_women_used_injectablePrEP_lastQ_15to24,
	    n_women_active_injectablePrEP_lastQ_15to24,
	    n_women_used_oralPrEP_lastQ_15plus_sdpartner,
	    n_women_active_oralPrEP_lastQ_15plus_sdpartner,
	    n_women_ever_oralPrEP_15plus_sdpartner,
	    n_women_used_dapivirinering_lastQ_15plus_sdpartner,
	    n_women_active_dapivirinering_lastQ_15plus_sdpartner,
	    n_women_used_injectablePrEP_lastQ_15plus_sdpartner,
	    n_women_active_injectablePrEP_lastQ_15plus_sdpartner
);
    strcat(temp_string, temp_string2);

    
    
        
    sprintf(temp_string2, "%li,%li,%li,%li,%li,%li,%8.6lf,%8.6lf,%8.6lf,%8.6lf,%8.6lf,%8.6lf,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,",
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15plus[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newbirths,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newbirths_HIVpos,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_15plus[MALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_15plus[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->YLL_15plus[MALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->YLL_15plus[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->YLL_children_under15,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->YLL_15plus_discounted[MALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->YLL_15plus_discounted[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->YLL_children_under15_discounted,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15to24F,
	    n_notonART_byCD4_15plus[0],n_notonART_byCD4_15plus[1],n_notonART_byCD4_15plus[2],n_notonART_byCD4_15plus[3],
	    N_HIVneg_15plus_in_SD_partnership[MALE],N_HIVneg_15plus_in_SD_partnership[FEMALE],N_HIVneg_15plus_in_SD_partnership_noART[MALE],N_HIVneg_15plus_in_SD_partnership_noART[FEMALE],
	    n_eversex_15plus[MALE],n_eversex_15plus[FEMALE],
	    n_usedcondomlastact_15plus[MALE],n_usedcondomlastact_15plus[FEMALE],
	    nonART_bysex_younger[MALE],nonART_bysex_younger[FEMALE],
	    naware_bysex_younger[MALE],naware_bysex_younger[FEMALE]);

    strcat(temp_string, temp_string2);


    sprintf(temp_string2, "%li,%li,%li,%li,%6.4lf,%6.4lf,%6.4lf\n",
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_symptomatic_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_symptomatic_15plus[FEMALE],n_concurrent_partnerships_15to49,n_multiple_partnerships_lastyear_15to49, N_longtermpartnerships_condomused/(N_longtermpartnerships+1e-12), N_nonregularpartnerships_condomused/(N_nonregularpartnerships+1e-12),N_concurrentpartnerships_condomused/(N_concurrentpartnerships+1e-12));
    strcat(temp_string, temp_string2);

    

    

    

/*     sprintf(temp_string, "%i,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li\n", */
/* 	    (int) floor(t), */
/* 	    npop_bysex_15to49[MALE],npop_bysex_15to49[FEMALE], */
/* 	    npop_bysex_younger[MALE],npop_bysex_younger[FEMALE], */
/* 	    npop_bysex_older[MALE],npop_bysex_older[FEMALE], */
/* 	    npositive_bysex_15to49[MALE],npositive_bysex_15to49[FEMALE], */
/* 	    npositive_bysex_younger[MALE],npositive_bysex_younger[FEMALE], */
/* 	    npositive_bysex_older[MALE],npositive_bysex_older[FEMALE], */
/* 	    N_men_MC_15to49, */
/* 	    N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24, */
/* 	    npop_bysex_15plus[MALE],npop_bysex_15plus[FEMALE],npop_children_under15, */
/* 	    npositive_bysex_15plus[MALE],npositive_bysex_15plus[FEMALE],npositive_children_under15, */
/* 	    naware_bysex_15plus[MALE],naware_bysex_15plus[FEMALE],naware_children_under15, */
/* 	    N_onART_bysex_15plus[MALE],N_onART_bysex_15plus[FEMALE], */
/* 	    N_VS_bysex_15plus[MALE],N_VS_bysex_15plus[FEMALE], */
/* 	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_20_59[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_20_59[FEMALE], */
/* patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_15plus[FEMALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_children_under15, */
/* patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15plus[FEMALE], */
/* patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15to24[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_25to49[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15to24[FEMALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_25to49[FEMALE], */
/* 	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus, */
/* 	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_VMMC_15to49);	 */

    

	//strcat(temp_string,"\n");
    
    /* Add the string `temp_string` to the `output` structure (so as to be written to file)*/
    join_strings_with_check(output->MIHPSA_outputs_string[p], 
			    temp_string, MIHPSA_OUTPUT_STRING_LENGTH, 
			    "output->MIHPSA_outputs_string[p] and temp_string in store_annual_outputs_MIHPSA()");
    
    
}


/* Called at the end of a run to write the MIHPSA outputs to file: */
void write_MIHPSA_outputs(file_struct *file_data_store, output_struct *output, int p){

    FILE *MIHPSA_FILE;
    /* Open connection to the patch-specific file where annual outputs are to be written to file */
    MIHPSA_FILE = fopen(file_data_store->filename_MIHPSA_outputs[p], "w");
    
    if(MIHPSA_FILE == NULL){
        printf("Cannot open MIHPSA_output file\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    /* Print the header of the file */
    if(MIHPSA_MODULE==1)
	fprintf(MIHPSA_FILE,"Year,NPop_15to49_male,NPop_15to49_female,NPop_15to24_male,NPop_15to24_female,NPop_25to49_male,NPop_25to49_female,NPos_15to49_male,NPos_15to49_female,NPos_15to24_male,NPos_15to24_female,NPos_25to49_male,NPos_25to49_female,Ncirc_15to49,N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24,Npop_15plus_male,Npop_15plus_female,Npop_children_under15,Npos_15plus_male,Npos_15plus_female,Npos_children_under15,Naware_15plus_male,Naware_15plus_female,Naware_children_under15,NonART_15plus_male,NonART_15plus_female,N_VS_15plus_male,N_VS_15plus_female,N_deaths_20_59_male,N_deaths_20_59_female,N_AIDSdeaths_15plus_male,N_AIDSdeaths_15plus_female,N_AIDSdeaths_children_under15,N_HIVtests_15plus_male,N_HIVtests_15plus_female,N_HIVtests_15to24F,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus_male,N_newHIVdiagnoses_15plus_female,N_newHIVdiagnoses_15to24F,N_VMMC_cumulative_15_49,N_ARTinitiations_15plus,N_ARTreinitiations_15plus,N_ARTexperienced_bysex_15plus_male,N_ARTexperienced_bysex_15plus_female,N_ARTexperienced_bysex_younger_male,N_ARTexperienced_bysex_younger_female,N_ARTexperienced_bysex_older_male,N_ARTexperienced_bysex_older_female,n_women_at_elevatedrisk_15to24,n_women_at_elevatedrisk_andonoralPrEP_15to24,N_VS_bysex_younger_male,N_VS_bysex_younger_female,N_VS_bysex_older_male,N_VS_bysex_older_female,n_women_used_oralPrEP_lastQ_15to24,n_women_active_oralPrEP_lastQ_15to24,n_women_ever_oralPrEP_15to24,n_women_used_dapivirinering_lastQ_15to24,n_women_active_dapivirinering_lastQ_15to24,n_women_used_injectablePrEP_lastQ_15to24,n_women_active_injectablePrEP_lastQ_15to24,n_women_used_oralPrEP_lastQ_15plus_sdpartner,n_women_active_oralPrEP_lastQ_15plus_sdpartner,n_women_ever_oralPrEP_15plus_sdpartner,n_women_used_dapivirinering_lastQ_15plus_sdpartner,n_women_active_dapivirinering_lastQ_15plus_sdpartner,n_women_used_injectablePrEP_lastQ_15plus_sdpartner,n_women_active_injectablePrEP_lastQ_15plus_sdpartner,N_newHIVinfections_15plus_male,N_newHIVinfections_15plus_female,N_newbirths,N_newbirths_HIVpos,N_deaths_15plus_male,N_deaths_15plus_female,YLL_15plus_male,YLL_15plus_female,YLL_children_under15,YLL_15plus_male_discounted,YLL_15plus_female_discounted,YLL_children_under15_discounted,N_firsttime_oralPrEPinitiations_15to24F,n_notonART_byCD4_15plus[0],n_notonART_byCD4_15plus[1],n_notonART_byCD4_15plus[2],n_notonART_byCD4_15plus[3],N_HIVneg_in_SD_partnership_M15plus,N_HIVneg_in_SD_partnership_F15plus,N_HIVneg_in_SD_partnership_noART_M15plus,N_HIVneg_in_SD_partnership_noART_F15plus,n_eversex_M15plus,n_eversex_F15plus,n_usedcondomlastact_M15plus,n_usedcondomlastact_F15plus,nonART_M15_24,nonART_F15_24,naware_M15_24,naware_F15_24,N_HIVtests_15plus_symptomatic_male,N_HIVtests_15plus_symptomatic_female,n_concurrent_partnerships_15to49,n_multiple_partnerships_lastyear_15to49,prop_longtermpartnership_condomuse,prop_nonregpartnership_condomuse,prop_concurrentpartnership_condomuse\n");	
    

    else
	fprintf(MIHPSA_FILE,"Year,NPop_15to49_male,NPop_15to49_female,NPop_15to29_male,NPop_15to24_female,NPop_30to54_male,NPop_25to54_female,NPos_15to49_male,NPos_15to49_female,NPos_15to29_male,NPos_15to24_female,NPos_30to54_male,NPos_25to54_female,Ncirc_15to49,Npop_15plus_male,Npop_15plus_female,Npos_15plus_male,Npos_15plus_female,Naware_15plus_male,Naware_15plus_female,Naware_15to29_male,Naware_15to24_female,Naware_30to54_male,Naware_25to54_female,NonART_15plus_male,NonART_15plus_female,N_VS_15plus_male,N_VS_15plus_female,NonART_15to29_male,NonART_15to24_female,NonART_30to54_male,NonART_25to54_female,N_AIDSdeaths_15plus_male,N_AIDSdeaths_15plus_female,N_HIVtests_15plus_male,N_HIVtests_15plus_female,N_HIVtests_15to24F,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus_male,N_newHIVdiagnoses_15plus_female,N_newHIVdiagnoses_15to24F,N_VMMC_cumulative_15_49,N_ARTinitiations_15plus,N_ARTreinitiations_15plus,N_ARTexperienced_bysex_15plus_male,N_ARTexperienced_bysex_15plus_female,N_ARTexperienced_bysex_younger_male,N_ARTexperienced_bysex_younger_female,N_ARTexperienced_bysex_older_male,N_ARTexperienced_bysex_older_female,n_women_at_elevatedrisk_15to24,n_women_at_elevatedrisk_andonoralPrEP_15to24,N_VS_bysex_younger_male,N_VS_bysex_younger_female,N_VS_bysex_older_male,N_VS_bysex_older_female,n_women_used_oralPrEP_lastQ_15to24,n_women_active_oralPrEP_lastQ_15to24,n_women_ever_oralPrEP_15to24,n_women_used_dapivirinering_lastQ_15to24,n_women_active_dapivirinering_lastQ_15to24,n_women_used_injectablePrEP_lastQ_15to24,n_women_active_injectablePrEP_lastQ_15to24,n_women_used_oralPrEP_lastQ_15plus_sdpartner,n_women_active_oralPrEP_lastQ_15plus_sdpartner,n_women_ever_oralPrEP_15plus_sdpartner,n_women_used_dapivirinering_lastQ_15plus_sdpartner,n_women_active_dapivirinering_lastQ_15plus_sdpartner,n_women_used_injectablePrEP_lastQ_15plus_sdpartner,n_women_active_injectablePrEP_lastQ_15plus_sdpartner,N_newHIVinfections_15plus_male,N_newHIVinfections_15plus_female,N_newbirths,N_newbirths_HIVpos,N_deaths_15plus_male,N_deaths_15plus_female,YLL_15plus_male,YLL_15plus_female,YLL_children_under15,YLL_15plus_male_discounted,YLL_15plus_female_discounted,YLL_children_under15_discounted,N_firsttime_oralPrEPinitiations_15to24F,n_notonART_byCD4_15plus[0],n_notonART_byCD4_15plus[1],n_notonART_byCD4_15plus[2],n_notonART_byCD4_15plus[3]\n");	

    fprintf(MIHPSA_FILE, "%s\n", output->MIHPSA_outputs_string[p]);
    fclose(MIHPSA_FILE);
}


