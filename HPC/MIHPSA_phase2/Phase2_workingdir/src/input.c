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

/************************************************************************/
/******************************* Includes  ******************************/
/************************************************************************/

#include "input.h"
#include "constants.h"
#include "utilities.h"
#include "prevention_cascades.h"
#include "mihpsa.h"
#include<math.h>

/************************************************************************/
/******************************** functions *****************************/
/************************************************************************/

/* These are the functions in this file:
read_param()
    Calls each of the individual read_params() functions (below)
read_demographic_params()
    - Read in demographic parameters from param_processed_patch$p_demographics.csv

read_hiv_params()
    - Read in hiv-related (transmission, progression) parameters from param_processed_patch$p_HIV.csv

read_hsv2_params()
    - Read in HSV2-related (transmission, progression) parameters from param_processed_patch$p_HSV2.csv


read_partnership_params()
    - Read in partnership parameters from param_processed_patch$p_partnerships.csv

read_time_params()
    - Read in time-related parameters (start of epidemic, start of ART etc) from
    param_processed_patch$p_times.csv

read_cascade_params()
    - Read in HIV cascade-related parameters from param_processed_patch$p_cascade.csv

read_popart_params():
    - Read in parameters related to the HIV trial (including CHiPS-related and PopART cascade parameters such as time to vmmc from CHiPs referral.

read_initial_params()
    Read in initial conditions (population size, etc) from param_processed_patch1_init.csv

We also currently keep the old seed for comparison
get_python_seed()
    Read in the seed used by python to generate the LHC
 */


void read_param(char *file_directory, parameters **param, int n_runs, patch_struct *patch){
    /* Call all other functions that read in parameters/data from file
    
    
    Arguments
    ---------
    file_directory : char
        Name of dir where parameter files ("param_processed*.csv") are stored.
    param : pointer to parameters struct
        Pointer to parameters structure in which to store parameter values for each simulation run.
    n_runs : int
        Number of runs of the simulation to be performed
    patch : patch_struct
        The (mainly empty) patch structure
    
    Returns
    -------
    Nothing; other functions for reading parameters are called and different structures are
    populated.  
    */
    int p;
    char patch_tag[LONGSTRINGLENGTH];
    char patch_number[10];
    
    /* Read in the information for each patch that doesn't change over time - community id, (if a trial) arm.*/

    read_patch_info(file_directory, patch);
    
    
    for(p = 0; p < NPATCHES; p++){
        sprintf(patch_number, "%i", p);
        strncpy(patch_tag, file_directory, LONGSTRINGLENGTH);
        
        /* Adds a / or \ as needed if working in directory other than current local dir. */
        add_slash(patch_tag);
        strcat(patch_tag, "param_processed_patch");
        strcat(patch_tag, patch_number);
        strcat(patch_tag, "_");

        read_demographic_params(patch_tag, param[p], n_runs);
        read_time_params(patch_tag, param[p], n_runs, p);
        read_hiv_params(patch_tag, param[p], n_runs, p, patch[0].country_setting);
        read_hsv2_params(patch_tag, param[p], n_runs, p);

        read_partnership_params(patch_tag, param[p], n_runs, patch[0].country_setting);
        read_cascade_params(patch_tag, param[p], n_runs);
	read_mtct_params(patch_tag, param[p], n_runs);
	read_PrEP_uptake_params(patch_tag, param[p], n_runs);
	if (SETTING==SETTING_POPART){
	    read_popart_params(patch_tag, param[p], n_runs);
	
	    /* Note that this MUST be called after read_cascade_params(). */
	    read_chips_uptake_params(patch_tag, param[p]);
	    read_pc0_enrolment_params(patch_tag, patch[p].community_id, param[p], n_runs, p);
	    read_pc_future_params(patch_tag, param[p], n_runs);
        }

	if (MANICALAND_CASCADE==1)
	    read_cascade_barrier_params(patch_tag, param[p], n_runs);

	
        /* Read in the parameters related to initial conditions. */
        read_initial_params(patch_tag, param[p], n_runs);

	/* Quick MIHPSA hack to set dapivirine ring and CABLA parameters: */
	MIHPSA_hack_set_PrEP_parameters(param[p], n_runs);

    }



    
    // Calling outside the patch loop to avoid a valgrind error where patch[1] is not initialised.
    if (SETTING==SETTING_POPART){
	copy_chips_params(param, n_runs);
	copy_pc_params(param, n_runs);
    }
    return;
}


void read_patch_info(char *file_directory, patch_struct *patch){
    /* Read in the community id and the arm for each patch - for PopART only. 
    
    This function reads the file `param_processed_patchinfo.txt` within the folder `file_directory`
    and saved the community ID and trial arm within that file to the attributes `community_id` and 
    and `trial_arm` of the patch structure.  
    
    Note that trial_arm can be overwritten later on if we are in a counterfactual 
    scenario (scenario_flag = 1 for POPART).
    
    Arguments
    ---------
    file_directory : char
        Name of dir where parameter files ("param_processed*.csv") are stored.
    patch : patch_struct
        The patch structure
    
    Returns
    -------
    Nothing; values are read from file and stored within attributes of the patch structure.  
    */
    
    FILE *patchinfo_file;
    char patchinfo_file_name[LONGSTRINGLENGTH];
    int p, checkreadok;
    double temp_int; /* Used to convert float/double to int. */

    // Add path before file name
    strncpy(patchinfo_file_name, file_directory, LONGSTRINGLENGTH);
    
    /* Add a / or \ as needed if working in directory other than current local dir. */
    add_slash(patchinfo_file_name);
    strcat(patchinfo_file_name, "param_processed_patchinfo.txt");

    // Open parameter file
    if ((patchinfo_file = fopen(patchinfo_file_name, "r")) == NULL){
        printf("Cannot open: %s", patchinfo_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Patch info read from: %s:\n",patchinfo_file_name);
        }
    }
    
    // For each patch, read the community ID and store in the patch structure
    for(p = 0; p < NPATCHES; p++){
        checkreadok = fscanf(patchinfo_file, "%lf", &temp_int);
        (patch + p)->community_id = (int) floor(temp_int);
        check_if_cannot_read_param(checkreadok, "patch[p]->community_id");
    }


    /* Only do this if we are simulating a trial (e.g. PopART) with separate arms. */
    if (SETTING==SETTING_POPART){
	// For each patch, read trial arm and store in the patch structure
	for(p = 0; p < NPATCHES; p++){
	    checkreadok = fscanf(patchinfo_file, "%lf", &temp_int);
	    (patch + p)->trial_arm = (int) floor(temp_int);
	    check_if_cannot_read_param(checkreadok, "param_local->trial_arm");
	}
    }
    else{
	for(p = 0; p < NPATCHES; p++)
	    (patch + p)->trial_arm = ARM_A;
    }
    
    /******************* closing patch info file ********************/
    fclose(patchinfo_file);
    return;
}


void read_demographic_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    /* Read parameters related to demographics; copy mortality and fertility parameters across
    to all simulation runs.  
    
    Values from the file param_processed_demographics.csv are read into the IBM and stored in the 
    allrunparameters structure (an array of parameter structures, one for each run).  Demographic 
    parameters may be different across the different simulation runs.  Fertility and mortality pars
    are assumed to be the same across simulation runs so these parameters are read into the first
    element of the allrunparameters array and then copied across to all other array elements.  
    
    The fertility and mortality parameters refer to several macros that are defined within 
    constants.h.  These are:
    N_UNPD_TIMEPOINTS
        the number of time periods for which fertility data is given by the UNPD (30)
    N_AGE_UNPD_FERTILITY
        the number of age groups in which fertility data is specified by the UNPD (7)
    N_AGE_UNPD_MORTALITY
        the number of age groups in which mortality data is specified by the UNPD (17)
    
    Arguments
    ---------
    patch_tag : pointer to a char
        Directory and file prefix for patch-specific file.  For instance, this will be:
        "./data/SAMPLED_PARAMETERS/PARAMS_COMMUNITY5/param_processed_patch1_" and is concatenated
        with "demographics.csv" or "fertility.csv" to create the full filenames.  
    allrunparameters : pointer to a parameters structure
        Array of 'parameters' structures, one for each simulation run (n_runs)
    n_runs : int
        Number of runs in the simulation
    
    Returns
    -------
    Nothing; values are read in and saved to the parameters structure.  
    
    */
    FILE * param_file;
    char param_file_name[LONGSTRINGLENGTH];
    int i_run, a_unpd, g, y;
    int checkreadok;
    // This is a temporary var so as not to keep writing allparameters+i_run
    // (or equivalently &allparameters[i_run]). 
    parameters *param_local;

    /********************************************************************/
    /****  Read in demographic data (apart from mortality/fertility) ****/
    /********************************************************************/
    // Add path before file name.
    
    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "demographics.csv");

    // Open parameter file; print error if file not found.
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Demographics parameters read from: %s:\n", param_file_name);
        }
    }
    
    // Throw away first line of the file (the header line)
    fscanf(param_file, "%*[^\n]\n");
    
    // Read parameters from each line (i_run) of the file
    for(i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;
        checkreadok = fscanf(param_file, "%lg", &(param_local->sex_ratio));
        check_if_cannot_read_param(checkreadok, "param_local->sex_ratio");
    }
    fclose(param_file);     // Closing demographics parameter file
    
    /*********************************************************/
    /*******************  Mortality data  ********************/
    /*********************************************************/
    // Add path before file name.
    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "mortality.csv");
    
    // Open parameter file; print error if file not found.
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Demographic mortality parameters read from: %s:\n", param_file_name);
        }
    }
    
    // Read mortality parameters
    // Store outputs in the i_run=0 parameter struct; later copy this to every other run.
    i_run = 0;
    param_local = allrunparameters + i_run;
    for(g = 0; g < N_GENDER; g++){
        for(a_unpd = 0; a_unpd < N_AGE_UNPD_MORTALITY; a_unpd++){
            checkreadok = fscanf(param_file, "%lg", 
                &(param_local->mortality_rate_by_gender_age_intercept[g][a_unpd]));
            check_if_cannot_read_param(checkreadok, 
                "param_local->mortality_rate_by_gender_age_intercept[g][a_unpd]");
        }
        for(a_unpd = 0; a_unpd < N_AGE_UNPD_MORTALITY; a_unpd++){
            param_local = allrunparameters + i_run;
            checkreadok = fscanf(param_file, "%lg", 
                &(param_local->mortality_rate_by_gender_age_slope[g][a_unpd]));
            check_if_cannot_read_param(checkreadok, 
                "param_local->mortality_rate_by_gender_age_slope[g][a_unpd]");
        }
    }
    // Close mortality parameter file
    fclose(param_file);
    
    // Copy parameters from the first simulation run across to all simulation runs
    // allrunparameters stores a copy of parameters used for each simulation run
    for(g = 0; g < N_GENDER; g++){
        for(a_unpd = 0; a_unpd < N_AGE_UNPD_MORTALITY; a_unpd++){
            for(i_run = 1; i_run < n_runs; i_run++){
                
                allrunparameters[i_run].mortality_rate_by_gender_age_intercept[g][a_unpd] =
                    allrunparameters[0].mortality_rate_by_gender_age_intercept[g][a_unpd];
                
                allrunparameters[i_run].mortality_rate_by_gender_age_slope[g][a_unpd] =
                    allrunparameters[0].mortality_rate_by_gender_age_slope[g][a_unpd];
            }
        }
    }

    /*********************************************************/
    /*******************  Fertility data  ********************/
    /*********************************************************/
    
    // Add path before file name
    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "fertility.csv");

    // Open parameter file; print error if file not found
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Demographic mortality parameters read from: %s:\n",param_file_name);
        }
    }
    
    // Read parameters; throw error if not read correctly
    i_run = 0;
    param_local = allrunparameters + i_run;
    for(y = 0; y < N_UNPD_TIMEPOINTS; y++){
        for(a_unpd = 0; a_unpd < N_AGE_UNPD_FERTILITY; a_unpd++){
            
            checkreadok = fscanf(param_file, "%lg", 
                &(param_local->fertility_rate_by_age[a_unpd][y]));
            check_if_cannot_read_param(checkreadok,
                "param_local->fertility_rate_by_age[a_unpd][y]");
        }
    }
    // Close mortality parameter file
    fclose(param_file);
    
    // Copy parameters from the first simulation run across to all simulation runs
    // allrunparameters stores a copy of parameters used for each simulation run
    for(y = 0; y < N_UNPD_TIMEPOINTS; y++){
        for(a_unpd = 0; a_unpd < N_AGE_UNPD_FERTILITY; a_unpd++){
            for(i_run = 1; i_run < n_runs; i_run++){
                
                allrunparameters[i_run].fertility_rate_by_age[a_unpd][y] =
                    allrunparameters[0].fertility_rate_by_age[a_unpd][y];
            }
        }
    }
    return;
}


void read_hiv_params(char *patch_tag, parameters *allrunparameters, int n_runs, int p, int country_setting){
    /* Read parameters related to HIV
    
    
    Does some small error checking.  
    
    
    For a given true CD4, p_misclassify_cd4[j] stores the probability that the
    measured cd4 cat is j.  Note that icd4 is the true cd4, and the other index is the measured cd4.
    
    
    Arguments
    ---------
    char *patch_tag, parameters *allrunparameters, int n_runs, int p
    
    Returns
    -------
    Nothing; 
    
    */
    
    
    FILE * param_file;
    char param_file_name[LONGSTRINGLENGTH];
    int spvl, icd4, checkreadok, i_run;
    double p_misclassify_cd4[NCD4], temp;
    
    // Temp variable to avoid having to write allparameters+i_run 
    //(or equivalently &allparameters[i_run]).
    parameters *param_local;

    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "HIV.csv");

    // Open parameter file
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("HIV parameters read from: %s:\n", param_file_name);
        }
    }
    // Throw away the first line of the parameter file (the header line)
    fscanf(param_file, "%*[^\n]\n");

    // Read parameters from each line (i_run) of the file
    for(i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;

        checkreadok = fscanf(param_file,"%lg", &(param_local->p_child_circ_trad));
        check_if_cannot_read_param(checkreadok, "param_local->p_child_circ_trad");

        checkreadok = fscanf(param_file,"%lg", &(param_local->p_child_circ_vmmc));
        check_if_cannot_read_param(checkreadok, "param_local->p_child_circ_vmmc");

        checkreadok = fscanf(param_file,"%lg", &(param_local->eff_circ_vmmc));
        check_if_cannot_read_param(checkreadok, "param_local->eff_circ_vmmc");

        checkreadok = fscanf(param_file,"%lg", &(param_local->eff_circ_tmc));
        check_if_cannot_read_param(checkreadok, "param_local->eff_circ_tmc");

        checkreadok = fscanf(param_file,"%lg", &(param_local->rr_circ_unhealed));
        check_if_cannot_read_param(checkreadok, "param_local->rr_circ_unhealed");

        checkreadok = fscanf(param_file,"%lg", &(param_local->eff_prep_semiadherent));
        check_if_cannot_read_param(checkreadok, "param_local->eff_prep_semiadherent");

	checkreadok = fscanf(param_file,"%lg", &(param_local->eff_prep_adherent));
        check_if_cannot_read_param(checkreadok, "param_local->eff_prep_adherent");


	checkreadok = fscanf(param_file,"%lg", &(param_local->eff_condom));
        check_if_cannot_read_param(checkreadok, "param_local->eff_condom");

	checkreadok = fscanf(param_file,"%lg", &(param_local->average_log_viral_load));
        check_if_cannot_read_param(checkreadok, "param_local->average_log_viral_load");

        checkreadok = fscanf(param_file,"%lg", &(param_local->average_annual_hazard_baseline));
        check_if_cannot_read_param(checkreadok, "param_local->average_annual_hazard_baseline");

        checkreadok = fscanf(param_file,"%lg", &(param_local->hazard_scale));
        check_if_cannot_read_param(checkreadok, "param_local->hazard_scale");
        checkreadok = fscanf(param_file,"%lg", &(param_local->t_hazard_starts_declining));
        check_if_cannot_read_param(checkreadok, "param_local->t_hazard_starts_declining");
        checkreadok = fscanf(param_file,"%lg", &(param_local->t_hazard_stabilizes));
        check_if_cannot_read_param(checkreadok, "param_local->t_hazard_stabilizes");


	if(country_setting==ZIMBABWE){
	    /* Need to make sure param_times is read in before this (so start_time_simul is defined): */
	    update_time_varying_hazard_onepatch(param_local->start_time_simul, param_local);
	}
	else{
	    param_local->average_annual_hazard = param_local->average_annual_hazard_baseline;
	}


        checkreadok = fscanf(param_file,"%lg", &(param_local->RRacute_trans));
        check_if_cannot_read_param(checkreadok, "param_local->RRacute_trans");

        checkreadok = fscanf(param_file,"%lg", &(param_local->RRmale_to_female_trans));
        check_if_cannot_read_param(checkreadok, "param_local->RRmale_to_female_trans");

        checkreadok = fscanf(param_file, "%lg %lg %lg %lg", 
            &(param_local->RRCD4[0]), &(param_local->RRCD4[1]), 
            &(param_local->RRCD4[2]), &(param_local->RRCD4[3]));
        check_if_cannot_read_param(checkreadok, "param_local->RRCD4");

        checkreadok = fscanf(param_file,"%lg", &(param_local->SPVL_beta_k));
        check_if_cannot_read_param(checkreadok, "param_local->SPVL_beta_k");

        checkreadok = fscanf(param_file,"%lg", &(param_local->SPVL_beta_50));
        check_if_cannot_read_param(checkreadok, "param_local->SPVL_beta_50");

        // Calc RR in infectivity from effectiveness of initial ART, ART when VS and ART when not VS
        // Reduction in infectivity is 1 - (effectiveness)
        
        checkreadok = fscanf(param_file, "%lg", &temp);
        check_if_cannot_read_param(checkreadok, "param_local->RR_ART_INITIAL");
        param_local->RR_ART_INITIAL = 1.0 - temp;

        checkreadok = fscanf(param_file, "%lg", &temp);
        check_if_cannot_read_param(checkreadok, "param_local->RR_ART_VS");
        param_local->RR_ART_VS = 1.0 - temp;

        checkreadok = fscanf(param_file, "%lg", &temp);
        check_if_cannot_read_param(checkreadok, "param_local->RR_ART_VU");
        param_local->RR_ART_VU = 1.0 - temp;

        checkreadok = fscanf(param_file, "%lg %lg", 
            &(param_local->min_dur_acute), &(param_local->max_dur_acute));
        check_if_cannot_read_param(checkreadok,"param_local->dur_acute");

        for(spvl = 0; spvl < NSPVL; spvl++){
            checkreadok = fscanf(param_file, "%lg", &(param_local->p_initial_cd4_gt500[spvl]));
            check_if_cannot_read_param(checkreadok, "param_local->p_initial_cd4_gt500");

            checkreadok = fscanf(param_file,"%lg", &(param_local->p_initial_cd4_350_500[spvl]));
            check_if_cannot_read_param(checkreadok, "param_local->p_initial_cd4_350_500");

            checkreadok = fscanf(param_file,"%lg", &(param_local->p_initial_cd4_200_350[spvl]));
            check_if_cannot_read_param(checkreadok, "param_local->p_initial_cd4_200_350");

            checkreadok = fscanf(param_file,"%lg", &(param_local->p_initial_cd4_lt200[spvl]));
            check_if_cannot_read_param(checkreadok, "param_local->p_initial_cd4_lt200");

            // Ensure these are normalized to sum to 1
            normalise_four_quantities(
                &param_local->p_initial_cd4_gt500[spvl],
                &param_local->p_initial_cd4_350_500[spvl],
                &param_local->p_initial_cd4_200_350[spvl], 
                &param_local->p_initial_cd4_lt200[spvl]);
                
            // Now to save recomputing these, make cumulative sums
            cumulative_four_quantities(
                param_local->p_initial_cd4_gt500[spvl], 
                param_local->p_initial_cd4_350_500[spvl], 
                param_local->p_initial_cd4_200_350[spvl],
                param_local->p_initial_cd4_lt200[spvl],
                &param_local->cumulative_p_initial_cd4_gt500[spvl],
                &param_local->cumulative_p_initial_cd4_350_500[spvl],
                &param_local->cumulative_p_initial_cd4_200_350[spvl],
                &param_local->cumulative_p_initial_cd4_lt200[spvl]); 
                
            if(PRINT_DEBUG_INPUT == 1){
                printf("Cumulative values = %f %f %f %f\n",
                    param_local->cumulative_p_initial_cd4_gt500[spvl],
                    param_local->cumulative_p_initial_cd4_350_500[spvl],
                    param_local->cumulative_p_initial_cd4_200_350[spvl],
                    param_local->cumulative_p_initial_cd4_lt200[spvl]);
            }
        }

        checkreadok = fscanf(param_file, "%lg", &(param_local->initial_SPVL_mu));
        check_if_cannot_read_param(checkreadok, "param_local->initial_SPVL_mu");
        checkreadok = fscanf(param_file, "%lg", &(param_local->initial_SPVL_sigma));
        check_if_cannot_read_param(checkreadok, "param_local->initial_SPVL_sigma");
        checkreadok = fscanf(param_file, "%lg", &(param_local->SPVL_sigma_M));
        check_if_cannot_read_param(checkreadok, "param_local->SPVL_sigma_M");
        checkreadok = fscanf(param_file, "%lg", &(param_local->SPVL_sigma_E));
        check_if_cannot_read_param(checkreadok, "param_local->SPVL_sigma_E");

        // For a given true CD4, p_misclassify_cd4[j] stores the probability that the 
        // measured cd4 cat is j.
        // Note that icd4 is the true cd4, and the other index is the measured cd4.
        for(icd4 = 0; icd4 < NCD4; icd4++){
            checkreadok = fscanf(param_file, "%lg %lg %lg %lg", 
                &(p_misclassify_cd4[0]), &(p_misclassify_cd4[1]), 
                &(p_misclassify_cd4[2]), &(p_misclassify_cd4[3]));
            
            check_if_cannot_read_param(checkreadok, "param_local->p_misclassify_cd4");
            
            normalise_four_quantities(
                &(p_misclassify_cd4[0]), &(p_misclassify_cd4[1]), 
                &(p_misclassify_cd4[2]), &(p_misclassify_cd4[3]));
            
            cumulative_four_quantities(
                p_misclassify_cd4[0], p_misclassify_cd4[1], 
                p_misclassify_cd4[2], p_misclassify_cd4[3],
                &param_local->cumulative_p_misclassify_cd4[icd4][0],
                &param_local->cumulative_p_misclassify_cd4[icd4][1],
                &param_local->cumulative_p_misclassify_cd4[icd4][2],
                &param_local->cumulative_p_misclassify_cd4[icd4][3]);
                
            if(PRINT_DEBUG_INPUT == 1){
                printf("Cumulative CD4 misclassification values: %lg %lg %lg %lg\n", 
                    param_local->cumulative_p_misclassify_cd4[icd4][0], 
                    param_local->cumulative_p_misclassify_cd4[icd4][1], 
                    param_local->cumulative_p_misclassify_cd4[icd4][2], 
                    param_local->cumulative_p_misclassify_cd4[icd4][3]);
            }
        }   

        for(spvl = 0; spvl < NSPVL; spvl++){
            for(icd4 = 0; icd4 < NCD4; icd4++){
                checkreadok = fscanf(param_file, "%lg ", &param_local->time_hiv_event[icd4][spvl]);
                check_if_cannot_read_param(checkreadok, "param_local->time_hiv_event");
            }
        }

        for(icd4 = 0; icd4 < NCD4; icd4++){
            checkreadok = fscanf(param_file, "%lg ",
                &param_local->CoxPH_SPVL_RR_CD4progression[icd4]);
            
            check_if_cannot_read_param(checkreadok, "param_local->CoxPH_SPVL_RR_CD4progression");
        }
        for(icd4 = 0; icd4 < NCD4; icd4++){
            if(param_local->CoxPH_SPVL_RR_CD4progression[icd4] < 1){
                
                printf("param_local->CoxPH_SPVL_RR_CD4progression[icd4] = ");
                printf("%lf was below 1. Have forced it to be 1.\n",
                    param_local->CoxPH_SPVL_RR_CD4progression[icd4]);
                
                param_local->CoxPH_SPVL_RR_CD4progression[icd4] = 1.0;
            }
        }
        
        checkreadok = fscanf(param_file, "%lg", 
            &(param_local->factor_for_slower_progression_ART_VU));
        check_if_cannot_read_param(checkreadok, 
            "param_local->factor_for_slower_progression_ART_VU");
    }
    // Close parameter file
    fclose(param_file);
    return;
}



void read_hsv2_params(char *patch_tag, parameters *allrunparameters, int n_runs, int p){
    /* Read parameters related to HSV-2. Does some small error checking.  
    
    Arguments
    ---------
    char *patch_tag, parameters *allrunparameters, int n_runs, int p
    
    Returns: nothing; 
    */
    
    
    FILE * param_file;
    char param_file_name[LONGSTRINGLENGTH];
    int checkreadok, i_run, hsv;
    
    // Temp variable to avoid having to write allparameters+i_run 
    //(or equivalently &allparameters[i_run]).
    parameters *param_local;

    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "HSV2.csv");

    // Open parameter file
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("HSV-2 parameters read from: %s:\n", param_file_name);
        }
    }
    // Throw away the first line of the parameter file (the header line)
    fscanf(param_file, "%*[^\n]\n");

    // Read parameters from each line (i_run) of the file
    for(i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;

        checkreadok = fscanf(param_file,"%lg", &(param_local->average_annual_hazard_hsv2));
        check_if_cannot_read_param(checkreadok, "param_local->average_annual_hazard_hsv2");


        for(hsv = 0; hsv < N_HSV2_EVENTS; hsv++){
            checkreadok = fscanf(param_file, "%lg", &(param_local->mean_dur_hsv2event[hsv]));
            check_if_cannot_read_param(checkreadok, "param_local->mean_dur_hsv2event[hsv]");
        }


	checkreadok = fscanf(param_file,"%lg", &(param_local->eff_condom_hsv2));
        check_if_cannot_read_param(checkreadok, "param_local->eff_condom_hsv2");
	if(i_run==0)
	    printf("eff_condom_hsv2=%lf\n",param_local->eff_condom_hsv2);

        checkreadok = fscanf(param_file,"%lg", &(param_local->eff_prep_semiadherent_hsv2));
        check_if_cannot_read_param(checkreadok, "param_local->eff_prep_semiadherent_hsv2");

	checkreadok = fscanf(param_file,"%lg", &(param_local->eff_prep_adherent_hsv2));
        check_if_cannot_read_param(checkreadok, "param_local->eff_prep_adherent_hsv2");
	
	    
	checkreadok = fscanf(param_file,"%lg", &(param_local->eff_circ_hsv2_vmmc));
        check_if_cannot_read_param(checkreadok, "param_local->eff_circ_hsv2_vmmc");
	if(i_run==0)
	    printf("eff_circ_hsv2_vmmc=%lf\n",param_local->eff_circ_hsv2_vmmc);

	
	checkreadok = fscanf(param_file,"%lg", &(param_local->eff_circ_hsv2_tmc));
        check_if_cannot_read_param(checkreadok, "param_local->eff_circ_hsv2_tmc");
	if(i_run==0)
	    printf("eff_circ_hsv2_tmc=%lf\n",param_local->eff_circ_hsv2_tmc);

	
    }
    // Close parameter file
    fclose(param_file);
    return;
}


void read_partnership_params(char *patch_tag, parameters *allrunparameters, int n_runs, int country_setting){
    /* Read partnership related parameters
    
    
    The parameters p_age_per_gender are not directly read in the input files
    what is read is p1, p2/(1-p1), p3/(1-p1-p2), etc...
    this avoids having constraints on these probabilities summing to 1.
    
    
    Arguments
    ---------
    patch_tag : pointer to a character array
    
    allrunparameters : pointer to an array of parameters structures
        Structure for storing all parameter values
    n_runs : int
        Number of runs in the simulation
    
    Returns
    -------
    Nothing; 
    
    */
    
    FILE * param_file;
    int g, ag, r, bg, i_run;

    int round; /* Round of the Manicaland cohort. */
    
    char param_file_name[LONGSTRINGLENGTH];
    
    // This is a temporary var so as not to keep writing allparameters+i_run
    // (or equivalently &allparameters[i_run]). 
    parameters *param_local;
    int checkreadok;
    double c_multiplier, breakup_scale_multiplier_overall, temp_int;
    double breakup_scale_multiplier_between_vs_within_patch;
    
    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "partnerships.csv");

    // Open parameter file
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s\n", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Partnership parameters read from: %s:\n", param_file_name);
        }
    }

    // Throw away the first line (the header file)
    fscanf(param_file, "%*[^\n]\n");

    // Read parameters from each line (i_run), one for each simulation run
    for(i_run = 0; i_run < n_runs; i_run++){

        param_local = allrunparameters + i_run;
        
        checkreadok = fscanf(param_file,"%lg", &(param_local->assortativity));
        check_if_cannot_read_param(checkreadok, "param_local->assortativity");

        checkreadok = fscanf(param_file,"%lg", &(param_local->prop_compromise_from_males));
        check_if_cannot_read_param(checkreadok, "param_local->prop_compromise_from_males");

        for(ag = 0; ag < N_AGE ; ag++){
            checkreadok = fscanf(param_file, "%lg",
                &(param_local->c_per_gender_within_patch_baseline[FEMALE][ag]));
            check_if_cannot_read_param(checkreadok, "param_local->c_per_gender_within_patch_baseline");
        }

        for(ag = 0; ag < N_AGE; ag++){
            checkreadok = fscanf(param_file, "%lg", 
                &(param_local->c_per_gender_within_patch_baseline[MALE][ag]));
            check_if_cannot_read_param(checkreadok, "param_local->c_per_gender_within_patch_baseline");
        }

        checkreadok = fscanf(param_file, "%lg", &c_multiplier);
        check_if_cannot_read_param(checkreadok, "c_multiplier");
        
        for(ag = 0; ag < N_AGE; ag++){
            param_local->c_per_gender_within_patch_baseline[FEMALE][ag] *= c_multiplier;
            param_local->c_per_gender_within_patch_baseline[MALE][ag] *= c_multiplier;
        }

	/* Modify the number of partners (to allow people earlier in the epidemic to have more partners for example). 
	   At present this is only for Zimbabwe (using Manicaland cohort). */
	if(country_setting==ZIMBABWE){

	    int i_young_old; /* Takes value 0/1, used as rr_mean_ly stratified into young/old (roughly <23, 23+ - note that I currently use <25, 25+ in the R script). */
	    for(i_young_old=0; i_young_old<2; i_young_old++){
		for(round=0; round <NCOHORTROUNDS; round++){
		    checkreadok = fscanf(param_file, "%lg", &(param_local->rr_mean_ly_F_byround[i_young_old][round]));
		    check_if_cannot_read_param(checkreadok, "param_local->rr_mean_ly_F_byround[i_young_old][round]");
		}
	    }
	    
	    for(i_young_old=0; i_young_old<2; i_young_old++){
		for(round=0; round <NCOHORTROUNDS; round++){
		    checkreadok = fscanf(param_file, "%lg", &(param_local->rr_mean_ly_M_byround[i_young_old][round]));
		    check_if_cannot_read_param(checkreadok, "param_local->rr_mean_ly_M_byround[i_young_old][round]");
		}
	    }


	    /* printf("param_local->rr_mean_ly_young_F_byround[r]="); */
	    /* for(round=0; round <NCOHORTROUNDS; round++) */
	    /* 	printf("%lf ",param_local->rr_mean_ly_F_byround[0][round]); */
	    /* printf("param_local->rr_mean_ly_old_F_byround[r]="); */
	    /* for(round=0; round <NCOHORTROUNDS; round++) */
	    /* 	printf("%lf ",param_local->rr_mean_ly_F_byround[1][round]); */

	    /* printf("param_local->rr_mean_ly_young_M_byround[r]="); */
	    /* for(round=0; round <NCOHORTROUNDS; round++) */
	    /* 	printf("%lf ",param_local->rr_mean_ly_M_byround[0][round]); */
	    /* printf("param_local->rr_mean_ly_old_M_byround[r]="); */
	    /* for(round=0; round <NCOHORTROUNDS; round++) */
	    /* 	printf("%lf ",param_local->rr_mean_ly_M_byround[1][round]); */

	    double rr_f[2] = {param_local->rr_mean_ly_F_byround[0][0],param_local->rr_mean_ly_F_byround[1][0]};
	    double rr_m[2] = {param_local->rr_mean_ly_M_byround[0][0],param_local->rr_mean_ly_M_byround[1][0]};
	    /* Assigns param_local->c_per_gender_within_patch given param_local->c_per_gender_within_patch_baseline: */

	    calculate_current_c_within_patch(param_local, rr_m, rr_f);
	    
	}
	else{ /* For non-Zimbabwe settings, the number of partners never changes (unless there's something similar to the Manicaland cohort): */
	    for(ag = 0; ag < N_AGE; ag++){
		param_local->c_per_gender_within_patch[FEMALE][ag] = param_local->c_per_gender_within_patch_baseline[FEMALE][ag];
		param_local->c_per_gender_within_patch[MALE][ag] = param_local->c_per_gender_within_patch_baseline[MALE][ag];
	    }
	}
	
	
        checkreadok = fscanf(param_file, "%lg",
            &(param_local->rel_rate_partnership_formation_between_patches));
        check_if_cannot_read_param(checkreadok,
            "param_local->rel_rate_partnership_formation_between_patches");

	/* This calculates param->c_per_gender_between_patches[][] based on c_per_gender_within_patch and rel_rate_partnership_formation_between_patches. */

	calculate_c_between_patches(param_local);
	

        checkreadok = fscanf(param_file, "%lg", &(param_local->rr_hiv_between_vs_within_patch));
        check_if_cannot_read_param(checkreadok, "param_local->rr_hiv_between_vs_within_patch");

        for(r = 0; r < N_RISK ; r++){
            checkreadok = fscanf(param_file, "%lg", 
                &(param_local->relative_number_partnerships_per_risk[r]));
            check_if_cannot_read_param(checkreadok, 
                "param_local->relative_number_partnerships_per_risk");
            
            // Because we're now defining everything relative to the low risk group we need this to
            // be forced to 1
            if(r == 0){
                param_local->relative_number_partnerships_per_risk[r] = 1.0;
            }
        }

        // The parameters p_age_per_gender are not directly read in the input files 
        // what is read is p1, p2/(1-p1), p3/(1-p1-p2), etc... 
        // this avoids having constraints on these probabilities summing to 1.  

        double p_age_per_gender_wrong_scale[N_GENDER][N_AGE][N_AGE], fact, check_sum;

        for(g = 0; g < N_GENDER; g++){
            for(ag = 0; ag < N_AGE; ag++){
                //printf("--- INDEX PERSON IN AGE GROUP %d; probability of choosing partner in each age group is:\n",ag);
                fact = 1;
                
                check_sum = 0;
                for(bg = 0; bg < N_AGE; bg++){
                    
                    checkreadok = fscanf(param_file, "%lg", 
                        &(p_age_per_gender_wrong_scale[g][ag][bg]));
                    check_if_cannot_read_param(checkreadok, "param_local->p_age_per_gender");
                    
                    param_local->p_age_per_gender[g][ag][bg] =
                        p_age_per_gender_wrong_scale[g][ag][bg] * fact;
                    
                    fact -= param_local->p_age_per_gender[g][ag][bg];
                    
                    //printf("%lg\t",param_local->p_age_per_gender[g][ag][bg]);
                    check_sum += param_local->p_age_per_gender[g][ag][bg];
                }
                //printf("\n");
                //fflush(stdout);
                
                if(fabs(check_sum - 1.0) > 1e-12){
                    printf("In input.c the sum of param_local->p_age_per_gender[g][ag][bg] ");
                    printf("over bg is 1-%e for ag=%d. Exiting", check_sum - 1.0, ag);
                    printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                    fflush(stdout);
                    exit(1);
                }
            }
        }

        //printf("------- UPON READING PARAM_PARTNERSHIPS -------\n");
        //fflush(stdout);

        for(r = 0; r < N_RISK; r++){
            checkreadok = fscanf(param_file, "%lf", &(temp_int));
            param_local->max_n_part_noage[r] = (int) floor(temp_int);
            check_if_cannot_read_param(checkreadok, "param_local->max_n_part_noage");
            
            //printf("param_local->max_n_part_noage in risk group %d is %d\n",r,param_local->max_n_part_noage[r]);
            //fflush(stdout);
        }

        for(r = 0; r < N_RISK; r++){
            checkreadok = fscanf(param_file, "%lg", 
                &(param_local->breakup_scale_lambda_within_patch[r]));
            check_if_cannot_read_param(checkreadok,
                "param_local->breakup_scale_lambda_within_patch");
            
            //printf("param_local->breakup_scale_lambda_within_patch in risk group %d is %lg\n",r,param_local->breakup_scale_lambda_within_patch[r]);
            //fflush(stdout);
        }
        for(r = 0; r < N_RISK; r++){
            checkreadok = fscanf(param_file, "%lg", &(param_local->breakup_shape_k[r]));
            check_if_cannot_read_param(checkreadok, "param_local->breakup_shape_k");
        }
        
        checkreadok = fscanf(param_file, "%lg", &breakup_scale_multiplier_overall);
        check_if_cannot_read_param(checkreadok, "breakup_scale_multiplier_overall");
        
        for(r = 0; r < N_RISK; r++){
            param_local->breakup_scale_lambda_within_patch[r] *= breakup_scale_multiplier_overall;
        }

        checkreadok = fscanf(param_file, "%lg", &breakup_scale_multiplier_between_vs_within_patch);
        check_if_cannot_read_param(checkreadok, "breakup_scale_multiplier_between_vs_within_patch");
        
        for(r = 0; r < N_RISK; r++){
            param_local->breakup_scale_lambda_between_patch[r] =
                param_local->breakup_scale_lambda_within_patch[r] *
                breakup_scale_multiplier_between_vs_within_patch;
        }

        /*printf("------- AFTER READING PARAM_PARTNERSHIPS AND DOING SOME CALCULATION -------\n");
        fflush(stdout);

        for(r=0 ; r<N_RISK ; r++)
        {
            printf("param_local->max_n_part_noage in risk group %d is %d\n",r,param_local->max_n_part_noage[r]);
            fflush(stdout);
        }

        for(r=0; r<N_RISK; r++){
            printf("param_local->breakup_scale_lambda_within_patch in risk group %d is %lg\n",r,param_local->breakup_scale_lambda_within_patch[r]);
            fflush(stdout);
        }
        for(r=0; r<N_RISK; r++){
            printf("param_local->breakup_shape_k in risk group %d is %lg\n",r,param_local->breakup_shape_k[r]);
            fflush(stdout);
        }
        printf("breakup_scale_multiplier_overall is %lg\n",breakup_scale_multiplier_overall);
        printf("breakup_scale_multiplier_between_vs_within_patch is %lg\n",breakup_scale_multiplier_between_vs_within_patch);
        fflush(stdout);

        printf("------- FINISH --- CHECK THIS IS OK! -------\n");
        fflush(stdout);*/

    } // end for i_run
    
    // Close parameter file
    fclose(param_file);
    return;
}


void read_time_params(char *patch_tag, parameters *allrunparameters, int n_runs, int p){
    /* Read time related parameters
    
    Arguments
    ---------
    char *patch_tag, parameters *allrunparameters, int n_runs, int p
    
    Returns
    -------
    Nothing; the allrunparameters structure is populated
    */
    
    FILE * param_file;
    char param_file_name[LONGSTRINGLENGTH];
    int i_run, i;
    
    // For rounding the time HIV/HSV-2 starts to the nearest timestep
    double time_start_hiv_undiscretised, time_start_hsv2_undiscretised;
    
    // This is a temporary var so as not to keep writing allparameters+i_run
    // (or equivalently &allparameters[i_run]). 
    parameters *param_local;
    int checkreadok;

    double temp_int;
    double temp;
    
    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "times.csv");

    // Open parameter file
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s\n", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Times parameters read from: %s:\n", param_file_name);
        }
    }

    // Throw away first line of the file (the header line)
    fscanf(param_file, "%*[^\n]\n");

    //printf("Opening file %s\n", param_file_name);

    // Read parameters from each line (i_run) of the file as used for each run of the simulation
    for(i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;

        checkreadok = fscanf(param_file, "%lg", &time_start_hiv_undiscretised);
        check_if_cannot_read_param(checkreadok, "param_local->start_time_hiv");
        
        // Here we want start_time_hiv to be equal to a timestep value (this avoids issues when
        // seeding infections, where new_infections looks for the person in age_index[] using the
        // index calculated using the infection time. If not a timestep then that may produce the
        // wrong index and the person is not found (so HIV status not updated etc).
        
        // The year when HIV is seeded
        param_local->start_time_hiv_discretised_year = (int) floor(time_start_hiv_undiscretised);
        
        // The timestep within that year when HIV is seeded
        param_local->start_time_hiv_discretised_timestep = (int) floor((time_start_hiv_undiscretised - param_local->start_time_hiv_discretised_year)*N_TIME_STEP_PER_YEAR);
        
        if(param_local->start_time_hiv_discretised_timestep >= N_TIME_STEP_PER_YEAR){
            printf("Error in calculating when HIV is seeded. Exiting\n");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        param_local->start_time_hiv = param_local->start_time_hiv_discretised_year +
            param_local->start_time_hiv_discretised_timestep / (1.0 * N_TIME_STEP_PER_YEAR);


        // Same for start_time_hsv2 - want it to be equal to a timestep value
        checkreadok = fscanf(param_file, "%lg", &time_start_hsv2_undiscretised);
        check_if_cannot_read_param(checkreadok, "param_local->start_time_hsv2");
        // The year when HSV-2 is seeded
        param_local->start_time_hsv2_discretised_year = (int) floor(time_start_hsv2_undiscretised);
        
        // The timestep within that year when HSV-2 is seeded:
        param_local->start_time_hsv2_discretised_timestep = (int) floor((time_start_hsv2_undiscretised - param_local->start_time_hsv2_discretised_year)*N_TIME_STEP_PER_YEAR);
        
        if(param_local->start_time_hsv2_discretised_timestep >= N_TIME_STEP_PER_YEAR){
            printf("Error in calculating when HSV-2 is seeded. Exiting\n");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        param_local->start_time_hsv2 = param_local->start_time_hsv2_discretised_year +
            param_local->start_time_hsv2_discretised_timestep / (1.0 * N_TIME_STEP_PER_YEAR);

	
        checkreadok = fscanf(param_file, "%lf", &temp_int);
        param_local->start_time_simul = (int) floor(temp_int);
        check_if_cannot_read_param(checkreadok, "param_local->start_time_simul");
        checkreadok = fscanf(param_file, "%lf", &temp_int);
        param_local->end_time_simul = (int) floor(temp_int);
        check_if_cannot_read_param(checkreadok, "param_local->end_time_simul");
    
        // If this message comes up make sure that age_list is correctly indexed
        if(
        ((param_local->end_time_simul-param_local->start_time_simul) >= 2*(MAX_AGE - AGE_ADULT)) &&
        i_run == 0 && 
        p == 0
        ){
            printf("Potential issue: param->end_time_simul-param->start_time_simul is bigger than");
            printf(" 2*(MAX_AGE-AGE_ADULT)=%i.\n", 2 * (MAX_AGE - AGE_ADULT));
            printf("There may be issues with the age index for the age_list[] array.\n");
        }
        
        checkreadok = fscanf(param_file, "%lf", &temp_int);
        param_local->COUNTRY_HIV_TEST_START = (int) floor(temp_int);
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_HIV_TEST_START");

        checkreadok = fscanf(param_file, "%lg", &(param_local->COUNTRY_ART_START));
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_ART_START");

        checkreadok = fscanf(param_file, "%lg", &(param_local->COUNTRY_EMERGENCY_ART_START));
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_EMERGENCY_ART_START");

        checkreadok = fscanf(param_file, "%lg", &(param_local->COUNTRY_CD4_350_START));
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_CD4_350_START");

        checkreadok = fscanf(param_file, "%lg", &(param_local->COUNTRY_CD4_500_START));
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_CD4_500_START");
        
        checkreadok = fscanf(param_file, "%lg", &(param_local->COUNTRY_IMMEDIATE_ART_START));
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_IMMEDIATE_ART_START");

        checkreadok = fscanf(param_file, "%lg", &(param_local->COUNTRY_VMMC_START));
        check_if_cannot_read_param(checkreadok, "param_local->COUNTRY_VMMC_START");

	param_local->COUNTRY_VMMC_START_timestep = (int) round((param_local->COUNTRY_VMMC_START - trunc(param_local->COUNTRY_VMMC_START))*N_TIME_STEP_PER_YEAR);
	
        if( (int) (param_local->start_time_simul) != (param_local->start_time_simul) || 
            (int) (param_local->end_time_simul) != param_local->end_time_simul){
            
            printf("start_time_simul and end_time_simul defined in '%s' ", param_file_name);
            printf("should be integers. Execution aborted.");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }

        if(param_local->end_time_simul - param_local->start_time_simul > MAX_N_YEARS){
            printf("MAX_N_YEARS < param_local->end_time_simul - param_local->start_time_simul.");
            printf(" Need to increase the value of MAX_N_YEARS. Execution aborted.");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
	
        checkreadok = fscanf(param_file, "%lg", &temp_int);
        check_if_cannot_read_param(checkreadok, "param_local->DHS_params->NDHSROUNDS");
        param_local->DHS_params->NDHSROUNDS = (int) temp_int;

        for(i = 0; i < param_local->DHS_params->NDHSROUNDS; i++){
            checkreadok = fscanf(param_file, "%lg", &temp_int);
            check_if_cannot_read_param(checkreadok, "param_local->DHS_params->DHS_YEAR[round]");
            param_local->DHS_params->DHS_YEAR[i] = (int) temp_int;
        }



        for(i = 0; i < NCOHORTROUNDS; i++){
            checkreadok = fscanf(param_file, "%lg", &temp);
            check_if_cannot_read_param(checkreadok, "param_local->COHORTDATES[round]");
            param_local->COHORTYEAR[i] = (int) trunc(temp);
	    param_local->COHORTTIMESTEP[i] = (int) round((temp-param_local->COHORTYEAR[i])*N_TIME_STEP_PER_YEAR);
	    //printf("At time t=%lf y=%i and t=%i\n",temp,param_local->COHORTYEAR[i],param_local->COHORTTIMESTEP[i]);
        }

    }
    // Close parameter file
    fclose(param_file);
    return;
}


/************************************************************************************/
/*******************     Cascade parameters - except CHiPs visit rates***************/
/************************************************************************************/
void read_cascade_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    FILE *param_file;
    int icd4;
    char param_file_name[LONGSTRINGLENGTH];
    int i_run;
    double max_temp;  /* Local variable which allows us to get the range from the max value. */
    /* This is a local temp variable we use so we don't have to keep writing allparameters+i_run (or equivalently &allparameters[i_run]). */
    parameters *param_local;
    int checkreadok;

    strncpy(param_file_name,patch_tag,LONGSTRINGLENGTH);
    strcat(param_file_name, "cascade.csv");

    /******************* opening parameter file ********************/
    if ((param_file=fopen(param_file_name,"r"))==NULL)
    {
        printf("Cannot open %s\n",param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else
    {
        if(VERBOSE_OUTPUT==1)
            printf("Cascade parameters read from: %s:\n",param_file_name);
    }

    /* The first line of this file is a header - the text below reads in just that line and throws it away.
     * The * instructs fscanf (all of the scanf family, in fact) to parse the data out as presented in the format string,
     * but NOT to store it at any target address (which is good, because there is none provided in an argument list).
     * the [^\n] means take anything except a newline, so ALL data will be consumed up to (but not including) the newline.
     *  Finally, the final \n means "and consume (and ignore) the newline" (which we just stopped at when fulfilling the
     *  prior format spec). */
    fscanf(param_file, "%*[^\n]\n");


    /******************* read parameters from each line i_run ********************/
    for (i_run = 0; i_run<n_runs; i_run++){
        param_local = allrunparameters + i_run;

        checkreadok = fscanf(param_file,"%lg",&(param_local->time_to_background_HIVtestNOW));
        //printf("param_local->time_to_background_HIVtestNOW = %lf\n",param_local->time_to_background_HIVtestNOW);
        check_if_cannot_read_param(checkreadok,"param_local->time_to_background_HIVtestNOW");

        checkreadok = fscanf(param_file,"%lg",&(param_local->time_to_background_HIVtest_maxval));
        //printf("param_local->time_to_background_HIVtest_maxval = %lf\n",param_local->time_to_background_HIVtest_maxval);
        check_if_cannot_read_param(checkreadok,"param_local->time_to_background_HIVtest_maxval");

        checkreadok = fscanf(param_file,"%lg",&(param_local->time_to_background_HIVtest_exponent));
        //printf("param_local->time_to_background_HIVtest_exponent = %lf\n",param_local->time_to_background_HIVtest_exponent);
        check_if_cannot_read_param(checkreadok,"param_local->time_to_background_HIVtest_exponent");

        checkreadok = fscanf(param_file,"%lg",&(param_local->time_to_background_HIVtest_midpoint));
        //printf("param_local->time_to_background_HIVtest_midpoint = %lf\n",param_local->time_to_background_HIVtest_midpoint);
        check_if_cannot_read_param(checkreadok,"param_local->time_to_background_HIVtest_midpoint");

        /* Input probabilities for the cascade events: */
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_pre2005));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_pre2005");
        
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2005_2010));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2005_2010");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2011));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2011");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2012));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2012");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2013));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2013");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2014));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2014");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2015));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2015");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2016));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2016");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2017));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2017");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2018));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2018");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2019));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2019");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_2020));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_2020");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_female_current));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_female_current");

	/* Now men: */
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_pre2005));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_pre2005");
        
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2005_2010));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2005_2010");
        
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2011));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2011");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2012));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2012");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2013));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2013");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2014));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2014");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2015));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2015");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2016));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2016");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2017));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2017");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2018));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2018");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2019));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2019");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_2020));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_2020");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_male_current));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_male_current");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_HIV_background_testing_age_adjustment_factor_youngest_age_group));
        check_if_cannot_read_param(checkreadok,"param_local->p_HIV_background_testing_age_adjustment_factor_youngest_age_group");


        checkreadok = fscanf(param_file,"%lg",&(param_local->HIV_rapid_test_sensitivity_ANC));
        check_if_cannot_read_param(checkreadok,"param_local->HIV_rapid_test_sensitivity_ANC");
	if (i_run==0)
	    printf("HIV rapid test sensitivity = %6.4lf\n",param_local->HIV_rapid_test_sensitivity_ANC);


        /* Input probabilities for the cascade events: */
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_hiv_test_results_cd4_over200));
        check_if_cannot_read_param(checkreadok,"param_local->p_collect_hiv_test_results_cd4_over200");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_hiv_test_results_cd4_under200));
        check_if_cannot_read_param(checkreadok,"param_local->p_collect_hiv_test_results_cd4_under200");
        //printf("param_local->p_collect_hiv_test_results_cd4_over200 = %lf\n",param_local->p_collect_hiv_test_results_cd4_over200);

        /* checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_cd4_nonpopart)); */
        /* check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_cd4_nonpopart"); */

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_and_start_ART_2008));
        check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_and_start_ART_2008");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_and_start_ART_2010));
        check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_and_start_ART_2010");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_and_start_ART_current));
        check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_and_start_ART_current");

	param_local->p_collect_cd4_test_results_and_start_ART = param_local->p_collect_cd4_test_results_and_start_ART_2008;
	
        checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_and_remain_in_cascade));
        check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_and_remain_in_cascade");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_emergency_ART));
        check_if_cannot_read_param(checkreadok,"param_local->p_emergency_ART");
	

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_mtct_nonART_new_adult_knows_status));
        check_if_cannot_read_param(checkreadok,"param_local->p_mtct_nonART_new_adult_knows_status");
	

        //printf("param_local->p_collect_hiv_test_results_cd4_under200 = %lf\n",param_local->p_collect_hiv_test_results_cd4_under200);
        //checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_cd4_over200));
        //check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_cd4_over200");
        //printf("param_local->p_collect_cd4_test_results_cd4_over200 = %lf\n",param_local->p_collect_cd4_test_results_cd4_over200);

        //checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_cd4_under200));
        //check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_cd4_under200");
        //printf("param_local->p_collect_cd4_test_results_cd4_under200 = %lf\n",param_local->p_collect_cd4_test_results_cd4_under200);

        for (icd4=0; icd4<NCD4; icd4++){
            checkreadok = fscanf(param_file,"%lg",&(param_local->p_dies_earlyart_cd4[icd4]));
            check_if_cannot_read_param(checkreadok,"param_local->p_dies_earlyart_cd4");
        }

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_leaves_earlyart_cd4_over200_if_not_die_early));
        check_if_cannot_read_param(checkreadok,"param_local->p_leaves_earlyart_cd4_over200_if_not_die_early");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_leaves_earlyart_cd4_under200_if_not_die_early));
        check_if_cannot_read_param(checkreadok,"param_local->p_leaves_earlyart_cd4_under200_if_not_die_early");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_becomes_vs_after_earlyart_if_not_die_early_or_leave));
        check_if_cannot_read_param(checkreadok,"param_local->p_becomes_vs_after_earlyart_if_not_die_early_or_leave");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_stays_virally_suppressed));
        check_if_cannot_read_param(checkreadok,"param_local->p_stays_virally_suppressed");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_stays_virally_suppressed_male));
        check_if_cannot_read_param(checkreadok,"param_local->p_stays_virally_suppressed_male");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_stops_virally_suppressed));
        check_if_cannot_read_param(checkreadok,"param_local->p_stops_virally_suppressed");

        checkreadok = fscanf(param_file,"%lg",&(param_local->p_vu_becomes_virally_suppressed));
        check_if_cannot_read_param(checkreadok,"param_local->p_vu_becomes_virally_suppressed");
        /* Input times for the cascade events: */
        checkreadok = fscanf(param_file,"%lg",&(param_local->t_earlyart_dropout_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_earlyart_dropout_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_earlyart_dropout_range");
        param_local->t_earlyart_dropout_range[NOTPOPART] = max_temp - param_local->t_earlyart_dropout_min[NOTPOPART];



        checkreadok = fscanf(param_file,"%lg",&(param_local->t_dies_earlyart_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_dies_earlyart_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_dies_earlyart_range");
        param_local->t_dies_earlyart_range[NOTPOPART] = max_temp - param_local->t_dies_earlyart_min[NOTPOPART];


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_early_art));
        check_if_cannot_read_param(checkreadok,"param_local->t_end_early_art");

        checkreadok = fscanf(param_file,"%lg",&(param_local->t_cd4_retest_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_cd4_retest_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_cd4_retest_range");
        param_local->t_cd4_retest_range[NOTPOPART] = max_temp - param_local->t_cd4_retest_min[NOTPOPART];


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_cd4_whenartfirstavail_min));
        check_if_cannot_read_param(checkreadok,"param_local->t_cd4_whenartfirstavail_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_cd4_whenartfirstavail_range");
        param_local->t_cd4_whenartfirstavail_range = max_temp - param_local->t_cd4_whenartfirstavail_min;

        checkreadok = fscanf(param_file,"%lg",&(param_local->t_delay_hivtest_to_cd4test_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_delay_hivtest_to_cd4test_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_delay_hivtest_to_cd4test_range");
        param_local->t_delay_hivtest_to_cd4test_range[NOTPOPART] = max_temp - param_local->t_delay_hivtest_to_cd4test_min[NOTPOPART];


        // Exponential version
        checkreadok = fscanf(param_file,"%lg",&(param_local->t_start_art_mean_non_popart));
        check_if_cannot_read_param(checkreadok,"param_local->t_start_art_mean_non_popart");

        
        checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vs_becomevu_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_becomevu_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_becomevu_range");
        param_local->t_end_vs_becomevu_range[NOTPOPART] = max_temp - param_local->t_end_vs_becomevu_min[NOTPOPART];


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vs_dropout_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_dropout_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_dropout_range");
        param_local->t_end_vs_dropout_range[NOTPOPART] = max_temp - param_local->t_end_vs_dropout_min[NOTPOPART];


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vu_becomevs_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_becomevs_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_becomevs_range");
        param_local->t_end_vu_becomevs_range[NOTPOPART] = max_temp - param_local->t_end_vu_becomevs_min[NOTPOPART];


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vu_dropout_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_dropout_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_dropout_range");
        param_local->t_end_vu_dropout_range[NOTPOPART] = max_temp - param_local->t_end_vu_dropout_min[NOTPOPART];  



        checkreadok = fscanf(param_file,"%lg",&(param_local->p_circ_nonpopart));
        check_if_cannot_read_param(checkreadok,"param_local->p_circ_nonpopart");


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_get_vmmc_min[NOTPOPART]));
        check_if_cannot_read_param(checkreadok,"param_local->t_get_vmmc_min");

        checkreadok = fscanf(param_file,"%lg",&max_temp);
        check_if_cannot_read_param(checkreadok,"param_local->t_get_vmmc_range");
        param_local->t_get_vmmc_range[NOTPOPART] = max_temp - param_local->t_get_vmmc_min[NOTPOPART];


        checkreadok = fscanf(param_file,"%lg",&(param_local->t_vmmc_healing));
        check_if_cannot_read_param(checkreadok,"param_local->t_vmmc_healing");

    }

    /******************* closing parameter file ********************/
    fclose(param_file);
    return;
}





/****************************************************************************/
/**************   Mother-to-child params taken from Spectrum ****************/
/****************************************************************************/
void read_mtct_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    FILE *param_file;
    int y; // year.
    int t_steps; // Number of timesteps in the Spectrum input data.
    double t; // Temporary store for time from datafile.
    char param_file_name[LONGSTRINGLENGTH];
    int i_run;

    int checkreadok;

    strncpy(param_file_name,patch_tag,LONGSTRINGLENGTH);
    strcat(param_file_name, "mtct.csv");

    /******************* opening parameter file ********************/
    if ((param_file=fopen(param_file_name,"r"))==NULL)
    {
        printf("Cannot open %s\n",param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else
    {
        if(VERBOSE_OUTPUT==1)
            printf("MTCT parameters read from: %s:\n",param_file_name);
    }


    checkreadok = fscanf(param_file, "%lg", &(allrunparameters[0].T_FIRST_MTCT_DATAPOINT));    
    check_if_cannot_read_param(checkreadok, "allrunparameters[0].T_FIRST_MTCT_DATAPOINT");

    checkreadok = fscanf(param_file, "%lg", &(allrunparameters[0].T_LAST_MTCT_DATAPOINT));    
    check_if_cannot_read_param(checkreadok, "allrunparameters[0].T_LAST_MTCT_DATAPOINT");

    t_steps = (int) (allrunparameters[0].T_LAST_MTCT_DATAPOINT - allrunparameters[0].T_FIRST_MTCT_DATAPOINT + 1);

    for(y=0; y<t_steps; y++){	
	checkreadok = fscanf(param_file, "%lg",&t);
	check_if_cannot_read_param(checkreadok, "t for allrunparameters[0].mtct_probability[y]");

	/* Check that t is an integer - if not, then the code needs modification to store the time as well as the probability (and then change the interpolation function too), so output an error message. */
	if (ceilf(t)!=t){
	    printf("Error: In read_mtct_params() we assume that the probabilities given are yearly. This does not seem to be correct. Please check the input file (this should be an Excel file containing output from Spectrum. Exiting. \n");
	    exit(1);
	}

	
	checkreadok = fscanf(param_file, "%lg", &(allrunparameters[0].mtct_probability[y]));
	check_if_cannot_read_param(checkreadok, "allrunparameters[0].mtct_probability[y]");
	checkreadok = fscanf(param_file, "%lg", &(allrunparameters[0].prop_births_to_hivpos_mothers[y]));
	check_if_cannot_read_param(checkreadok, "allrunparameters[0].prop_births_to_hivpos_mothers[y]");
	checkreadok = fscanf(param_file, "%lg", &(allrunparameters[0].prop_children_on_ART_spectrum[y]));
	check_if_cannot_read_param(checkreadok, "allrunparameters[0].prop_children_on_ART_spectrum[y]");
	//printf("MTCT: %lf %lf %lf %lf\n",t,allrunparameters[0].mtct_probability[y],allrunparameters[0].prop_births_to_hivpos_mothers[y],allrunparameters[0].prop_children_on_ART_spectrum[y]);
    }

    // Close mtct parameter file
    fclose(param_file);

    /* Make sure rest of array by time is populated with some value - assume pmtct remains same as at last timestep. */
    for(y=t_steps; y<N_MAX_MTCT_TIMEPOINTS; y++){
	allrunparameters[0].mtct_probability[y] = allrunparameters[0].mtct_probability[t_steps-1];
	allrunparameters[0].prop_births_to_hivpos_mothers[y] = allrunparameters[0].prop_births_to_hivpos_mothers[t_steps-1];
	allrunparameters[0].prop_children_on_ART_spectrum[y] = allrunparameters[0].prop_children_on_ART_spectrum[t_steps-1];
    }
    
    // Copy parameters from the first simulation run across to all simulation runs
    // allrunparameters stores a copy of parameters used for each simulation run

    for(i_run=1; i_run<n_runs; i_run++){
	allrunparameters[i_run].T_FIRST_MTCT_DATAPOINT = allrunparameters[0].T_FIRST_MTCT_DATAPOINT;
	allrunparameters[i_run].T_LAST_MTCT_DATAPOINT = allrunparameters[0].T_LAST_MTCT_DATAPOINT;
	for(y=0; y<N_MAX_MTCT_TIMEPOINTS; y++){
	    allrunparameters[i_run].mtct_probability[y] = allrunparameters[0].mtct_probability[y];
	    allrunparameters[i_run].prop_births_to_hivpos_mothers[y] = allrunparameters[0].prop_births_to_hivpos_mothers[y];
	    allrunparameters[i_run].prop_children_on_ART_spectrum[y] = allrunparameters[0].prop_children_on_ART_spectrum[y];
        }
    }




    /* for(i_run=0; i_run<2; i_run++){ */
    /* 	printf("%i %i\n",(int) allrunparameters[i_run].T_FIRST_MTCT_DATAPOINT, (int) allrunparameters[i_run].T_LAST_MTCT_DATAPOINT); */
    /* 	for(y=0; y<N_MAX_MTCT_TIMEPOINTS; y++){ */
    /* 	    printf("%i %lf %lf %lf\n",y,allrunparameters[i_run].mtct_probability[y],allrunparameters[i_run].prop_births_to_hivpos_mothers[y],allrunparameters[i_run].prop_children_on_ART_spectrum[y]); */
    /* 	} */
    /* } */


}

void read_popart_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    FILE *param_file;
    int iround;
    char param_file_name[LONGSTRINGLENGTH];
    int i_run,i;
    double max_temp;  /* Local variable which allows us to get the range from the max value. */
    /* This is a local temp variable we use so we don't have to keep writing allparameters+i_run (or equivalently &allparameters[i_run]). */

    double temp_int; /* Used to convert float/double to int. */

    parameters *param_local;
    int checkreadok;

    double CHIPS_START, CHIPS_END;
    
    // What is wanted is not the time of the end of the last timestep in a CHiPS round but the time
    // at the beginning of that timestep. i.e. CHIPS_END_STARTOFTIMESTEP = CHIPS_END-TIME_STEP;
    double CHIPS_END_STARTOFTIMESTEP;

    
    strncpy(param_file_name,patch_tag,LONGSTRINGLENGTH);
    strcat(param_file_name, "popart.csv");

    /******************* opening parameter file ********************/
    if ((param_file=fopen(param_file_name,"r"))==NULL)
    {
        printf("Cannot open %s\n",param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else
    {
        if(VERBOSE_OUTPUT==1)
            printf("PopART trial-related parameters read from: %s:\n",param_file_name);
    }

    /* The first line of this file is a header - the text below reads in just that line and throws it away.
     * The * instructs fscanf (all of the scanf family, in fact) to parse the data out as presented in the format string,
     * but NOT to store it at any target address (which is good, because there is none provided in an argument list).
     * the [^\n] means take anything except a newline, so ALL data will be consumed up to (but not including) the newline.
     *  Finally, the final \n means "and consume (and ignore) the newline" (which we just stopped at when fulfilling the
     *  prior format spec). */
    fscanf(param_file, "%*[^\n]\n");


    /******************* read parameters from each line i_run ********************/
    for (i_run = 0; i_run<n_runs; i_run++){
        param_local = allrunparameters + i_run;

	/* Params orginally in params_cascade.txt. */
        for(i = 0; i < NCHIPSROUNDS; i++){
            checkreadok = fscanf(param_file, "%lg", &CHIPS_START);
            check_if_cannot_read_param(checkreadok, "CHIPS_START");
            
            param_local->CHIPS_START_YEAR[i] = (int) CHIPS_START;
            param_local->CHIPS_START_TIMESTEP[i] = (int) round((CHIPS_START - 
                param_local->CHIPS_START_YEAR[i])*N_TIME_STEP_PER_YEAR);

            checkreadok = fscanf(param_file, "%lg", &CHIPS_END);
            check_if_cannot_read_param(checkreadok, "CHIPS_END");
            
            // What is wanted is not the time of the end of the last timestep in a CHiPS round but
            // the time at the beginning of that timestep. i.e. CHIPS_END_STARTOFTIMESTEP =
            // CHIPS_END-TIME_STEP;
            
            CHIPS_END_STARTOFTIMESTEP = CHIPS_END - TIME_STEP;
            param_local->CHIPS_END_YEAR[i] = (int) CHIPS_END_STARTOFTIMESTEP;
            param_local->CHIPS_END_TIMESTEP[i] = (int) round((CHIPS_END_STARTOFTIMESTEP -
                param_local->CHIPS_END_YEAR[i]) * N_TIME_STEP_PER_YEAR);
            
            /* This is derived from the above times. */
            //printf("STart = %i %i End = %i %i\n",param_local->CHIPS_START_YEAR[i],param_local->CHIPS_START_TIMESTEP[i],param_local->CHIPS_END_YEAR[i],param_local->CHIPS_END_TIMESTEP[i]);
            param_local->chips_params->n_timesteps_per_round[i] =
                (param_local->CHIPS_END_YEAR[i]-param_local->CHIPS_START_YEAR[i]) *
                N_TIME_STEP_PER_YEAR +
                (param_local->CHIPS_END_TIMESTEP[i] - param_local->CHIPS_START_TIMESTEP[i]) + 1;
        }

        param_local->CHIPS_START_TIMESTEP_POSTTRIAL = 
            param_local->CHIPS_END_TIMESTEP[NCHIPSROUNDS - 1] + 1;
        
        if(param_local->CHIPS_START_TIMESTEP_POSTTRIAL >= N_TIME_STEP_PER_YEAR){
            param_local->CHIPS_START_TIMESTEP_POSTTRIAL =
                param_local->CHIPS_START_TIMESTEP_POSTTRIAL - N_TIME_STEP_PER_YEAR;
        }

        checkreadok = fscanf(param_file, "%lf", &temp_int);
        param_local->chips_params->n_timesteps_per_round_posttrial = (int) floor(temp_int);
        check_if_cannot_read_param(checkreadok, "param_local->n_timesteps_per_round_posttrial");

	/* Params orginally in params_cascade.txt. */
	checkreadok = fscanf(param_file,"%lg",&(param_local->HIV_rapid_test_sensitivity_CHIPS));
	check_if_cannot_read_param(checkreadok,"param_local->HIV_rapid_test_sensitivity_CHIPS");
	//printf("HIV rapid test sensitivity = %6.4lf\n",param_local->HIV_rapid_test_sensitivity_CHIPS);
	
	checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_cd4_popartYEAR1));
	check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_cd4_popartYEAR1");

	checkreadok = fscanf(param_file,"%lg",&(param_local->p_collect_cd4_test_results_cd4_popartYEAR2onwards));
	check_if_cannot_read_param(checkreadok,"param_local->p_collect_cd4_test_results_cd4_popartYEAR2onwards");
	printf("param_local->p_collect_cd4_test_results_cd4_popartYEAR2onwards = %lf\n",param_local->p_collect_cd4_test_results_cd4_popartYEAR2onwards);


	checkreadok = fscanf(param_file,"%lg",&(param_local->t_earlyart_dropout_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_earlyart_dropout_min");


	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_earlyart_dropout_range");
	param_local->t_earlyart_dropout_range[POPART]    = max_temp - param_local->t_earlyart_dropout_min[POPART];

	checkreadok = fscanf(param_file,"%lg",&(param_local->t_dies_earlyart_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_dies_earlyart_min");

	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_dies_earlyart_range");
	param_local->t_dies_earlyart_range[POPART]    = max_temp - param_local->t_dies_earlyart_min[POPART];
			
	checkreadok = fscanf(param_file,"%lg",&(param_local->t_cd4_retest_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_cd4_retest_min");

	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_cd4_retest_range");
	param_local->t_cd4_retest_range[POPART]    = max_temp - param_local->t_cd4_retest_min[POPART]; 

	checkreadok = fscanf(param_file,"%lg",&(param_local->t_delay_hivtest_to_cd4test_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_delay_hivtest_to_cd4test_min");

	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_delay_hivtest_to_cd4test_range");
	param_local->t_delay_hivtest_to_cd4test_range[POPART]    = max_temp - param_local->t_delay_hivtest_to_cd4test_min[POPART];

	double temp;

	for(iround = 0 ; iround<NCHIPSROUNDS ; iround++)
	    {
		/*print_here(iround);*/
		checkreadok = fscanf(param_file,"%lg",&temp);
		param_local->n_time_periods_art_popart_per_round[iround] = (int) temp;
		check_if_cannot_read_param(checkreadok,"param_local->n_time_periods_art_popart_per_round");
		/*printf("param_local->n_time_periods_art_popart_per_round[%d] is %d\n",iround,param_local->n_time_periods_art_popart_per_round[iround]);
		  fflush(stdout);*/
	    }
        
	for(iround = 0 ; iround < NCHIPSROUNDS; iround++){
	    for(i = 0; i < param_local->n_time_periods_art_popart_per_round[iround]; i++){
		checkreadok = fscanf(param_file, "%lg", 
				     &(param_local->t_start_art_mean_fast_popart[iround][i]));
                
		check_if_cannot_read_param(checkreadok,
					   "param_local->t_start_art_mean_fast_popart_round1");
	    }
            
	    for(i = 0; i < param_local->n_time_periods_art_popart_per_round[iround] ; i++){
		checkreadok = fscanf(param_file, "%lg", 
				     &(param_local->t_start_art_mean_slow_popart[iround][i]));
		check_if_cannot_read_param(checkreadok,
					   "param_local->t_start_art_mean_slow_popart_round1");
	    }
            
	    for(i = 0; i < param_local->n_time_periods_art_popart_per_round[iround]; i++){
		checkreadok = fscanf(param_file, "%lg",
				     &(param_local->p_start_art_mean_fast_popart[iround][i]));
		check_if_cannot_read_param(checkreadok, 
					   "param_local->p_start_art_mean_fast_popart_round1");
	    }
	}


	checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vs_becomevu_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_becomevu_min");
	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_becomevu_range");
	param_local->t_end_vs_becomevu_range[POPART] = max_temp - param_local->t_end_vs_becomevu_min[POPART];

    
	checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vs_dropout_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_dropout_min");
	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vs_dropout_range");
	param_local->t_end_vs_dropout_range[POPART] = max_temp -  param_local->t_end_vs_dropout_min[POPART];


	checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vu_becomevs_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_becomevs_min");

	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_becomevs_range");
	param_local->t_end_vu_becomevs_range[POPART] = max_temp - param_local->t_end_vu_becomevs_min[POPART];

	checkreadok = fscanf(param_file,"%lg",&(param_local->t_end_vu_dropout_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_dropout_min");

	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_end_vu_dropout_range");
	param_local->t_end_vu_dropout_range[POPART] = max_temp - param_local->t_end_vu_dropout_min[POPART];  


	/* This is the probability of getting back into the cascade during PopART for someone who 
	 * dropped out before PopART. */
	//for (i=0; i<NCHIPSROUNDS; i++){
	for (i=0; i<1; i++){ /* Change after DSMB. */
	    checkreadok = fscanf(param_file,"%lg",&(param_local->p_popart_to_cascade[i]));
	    printf("p_popart_to_cascade[%i] = %lf\n",i,param_local->p_popart_to_cascade[i]);
	    check_if_cannot_read_param(checkreadok,"param_local->p_popart_to_cascade[i]");
	}


	//for (i=0; i<NCHIPSROUNDS; i++){
	for (i=0; i<1; i++){ /* Change after DSMB. */
	    checkreadok = fscanf(param_file,"%lg",&(param_local->p_circ_popart[i]));
	    check_if_cannot_read_param(checkreadok,"param_local->p_circ_popart[i]");
	}

	checkreadok = fscanf(param_file,"%lg",&(param_local->t_get_vmmc_min[POPART]));
	check_if_cannot_read_param(checkreadok,"param_local->t_get_vmmc_min");

	checkreadok = fscanf(param_file,"%lg",&max_temp);
	check_if_cannot_read_param(checkreadok,"param_local->t_get_vmmc_range");
	param_local->t_get_vmmc_range[POPART] = max_temp - param_local->t_get_vmmc_min[POPART];
    }


    /******************* closing parameter file ********************/
    fclose(param_file);
    return;
    
}

void read_chips_uptake_params(char *patch_tag, parameters *allrunparameters){
    /* Read in CHiPs uptake parameters
    
    This function loops through CHiPs rounds and reads the CHiPs uptake data from this.  It 
    populates the following arrays
    
        parameters->chips_params->prop_tested_by_chips_in_round[][][]
    
        parameters->chips_params->n_timesteps_per_round[NCHIPSROUNDS]
    
    And similarly the post-trial round equivalents of these arrays:
        
        parameters->chips_params->prop_tested_by_chips_in_round_posttrial[][][]
    
        parameters->chips_params->n_timesteps_per_round_posttrial[NCHIPSROUNDS]
    
    The values saved within the `n_timesteps_per_round_posttrial` arrays are imported in the 
    read_time_params() function.  
    
    
    Arguments
    ---------
    patch_tag : pointer to a char
    allrunparameters : pointer to an array of parameters structs
    
    Returns
    -------
    Nothing; populates parameters->chips_params->prop_tested_by_chips_in_round
    */
    int i_run, n_steps;
    double temp_time_continuous;
    int temp_time_discrete;
    int g, ac, i;  /* Indices for gender, age group and the timestep (within a chips round) */
    int chips_round; /* Index for the chips round. */
    
    /* This is a local temp variable we use so we don't have to keep writing 
    allparameters + i_run (or equivalently &allparameters[i_run]). */
    parameters *param_local;
    FILE *param_file;
    int checkreadok;
    /*******************  adding path before file name ********************/
    char param_file_name[LONGSTRINGLENGTH];
    char temp_tag[100];

    /********************************************************************/
    /*******************  Read in CHiPs uptake data ********************/
    /********************************************************************/
    for(chips_round = 0; chips_round <= NCHIPSROUNDS; chips_round++){
        
        // Add path before file name.
        strncpy(param_file_name,patch_tag,LONGSTRINGLENGTH);
        
        if(chips_round < NCHIPSROUNDS){
            // Chips round files are labelled 1,2,3,4
            sprintf(temp_tag, "chipsuptake_round%i.csv", chips_round + 1);
        }else{
            // Post-trial uptake.
            sprintf(temp_tag,"chipsuptake_roundposttrial.csv");
        }
        strcat(param_file_name, temp_tag);
        
        /******************* opening parameter file ********************/
        if((param_file = fopen(param_file_name, "r")) == NULL){
            printf("Cannot open %s",param_file_name);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }else{
            if(VERBOSE_OUTPUT == 1)
                printf("CHiPs uptake parameters read from: %s:\n", param_file_name);
        }
        /******************* read parameters ********************/

        /* First line offile is a header, read that line and throw it away.*/
        fscanf(param_file, "%*[^\n]\n");

        /* Store outputs in the i_run = 0 parameter struct, and later copy it to every other run. */
        i_run = 0;
        /* No need for the i_run to be added - but just keep here for clarity. */
        param_local = allrunparameters + i_run;
        
        /* Set the cumulative counters to be zero. */
        for(g = 0; g < N_GENDER; g++){
            for(ac = 0; ac < (MAX_AGE - AGE_CHIPS + 1); ac++){
                if(chips_round < NCHIPSROUNDS){
                    param_local->chips_params->prop_tested_by_chips_in_round[g][ac][chips_round]=0;
                    n_steps = param_local->chips_params->n_timesteps_per_round[chips_round];
                }else{
                    param_local->chips_params->prop_tested_by_chips_in_round_posttrial[g][ac] = 0;
                    n_steps = param_local->chips_params->n_timesteps_per_round_posttrial;
                }
            }
        }
        
        /* Read in the data from the CHiPs uptake file*/
        for(i = 0; i < n_steps; i++){
            checkreadok = fscanf(param_file,"%lg", &temp_time_continuous);
            check_if_cannot_read_param(checkreadok, "atemp_time_continuous");
            
            checkreadok = fscanf(param_file,"%i", &temp_time_discrete);
            check_if_cannot_read_param(checkreadok, "temp_time_discrete");
            
            checkreadok = fscanf(param_file,"%i", &temp_time_discrete);
            check_if_cannot_read_param(checkreadok, "temp_time_discrete");
            
            for(g = 0; g < N_GENDER; g++){
                for(ac = 0; ac < (MAX_AGE - AGE_CHIPS + 1); ac++){
                    if(chips_round < NCHIPSROUNDS){
                        checkreadok = fscanf(param_file, "%lg", 
                            &(param_local->chips_params->prop_tested_by_chips_per_timestep[g][ac][i][chips_round]));
                        check_if_cannot_read_param(checkreadok,
                            "params->chips_params->prop_tested_...step[g][ac][i][chips_round]");

                        /* Update cumulative counters: */
                        param_local->chips_params->prop_tested_by_chips_in_round[g][ac][chips_round] += param_local->chips_params->prop_tested_by_chips_per_timestep[g][ac][i][chips_round];
                    }else{
                        checkreadok = fscanf(param_file, "%lg", &(param_local->chips_params->prop_tested_by_chips_per_timestep_posttrial[g][ac][i]));
                        check_if_cannot_read_param(checkreadok,
                            "params->chips_params->prop_tested_..._posttrial[g][ac][i]");

                        /* Update cumulative counters: */
                        param_local->chips_params->prop_tested_by_chips_in_round_posttrial[g][ac] += param_local->chips_params->prop_tested_by_chips_per_timestep_posttrial[g][ac][i];
                    }
                }
            }
        }
        /* Check there's nothing remaining in the file; otherwise there's a mismatch btw the
        number of timesteps in the chips round we calculate and the number of lines of data*/
        char buffer[100];
        int firsterror = 1;
        while(!feof(param_file)){
            /* Only print error statement once. */
            if(firsterror == 1){
                printf("Error: extra data in %s\n", param_file_name);
                firsterror=0;
            }
            fgets(buffer, sizeof buffer, param_file);
            fputs(buffer, stdout);
        }
        if(firsterror == 0){
            printf("Exiting\n");
            fclose(param_file);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        /* If no problems, close chips uptake parameter file */
        fclose(param_file);
    }
}

void copy_chips_params( parameters **allrunparameters, int n_runs){
    int i, g, ac, i_run, chips_round, p;
    /* We assume that the CHiPs parameters are fixed from one run to the next: */
    for (i_run = 1; i_run<n_runs; i_run++){
        for (p=0; p<NPATCHES; p++){
            for (g=0; g<N_GENDER;g++){
                for (ac = 0; ac<(MAX_AGE-AGE_CHIPS+1); ac++){
                    for (chips_round=0;chips_round<NCHIPSROUNDS;chips_round++){
                        allrunparameters[p][i_run].chips_params->prop_tested_by_chips_in_round[g][ac][chips_round] = allrunparameters[p][0].chips_params->prop_tested_by_chips_in_round[g][ac][chips_round];
                        for(i=0; i<allrunparameters[p][0].chips_params->n_timesteps_per_round[chips_round];i++){
                            allrunparameters[p][i_run].chips_params->prop_tested_by_chips_per_timestep[g][ac][i][chips_round] = allrunparameters[p][0].chips_params->prop_tested_by_chips_per_timestep[g][ac][i][chips_round];
                        }
                    }
                    /* Now copy posttrial inputs. */
                    allrunparameters[p][i_run].chips_params->prop_tested_by_chips_in_round_posttrial[g][ac] = allrunparameters[p][0].chips_params->prop_tested_by_chips_in_round_posttrial[g][ac];
                    for(i=0; i<allrunparameters[p][0].chips_params->n_timesteps_per_round_posttrial;i++){
                        allrunparameters[p][i_run].chips_params->prop_tested_by_chips_per_timestep_posttrial[g][ac][i] = allrunparameters[p][0].chips_params->prop_tested_by_chips_per_timestep_posttrial[g][ac][i];
                    }


                }
            }
        }
    }
}


/* Read in the PC enrolment parameters. */
void read_pc0_enrolment_params(char *patch_tag, int community_id, parameters *allrunparameters, int n_runs, int p){
    int i_run;
    double temp_time_continuous;
    int temp_timestep_discrete, temp_year_discrete;
    int g, ap, i_pc_category, i;    /* Indices for gender, age group, HIV subgroup (HIV-, HIV+ aware, HIV+ unaware) and the timestep within a given PC round. */
    int pc_round; /* Index for the PC round. In this file we input PC0 numbers only *This will be true until the end of the trial*. */
    /* This is a local temp variable we use so we don't have to keep writing allparameters+i_run (or equivalently &allparameters[i_run]). */
    parameters *param_local;
    FILE *param_file;
    int checkreadok;
    /*******************  adding path before file name ********************/
    char param_file_name[LONGSTRINGLENGTH];
    char temp_tag[100];
    char buffer[100];


    int pc_enrolment_round = 0; /* We are reading in PC0 enrollee data only, not PC12N/24N. */

    /********************************************************************/
    /*******************  Read in PC enrolment data ********************/
    /********************************************************************/
    i_run=0; /* We store the outputs in the i_run=0 parameter struct, and later copy it to every other run. */
    param_local = allrunparameters + i_run; /* No need for the i_run to be added - but just keep here for clarity. */



    for (pc_round=0;pc_round<NPC_ROUNDS;pc_round++){

        strncpy(param_file_name,patch_tag,LONGSTRINGLENGTH);   // Adding path before file name.
        sprintf(temp_tag,"PC%i_community%i.csv",pc_round,community_id);   // NOTE - we use pc_round+1 so the round files are labelled 1,2,3,4.
        strcat(param_file_name, temp_tag);

        /******************* opening parameter file ********************/
        if ((param_file=fopen(param_file_name,"r"))==NULL){    // Opening parameter file - print error if file not found.
            printf("Cannot open %s",param_file_name);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }else{
            if(VERBOSE_OUTPUT==1)
                printf("PC enrolment parameters read from: %s:\n",param_file_name);
        }


        /******************* read parameters ********************/


        /* The first line of this file is a header - the text below reads in just that line and throws it away.
         * The * instructs fscanf (all of the scanf family, in fact) to parse the data out as presented in the format string,
         * but NOT to store it at any target address (which is good, because there is none provided in an argument list).
         * the [^\n] means take anything except a newline, so ALL data will be consumed up to (but not including) the newline.
         *  Finally, the final \n means "and consume (and ignore) the newline" (which we just stopped at when fulfilling the
         *  prior format spec). Btw, the NULL isn't required in the argument list. */
        //fscanf(param_file, "%*[^\n]\n", NULL);
        fscanf(param_file, "%*[^\n]\n");



        /* Now read in the data from the given file: */
        i = 0;
        while(!feof(param_file)){

            /* We don't need these numbers - they are to make the csv files more readable. */
            checkreadok = fscanf(param_file,"%lg",&temp_time_continuous);
            if(feof(param_file)){
                /* Previous timestep was the last one. */
                param_local->PC_params->PC_END_TIMESTEP[pc_round] = temp_timestep_discrete;
                param_local->PC_params->PC_END_YEAR[pc_round] =  temp_year_discrete;
                break;
            }
            check_if_cannot_read_param(checkreadok,"btemp_time_continuous");
            checkreadok = fscanf(param_file,"%d",&temp_year_discrete);
            check_if_cannot_read_param(checkreadok,"temp_year_discrete");
            checkreadok = fscanf(param_file,"%d",&temp_timestep_discrete);
            check_if_cannot_read_param(checkreadok,"temp_timestep_discrete");

            /* Now start reading data.
             * First row after the header row gives the start time of the first round (note this is PC0 hence the '0' index). */
            if(i==0){
                param_local->PC_params->PC_START_TIMESTEP[pc_round] = temp_timestep_discrete;
                param_local->PC_params->PC_START_YEAR[pc_round] =  temp_year_discrete;
            }

            for (i_pc_category=0; i_pc_category<N_PC_HIV_STRATA; i_pc_category++){
                for (g=0; g<N_GENDER;g++){
                    for (ap = 0; ap<(AGE_PC_MAX-AGE_PC_MIN+1); ap++){
                        checkreadok = fscanf(param_file,"%d",&(param_local->PC_params->number_seen_by_PC_per_timestep[g][ap][i_pc_category][i][pc_round]));
                        if (checkreadok<1){
                            printf("ERROR: Format of PC enrolment file %s is not correct. Exiting\n",param_file_name);
                            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                            fflush(stdout);
                            exit(1);
                        }

                        //printf("%d ",param_local->PC_params->number_seen_by_PC_per_timestep[g][ap][i_pc_category][i][pc_round]);

                    }
                }
            }
            //printf("\n");
            i = i+1;
        }

        param_local->PC_params->n_timesteps_per_round[pc_round] = (param_local->PC_params->PC_END_YEAR[pc_round]-param_local->PC_params->PC_START_YEAR[pc_round])*N_TIME_STEP_PER_YEAR + param_local->PC_params->PC_END_TIMESTEP[pc_round] - param_local->PC_params->PC_START_TIMESTEP[pc_round]+1;
        
        // Calculate PC midpoints from input data
        int midpoint_timestep = (param_local->PC_params->PC_START_TIMESTEP[pc_round] +
            param_local->PC_params->n_timesteps_per_round[pc_round]/2); 
        
        param_local->PC_params->PC_MIDPOINT_TIMESTEP[pc_round] = 
            midpoint_timestep % N_TIME_STEP_PER_YEAR;
        
        param_local->PC_params->PC_MIDPOINT_YEAR[pc_round] =
            param_local->PC_params->PC_START_YEAR[pc_round] + 
            midpoint_timestep / N_TIME_STEP_PER_YEAR;
        
        /* For debugging - check that total number of people seen agrees with the csv files, and check right duration of round. */
        if (param_local->PC_params->n_timesteps_per_round[pc_round]!=i){
            printf("ERROR: Mismatch in number of timesteps in PC round %i = %i %i. Exiting\n",pc_round,param_local->PC_params->n_timesteps_per_round[pc_round],i);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        //      int Nseen = 0;
        //      for (i_pc_category=0; i_pc_category<N_PC_HIV_STRATA; i_pc_category++){
        //          for (g=0; g<N_GENDER;g++)
        //              for (ap = 0; ap<(AGE_PC_MAX-AGE_PC_MIN+1); ap++)
        //                  Nseen += param_local->PC_params->number_seen_in_PC_round[g][ap][i_pc_category][pc_round];
        //      }
        //printf("Number seen in patch %s = %i\n",patch_tag,Nseen);
        //printf("number men age 18, cat 0 = %i\n",param_local->PC_params->number_seen_in_PC_round[MALE][0][0][0]);

        /* Now check that there was nothing else in the file - ie there's no mismatch between the number of timesteps in the PC round we calculate and the number of lines of data we have. */
        int firsterror = 1;
        while (!feof(param_file)){
            /* Only print error statement once. */
            if (firsterror==1){
                printf("Error -extra data in %s\n",param_file_name);
                firsterror=0;
            }
            fgets(buffer, sizeof buffer, param_file);
            fputs(buffer, stdout);
        }
        if (firsterror==0){
            printf("Exiting\n");
            fclose(param_file);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }

        /* If no problems, then continue. */
        fclose(param_file);     // Closing PC uptake parameter file
        //printf("(pc_round=%i): Number of timesteps = %i . Start = %i %i. End = %i %i\n",pc_round,param_local->PC_params->n_timesteps_per_round[0], param_local->PC_params->PC_START_YEAR[0], param_local->PC_params->PC_START_TIMESTEP[0], param_local->PC_params->PC_END_YEAR[0], param_local->PC_params->PC_END_TIMESTEP[0]);
    }


    /* Set counters to zero: */
    for (g=0; g<N_GENDER;g++)
        for (ap = 0; ap<(AGE_PC_MAX-AGE_PC_MIN+1); ap++)
            for (i_pc_category=0; i_pc_category<N_PC_HIV_STRATA; i_pc_category++)
                param_local->PC_params->number_enrolled_in_PC_round[g][ap][i_pc_category][pc_enrolment_round] = 0;

    /* Cohort size is the same throughout (we deal with dropouts by ignoring some people in the cohort). */
    param_local->PC_params->cohort_size = 0;

    /* Now use the baseline PC0 to add up totals who should be seen in this cohort throughout the trial (if retention is 100%): */
    pc_round = 0;
    for (i_pc_category=0; i_pc_category<N_PC_HIV_STRATA; i_pc_category++){
        for (g=0; g<N_GENDER;g++){
            for (ap = 0; ap<(AGE_PC_MAX-AGE_PC_MIN+1); ap++){
                for (i=0; i<param_local->PC_params->n_timesteps_per_round[pc_round]; i++)
                    param_local->PC_params->number_enrolled_in_PC_round[g][ap][i_pc_category][pc_enrolment_round] += param_local->PC_params->number_seen_by_PC_per_timestep[g][ap][i_pc_category][i][pc_round];
                param_local->PC_params->cohort_size += param_local->PC_params->number_enrolled_in_PC_round[g][ap][i_pc_category][pc_enrolment_round];
            }
        }
    }

    /* Only need to worry about PC in patch 0: */
    if (p==0)
        printf("Cohort size = %i\n",param_local->PC_params->cohort_size);
    //printf("Number of timesteps = %i . Start = %i %i. End = %i %i\n",param_local->PC_params->n_timesteps_per_round[0], param_local->PC_params->PC_START_YEAR[0], param_local->PC_params->PC_START_TIMESTEP[0], param_local->PC_params->PC_END_YEAR[0], param_local->PC_params->PC_END_TIMESTEP[0]);

}

void copy_pc_params( parameters **allrunparameters, int n_runs){
    int i, g, ap, i_run, i_pc_category, pc_round, p, pc_enrolment_round;
    //printf("Running copy_pc_params\n");
    /* We assume that the PC parameters are fixed from one run to the next: */
    for (i_run = 1; i_run<n_runs; i_run++){
        for (p=0; p<NPATCHES; p++){
            allrunparameters[p][i_run].PC_params->cohort_size = allrunparameters[p][0].PC_params->cohort_size;
            for (g=0; g<N_GENDER;g++){
                for (ap = 0; ap<(AGE_PC_MAX-AGE_PC_MIN+1); ap++){
                    for (i_pc_category=0; i_pc_category<N_PC_HIV_STRATA; i_pc_category++){
                        for (pc_enrolment_round=0;pc_enrolment_round<NPC_ENROLMENTS;pc_enrolment_round++){
                            allrunparameters[p][i_run].PC_params->number_enrolled_in_PC_round[g][ap][i_pc_category][pc_enrolment_round] = allrunparameters[p][0].PC_params->number_enrolled_in_PC_round[g][ap][i_pc_category][pc_enrolment_round];
                        }
                    }
                }
            }
            for (pc_round=0;pc_round<NPC_ROUNDS;pc_round++){
                allrunparameters[p][i_run].PC_params->PC_retention[pc_round] = allrunparameters[p][0].PC_params->PC_retention[pc_round];
                for (i_pc_category=0; i_pc_category<N_PC_HIV_STRATA; i_pc_category++){
                    for (g=0; g<N_GENDER;g++){
                        for (ap = 0; ap<(AGE_PC_MAX-AGE_PC_MIN+1); ap++){
                            for(i=0; i<allrunparameters[p][0].PC_params->n_timesteps_per_round[pc_round];i++){
                                allrunparameters[p][i_run].PC_params->number_seen_by_PC_per_timestep[g][ap][i_pc_category][i][pc_round] = allrunparameters[p][0].PC_params->number_seen_by_PC_per_timestep[g][ap][i_pc_category][i][pc_round];
                            }
                        }
                    }
                }
                allrunparameters[p][i_run].PC_params->n_timesteps_per_round[pc_round] = allrunparameters[p][0].PC_params->n_timesteps_per_round[pc_round];
                allrunparameters[p][i_run].PC_params->PC_START_TIMESTEP[pc_round] = allrunparameters[p][0].PC_params->PC_START_TIMESTEP[pc_round];
                allrunparameters[p][i_run].PC_params->PC_START_YEAR[pc_round] =  allrunparameters[p][0].PC_params->PC_START_YEAR[pc_round];
                allrunparameters[p][i_run].PC_params->PC_END_TIMESTEP[pc_round] = allrunparameters[p][0].PC_params->PC_END_TIMESTEP[pc_round];
                allrunparameters[p][i_run].PC_params->PC_END_YEAR[pc_round] =  allrunparameters[p][0].PC_params->PC_END_YEAR[pc_round];
                
                allrunparameters[p][i_run].PC_params->PC_MIDPOINT_TIMESTEP[pc_round] = allrunparameters[p][0].PC_params->PC_MIDPOINT_TIMESTEP[pc_round];
                allrunparameters[p][i_run].PC_params->PC_MIDPOINT_YEAR[pc_round] =  allrunparameters[p][0].PC_params->PC_MIDPOINT_YEAR[pc_round];
            }
        }
    }

}
/* Reads in dates of PC12,24,36 and expected retention rate. */
void read_pc_future_params(char *patch_tag, parameters *allrunparameters, int n_runs)
{
    FILE *param_file;
    int pc_round;   /* Index for PC round number. */
    //double PC_TIME; /* Temporary store of the (decimal) time when PC round starts/ends - used when we convert to discrete time. */

    int i_run;
    /* This is a local temp variable we use so we don't have to keep writing allparameters+i_run (or equivalently &allparameters[i_run]). */
    parameters *param_local;
    int checkreadok;
    /*******************  adding path before file name ********************/
    char param_file_name[LONGSTRINGLENGTH];

    strncpy(param_file_name,patch_tag,LONGSTRINGLENGTH);
    strcat(param_file_name, "PC.csv");


    /******************* opening parameter file ********************/
    if ((param_file=fopen(param_file_name,"r"))==NULL){
        printf("Cannot open %s\n",param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    else
        if(VERBOSE_OUTPUT==1)
            printf("PC parameters read from: %s:\n",param_file_name);

    /* The first line of this file is a header - the text below reads in just that line and throws it away.
     * The * instructs fscanf (all of the scanf family, in fact) to parse the data out as presented in the format string,
     * but NOT to store it at any target address (which is good, because there is none provided in an argument list).
     * the [^\n] means take anything except a newline, so ALL data will be consumed up to (but not including) the newline.
     *  Finally, the final \n means "and consume (and ignore) the newline" (which we just stopped at when fulfilling the
     *  prior format spec). */
    fscanf(param_file, "%*[^\n]\n");


    /******************* read parameters from each line i_run ********************/
    for (i_run = 0; i_run<n_runs; i_run++){
        param_local = allrunparameters + i_run;


        //      /* Times run from PC12 to PC36 (round 1 to round 3). */
        //      for(pc_round=1;pc_round<NPC_ROUNDS; pc_round++){
        //          checkreadok = fscanf(param_file,"%lg",&PC_TIME);
        //          check_if_cannot_read_param(checkreadok,"PC start time");
        //          param_local->PC_params->PC_START_YEAR[pc_round] = (int) PC_TIME;
        //          param_local->PC_params->PC_START_TIMESTEP[pc_round] = (int) ((PC_TIME - param_local->PC_params->PC_START_YEAR[pc_round])*N_TIME_STEP_PER_YEAR);
        //
        //          checkreadok = fscanf(param_file,"%lg",&PC_TIME);
        //          check_if_cannot_read_param(checkreadok,"PC end time");
        //          param_local->PC_params->PC_END_YEAR[pc_round] = (int) PC_TIME;
        //          param_local->PC_params->PC_END_TIMESTEP[pc_round] = (int) ((PC_TIME - param_local->PC_params->PC_END_YEAR[pc_round])*N_TIME_STEP_PER_YEAR);
        //
        //          param_local->PC_params->n_timesteps_per_round[pc_round] = (param_local->PC_params->PC_END_YEAR[pc_round]-param_local->PC_params->PC_START_YEAR[pc_round])*N_TIME_STEP_PER_YEAR + param_local->PC_params->PC_END_TIMESTEP[pc_round] - param_local->PC_params->PC_START_TIMESTEP[pc_round];
        //
        //          printf("param_local->PC_params->n_timesteps_per_round[%i] = %i\n",pc_round,param_local->PC_params->n_timesteps_per_round[pc_round]);
        //          //printf("PC start/stop times round %d = %i %i, %i %i\n",pc_round,param_local->PC_params->PC_START_YEAR[pc_round],param_local->PC_params->PC_START_TIMESTEP[pc_round],param_local->PC_params->PC_END_YEAR[pc_round],param_local->PC_params->PC_END_TIMESTEP[pc_round]);
        //
        //      }

        for(pc_round=0;pc_round<NPC_ROUNDS; pc_round++){
            checkreadok = fscanf(param_file,"%lg",&(param_local->PC_params->PC_retention[pc_round]));
            check_if_cannot_read_param(checkreadok,"param_local->PC_retention");

            //printf("PC retention round %i = %lf\n",pc_round,param_local->PC_params->PC_retention[pc_round]);
        }


    }

    fclose(param_file);

    return;
}


void read_initial_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    /* Read initial condition parameter values from param_processed_patch$p_init.csv
    
    Parameters
    ----------
    file_directory: pointer to string
        Ptr to name of the dir where the parameter file is stored
    param: a pointer to the "parameters" struct
        Structure where parameter values will be stored once read in from file
    
    Returns
    -------
    Nothing; reads in parameter values and populates a parameters struct
    
    */
    
    FILE *param_file;

    /* Indices for age group (0..N_AGE-1), risk and gender. */
    int ag, r, g;
    
    double checksum;
    double temp_int; /* Used when file input is a decimal but want to convert to an integer. */
    double temp_initial_propbyrisk[N_GENDER][N_RISK - 1];
    double temp_sum[N_GENDER];

    // A scaling factor (on log scale) which multiplies the size of the initial HIV seed 
    // (ie % of people who we seed to be HIV+).  
    double log_seed_multiplier; 
    double seed_multiplier; /* 10^log_seed_multiplier. */

    int i_run;
    
    // This is a local temp variable we use so we don't have to keep 
    // writing allparameters+i_run (or equivalently &allparameters[i_run]).
    parameters *param_local;
    int checkreadok;
    /*******************  adding path before file name ********************/
    char param_file_name[LONGSTRINGLENGTH];

    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "init.csv");

    /******************* opening parameter file ********************/
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s\n", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Init parameters read from: %s:\n", param_file_name);
        }
    }

    // Throw away the first line of the parameter file (the header)
    fscanf(param_file, "%*[^\n]\n");

    /******************* read parameters from each line i_run ********************/
    for (i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;
        
        // Read the random seed
        checkreadok = fscanf(param_file,"%lf",&temp_int);
        param_local->rng_seed = (long) floor(temp_int);
        //checkreadok = fscanf(param_file,"%ld",&(param_local->rng_seed));
        //printf("Reading rng_seed = %li\n",param_local->rng_seed);
        check_if_cannot_read_param(checkreadok,"param_local->rng_seed");

        // Read the initial population size
        checkreadok = fscanf(param_file,"%lg",&(param_local->initial_population_size));
        check_if_cannot_read_param(checkreadok,"param_local->initial_population_size");

        // Read initial proportion of individuals in each age group
        for(ag = 0; ag < N_AGE; ag++){
            checkreadok = fscanf(param_file, "%lg", &(param_local->initial_prop_age[ag]));
            check_if_cannot_read_param(checkreadok, "param_local->initial_prop_age");
        }
        
        /* Load proportion of total popn who are of gender k and risk group r. */
        for(g = 0; g < N_GENDER; g++){
            temp_sum[g] = 0.0;
        }

        for(r = 0; r < N_RISK - 1; r++){
            for(g = 0; g < N_GENDER; g++){
                checkreadok = fscanf(param_file, "%lg", &(temp_initial_propbyrisk[g][r]));
                check_if_cannot_read_param(checkreadok, "param_local->initial_prop_gender_risk");
                
                if(r == 0){
                    param_local->initial_prop_gender_risk[g][r] = temp_initial_propbyrisk[g][r];
                }else{
                    param_local->initial_prop_gender_risk[g][r] =
                         temp_initial_propbyrisk[g][r] * 
                             (1.0 - param_local->initial_prop_gender_risk[g][r - 1]);
                }
                temp_sum[g] += param_local->initial_prop_gender_risk[g][r];
            }
        }
        if(N_RISK > 2){
            for(g = 0; g < N_GENDER; g++){
                param_local->initial_prop_gender_risk[g][N_RISK - 1] = 1.0 - temp_sum[g];
            }
        }

        /* Code if we want to fix male/female proportions to be the same: */
//      if (i_run==0) /* Only print out warning once. */
//          printf("WARNING: Setting female risk proportion to be same as male proportion by hand for now. May want to change this later. \n");
//      for (r=0; r<N_RISK; r++)
//          param_local->initial_prop_gender_risk[FEMALE][r] = param_local->initial_prop_gender_risk[MALE][r];


        //for (r=0; r<N_RISK; r++){
        //  for (g=0; g<N_GENDER; g++){
        //      printf("param_local->initial_prop_gender_risk[g=%i][r=%i] = %lf\n",g,r,param_local->initial_prop_gender_risk[g][r]);
        //  }
        //}

        // Load proportion of gender-risk specific population who are 
        // HIV+ at time of HIV introduction
        for(r = 0; r < N_RISK; r++){
            for(g = 0; g < N_GENDER; g++){
                checkreadok = fscanf(param_file, "%lg", 
                    &(param_local->initial_prop_infected_gender_risk[g][r]));
                    
                check_if_cannot_read_param(checkreadok,
                    "param_local->initial_prop_infected_gender_risk");
            }
        }

        checkreadok = fscanf(param_file, "%lg", &(log_seed_multiplier));
        check_if_cannot_read_param(checkreadok, "log_seed_multiplier");
        seed_multiplier = pow(10, log_seed_multiplier);
        
        /* Now scale up each % seeded: */
        for(r = 0; r < N_RISK; r++){
            for(g = 0; g < N_GENDER; g++){
                param_local->initial_prop_infected_gender_risk[g][r] =
                    param_local->initial_prop_infected_gender_risk[g][r] * seed_multiplier;
            }
        }
        
        checkreadok = fscanf(param_file, "%lf", &temp_int);
        param_local->n_years_HIV_seeding = (int) floor(temp_int);
        check_if_cannot_read_param(checkreadok, "param_local->n_years_HIV_seeding");

	/* Proportion of population seeded to be HSV-2 positive at start_time_hsv2: */
        checkreadok = fscanf(param_file,"%lg",&(param_local->initial_prop_hsv2infected));
        check_if_cannot_read_param(checkreadok,"param_local->initial_prop_hsv2infected");

	
        ////// This is for debugging: 
        ////// Make sure proportions add to 1.
        ////// Shall we do it this way or have only 2 of the 3 read in a file and automatically calculating the third one? Could then print the third one to warn the user

        for(g = 0; g < N_GENDER; g++){
            checksum = 0.0;
            for(r = 0; r < N_RISK; r++){
                checksum += param_local->initial_prop_gender_risk[g][r];
            }
            if(fabs(checksum - 1.0) > 1e-12){
                printf("Sum of proportions of initial population by risk is not 1 %f.\n", checksum-1.0);
                printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                fflush(stdout);
                exit(1);
            }
        }
        checksum = 0;
        for(ag = 0; ag < N_AGE; ag++){
            checksum += param_local->initial_prop_age[ag];	    
        }
        if(fabs(checksum-1.0>1e-12)){
            printf("Sum of proportions of initial population by age is not 1 = %f.\n", checksum);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        /* End of debugging. */


	
    }
    fclose(param_file);
    return;
}


void read_PrEP_uptake_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    int i_run;
    double t_prep_start_background;
    double t_prep_start_intervention = 9999.0;  /* Dummy initial value set far into future... */

    t_prep_start_background = read_PrEP_background_uptake_params(patch_tag, allrunparameters, n_runs);

    if (RUN_PREP_INTERVENTION==1)
	t_prep_start_intervention = read_PrEP_intervention_uptake_params(patch_tag, allrunparameters, n_runs);
	
    double t_prep_start;
    if (RUN_PREP_INTERVENTION==1){
	if (t_prep_start_background<t_prep_start_intervention)
	    t_prep_start = t_prep_start_background;
	else
	    t_prep_start = t_prep_start_intervention;
    }
    else
	t_prep_start = t_prep_start_background;

    printf("Time of PrEP start = %lf\n",t_prep_start);
    for (i_run = 0; i_run < n_runs; i_run++)
	allrunparameters[i_run].COUNTRY_T_PrEP_START = t_prep_start;

}

double read_PrEP_background_uptake_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    /* Read in PrEP background uptake/adherence parameters
    
    This function reads the PrEP parameters related to background (non-intervention) PrEP.  It populates the following array:
        parameters->PrEP_background_params
    
    Arguments
    ---------
    patch_tag : pointer to a char
    allrunparameters : pointer to an array of parameters structs
    
    Returns
    -------
    Nothing; populates parameters->PrEP_background_params
    */


    FILE * param_file;
    char param_file_name[LONGSTRINGLENGTH];
    int ap, i_run, checkreadok;

    double time_start_prep_undiscretised;
    
    // Temp variable to avoid having to write allparameters+i_run 
    //(or equivalently &allparameters[i_run]).
    parameters *param_local;

    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "PrEP_background.csv");

    // Open parameter file
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("PrEP background parameters read from: %s:\n", param_file_name);
        }
    }
    // Throw away the first line of the parameter file (the header line)
    fscanf(param_file, "%*[^\n]\n");

    // Read parameters from each line (i_run) of the file
    for(i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;
	    
        checkreadok = fscanf(param_file, "%lg", &time_start_prep_undiscretised);
        check_if_cannot_read_param(checkreadok, "start_time_PrEP_background");
        
        // Here we want start_time_hiv to be equal to a timestep value (this avoids issues when
        // seeding infections, where new_infections looks for the person in age_index[] using the
        // index calculated using the infection time. If not a timestep then that may produce the
        // wrong index and the person is not found (so HIV status not updated etc).
        
        // The time when PrEP becomes available:
	param_local->PrEP_background_params->year_start_background = (int) floor(time_start_prep_undiscretised);
	param_local->PrEP_background_params->timestep_start_background = (int) floor((time_start_prep_undiscretised - param_local->PrEP_background_params->year_start_background)*N_TIME_STEP_PER_YEAR);

	for (ap=0; ap<=(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND); ap++){
	    checkreadok = fscanf(param_file,"%lg", &(param_local->PrEP_background_params->proportion_seen_by_age[ap]));
	    check_if_cannot_read_param(checkreadok, "param_local->PrEP_background_params->proportion_seen_by_age[ap]");
	}
	
        checkreadok = fscanf(param_file, "%lg", &(param_local->PrEP_background_params->p_becomes_PrEP_adherent_background));
        check_if_cannot_read_param(checkreadok, "param_local->PrEP_background_params->p_becomes_PrEP_adherent_background");

        checkreadok = fscanf(param_file, "%lg", &(param_local->PrEP_background_params->p_semiadherent_acts_covered_background));
        check_if_cannot_read_param(checkreadok, "param_local->PrEP_background_params->p_semiadherent_acts_covered_background");
    }
    fclose(param_file);

    return time_start_prep_undiscretised;
}
    

double read_PrEP_intervention_uptake_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    /* Read in PrEP intervention uptake/adherence parameters
    
    This function reads the PrEP parameters related to intervention  PrEP.  It populates the following array:
        parameters->PrEP_intervention_params
    
    Arguments
    ---------
    patch_tag : pointer to a char
    allrunparameters : pointer to an array of parameters structs
    
    Returns
    -------
    Nothing; populates parameters->PrEP_intervention_params
    */

    

    FILE * param_file;
    char param_file_name[LONGSTRINGLENGTH];
    int ap, i_run, checkreadok;


    double time_start_prep_undiscretised;
    double temp;
    // Temp variable to avoid having to write allparameters+i_run 
    //(or equivalently &allparameters[i_run]).
    parameters *param_local;

    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "PrEP_intervention.csv");

    // Open parameter file
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("PrEP intervention parameters read from: %s:\n", param_file_name);
        }
    }
    // Throw away the first line of the parameter file (the header line)
    fscanf(param_file, "%*[^\n]\n");

    // Read parameters from each line (i_run) of the file
    for(i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;

       	    
        checkreadok = fscanf(param_file, "%lg", &time_start_prep_undiscretised);
        check_if_cannot_read_param(checkreadok, "start_time_PrEP_intervention");
        
        // For simplicity we want start_time_PrEP_intervention to be equal to a timestep value. Here we discretise time:
	param_local->PrEP_intervention_params->year_start_intervention = (int) floor(time_start_prep_undiscretised);
	param_local->PrEP_intervention_params->timestep_start_intervention = (int) floor((time_start_prep_undiscretised - param_local->PrEP_intervention_params->year_start_intervention)*N_TIME_STEP_PER_YEAR);

	for (ap=0; ap<=(MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION); ap++){
	    checkreadok = fscanf(param_file,"%lg", &(param_local->PrEP_intervention_params->proportion_seen_by_age[ap]));
	    check_if_cannot_read_param(checkreadok, "param_local->PrEP_intervention_params->proportion_seen_by_age[ap]");
	}

	/* Read in as float, then recast as int: */
	checkreadok = fscanf(param_file, "%lg", &(temp));
        check_if_cannot_read_param(checkreadok, "param_local->PrEP_intervention_params->n_timesteps_in_round");
	param_local->PrEP_intervention_params->n_timesteps_in_round = (int) temp;


	if (param_local->PrEP_intervention_params->n_timesteps_in_round>N_PREP_INTERVENTION_TIMESTEPS){
	    printf("Error: parameter PrEP_intervention_params->n_timesteps_in_round MUST be less than N_PREP_INTERVENTION_TIMESTEPS=%i, otherwise the array PrEP_intervention_sample->number_to_see_per_timestep is too small, causing a memory error.\nExiting\n",N_PREP_INTERVENTION_TIMESTEPS);
	    fflush(stdout);
	    exit(1);
	}

        checkreadok = fscanf(param_file, "%lg", &(param_local->PrEP_intervention_params->p_becomes_PrEP_adherent_intervention));
        check_if_cannot_read_param(checkreadok, "param_local->PrEP_intervention_params->p_becomes_PrEP_adherent_intervention");

        checkreadok = fscanf(param_file, "%lg", &(param_local->PrEP_intervention_params->p_semiadherent_acts_covered_intervention));
        check_if_cannot_read_param(checkreadok, "param_local->PrEP_intervention_params->p_semiadherent_acts_covered_intervention");
    }
    fclose(param_file);

    return time_start_prep_undiscretised;
}
    


void read_cascade_barrier_params(char *patch_tag, parameters *allrunparameters, int n_runs){
    /* Read initial condition parameter values from param_processed_patch$p_init.csv
    
    Parameters
    ----------
    file_directory: pointer to string
        Ptr to name of the dir where the parameter file is stored
    param: a pointer to the "parameters" struct
        Structure where parameter values will be stored once read in from file
    
    Returns
    -------
    Nothing; reads in parameter values and populates a parameters struct
    
    */
    
    FILE *param_file;

    int i_run;
    int i_barrier_group; /* Loop over the different sub-populations for that particular prevention method. */
    // This is a local temp variable we use so we don't have to keep 
    // writing allparameters+i_run (or equivalently &allparameters[i_run]).
    parameters *param_local;
    int checkreadok;
    /*******************  adding path before file name ********************/
    char param_file_name[LONGSTRINGLENGTH];

    strncpy(param_file_name, patch_tag, LONGSTRINGLENGTH);
    strcat(param_file_name, "barriers.csv");

    /******************* opening parameter file ********************/
    if((param_file = fopen(param_file_name, "r")) == NULL){
        printf("Cannot open %s\n", param_file_name);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }else{
        if(VERBOSE_OUTPUT == 1){
            printf("Barrier parameters read from: %s:\n", param_file_name);
        }
    }

    // Throw away the first line of the parameter file (the header)
    fscanf(param_file, "%*[^\n]\n");

    /******************* read parameters from each line i_run ********************/
    for (i_run = 0; i_run < n_runs; i_run++){
        param_local = allrunparameters + i_run;
	checkreadok = fscanf(param_file,"%lg",&(param_local->barrier_params.t_start_prevention_cascade_intervention));

	/* Read in the pre-intervention values - post-intervention is calculated afterwards with a multiplier. */
	for (i_barrier_group=0; i_barrier_group<N_VMMC_PREVENTIONBARRIER_GROUPS; i_barrier_group++){	    
	    checkreadok = fscanf(param_file,"%lg",&(param_local->barrier_params.p_use_VMMC_present[i_barrier_group][0]));
	    check_if_cannot_read_param(checkreadok,"param_local->barrier_params.p_use_VMMC_present[][]");
	    //printf("i=%i after param_local->barrier_params.p_use_VMMC_present[i_barrier_group][i_barrier_intervention] = %lf\n",i_barrier_group,param_local->barrier_params.p_use_VMMC_present[i_barrier_group][i_barrier_intervention]);
	    
	}

	

	    
	for (i_barrier_group=0; i_barrier_group<N_PrEP_PREVENTIONBARRIER_GROUPS; i_barrier_group++){	    
	    checkreadok = fscanf(param_file,"%lg",&(param_local->barrier_params.p_use_PrEP[i_barrier_group][0]));
	    check_if_cannot_read_param(checkreadok,"param_local->barrier_params.p_use_PrEP[][]");
	}
	    
	for (i_barrier_group=0; i_barrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_barrier_group++){	    
	    checkreadok = fscanf(param_file,"%lg",&(param_local->barrier_params.p_use_cond_casual_present[i_barrier_group][0]));
	    check_if_cannot_read_param(checkreadok,"param_local->barrier_params.p_use_cond_casual_present[][]");
	}

	/* For now, we keep casual and long-term condom use the same (as Louisa's analysis cannot distinguish). */
	for (i_barrier_group=0; i_barrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_barrier_group++){
	    param_local->barrier_params.p_use_cond_LT_present[i_barrier_group][0] = param_local->barrier_params.p_use_cond_casual_present[i_barrier_group][0];
	    //checkreadok = fscanf(param_file,"%lg",&(param_local->barrier_params.p_use_cond_LT_present[i_barrier_group][i_barrier_intervention]));
	    //check_if_cannot_read_param(checkreadok,"param_local->barrier_params.p_use_cond_LT_present[][]");
	}

    
	/**** Now the intervention: */
	double rr_HIV_prevention_cascade_intervention;

	
	checkreadok = fscanf(param_file,"%lg",&(rr_HIV_prevention_cascade_intervention));
	check_if_cannot_read_param(checkreadok,"rr_HIV_prevention_cascade_intervention");

	/* Can't be bothered to make this one an array :-) */
	double rr_HIV_prevention_cascade_intervention_condom = rr_HIV_prevention_cascade_intervention;
	double rr_HIV_prevention_cascade_intervention_PrEP[N_PrEP_PREVENTIONBARRIER_GROUPS] = {0,rr_HIV_prevention_cascade_intervention,rr_HIV_prevention_cascade_intervention,0,0,rr_HIV_prevention_cascade_intervention,rr_HIV_prevention_cascade_intervention,0,0,0};
	double rr_HIV_prevention_cascade_intervention_VMMC[N_VMMC_PREVENTIONBARRIER_GROUPS] = {0,rr_HIV_prevention_cascade_intervention,rr_HIV_prevention_cascade_intervention,0,0};

	
	for (i_barrier_group=0; i_barrier_group<N_VMMC_PREVENTIONBARRIER_GROUPS; i_barrier_group++){	    
	    param_local->barrier_params.p_use_VMMC_present[i_barrier_group][1] = 1 - (1-rr_HIV_prevention_cascade_intervention_VMMC[i_barrier_group]) * (1-param_local->barrier_params.p_use_VMMC_present[i_barrier_group][0]);
	}
	    
	for (i_barrier_group=0; i_barrier_group<N_PrEP_PREVENTIONBARRIER_GROUPS; i_barrier_group++){	    
	    param_local->barrier_params.p_use_PrEP[i_barrier_group][1] = 1 - (1-rr_HIV_prevention_cascade_intervention_PrEP[i_barrier_group]) * (1.0-param_local->barrier_params.p_use_PrEP[i_barrier_group][0]);
	}

	/* No need to change condom use groups: */
	for (i_barrier_group=0; i_barrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_barrier_group++){	    
	    param_local->barrier_params.p_use_cond_casual_present[i_barrier_group][1] = 1 - (1-rr_HIV_prevention_cascade_intervention_condom) * (1-param_local->barrier_params.p_use_cond_casual_present[i_barrier_group][0]);
	}

	/* For now, we keep casual and long-term condom use the same (as Louisa's analysis cannot distinguish). */
	for (i_barrier_group=0; i_barrier_group<N_COND_PREVENTIONBARRIER_GROUPS; i_barrier_group++){
	    param_local->barrier_params.p_use_cond_LT_present[i_barrier_group][1] = param_local->barrier_params.p_use_cond_casual_present[i_barrier_group][1];
	    //checkreadok = fscanf(param_file,"%lg",&(param_local->barrier_params.p_use_cond_LT_present[i_barrier_group][i_barrier_intervention]));
	    //check_if_cannot_read_param(checkreadok,"param_local->barrier_params.p_use_cond_LT_present[][]");
	}

	/* Now generate the lookup table for increased condom use in existing partnerships at the start of the intervention: */
	generate_intervention_increase_in_partnership_condom_use_lookuptable(&(param_local->barrier_params));

	/* Now populate param->barrier_params.p_use_cond_casual/LT and p_use_VMMC for each run: */
	update_condomrates(param_local->start_time_simul, param_local);

	/* This is the 'adjustment' for the fact that not everyone in a given priority population will be eligible for VMMC (because either already circumcised or HIV+). */
	double dummy_adjustment[i_VMMC_PREVENTIONBARRIER_OLD_M-i_VMMC_PREVENTIONBARRIER_YOUNG_M+1] = {1,1};
	update_VMMCrates(param_local->start_time_simul, param_local, dummy_adjustment);

    }




    fclose(param_file);
    return;
}


long get_python_seed(char *file_directory){
    /* Read in the seed used by python to generate the LHC.
    
    Arguments
    ---------
    file_directory : char
        Name of dir where parameter file `python_seed.txt` is stored.
    
    Returns
    -------
    seed : int
        The seed within the file `python_seed.txt`.  
    */
    long seed;
    FILE *PYTHON_SEED_FILE;
    PYTHON_SEED_FILE = fopen("", "r");
    char python_seed_filename[LONGSTRINGLENGTH];
    strncpy(python_seed_filename, file_directory, LONGSTRINGLENGTH);
    
    /* Adds a / or \ as needed if working in directory other than current local dir. */
    add_slash(python_seed_filename);
    strcat(python_seed_filename, "python_seed.txt");
    
    /******************* opening parameter file ********************/
    if((PYTHON_SEED_FILE = fopen(python_seed_filename, "r")) == NULL){
        printf("Cannot open python_seed.txt");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    // Read the seed
    int checkreadok = fscanf(PYTHON_SEED_FILE, "%ld", &seed);
    
    /******************* closing parameter file ********************/
    fclose(PYTHON_SEED_FILE);
    
    if(checkreadok < 1){
        printf("Could not read python seed from python_seed.txt");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    return(seed);
}
