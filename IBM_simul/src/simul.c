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

#include "simul.h"
#include "demographics.h"
#include "partnership.h"
#include "utilities.h"
#include "hiv.h"
#include "hsv.h"
#include "init.h"
#include "interventions.h"
#include "structures.h"
#include "fitting.h"
#include "debug.h"
#include "output.h"
#include "pc.h"
#include "prevention_cascades.h"
#include "mihpsa_output.h"

/************************************************************************/
/******************************** functions *****************************/
/************************************************************************/


/*
Functions within this file: 

carry_out_processes()
    Function that is called by the main() function within main.c.  
carry_out_partnership_processes_by_time_step()
    Carry out processes associated with partnership dissolution (non-death related), partnership
    formation and HIV acquisition between serodiscordant partnerships.  
carry_out_processes_by_patch_by_time_step()
    
*/


int carry_out_processes(int t0, fitting_data_struct *fitting_data, patch_struct *patch,
    all_partnerships * overall_partnerships, output_struct *output, int rng_seed_offset, 
    int rng_seed_offset_PC, debug_struct *debug, file_struct *file_data_store, 
    int scenario_flag, int i_run){
    /* Main function for carrying out 
    
    
    Arguments
    ---------
    
    t0 : int
    fitting_data : pointer to fitting_data_struct structure
    patch : pointer to an array of patch_struct
    overall_partnerships : pointer to an array of all_partnerships structures
    output : pointer to an array of output_struct
    rng_seed_offset : int
        Offset for the integer used to seed the random number generator in GSL
    rng_seed_offset_PC : int
        Offset for the integer used to seed the random number generator in GSL used for PC sampling
    debug : pointer to a debug_struct
    file_data_store : pointer to a file_struct
    scenario_flag : int
        For PopART this is an indicator for whether the counterfactual is being run or not (1 Yes, 0 No)
	For Manicaland this is an indicator as to what barriers of PrEP/VMMC/Condoms exist (scenario_flag is a 3 digit number here).
    
    
    Returns
    -------
    Integer; 
    
    */
    
    int p, t_step, fit_flag;
    int icd4, i, r;
    double t;


    
    // Reset the counters for newly infected individuals
    for(p = 0; p < NPATCHES; p++){
        set_population_count_one_year_zero(patch[p].n_newly_infected);
        set_population_count_one_year_zero(patch[p].n_newly_infected_hsv2);
        patch[p].n_newly_infected_total = 0;
        patch[p].n_newly_infected_total_from_outside = 0;
        patch[p].n_newly_infected_total_from_acute = 0;
        patch[p].n_newly_infected_total_pconly = 0;
        patch[p].n_newly_infected_total_from_outside_pconly = 0;
        patch[p].n_newly_infected_total_from_acute_pconly = 0;
        
        for(r = 0; r < N_RISK; r++){
            patch[p].n_newly_infected_total_by_risk[r] = 0;
            patch[p].n_newly_infected_total_by_risk_pconly[r] = 0;
            patch[p].n_died_from_HIV_by_risk[r] = 0;
        }
        
        for(icd4 = 0; icd4 < NCD4; icd4++){
            patch[p].py_n_positive_on_art[icd4] = 0;
            patch[p].py_n_positive_not_on_art[icd4] = 0;
        }
    }

    long npop_check;
    int g, ai, aa;

    for(p = 0; p < NPATCHES; p++){
        npop_check = 0;
        for(g = 0; g < N_GENDER; g++){
            for(aa = AGE_ADULT; aa < MAX_AGE; aa++){
                ai = aa + patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index;
                while(ai > (MAX_AGE - AGE_ADULT - 1)){
                    ai = ai - (MAX_AGE - AGE_ADULT);
                }
                npop_check += patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
            }
            npop_check += patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
        }

    }



    /* This is the 'adjustment' for the fact that not everyone in a given priority population will be eligible for VMMC (because either already circumcised or HIV+). Note - this is slow, so put it outside the t_step loop *so that it is calculated annually*)
     */
    double vmmc_rate_adjustment[NPATCHES][i_VMMC_PREVENTIONBARRIER_OLD_M-i_VMMC_PREVENTIONBARRIER_YOUNG_M+1];
    for(p = 0; p < NPATCHES; p++){
	get_VMMC_rate_adjustment_foralreadycirc_hivpos((double) t0, patch, p, vmmc_rate_adjustment[p]);
    }

    
    for(t_step = 0; t_step < N_TIME_STEP_PER_YEAR; t_step++){

	t = t0 + t_step*TIME_STEP;
        if((t == TIME_PC0 && WRITE_PARTNERSHIPS_AT_PC0 == 1) && (PRINT_EACH_RUN_OUTPUT == 1)){
            sweep_through_all_and_compute_distribution_lifetime_and_lastyear_partners(patch, overall_partnerships, t0, t_step, output);
            write_distr_n_lifetime_partners_and_n_partners_lastyear(patch, file_data_store);
        }

        // When CHiPs starts for the first time (round 1) we reseed the random number generator.
        // This allows us to see how stochasticity during PopART affects impact.  
        if (SETTING==SETTING_POPART){
	    if((t0 == patch[0].param->CHIPS_START_YEAR[0]) &&
	       (t_step==patch[0].param->CHIPS_START_TIMESTEP[0])){
		gsl_rng_set(rng, patch[0].param->rng_seed + rng_seed_offset);
	    }
        }


	/* For Zimbabwe we want partner numbers to change over time.
	   For other settings, we currently don't do this. */
	if(patch[0].country_setting==ZIMBABWE){
	    /* Only update once we have data (i.e. once cohort starts): 
	       Pre-cohort, value is set to be at cohort value in read_partnership_params(). */
	    if(t>(patch[0].param->COHORTYEAR[0]+TIME_STEP*patch[0].param->COHORTTIMESTEP[0])){
		update_number_new_partners(t,patch);
	    }

	    /* Allows hazard to vary over time, once epidemic starts: */
	    if(t>=patch[0].param->start_time_hiv)
		update_time_varying_hazard_allpatches(t,patch);

	    
	    if(t>=1989){
		
		if(i_run==0 && t==1989.0)
		    printf("Condom use now changes at each timestep\n");
		/* This function varies condom use uptake. 
		   It incorporates the intervention (if it happens). */
		for(p = 0; p < NPATCHES; p++)
		    update_condomrates(t,patch[p].param);
	    }


	    if(t>=patch[0].param->COUNTRY_ART_START){
		for(p = 0; p < NPATCHES; p++)
		    set_probability_starts_ART_if_positive_and_eligible(t, patch[p].param);
	    }
	    
	    
	    if(t>=patch[0].param->COUNTRY_VMMC_START){
		if(i_run==0 && t==patch[0].param->COUNTRY_VMMC_START && MIHPSA_MODULE==1)
		    printf("Warning: Overriding p_use_VMMC for MIHPSA project\n");

		for(p = 0; p < NPATCHES; p++){
		    //get_VMMC_rate_adjustment_foralreadycirc_hivpos(t, patch, p, vmmc_rate_adjustment);
		    /* This function varies VMMC uptake on an annual basis. If MIHPSA_MODULE==1 it  overrides the values of p_use_VMMC_present[] set in input.c.*/		    
		    update_VMMCrates(t,patch[p].param,vmmc_rate_adjustment[p]);
		}
	    }

	}


        // Carry out main processes
        for(p = 0; p < NPATCHES; p++){
	    //printf("Running carry_out_processes_by_patch_by_time_step() for p=%i,t=%i %i\n",p,t0,t_step);
	    //fflush(stdout);
            fit_flag = carry_out_processes_by_patch_by_time_step(t_step, t0, fitting_data, patch,
								 p, overall_partnerships, output, rng_seed_offset, rng_seed_offset_PC, debug, i_run,
								 file_data_store, scenario_flag);
        }
	

	
        carry_out_partnership_processes_by_time_step(t_step, t0,patch, overall_partnerships, output,
						     debug, file_data_store, scenario_flag);
        
        // store_timestep_outputs() is called at the end of this timestep, 
        // so time = t+TIME_STEP.*/
        for(p = 0; p < NPATCHES; p++){
            if(
                (WRITE_EVERYTIMESTEP == 1) && 
                ((t0 + t_step*TIME_STEP) >= patch[p].param->start_time_hiv) &&
                (t_step%OUTPUTTIMESTEP == (OUTPUTTIMESTEP - 1))
            ){
                /* Stores data for all age groups. */
                store_timestep_outputs(patch, p ,t0 + (t_step + 1)*TIME_STEP, output, 0, t0, t_step);
                
                /* Stores data for PC age groups only. */
		if (SETTING==SETTING_POPART)
		    store_timestep_outputs(patch, p , t0 + (t_step + 1)*TIME_STEP, output, 1, t0, t_step);
                
                // Store age-specific timestep outputs
                if(TIMESTEP_AGE == 1){
                    /* Stores data for all age groups. */
                    store_timestep_age_outputs(patch, p ,t0 + (t_step + 1)*TIME_STEP, output, 0);
                    
                    /* Stores data for PC age groups only. */
                    store_timestep_age_outputs(patch, p , t0 + (t_step + 1)*TIME_STEP, output, 1);
                }
                
                if(WRITE_COST_EFFECTIVENESS_OUTPUT == 1){
                    // Loop through all individuals in the current patch; count person-years events
                    for(i = 0; i < patch[p].id_counter; i++){
                        if(patch[p].individual_population[i].cd4 != DEAD){
                        
                            // Check that person is HIV positive
                            if(patch[p].individual_population[i].HIV_status > UNINFECTED){
                            
                                // Find the CD4 category of the person in question
                                icd4 = patch[p].individual_population[i].cd4;
                            
                                // Check that the person is on ART
                                if(patch[p].individual_population[i].ART_status > ARTNAIVE &&
                                    patch[p].individual_population[i].ART_status < ARTDROPOUT){
				   
                                
                                    patch[p].py_n_positive_on_art[icd4] += TIME_STEP;
                                }else{ // Otherwise, the person is not on ART
                                
                                    patch[p].py_n_positive_not_on_art[icd4] += TIME_STEP;
                                }
                            }
                        }
                    }
                }
                
                if(WRITE_ART_STATUS_BY_AGE_SEX == 1){
                    store_art_status_by_age_sex(patch, p, t0 + (t_step + 1)*TIME_STEP, output);
                }
	   
            }
        }
        
        // Store PC outputs that are a cross-section (prev, cascade, etc) to calibration file.
	if (SETTING==SETTING_POPART){
	    if(WRITE_CALIBRATION == 1){
            
		int pc_round;
            
		for(p = 0; p < NPATCHES; p++){
                
		    // Store the "person-timesteps" for the given PC round
		    save_person_timesteps_pc(patch, p, output, t0, t_step);
                
		    // Check we're at the start of a PC round.  
		    for(pc_round = 0; pc_round < NPC_ROUNDS; pc_round++){
                    
			if(t0 == patch[p].param->PC_params->PC_MIDPOINT_YEAR[pc_round] &&
			   t_step == patch[p].param->PC_params->PC_MIDPOINT_TIMESTEP[pc_round]){
			    
			    save_calibration_outputs_pc(patch, p, output, t0, t_step);
			}
		    }
		}
	    }
        }


	if (SETTING==SETTING_MANICALAND){
	    if(WRITE_CALIBRATION == 1){
		int r;
		for(p = 0; p < NPATCHES; p++){
		    r = is_manicaland_cohort_time(t0,t_step, patch[p].param); // -1 if not time for a cohort snapshot. 
		    if(r>=0){
			store_calibration_outputs_cohortpopulation_snapshot(patch, p, output, r);
		    }
		}
	    }

	    /* Output HIV prevention cascade barriers for patch 0 at specific timesteps. */

	    if(DEBUG_HIV_PREVENTION_CASCADES==1){
		if(t0 + t_step*TIME_STEP==2018 || t0 + t_step*TIME_STEP==2020 || t0 + t_step*TIME_STEP==2022){
		    //printf("Writing individual HIV cascades at t=%lf\n",t0+t_step*TIME_STEP);
		    write_individual_HIVpreventioncascade_barriers(t0+t_step*TIME_STEP, patch, 0,i_run);
		}
	    }
	    
	}

	/* MIHPSA outputs are stored from 1990 onwards, in the timestep 1 July. */
	//if(MIHPSA_MODULE==1){
	// This file is now some additional outputs - useful for diagnostics, but not needed for every year from start of simulation.
	
	if(t0>=1990){
	    /* This corresponds to 1 July in the year (note - the .0 is to avoid integer division): */
	    if(t_step==(int) round((191.0/365)*N_TIME_STEP_PER_YEAR))
		for(p = 0; p < NPATCHES; p++)
		    store_annual_outputs_MIHPSA(patch, p, output, t0 + t_step*TIME_STEP);
	}
	//}
	
    }
    
    // At the end of the year, check that everyone who should be in a given list is in that list
    t_step = N_TIME_STEP_PER_YEAR - 1;
    
    if(SWEEP_THROUGH_TO_CHECK_LISTS == 1){
        // if in check mode then loop over every individual to check that they are where they
        // should be 1/ in the list of susceptibles in serodiscordant partnership and 2/ in the
        // list of available partners
        sweep_through_all_and_check_lists_serodiscordant_and_available_partners(patch, 
                overall_partnerships, t0, t_step);
    }
    
    if(SWEEP_THROUGH_TO_CHECK_N_PARTNERS_OUTSIDE_AND_N_HIVPOS_PARTNERS_AND_N_HIVPOS_PARTNERS_OUTSIDE == 1){
        sweep_through_all_and_check_n_partners_outside_n_HIVpos_partners_and_n_HIVpos_partners_outside(patch, overall_partnerships, t0, t_step);
    }
    
    if(CHECK_AGE_AND_RISK_ASSORTATIVITY == 1){
        sweep_through_all_and_check_age_and_risk_of_partners (patch, overall_partnerships, t0, 
                t_step, debug);
    }

    // Use to check population counters are all consistent - i.e. we're updating them all correctly. Most recent check 13 Jan 2020 to check introduction of MTCT is OK.
    if (CHECK_POPULATION_SIZE_CONSISTENCY==1){
	if (t0+t_step*TIME_STEP<1901 && i_run==1)
	    printf("Warning: checking population size function count_population_size_three_ways() is active. This slows down the code\n");
	for (p=0; p<NPATCHES; p++)
	    count_population_size_three_ways(patch, p, t0 + t_step*TIME_STEP);
    }
    
    if(fit_flag == 0){
        return 0;
    }
    return 1;
}


void carry_out_partnership_processes_by_time_step(int t_step, int t0, patch_struct *patch,
    all_partnerships * overall_partnerships, output_struct *output, debug_struct *debug,
						  file_struct *file_data_store, int scenario_flag){
    /* Carry out processes associated with partnership dissolution (non-death related), partnership
    formation and HIV acquisition between serodiscordant partnerships.  
    
    This is a "high-level" function, in that is mainly calls other others to update the above 
    processes.  This function is called by carry_out_processes().  
    
    
    Arguments
    ---------
    t_step : int
    t0 : int
    patch : pointer to a patch_struct structure
    overall_partnerships : pointer to a all_partnerships structure
    output : pointer to a output_struct structure
    debug : pointer to a debug_struct structure
    file_data_store : pointer to a file_struct structure
    
    
    Returns
    -------
    Nothing
    
    */
    
    
    long k;
    double t;
    int p, q;

     /* Current time in yrs. */
    t = t0 + t_step * TIME_STEP;

    /*************************************************/
    /* Partnership dissolution (not forced by death) */
    /*************************************************/

    /* Loop through all planned breakups in this timestep: */
    for(k = 0; k < overall_partnerships->n_planned_breakups[N_TIME_STEP_PER_YEAR*(t0 - patch[0].param->start_time_simul) + t_step]; k++){
        
        /* Breaking up an individual partnership: */
        /* Automatically done in breakup() function: putting each partner is put back into the list
        of available partners and  partnership is removed from list of serodiscordant partnerships
        (if applicable). */
        breakup(t, overall_partnerships->planned_breakups[N_TIME_STEP_PER_YEAR*(t0 - patch[0].param->start_time_simul) + t_step][k], 
            overall_partnerships);
    }
    
    /************************************************************************/
    /* Partnership formation */
    /************************************************************************/
    
    /* Updates the elements of n_population based on the population size of the smallest entity
    (gender/age/risk).  This is needed before drawing partnerships because we need an up-to-date
    prop_pop_per_risk_per_gender. */
    for(p = 0; p < NPATCHES; p++){
        calcul_population(patch[p].n_population, patch[p].n_population_stratified);
    }
    
    /* Now draw new partnerships (ie allocate people with available partnerships to these
    partnerships) and update all applicable lists (available partners, partnerships, serodiscordant
    couples (if applicable) and schedule a future breakup. */
    
    for(p = 0; p < NPATCHES; p++){
        
        //q = 1-p; // for between patches partnerships only
        //q = p; // for within patches partnerships only
        
        for(q = 0; q < NPATCHES; q++){
            
            /* Draw partnerships between females in patch p and males in patch q */
            draw_new_partnerships(t, overall_partnerships, patch, patch[p].param, p, q, debug,
                file_data_store);
        }
    }
    
    /************************************************************************/
    /* HIV transmission within partnerships */
    /************************************************************************/
    
    // Loop through all susceptible individuals who are in serodiscordant partnerships
    for(k = 0; k < overall_partnerships->n_susceptible_in_serodiscordant_partnership[0]; k++){
        
        // If the susceptible individual in the serodiscordant partnership is alive
        if(overall_partnerships->susceptible_in_serodiscordant_partnership[k]->cd4 > DEAD){
            
            hiv_acquisition(overall_partnerships->susceptible_in_serodiscordant_partnership[k], t,
                patch,
                overall_partnerships->susceptible_in_serodiscordant_partnership[k]->patch_no, 
                overall_partnerships, output, debug, file_data_store, t0, t_step);
            
        }else{
            printf("Here problem: trying to make a dead person acquire HIV. ID = %li\n",
                overall_partnerships->susceptible_in_serodiscordant_partnership[k]->id);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        //The list of serodiscordant partnerships is updated accordingly automatically within
        // the function hiv_acquisition().
    }


    /************************************************************************/
    /* HSV-2 transmission within partnerships */
    /************************************************************************/
    
    // Loop through all HSV2-susceptible individuals who are in HSV2-serodiscordant partnerships
    for(k = 0; k < overall_partnerships->n_susceptible_in_hsv2serodiscordant_partnership[0]; k++){
        
        // If the susceptible individual in the HSV-2 serodiscordant partnership is alive (yes we check being alive by looking at the cd4 characteristic!)
        if(overall_partnerships->susceptible_in_hsv2serodiscordant_partnership[k]->cd4 > DEAD){
            
            hsv2_acquisition(overall_partnerships->susceptible_in_hsv2serodiscordant_partnership[k], t, patch, overall_partnerships->susceptible_in_hsv2serodiscordant_partnership[k]->patch_no, overall_partnerships, output, debug, file_data_store, t0, t_step);
            
        }else{
            printf("Here problem: trying to make a dead person acquire HSV-2. ID = %li\n",
                overall_partnerships->susceptible_in_hsv2serodiscordant_partnership[k]->id);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        //The list of HSV-2 serodiscordant partnerships is updated accordingly automatically within the function hsv2_acquisition().
    }

}


int carry_out_processes_by_patch_by_time_step(int t_step, int t0, fitting_data_struct *fitting_data,
        patch_struct *patch, int p, all_partnerships * overall_partnerships, output_struct *output,
					      int rng_seed_offset, int rng_seed_offset_PC, debug_struct *debug, int i_run,
        file_struct *file_data_store, int scenario_flag){
    /* This function calls a range of processes used in the simulation
    
    In the following order, this function calls the following processes: 
        1. Set up PC sample
        2. Set up CHiPs sample
        3. HIV testing
        4. Births and deaths
        5. HIV introduction
        6. HIV events
        7. HIV care cascade events
        8. Carry out PC visits (if necessary)
        9. PopART intervention (or post-trial TasP)
        10. Carry out VMMC events
    
    Arguments
    --------
    t_step : int
        
    t0 : int
        
    fitting_data : pointer to a fitting_data_struct structure
        
    patch : pointer to a patch_struct structure
        
    p : int
        Patch number (indexed from zero)
    overall_partnerships : pointer to a all_partnerships structure
        
    output : pointer to a output_struct structure
        
    rng_seed_offset : int
        Offset for the integer used to seed the random number generator
    rng_seed_offset_PC : int
        Offset for the integer used to seed the random number generator used for the PC sampling
    debug : pointer to a debug_struct structure
        
    file_data_store : pointer to a file_struct structure
        
    scenario_flag : int
        For PopART: indicator of whether this is for a counterfactual run or not.  This is used to determine when to run the CHiPs intervention.  
	For Manicaland: this determines which of the PrEP/VMMC/condom barriers exist.
    
    */
    
    int chips_round ,pc_round, pc_enrolment_round, chips_start_timestep;
    double t;
    int aa, ai, g;
    long k;
    
    /* This stores the return value of fit_data() - it is 1 if there was no fitting or if the run
    passed all the fits during the year, and 0 if there was a fit criterion which was not satisfied.
    This allows us to see if a run should be terminated early or not. */
    int fit_flag, POPART_FINISHED;
    
    /* Current time in yrs. */
    t = t0 + t_step * TIME_STEP;


    // Determine if the current time is within the final CHiPs round or not.  The variable
    // `POPART_FINISHED` takes value 1 after the end of the final CHiPs round. Once
    // PopART finishes assume that test-and-treat continues like the last CHiPs round.
  
    if (SETTING==SETTING_POPART){

	if(
	   (t0 > patch[p].param->CHIPS_END_YEAR[NCHIPSROUNDS - 1]) ||
	   ((t0 == patch[p].param->CHIPS_END_YEAR[NCHIPSROUNDS - 1]) &&
	    (t_step > patch[p].param->CHIPS_END_TIMESTEP[NCHIPSROUNDS - 1])
	    )
	   ){
	    POPART_FINISHED = 1;
	}else{
	    POPART_FINISHED = 0;
	}
    }
    else
	POPART_FINISHED = 1;	

    
    if (SETTING==SETTING_POPART){
	// Write chips data to file if we're in a period when CHiPs are active
	// (and at the start of the year)
	if(
	   t0 >= patch[p].param->CHIPS_START_YEAR[0] &&
	   t_step == 0 &&
	   PRINT_EACH_RUN_OUTPUT == 1){
	    write_chips_data_annual(patch ,p, t0, t_step, POPART_FINISHED, file_data_store);
	}
    }

    /********************************************/
    /*      1. Set up PC sample                 */
    /********************************************/
    
    if (SETTING==SETTING_POPART){
	if(RUN_PC == 1){
	    /* We only create a PC sample in patch 0. */
	    if(p == 0){
		/* Only create PC sample during the PC years. */
		if(
		   t0 >= patch[p].param->PC_params->PC_START_YEAR[0] &&
		   t0 < patch[p].param->PC_params->PC_END_YEAR[NPC_ROUNDS - 1]
		   ){
		    /* Code this way to allow multiple rounds of enrolment (PC0, PC12N, etc). */
		    pc_round = 0;
                
		    for(pc_round = 0; pc_round < NPC_ROUNDS; pc_round++){
			if(
			   t0 == patch[p].param->PC_params->PC_START_YEAR[pc_round] &&
			   t_step==patch[p].param->PC_params->PC_START_TIMESTEP[pc_round]
			   ){
			    if(pc_round < NPC_ENROLMENTS){
				gsl_rng_set(rng, 
					    patch[0].param->rng_seed + rng_seed_offset + rng_seed_offset_PC);
                            
				if(VERBOSE_OUTPUT == 1){
				    printf("Creating PC round %i sample with offset %i at t=%6.4f\n",
					   pc_round, rng_seed_offset + rng_seed_offset_PC, 
					   t0 + t_step*TIME_STEP);
				    fflush(stdout);
				}
                            
				create_popart_pc_sample(patch, patch[p].age_list, patch[p].PC_sample,
							patch[p].param, pc_round, p);
                            
				gsl_rng_set(rng, patch[0].param->rng_seed + rng_seed_offset +
					    patch[p].param->PC_params->PC_START_YEAR[0]);
			    }
			}
		    } // for(pc_round = 0; pc_round < NPC_ROUNDS; pc_round++)
		}
	    } // if(p == 0)
	} // if(RUN_PC == 1)
    }    
    /********************************************/
    /*      2. Set up CHiPs sample              */
    /********************************************/

    if (SETTING==SETTING_POPART){
	// Set up CHiPs sample for the given CHiPs round if needed
	if(patch[p].trial_arm == ARM_A || patch[p].trial_arm == ARM_B){

	    // The code below means we can control exactly when each CHiPS round starts. 
	    // Note - the "if" statement means we only establish a sampling frame once at the start of
	    // each round
        
	    if(is_start_of_chips_round(patch[p].param, t0, t_step, patch[p].trial_arm) == 1){
		//printf("Calling chips_round() at %i %i for arms A or B\n", t0, t_step);
            
		chips_round = get_chips_round(patch[p].param, t0, t_step);

		if(chips_round >= 0 && chips_round < NCHIPSROUNDS){
		    chips_start_timestep = patch[p].param->CHIPS_START_TIMESTEP[chips_round];
		}else if(chips_round == CHIPSROUNDPOSTTRIAL){
		    chips_start_timestep = patch[p].param->CHIPS_START_TIMESTEP_POSTTRIAL;
		}else{
		    printf("ERROR: Unknown chips_round value =%d. Exiting\n",chips_round);
		    printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
		    fflush(stdout);
		    exit(1);
		}
            
		if(t_step == chips_start_timestep){
		    if(VERBOSE_OUTPUT == 1){
			printf("PopART round carried out at time t=%f\n",t);
			fflush(stdout);
		    }
		    POPART_SAMPLING_FRAME_ESTABLISHED = 1;
		    create_popart_chips_samples(patch[p].age_list, patch[p].chips_sample,
						patch[p].param, chips_round, p);
		}
            
		// Sets the value of VISITED_BY_CHIPS_THISROUND to be FALSE. Note that because CHiPs
		// rounds are not one year we need this to be reset when we set up the chips sampling
		// frame.  
		if(WRITE_DEBUG_CHIPS_STATES == 1){
		    reset_annual_chips_visit_counter(patch[p].age_list);
		}
	    }
	}
    
	// In the case of an external patch (arm C like but with PopART) assume PopART-like household
	// intervention adopted from end of PopART onwards - for non-counterfactual only.  
	if(
	   (patch[p].trial_arm == ARM_C) && 
	   (scenario_flag == NOT_COUNTERFACTUAL_RUN)
	   ){
	    if(is_start_of_chips_round(patch[p].param, t0, t_step, patch[p].trial_arm) == 1){
            
		//printf("Calling chips_round() at %i %i for arm C\n", t0, t_step);
		chips_round = CHIPSROUNDPOSTTRIAL;
            
		if(t_step == patch[p].param->CHIPS_START_TIMESTEP_POSTTRIAL){
		    if(VERBOSE_OUTPUT == 1){
			printf("PopART occurring in external (non-popart) patch at time ");
			printf("t = %f using post-trial data\n", t);
			fflush(stdout);
		    }
		    POPART_SAMPLING_FRAME_ESTABLISHED = 1;  // This shouldn't matter.
                
		    create_popart_chips_samples(patch[p].age_list, patch[p].chips_sample,
						patch[p].param, chips_round, p);
		}
	    }
	}
    
	// In the case of a counterfactual run where we would like CHiPs rollout post-trial to occur
	if(
	   (patch[p].trial_arm == ARM_C) && 
	   (scenario_flag == IS_COUNTERFACTUAL_RUN) &&
	   (ALLOW_COUNTERFACTUAL_ROLLOUT == 1)
	   ){
	    if(is_start_of_chips_round(patch[p].param, t0, t_step, patch[p].trial_arm) == 1){
            
		if(POPART_FINISHED == 1 && t0 >= T_ROLLOUT_CHIPS_EVERYWHERE){
		    if(VERBOSE_OUTPUT == 1){
			printf("Post-round CHiPs rollout carried out at time t=%f\n",t);
			fflush(stdout);
		    }
		    chips_round = CHIPSROUNDPOSTTRIAL;
                
		    POPART_SAMPLING_FRAME_ESTABLISHED = 1;
		    create_popart_chips_samples(patch[p].age_list, patch[p].chips_sample,
						patch[p].param, chips_round, p);
		}
	    }
	}
    }
    
    /********************************************/
    /*      3. HIV testing                      */
    /********************************************/
    
    // Has to be called before deaths_natural_causes() or individual_death_AIDS() in given t.s. 
    
    if(t >= patch[p].param->COUNTRY_HIV_TEST_START && t < (patch[p].param->COUNTRY_HIV_TEST_START + TIME_STEP) && DO_HIV_TESTING == 1){
        if(VERBOSE_OUTPUT == 1){
            printf("Setting up initial HIV cascade events\n");
        }
        if(HIVTESTSCHEDULE == 0){
            // This function will go through all people currently alive and schedule HIV tests for
            // them at some point in the future.
            draw_initial_hiv_tests(patch[p].param, patch[p].age_list, t, patch[p].cascade_events, 
                patch[p].n_cascade_events, patch[p].size_cascade_events);
        }else{
	    if(VERBOSE_OUTPUT)
		printf("Setting up initial HIV cascade events at t=%lf\n",t);
		
            /// The difference between this function and the draw_initial_hiv_tests() function is
            // that these are drawn up to a set time, when HIV tests are redrawn
	    // Note - only need to call this if the first test is before 2005 - otherwise the following years if statement will capture this. 
	    if (patch[p].param->COUNTRY_HIV_TEST_START<=2004)
		draw_hiv_tests(patch[p].param, patch[p].age_list, t0, patch[p].cascade_events, patch[p].n_cascade_events, patch[p].size_cascade_events, patch[p].country_setting);
        }
    }
    // Again, this has to be called before deaths_natural_causes() or individual_death_AIDS() 
    // in the given timestep
    if((HIVTESTSCHEDULE == 1) && (t0 >= 2005) && (t_step == 0) && DO_HIV_TESTING == 1){
         // Schedule these annually starting in 2007:
        
        //printf("Drawing new HIV test events at time %f\n",t);
        draw_hiv_tests(patch[p].param, patch[p].age_list, t0, patch[p].cascade_events,
            patch[p].n_cascade_events, patch[p].size_cascade_events, patch[p].country_setting);
    }
    
    if(PRINT_DEBUG_DEMOGRAPHICS == 1){
        
        int male_i = patch[p].age_list->age_list_by_gender[MALE]->youngest_age_group_index;
        int female_i = patch[p].age_list->age_list_by_gender[FEMALE]->youngest_age_group_index;
        
        printf("Number in age 13 age group is %li\n",
            patch[p].age_list->age_list_by_gender[MALE]->number_per_age_group[male_i] +
            patch[p].age_list->age_list_by_gender[FEMALE]->number_per_age_group[female_i]);
        
        printf("******************Time = %f %li\n", t, 
        patch[p].age_list->age_list_by_gender[MALE]->number_oldest_age_group +
        patch[p].age_list->age_list_by_gender[FEMALE]->number_oldest_age_group);
        
        fflush(stdout);
    }
    
    /************************************************************************/
    /* 4. Births and deaths (natural causes) */
    /************************************************************************/
    // MTCT TO BE ADDED + ACCOUNT FOR BIRTH AND DEATHS IN LIST OF AVAILABLE PARTNERS + PARTNERSHIPS
    // When someone becomes 13 they enter
    //          the age list
    //          the list of available partners
    //          the list of HIV+ people if HIV+ (list not existing yet)
    // When someone dies, they are removed from
    //          the age list
    //          the list of available partners
    //          the list of HIV+ people if they are HIV+
    //          the list of serodiscordant partnerships if applicable
    //          the list of pregnant women if applicable
    //          their partnerships are dissolved
    
    // This function draws people to die from each year-age group.  For each individual chosen to
    // die it calls functions to update all lists which featured this person (age list,
    // partnerships, serodiscordant people, planned breakups, available partners).  
     // Finally for each dead person we set CD4=-2 (note -2 is defined as DEAD in constants.h) so
    // we know they're dead. */


    deaths_natural_causes(t, patch, p, overall_partnerships, file_data_store);


    if(PRINT_DEBUG_DEMOGRAPHICS == 1){
        printf("Making new adults at time t = %f\n", t);
    }
    // Making new adults (from the child_population) and adding them to the individual_population,
    // n_population, and other lists (available partners, etc.). */
    make_new_adults(t, t_step, patch, p, overall_partnerships, scenario_flag);


    
    // Add children who have just been born to the child population
    // the number of kids is randomly drawn based on fertility rate, current adult pop size, etc
    add_new_kids(t, patch, p);
    if (t>2000 && (t-floor(t)<1e-9) && (p==0))
	count_number_by_age_gender_risk_cascade_cd4(patch, p, t);


    /// Validation of age groups:
    //validate_ages_based_on_age_group(age_list, 13, t);

    //print_demographics(individual_population, n_population, t);
    //print_population(n_population);
    //print_number_by_age(age_list);

    /************************************************************************/
    /* Planned pregnancies */
    /************************************************************************/
    // TO BE ADDED
    // ONCE TIME TO DISSOLUTION IS DECIDED, DEPENDING ON AGES AND RISKS OF 2 PARTNERS, DRAW NUMBER OF KIDS AND TIMES OF CONCEPTION
    // FORGET THIS FOR NOW, KEEP FOR VERSION 1.1

    /************************************************************************/
    /* Partnership dissolution and formation are handled outside the patch at global level */
    /************************************************************************/


    /************************************************************************/
    /* 5. HIV introduction (at time param->start_time_hiv) */
    /************************************************************************/

    // This loop seeds HIV once in the simulation at t = param->start_time_hiv
    // Initial cases are drawn according to the params `initial_prop_infected_gender_risk`
    // in the parameters structure
    if(
((t0 >= patch[p].param->start_time_hiv_discretised_year) &&
(t0 <= (patch[p].param->start_time_hiv_discretised_year + patch[p].param->n_years_HIV_seeding))) &&
(t_step==patch[p].param->start_time_hiv_discretised_timestep)
    ){
        
        // For all but the age group 80+ (which is in a separate part of the age_list struct)
        for(g = 0; g < N_GENDER; g++){
            
            // Seed HIV infection between these ages only.
            for(aa = (YOUNGEST_AGE_SEED_WITH_HIV - AGE_ADULT);
                aa <= (OLDEST_AGE_SEED_WITH_HIV - AGE_ADULT); 
                aa++){
                
                // ai is the index of the array age_list->number_per_age_group of the age group
                // of people you want to be dead
                
                ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;
                
                while(ai > (MAX_AGE - AGE_ADULT - 1)){
                    ai = ai - (MAX_AGE - AGE_ADULT);
                }
                
                for(k = 0; k < patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
                    k++){
                    // For each individual in that annual age group:
                    // Draw whether each person is initially HIV infected or not according to a
                    // Bernoulli trial with probability depending on gender and risk group.  
                    // Note - we could draw individuals from appropriate groups but we don't have
                    // the exact grouping we would want at present. It is not clear that it would
                    // be quicker to generate these lists and draw from them than just to do
                    // Bernoulli trials (and this method is more easy to change what probability of
                    // prevalence depends on)
                        
                    draw_initial_infection(t, 
                        patch[p].age_list->age_list_by_gender[g]->age_group[ai][k], patch, p,
                        overall_partnerships, output,file_data_store, t0, t_step);
                }
            }
            
            // For the last age group
            if(OLDEST_AGE_SEED_WITH_HIV >= MAX_AGE){
                // For each individual in that age group
                for(k = 0; k < patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group;
                    k++){
                    // draw whether initially HIV infected or not according to a Bernoulli trial
                    // with probability depending on gender and risk group */
                    draw_initial_infection(t,
                        patch[p].age_list->age_list_by_gender[g]->oldest_age_group[k], patch, p,
                        overall_partnerships, output,file_data_store, t0, t_step);
                }
            }
        }
	
        if(VERBOSE_OUTPUT == 1){
            printf("Prevalence at time t=%lf of HIV introduction\n",t);
            print_prevalence(patch[p].n_population, patch[p].n_infected_wide_age_group,
                patch[p].n_infected);
            printf("-------------------------------------\n");
            printf("-------------------------------------DEBUGGING\n");
        }
    }
    
    /******************************************************************/
    /* 6. HIV transmission within partnerships ALSO DONE AT GLOBAL LEVEL */
    /******************************************************************/
    
    /******************************************/
    /* 6. Progressing (HIV) or dying from HIV */
    /******************************************/
    
    if(t >= patch[p].param->start_time_hiv){
        
        carry_out_HIV_events_per_timestep(t, patch, p, overall_partnerships, debug,
            file_data_store);
        /*
            printf("Incident cases time step starting at %g:\n", t);
            print_population(n_newly_infected);
            printf("-------------------------------------\n");
         */
    }
    
    /******************************************/
    /* 7.       HIV care cascade              */
    /******************************************/
    
    if(t >= patch[p].param->COUNTRY_HIV_TEST_START){
        carry_out_cascade_events_per_timestep(t, patch, p, overall_partnerships, debug,
            file_data_store);
    }
    
    /*****************************************/
    /* 8. Carry out PC visits (if necessary) */
    /*****************************************/
    
    if(RUN_PC == 1){
        
        // Only do PC for patch 0; check patch is patch 0
        if(p == 0){
            
            // Find the PC round
            pc_round = get_pc_round(t0, t_step, patch, p);
            
            if(pc_round >= 0){
                
                // At the start of each PC round, reset the PC visit counter
                if(
                    (t0 == patch[0].param->PC_params->PC_START_YEAR[pc_round]) &&
                    (t_step == patch[0].param->PC_params->PC_START_TIMESTEP[pc_round])
                ){
                    reset_visit_counter(patch, p);
                }
                //printf("PC round %i  at t=%6.4f\n",pc_round,t0+t_step*TIME_STEP);
                //fflush(stdout);
                
                // Enroll new people if necessary (e.g. in PC24 we enroll PC24N)
                // NPC_ENROLMENTS is the number of rounds of PC enrollments (currently just 1)
                if(pc_round < NPC_ENROLMENTS){
                    // Enroll new people into the cohort
                    carry_out_PC_enrolment_per_timestep(t0, t_step, patch, p, pc_round);
                    
                    //printf("Enrolling people in PC round %i\n", pc_round);
                    //fflush(stdout);
                }
                
                // Now visit individuals in the PC who was enrolled in earlier rounds
                for(pc_enrolment_round = 0; 
                    pc_enrolment_round < fmin(NPC_ENROLMENTS, pc_round); 
                    pc_enrolment_round++){
                    
                    //printf("PC visit = %i for people enrolled in ", pc_round);
                    //printf("PCround = %i at t = %f\n", pc_enrolment_round, 
                    //    t0 + t_step * TIME_STEP);
                    
                    carry_out_PC_visits_per_timestep(t0, t_step, patch, p, pc_round,
                        pc_enrolment_round);
                }
                // Just after the last PC visit, output everything from the cohort. 
                // Note that because of the way get_pc_round() works
                if(
                    (t0 == patch[0].param->PC_params->PC_END_YEAR[NPC_ROUNDS - 1]) &&
                    (t_step == (patch[0].param->PC_params->PC_END_TIMESTEP[NPC_ROUNDS-1]-1)) && 
                    (PRINT_EACH_RUN_OUTPUT == 1)
                ){
                    write_pc_data(patch, p, file_data_store);
                }
            }
        }
    }
    
    /*************************************************************************/
    /* 9. Carry out PopART intervention (if necessary) (or post-popart TasP) */
    /*************************************************************************/
    if (SETTING==SETTING_POPART){    
	if(
	   (patch[p].trial_arm == ARM_A || patch[p].trial_arm == ARM_B) && 
	   (RUN_POPART == 1)
	   ){
	    int RUN_CHIPS = 1;
        
	    if( POPART_FINISHED == 1){
		if( (ROLL_OUT_CHIPS_INSIDE_PATCH == 0) && (t0 >= T_STOP_ROLLOUT_CHIPS_INSIDE_PATCH)){
		    RUN_CHIPS = 0;
		}
	    }
        
	    if(RUN_CHIPS == 1){
		if(get_chips_round(patch[p].param, t0, t_step) > CHIPSNOTRUNNING){
            
		    if(POPART_SAMPLING_FRAME_ESTABLISHED == 0){
			printf("Error -trying to start PopART before PopART sample is set up at time ");
			printf("t=%f Exiting\n", t);
			printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
			fflush(stdout);
			exit(1);
		    }
                
		    chips_round = get_chips_round(patch[p].param, t0, t_step);
                
		    carry_out_chips_visits_per_timestep(t0, t_step, patch, p, 
							chips_round, debug, output);
		}
	    }
	}
    
	/* In the case of an external patch (arm C like but with PopART) assume popart-like household
	   intervention adopted from end of PopART onwards. */
	if(
	   (patch[p].trial_arm == ARM_C) &&
	   (scenario_flag == NOT_COUNTERFACTUAL_RUN) && 
	   (RUN_POPART == 1)
	   ){
	    if(POPART_FINISHED == 1 && t0 >= T_ROLLOUT_CHIPS_EVERYWHERE){
		// To indicate we are post-trial
		chips_round = CHIPSROUNDPOSTTRIAL;
            
		if(POPART_SAMPLING_FRAME_ESTABLISHED == 0){
		    printf("Error -trying to start PopART before PopART sample is set up at time ");
		    printf("t=%f Exiting\n", t);
		    printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
		    fflush(stdout);
		    exit(1);
		}
		carry_out_chips_visits_per_timestep(t0, t_step, patch, p, chips_round, debug, output);
	    }
	}
    
	/* In the case of a counterfactual run but we would like to simulate post-trial rollout */
	if(
	   (patch[p].trial_arm == ARM_C) &&
	   (scenario_flag == IS_COUNTERFACTUAL_RUN) && 
	   (RUN_POPART == 1) &&
	   (ALLOW_COUNTERFACTUAL_ROLLOUT == 1)
	   ){
	    if(POPART_FINISHED == 1 && t0 >= T_ROLLOUT_CHIPS_EVERYWHERE){
		// To indicate we are post-trial
		chips_round = CHIPSROUNDPOSTTRIAL;
            
		if(POPART_SAMPLING_FRAME_ESTABLISHED == 0){
		    printf("Error -trying to start PopART before PopART sample is set up at time ");
		    printf("t=%f Exiting\n", t);
		    printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
		    fflush(stdout);
		    exit(1);
		}
		carry_out_chips_visits_per_timestep(t0, t_step, patch, p, chips_round, debug, output);
	    }
	}
    }    
    


    /*********************************************************************/
    /* 10a. Set up women to receive PrEP background                    */
    /*********************************************************************/

    if(MANICALAND_CASCADE==0){
	if((t>=patch[p].param->PrEP_background_params->year_start_background) && (t_step==patch[p].param->PrEP_background_params->timestep_start_background)){
	    //printf("Starting PrEP background at t=%lf\n",t);
	    schedule_PrEP_background(patch[p].age_list, patch[p].PrEP_background_sample, patch[p].param->PrEP_background_params, patch, p, t);
	}
    }
    else if(MANICALAND_CASCADE==1){
	/*Need to do this before start of PrEP otherwise older people have wrong cascade probabilities as they pass the age threshold before the start of PrEP. */
	update_PrEPbarriers_from_ageing(t, t_step, patch, p);

	if(t>=(patch[p].param->PrEP_background_params->year_start_background + patch[p].param->PrEP_background_params->timestep_start_background*TIME_STEP)){
	    sweep_pop_for_PrEP_per_timestep_given_barriers(t, patch, p);
	}
    }

    /*********************************************************************/
    /* 10b. Carry out PrEP background (if it has started)               */
    /*********************************************************************/
    
    if(t>=patch[p].param->PrEP_background_params->year_start_background+TIME_STEP*patch[p].param->PrEP_background_params->timestep_start_background){
	if(MANICALAND_CASCADE==0)
	    carry_out_PrEP_background_events_per_timestep(t_step, t, patch, p);
	else if(MANICALAND_CASCADE==1)
	    carry_out_PrEP_events_per_timestep(t,patch, p);

    }
	
    /* If not Manicaland prevention cascade project, then we can introduce an intervention (PrEP channel operating in addition to background PrEP channel).
       For Manicaland prevention cascade we do not allow this. */
    if(MANICALAND_CASCADE==0){
	if (RUN_PREP_INTERVENTION==1){
	    /***************************************************************/
	    /* 11a. Set up women to receive PrEP intervention              */
	    /***************************************************************/
	    if((t>=patch[p].param->PrEP_intervention_params->year_start_intervention) && (t_step==patch[p].param->PrEP_intervention_params->timestep_start_intervention)){
		//printf("Starting PrEP intervention at t=%lf\n",t);
		schedule_PrEP_intervention(patch[p].age_list, patch[p].PrEP_intervention_sample, patch[p].param->PrEP_intervention_params, patch, p);
		
	    }
	    
	    /***************************************************************/
	    /* 11b. Carry out PrEP intervention (if it has started)        */
	    /***************************************************************/
	    
	    if((t >= patch[p].param->PrEP_intervention_params->year_start_intervention + TIME_STEP*patch[p].param->PrEP_background_params->timestep_start_background )){
		//printf("Carrying out PrEP intervention at t=%lf\n",t);
		carry_out_PrEP_intervention_events_per_timestep(t_step, t, patch, p);
	    }
	}
    }


    //check_prep_uptake(t, t_step, patch, p);
    /************************************************************************/
    /* 12. VMMC (for Manicaland cascade - i.e. not part of HIV testing) */
    /************************************************************************/
    if(MANICALAND_CASCADE==1){
	
	update_VMMCbarriers_from_ageing(t, t_step, patch, p);
	if(t >= patch[p].param->COUNTRY_VMMC_START){
	    sweep_pop_for_VMMC_per_timestep_given_barriers(t, patch, p);
	}
    }


    /************************************************************************/
    /* 13. Condom use update (for Manicaland cascade, when reach 25/30 for F/M) */
    /************************************************************************/
    if(MANICALAND_CASCADE==1){

	
	update_condombarriers_from_ageing(t, t_step, patch, p);
    }
    

    /************************************************************************/
    /* 13. Prevention cascade intervention (for Manicaland)                 */
    /************************************************************************/
    if(MANICALAND_CASCADE==1){
	
	int year_prevention_cascade_intervention = (int) floor(patch[p].param->barrier_params.t_start_prevention_cascade_intervention);

	if(t0==year_prevention_cascade_intervention){
	    int tstep_prevention_cascade_intervention = (int) floor((patch[p].param->barrier_params.t_start_prevention_cascade_intervention-year_prevention_cascade_intervention)*N_TIME_STEP_PER_YEAR);

	    if(t_step==tstep_prevention_cascade_intervention){
		if(patch[p].param->barrier_params.i_VMMC_barrier_intervention_flag>0){
		    prevention_cascade_intervention_VMMC(t, patch, p);
		    printf("Running VMMC prevention cascade intervention %i at t=%lf. ",patch[p].param->barrier_params.i_VMMC_barrier_intervention_flag,t);
		}
		
		if(patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag>0){
		    prevention_cascade_intervention_PrEP(t, patch, p);
		    printf("Running PrEP prevention cascade intervention %i at t=%lf. ",patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag,t);
		}

		/* This function redraws condom use in *existing* partnerships where condoms are not already used. Note that an individual's preferences for condoms is automatically updated via the function update_condomrates(). */
		if(patch[p].param->barrier_params.i_condom_barrier_intervention_flag>0){
		    prevention_cascade_intervention_condom(t, patch, p);
		    printf("Running condom prevention cascade intervention %i at t=%lf\n",patch[p].param->barrier_params.i_condom_barrier_intervention_flag,t);
		}
		    

		if(VERBOSE_OUTPUT || PRINT_HIV_PREVENTION_CASCADE_INFO){
		    printf("Running prevention cascade intervention at t=%lf. ",t);
		    printf("Intervention scenarios: PrEP = %i VMMC = %i, condoms = %i \n",patch[p].param->barrier_params.i_PrEP_barrier_intervention_flag,patch[p].param->barrier_params.i_VMMC_barrier_intervention_flag,patch[p].param->barrier_params.i_condom_barrier_intervention_flag);
		}
		//printf("*** need to restart condom prevention cascade intervention***\n");
	    }
	}
    }

    
    
    /************************************************************************/
    /* 14. HSV-2 introduction (at time param->start_time_hsv2) */
    /************************************************************************/

    // This loop seeds HSV-2 once in the simulation at t = param->start_time_hsv2
    // Initial cases are drawn according to the params `initial_prop_hsv2infected in the parameters structure.
    if((t0 >= patch[p].param->start_time_hsv2_discretised_year) && (t0 <= (patch[p].param->start_time_hsv2_discretised_year)) && (t_step==patch[p].param->start_time_hsv2_discretised_timestep)){

	//printf("Seeding HSV-2 at t=%lf\n",t0+t_step*TIME_STEP);

        // For all but the age group 80+ (which is in a separate part of the age_list struct)
        for(g = 0; g < N_GENDER; g++){
            
            // Seed HSV-2 infection from age YOUNGEST_AGE_SEED_WITH_HSV2 up. 
            for(aa=(YOUNGEST_AGE_SEED_WITH_HSV2-AGE_ADULT); aa<=(MAX_AGE-AGE_ADULT); aa++){
                
                // ai is the index of the array age_list->number_per_age_group of the age group of people you want to be infected
                
                ai = patch[p].age_list->age_list_by_gender[g]->youngest_age_group_index + aa;
                
                while(ai > (MAX_AGE - AGE_ADULT - 1)){
                    ai = ai - (MAX_AGE - AGE_ADULT);
                }
                
                for(k = 0; k < patch[p].age_list->age_list_by_gender[g]->number_per_age_group[ai];
                    k++){
                    // For each individual in that annual age group:
                    // Draw whether each person is initially HSV-2 infected or not according to a Bernoulli trial. The probability can be made to vary by age/gender if needed.
                        
                    draw_initial_hsv2_infection(t, patch[p].age_list->age_list_by_gender[g]->age_group[ai][k], patch, p, overall_partnerships, output,file_data_store);
                        
                }
            }
            

	    // For the last age group: for each individual in that age group draw whether initially HSV-2 infected or not according to a Bernoulli trial.
	    for(k=0; k<patch[p].age_list->age_list_by_gender[g]->number_oldest_age_group; k++){
		draw_initial_hsv2_infection(t, patch[p].age_list->age_list_by_gender[g]->oldest_age_group[k], patch, p, overall_partnerships, output,file_data_store);
            }


        }
                        

	/******************************************/
	/* 15. Progressing (HSV-2)                */
	/******************************************/
    
	if(t>=patch[p].param->start_time_hsv2){        
	    carry_out_HSV2_events_per_timestep(t, patch, p, overall_partnerships, debug, file_data_store);
	}
                        

	
    }

                        
    
    // Function determines if there are any things we need to fit to at the current timestep, 
    // and carries out any fitting needed.
    fit_flag = fit_data(t0, t_step, fitting_data, patch, p);
    
    // If run did not fit given data, then return from this function - stops any further timesteps,
    // and this run is then terminated in main.c.
    
    // We then move on to the next parameter set.
    if(fit_flag == 0){
        return(0);
    }
    return(1);
}
