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
    int art; /* ART status. */

    individual *indiv; /* Pointer used to make code more readable - points to already allocated memory so no need to malloc. */

    long npop_bysex_15to49[N_GENDER]={0,0}; /* Population aged 15-49. */
    long npop_bysex_15to24[N_GENDER]={0,0}; /* Population aged 15-24. */
    long npop_bysex_25to49[N_GENDER]={0,0}; /* Population aged 25-49. */
    long npositive_bysex_15to49[N_GENDER]={0,0}; /* No. of HIV+ aged 15-49. */
    long npositive_bysex_15to24[N_GENDER]={0,0}; /* No. of HIV+ aged 15-24. */
    long npositive_bysex_25to49[N_GENDER]={0,0}; /* No. of HIV+ aged 25-49. */

    long N_men_MC_15to49 = 0; /* Number of men aged 15-49 circumcised (VMMC or TMC). */

    long N_women_sexuallyactive_15to24 = 0;
    long N_women_usecondomlastact_15to24 = 0;


    long npop_bysex_15plus[N_GENDER]={0,0}; /* Population aged 15+. */

    
    long npositive_bysex_15plus[N_GENDER]={0,0}; /* Number of HIV+ aged 15+. */

    
    long naware_bysex_15plus[N_GENDER]={0,0}; /* Number of HIV+ diagnosed aged 15+. */
    
    long N_onART_bysex_15plus[N_GENDER]={0,0}; /* Number on ART aged 15+. */
    long N_VS_bysex_15plus[N_GENDER]={0,0}; /* Number virally suppressed aged 15+. */


    long npop_children_under15 = 0;
    long npositive_children_under15 = 0;
    long naware_children_under15 = 0;
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
		if(age>=15 && age<=24)
		    npop_bysex_15to24[g]++;
		else if(age>=25 && age<=49)
		    npop_bysex_25to49[g]++;
		if(indiv->HIV_status>UNINFECTED){
		    npositive_bysex_15to49[g]++;
		    if(age>=15 && age<=24)
			npositive_bysex_15to24[g]++;
		    else if(age>=25 && age<=49)
			npositive_bysex_25to49[g]++;
		}
		/* Now if circumcised (including healing): */
		if (g==MALE){
		    if((indiv->circ == VMMC) || (indiv->circ == VMMC_HEALING) || (indiv->circ == TRADITIONAL_MC))
			N_men_MC_15to49++;
		}
	    }

	    /* Now outputs aged 15+ */
	    if(age>=15){
		npop_bysex_15plus[g]++;

		if(indiv->HIV_status>UNINFECTED){
		    npositive_bysex_15plus[g]++;
		    art = indiv->ART_status;
		    /* Aware of status: */
		    if((art==ARTNAIVE) || (art==EARLYART) || (art==LTART_VS) || (art==LTART_VU) || (art==ARTDROPOUT) || (art==CASCADEDROPOUT)){
			naware_bysex_15plus[g]++;
			/* On ART: */
			if((art==EARLYART) || (art==LTART_VS) || (art==LTART_VU)){
			    N_onART_bysex_15plus[g]++;
			    /* Now virally suppressed: */
			    if(art==LTART_VS)
			        N_VS_bysex_15plus[g]++;
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

		if(indiv->n_lifetime_partners>0){
		   N_women_sexuallyactive_15to24++;
		   /* Function that approximates a woman's condom use at last act based on partners and condom use at present, and returns 1 if condom was used, 0 if not: */
		   N_women_usecondomlastact_15to24 += get_MIHPSA_condom_use_last_act(indiv);
		}
	    }

		


	}
    }


    sprintf(temp_string, "%i,%li,%li,",
	    (int) floor(t),npop_bysex_15to49[MALE],npop_bysex_15to49[FEMALE]);
    
	
    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,%li,%li,%li,",	
		npop_bysex_15to24[MALE],npop_bysex_15to24[FEMALE],
		npop_bysex_25to49[MALE],npop_bysex_25to49[FEMALE]);
	strcat(temp_string, temp_string2);
    }
    
    sprintf(temp_string2, "%li,%li,",	
	    npositive_bysex_15to49[MALE],npositive_bysex_15to49[FEMALE]);
    strcat(temp_string, temp_string2);

    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,%li,%li,%li,",
		npositive_bysex_15to24[MALE],npositive_bysex_15to24[FEMALE],
		npositive_bysex_25to49[MALE],npositive_bysex_25to49[FEMALE]);
	strcat(temp_string, temp_string2);
    }
	
    sprintf(temp_string2, "%li,",
	    N_men_MC_15to49);
    strcat(temp_string, temp_string2);

    if(MIHPSA_MODULE==1){
	sprintf(temp_string2, "%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li,%li\n",
	
		N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24,
		npop_bysex_15plus[MALE],npop_bysex_15plus[FEMALE],npop_children_under15,
		npositive_bysex_15plus[MALE],npositive_bysex_15plus[FEMALE],npositive_children_under15,
		naware_bysex_15plus[MALE],naware_bysex_15plus[FEMALE],naware_children_under15,
		N_onART_bysex_15plus[MALE],N_onART_bysex_15plus[FEMALE],
		N_VS_bysex_15plus[MALE],N_VS_bysex_15plus[FEMALE],
		patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_20_59[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_deaths_20_59[FEMALE],
		    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_15plus[FEMALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_AIDSdeaths_children_under15,
		patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15plus[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_HIVtests_15plus[FEMALE],
		patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15to24[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_25to49[MALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_15to24[FEMALE],patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVinfections_25to49[FEMALE],
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus,
	    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_VMMC_15plus);
    }
    else{
	sprintf(temp_string2, "\n");
    }

    strcat(temp_string, temp_string2);

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
	fprintf(MIHPSA_FILE,"Year,NPop_15to49_male,NPop_15to49_female,NPop_15to24_male,NPop_15to24_female,NPop_25to49_male,NPop_25to49_female,NPos_15to49_male,NPos_15to49_female,NPos_15to24_male,NPos_15to24_female,NPos_25to49_male,NPos_25to49_female,Ncirc_15to49,N_women_sexuallyactive_15to24,N_women_usecondomlastact_15to24,Npop_15plus_male,Npop_15plus_female,Npop_children_under15,Npos_15plus_male,Npos_15plus_female,Npos_children_under15,Naware_15plus_male,Naware_15plus_female,Naware_children_under15,NonART_15plus_male,NonART_15plus_female,N_VS_15plus_male,N_VS_15plus_female,N_deaths_20_59_male,N_deaths_20_59_female,N_AIDSdeaths_15plus_male,N_AIDSdeaths_15plus_female,N_AIDSdeaths_children_under15,N_HIVtests_15plus_male,N_HIVtests_15plus_female,N_newHIVinfections_15to24_male,N_newHIVinfections_25to49_male,N_newHIVinfections_15to24_female,N_newHIVinfections_25to49_female,N_newHIVdiagnoses_15plus,N_VMMC_cumulative_15_49\n");	
    else
	fprintf(MIHPSA_FILE,"Year,NPop_15to49_male,NPop_15to49_female,NPos_15to49_male,NPos_15to49_female,Ncirc_15to49\n");	
    
    fprintf(MIHPSA_FILE, "%s\n", output->MIHPSA_outputs_string[p]);
    fclose(MIHPSA_FILE);
}


