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

/* 
Functions related to PopART/CHiPs:
create_popart_chips_samples()
    at the start of a PopART year, decide who will be visited by CHiPs and in what order.
schedule_chips_visits()
    decide how many of these people  will be visited each timestep.
carry_out_chips_visits_per_timestep()
    goes through the list of people being visited by CHiPs and sets up their next cascade event 
    accordingly (HIV test, CD4 test).
chips_visit_person()
    

Functions related to circumcision:
draw_if_VMMC()
    Decides if an individual will get VMMC, and if they do, calls schedule_vmmc() to schedule 
    circumcision for a future timestep in vmmc_events[].  
schedule_vmmc()
    Adds an event for circumcision to vmmc_events[] to schedule an individual to get circumcised in
    future.
schedule_vmmc_healing()
    Adds an event for someone to finish healing after a VMMC op to vmmc_events[].
finish_vmmc_healing()
    Updates a person's status when they have finished healing after a VMMC op. At this point they
    have no further VMMC events happening to them.
schedule_generic_vmmc_event()
    Does the actual adding of a VMMC event to vmmc_event[] - function is called by schedule_vmmc 
    and schedule_vmmc_healing.
carry_out_VMMC_events_per_timestep()
    Carry out any event associated with VMMC in the current time step.  

Manicaland cascades:
 - PrEP

 */

/************************************************************************/
/******************************* Includes  ******************************/
/************************************************************************/

#include "interventions.h"
#include "structures.h"
#include "constants.h"
#include "hiv.h"

/************************************************************************/
/******************************** functions *****************************/
/************************************************************************/


void create_popart_chips_samples(age_list_struct *age_list, chips_sample_struct *chips_sample, 
    parameters *param, int chips_round, int p){
    
    /*
    This takes the population of currently alive people (using age_list) and firstly sub-divides
    them into a 'chips_sampling_frame', e.g. dividing up men and women, as CHiPs tends to visit
    more women than men.  We can also exclude certain people (e.g. <15 years old) as needed.  The
    sampling frame is then drawn from to pick chips_sample->size_n_m men and chips_sample->size_n_f
    women who will be the people visited in the year.  We then shuffle each of these lists, so the
    shuffled list will be the order in which people are visited.  Finally we call
    schedule_chips_visits() which sets the number of people to be visited in each timestep so that
    the total number of people visited in a year adds up to the correct total.
    
    NOTE: The way we divide up the population means that we may try to visit people who died during
    the year.  However, this should not be a big factor, and I think it may even` mimic CHiPs in
    that people may move/die between enumeration/mapping and CHiPs visit. 
    
    Arguments
    ----------
    age_list : pointer to age_list_struct structure
        
    chips_sample : pointer to chips_sample_struct structure
        
    param : pointer to parameters structure
        Parameters structure
    chips_round : int
        CHiPs round of interest
    p : int
        Patch number
    
    Returns
    -------
    
    */
    int g;
    int aa, ai,i, ac;
    /* For use with FOLLOW_INDIVIDUAL - we store these the first time we find them so we can find 
    them easily next time: */
    int g_persontofollow = -1; /* Default value indicates that the FOLLOW_INDIVIDUAL did not turn 
        up when going through - this is because they are too young to be visited by CHiPs. */
    int ac_persontofollow = -1;
    
    if(chips_round < -1 || chips_round >= NCHIPSROUNDS){
        printf("ERROR: The calculated CHiPS round is %d, outside the range -1 to %d. Exiting\n",
            chips_round, NCHIPSROUNDS - 1);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    /* This is a temporary store of the sampling frame. Only called annually at present so should
    be OK as a local variable. */
    chips_sample_struct *csf; // csf = "chips sampling frame"
    csf = malloc(sizeof(chips_sample_struct)); 
    
    if(csf == NULL){ /* Check memory allocated successfully. */
        printf("Unable to allocate csf in create_popart_chips_samples().");
        printf(" Execution aborted.");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    // Set counters to zero (we use these to index within each array).
    for(g = 0; g < N_GENDER; g++){
        /* ac is the var we use as the index for age group in the chips_sample_struct structure.*/
        for(ac = 0; ac < (MAX_AGE - AGE_CHIPS + 1); ac++){
            csf->number_to_visit[g][ac] = 0;
        }
    }
    
    for(g = 0; g < N_GENDER; g++){
        /* aa is age index for age_list by gender (not adjusting for youngest age group).
        Here it is chosen to correspond to ages from AGE_CHIPS to 79. */
        for(aa = (AGE_CHIPS - AGE_ADULT); aa < (MAX_AGE - AGE_ADULT); aa++){
            
            /* ai is the index of the array age_list->number_per_age_group of the age group of 
            people you want to be dead */
            ai = age_list->age_list_by_gender[g]->youngest_age_group_index + aa;
            while(ai > (MAX_AGE - AGE_ADULT - 1)){
                ai = ai - (MAX_AGE-AGE_ADULT);
            }
            
            for(i = 0; i < age_list->age_list_by_gender[g]->number_per_age_group[ai]; i++){
                /* This is the relationship between the index aa and ac (the index for the 
                chips_sample_struct structures). */
                ac = aa - (AGE_CHIPS - AGE_ADULT);
                
                /* For debugging; check if we're following an individual and a patch. */
                if(
                (age_list->age_list_by_gender[g]->age_group[ai][i]->id == FOLLOW_INDIVIDUAL) &&
                (age_list->age_list_by_gender[g]->age_group[ai][i]->patch_no == FOLLOW_PATCH)
                ){
                    printf("Possible CHiPs visit %ld %d %d in round %d \n",
                        age_list->age_list_by_gender[g]->age_group[ai][i]->id,ai,i,chips_round);
                    
                    fflush(stdout);
                    /* Now store their characteristics so it's easier to find them: */
                    g_persontofollow = g;
                    ac_persontofollow = ac;
                }
                /* Also for debugging. */
                if(
                (age_list->age_list_by_gender[g]->age_group[ai][i]->cd4 == DUMMYVALUE) ||
                (age_list->age_list_by_gender[g]->age_group[ai][i]->cd4 == DEAD)
                ){
                    printf("Error -trying to schedule CHiPs visit for dead/non-existent ");
                    printf("person %ld\n",
                        age_list->age_list_by_gender[g]->age_group[ai][i]->id);
                    printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                    fflush(stdout);
                    exit(1);
                }
                
                /* At the moment, just split by gender and age. 
                Can also add in some undersampling of high risk groups. */
                csf->list_ids_to_visit[g][ac][csf->number_to_visit[g][ac]] = age_list->age_list_by_gender[g]->age_group[ai][i]->id;
                
                csf->number_to_visit[g][ac]++;
            }
        }
        
        /* Now look at oldest age group: */
        for(i = 0; i < age_list->age_list_by_gender[g]->number_oldest_age_group; i++){
            
            if(
            (age_list->age_list_by_gender[g]->oldest_age_group[i]->id == FOLLOW_INDIVIDUAL) &&
            (age_list->age_list_by_gender[g]->oldest_age_group[i]->patch_no==FOLLOW_PATCH)
            ){
                
                printf("Possible CHiPs visit %ld oldest age gp i=%d\n",
                    age_list->age_list_by_gender[g]->oldest_age_group[i]->id,i);
                fflush(stdout);
                /* Now store their characteristics so it's easier to find them: */
                g_persontofollow = g;
                /* This is MAX_AGE-AGE_ADULT-(AGE_CHIPS-AGE_ADULT). */
                ac_persontofollow = MAX_AGE-AGE_CHIPS;
            }
            csf->list_ids_to_visit[g][MAX_AGE - AGE_CHIPS][csf->number_to_visit[g][MAX_AGE - AGE_CHIPS]] =
                    age_list->age_list_by_gender[g]->oldest_age_group[i]->id;
            csf->number_to_visit[g][MAX_AGE - AGE_CHIPS]++;
        }
    }
    
    /* These decide how many people are going to be visited by CHiPs. Can be implemented as a
    number rather than a percentage of population. */
    for(g = 0; g < N_GENDER; g++){
        /* Run from AGE_CHIPS to 80+ (note - this is different from previous loop). */
        for(ac = 0; ac < (MAX_AGE - AGE_CHIPS + 1); ac++){
            if(chips_round >= 0 && chips_round < NCHIPSROUNDS){
                chips_sample->number_to_visit[g][ac] = (int)  floor(csf->number_to_visit[g][ac]*param->chips_params->prop_tested_by_chips_in_round[g][ac][chips_round]);
            }else if (chips_round==CHIPSROUNDPOSTTRIAL){
                chips_sample->number_to_visit[g][ac] = (int)  floor(csf->number_to_visit[g][ac]*param->chips_params->prop_tested_by_chips_in_round_posttrial[g][ac]);
            }else{
                printf("ERROR: Unknown value of chips_round=%d. Exiting\n", chips_round);
                printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                fflush(stdout);
                exit(1);
            }
            
            if (chips_sample->number_to_visit[g][ac]>0){
                
                /* Choose chips_sample->number_to_visit[g][ac] from the array csf->m. */
                gsl_ran_choose(rng, chips_sample->list_ids_to_visit[g][ac],
                    chips_sample->number_to_visit[g][ac],
                    csf->list_ids_to_visit[g][ac],
                    csf->number_to_visit[g][ac], sizeof (long));
                
                /* Randomise the order (as gsl_ran_choose maintains the order of 
                the original list). */
                gsl_ran_shuffle(rng, chips_sample->list_ids_to_visit[g][ac],
                    chips_sample->number_to_visit[g][ac], sizeof (long));
            }
        }
    }
    
    /* Check to see if this person was visited. Note that if g_persontofollow==-1 then they are too
    young to be in csf->list_ids_to_visit. */
    
    if(p == FOLLOW_PATCH && g_persontofollow > -1){
        for(i = 0; 
        i < csf->number_to_visit[g_persontofollow][ac_persontofollow]; 
        i++){
            
            if(csf->list_ids_to_visit[g_persontofollow][ac_persontofollow][i] == FOLLOW_INDIVIDUAL){
                
                printf("CHiPs visit for adult %ld, gender %i from patch %d now scheduled\n",
                    csf->list_ids_to_visit[g_persontofollow][ac_persontofollow][i],
                    g_persontofollow, p);
                fflush(stdout);
            }
        }
    }
    schedule_chips_visits(chips_sample, param, chips_round);
    free(csf);
}


void schedule_chips_visits(chips_sample_struct *chips_sample, parameters *param, int chips_round){
   /* Given a sample of people who are to be visited each year (currently chips_sample->m and
    chips_sample->f) schedule their visits in the arrays
    chips_sample->number_to_see_per_timestep_m/f.  These arrays contain the number of people to see
    at each timestep, and we run through e.g. chips_sample->m until we have seen that many people
    each timestep.  
    
    
    Arguments
    ---------
    chips_sample : pointer to a chips_sample_struct struct
    param : pointer to a parameters struct
        All the parameters of interest for the patch in question.  
    chips_round : int
        CHiPs round of interest
    
    Returns
    -------
    Nothing; 
    
    */
    
    
    
    int g,ac;
    double temp_chips_expected_cumulative_proportion_visited = 0;
    double temp_chips_expected_cumulative_number_visited = 0;
    long temp_chips_cumulative_number_scheduled;
    /* We use this to store the fraction of people who will be visited in a round who are visited
    in a given timestep. */
    double temp_fraction_visited_normalised; 

    /* We need to deal with rounding issues (described more below). To do this we ensure we are
    always within 1 of the expected cumulative number of visits.  However computer rounding means
    we need to adjust that very slightly, so subtract an arbitrary small amount. */
    double TOLERANCE = 1.0-1e-9;

    /* Initialise values in chips_sample->next_person_to_see[] so begin at the start of the list. */
    for(g = 0; g < N_GENDER; g++){
        
        /* Run from AGE_CHIPS to 80+. */
        for(ac = 0; ac <(MAX_AGE - AGE_CHIPS + 1); ac++){
            chips_sample->next_person_to_see[g][ac] = 0;
        }
    }

    // Determine the number of time steps for the chips round in question
    int n_steps_in_round;
    if(chips_round >= 0 && chips_round < NCHIPSROUNDS){
        n_steps_in_round = param->chips_params->n_timesteps_per_round[chips_round];
    }else if (chips_round == CHIPSROUNDPOSTTRIAL){
        n_steps_in_round = param->chips_params->n_timesteps_per_round_posttrial;
    }else{
        printf("ERROR: Unknown chips_round value =%d. Exiting\n", chips_round);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    int i;
    /* This is just a crude way to make sure we see everyone we're supposed to see that month: */ 
    for(g = 0; g < N_GENDER; g++){
        /* CHiPs visit everyone from from AGE_CHIPS to 80+. */
        for(ac = 0; ac < (MAX_AGE - AGE_CHIPS + 1); ac++){
            temp_chips_expected_cumulative_proportion_visited = 0;
            temp_chips_expected_cumulative_number_visited = 0;
            temp_chips_cumulative_number_scheduled = 0;
            
            for(i = 0; i < n_steps_in_round; i++){
                /* This is the fraction of people who will be visited in a round who are visited in
                a given timestep. */
                if(chips_round >= 0 && chips_round < NCHIPSROUNDS){
                    temp_fraction_visited_normalised = param->chips_params->prop_tested_by_chips_per_timestep[g][ac][i][chips_round]/param->chips_params->prop_tested_by_chips_in_round[g][ac][chips_round];
                }else if (chips_round == CHIPSROUNDPOSTTRIAL){
                    temp_fraction_visited_normalised = param->chips_params->prop_tested_by_chips_per_timestep_posttrial[g][ac][i]/param->chips_params->prop_tested_by_chips_in_round_posttrial[g][ac];
                }
                
                chips_sample->number_to_see_per_timestep[g][ac][i] = (int) round(
                    chips_sample->number_to_visit[g][ac] * temp_fraction_visited_normalised);
                
                /* Now deal with the fact that there are rounding issues - we may end up seeing
                more/less people than intended as a result. For example if we are to see 10 people
                over 9 timesteps equally at a rate of 1/9 then we would see 1 at each timestep and
                hence only 9 people at the end.  This code below will find a place to add the extra
                person, in such a way that the adjustments are distributed reasonably over the
                whole CHiPs round.     */
                
                /* This is the number of people we have scheduled so far: */
                temp_chips_cumulative_number_scheduled += chips_sample->number_to_see_per_timestep[g][ac][i];

                temp_chips_expected_cumulative_proportion_visited += temp_fraction_visited_normalised;
                /* This is the number of people we 'should' have visited so far. 
                We allow it to be non-integer. */
                temp_chips_expected_cumulative_number_visited = chips_sample->number_to_visit[g][ac] * temp_chips_expected_cumulative_proportion_visited;
                
                while(
                (temp_chips_cumulative_number_scheduled -
                temp_chips_expected_cumulative_number_visited) >= TOLERANCE &&
                (chips_sample->number_to_see_per_timestep[g][ac][i] >=1)
                ){
                    chips_sample->number_to_see_per_timestep[g][ac][i] -= 1;
                    temp_chips_cumulative_number_scheduled -= 1;
                }
                /* Print a warning message if the issue is not fixed: */
                if(
                (temp_chips_cumulative_number_scheduled - temp_chips_expected_cumulative_number_visited) >= TOLERANCE){
                    printf("Warning - may need to adjust schedule_chips_visits() at ");
                    printf("i=%i = %li %6.4lf - have scheduled incorrectly?\n", i,
                        temp_chips_cumulative_number_scheduled,
                        temp_chips_expected_cumulative_number_visited);
                }

                /* If we have scheduled too few people: */
                while((temp_chips_expected_cumulative_number_visited - temp_chips_cumulative_number_scheduled) >= TOLERANCE){
                    chips_sample->number_to_see_per_timestep[g][ac][i] += 1;
                    temp_chips_cumulative_number_scheduled += 1;
                }
                /* Print a warning message if the issue is not fixed: */
                if((temp_chips_expected_cumulative_number_visited - temp_chips_cumulative_number_scheduled) >= TOLERANCE){
                    printf("Warning - may need to adjust schedule_chips_visits() at ");
                    printf("i=%i = %li %6.4lf - have scheduled incorrectly?\n", i,
                        temp_chips_cumulative_number_scheduled,
                        temp_chips_expected_cumulative_number_visited);
                }
            }
        }
    }
}


/*************************** Functions which do the CHiPs visits: ************************/


void carry_out_chips_visits_per_timestep(int t0, int t_step, patch_struct *patch, int p, 
        int chips_round, debug_struct *debug, output_struct *output){
    /* Carry out the CHiPS visits for a given timestep at time t. 
    
    Arguments
    ---------
    t0 : int
    t_step : int
    patch : patch_struct struct
    p : int
        Patch identifier.  
    chips_round : int
        CHiPs round in question
    debug : pointer to a debug_struct struct
    output : pointer to an output_struct struct
    
    Returns
    -------
    Nothing; 
    */
    long i;  
    int g,ac;
    int n_steps_in_round;
    if(chips_round >= 0 && chips_round < NCHIPSROUNDS){
        n_steps_in_round = patch[p].param->chips_params->n_timesteps_per_round[chips_round];
    }else if(chips_round == CHIPSROUNDPOSTTRIAL){
        n_steps_in_round = patch[p].param->chips_params->n_timesteps_per_round_posttrial;
    }else{
        printf("ERROR: Unknown chips_round value =%d. Exiting\n", chips_round);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    /* t_i is the index of the timestep within chips_sample corresponding to the current time t.
    For example chips_sample->number_to_see_per_timestep_m[t_i] is no. men to visit at time t. */
    int t_i;
    
    /* If the trial has not ended yet: */
    if(chips_round > -1){
        t_i = (t0 - patch[p].param->CHIPS_START_YEAR[chips_round]) * N_TIME_STEP_PER_YEAR +
            (t_step-patch[p].param->CHIPS_START_TIMESTEP[chips_round]);
    }else{
        /* Assume that from end of trial onwards CHiPs rounds are ANNUAL, and that they start 1
        week after the last timestep of the previous round. */
        
        /* Copy the first timestep from the previous round. */
        t_i = t_step - patch[p].param->CHIPS_START_TIMESTEP_POSTTRIAL;
        if(t_i < 0){
            t_i = t_i + N_TIME_STEP_PER_YEAR;
        }
    }
    
    /* For debugging: */
    if(t_i >= MAX_N_TIMESTEPS_PER_CHIPS_ROUND){
        printf("Problem - MAX_N_TIMESTEPS_PER_CHIPS_ROUND is too small. ");
        printf("We are %i timesteps into CHiPs round %i. Exiting\n", t_i, chips_round);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    if(t_i < 0 || t_i >= n_steps_in_round){
        printf("Error: t_i=%i is outside range [0,%d]", t_i, n_steps_in_round);
        printf(" in CHiPs round %d at time %6.4lf. ", chips_round, t0 + t_step * TIME_STEP);
        printf("Exiting\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    /* Now CHiPs visits each sub-population (currently men/women by year age group ac) in turn: */
    /* Go through the list of id's of people to visit, and visit them: */
    for(g = 0; g < N_GENDER; g++){
        /* Run from AGE_CHIPS to 80+. */
        for (ac = 0; ac < (MAX_AGE - AGE_CHIPS + 1); ac++){
            
            for(i = patch[p].chips_sample->next_person_to_see[g][ac]; 
                (i < (patch[p].chips_sample->next_person_to_see[g][ac] +
                    patch[p].chips_sample->number_to_see_per_timestep[g][ac][t_i])); 
                 i++){
                    if((patch[p].chips_sample->next_person_to_see[g][ac] +
                        patch[p].chips_sample->number_to_see_per_timestep[g][ac][t_i]) > 
                    (patch[p].chips_sample->number_to_visit[g][ac])){
                    
                    /* Only print out error message if we are over 2 too many otherwise just skip
                    those people. */
                    if((patch[p].chips_sample->next_person_to_see[g][ac] + 
                        patch[p].chips_sample->number_to_see_per_timestep[g][ac][t_i]) >
                        (patch[p].chips_sample->number_to_visit[g][ac])){
                        
                        if(VERBOSE_OUTPUT == 1){
                        printf("Visited too many people in patch %i at ", p);
                        printf("time=%6.4f g=%i ac=%i Excess=%li Number = %li\n",
                            t0 + t_step * TIME_STEP, g, ac, 
                                                        patch[p].chips_sample->next_person_to_see[g][ac]+patch[p].chips_sample->number_to_see_per_timestep[g][ac][t_i] - patch[p].chips_sample->number_to_visit[g][ac],
                            patch[p].chips_sample->number_to_visit[g][ac]);
                        }
                    }
                    
                    }else{
                    
                    /* Send the address (ie pointer) to this person. */
                    chips_visit_person(&(patch[p].individual_population[patch[p].chips_sample->list_ids_to_visit[g][ac][i]]), 
                        patch[p].cumulative_outputs,
                        patch[p].calendar_outputs,
                        t0 + t_step*TIME_STEP,
                        patch[p].cascade_events,
                        patch[p].n_cascade_events,
                        patch[p].size_cascade_events,
                        patch[p].hiv_pos_progression,
                        patch[p].n_hiv_pos_progression,
                        patch[p].size_hiv_pos_progression,
                        patch[p].param,
                        patch[p].vmmc_events,
                        patch[p].n_vmmc_events,
                        patch[p].size_vmmc_events, 
                        patch, p, chips_round, debug, output, g, ac);
                }
            }
            /* Update this index ready for the next timestep: */
            patch[p].chips_sample->next_person_to_see[g][ac] +=
                patch[p].chips_sample->number_to_see_per_timestep[g][ac][t_i];
        }
    }
}


void chips_visit_person(individual *indiv, cumulative_outputs_struct *cumulative_outputs,
    calendar_outputs_struct *calendar_outputs, double t, individual ***cascade_events, 
    long *n_cascade_events, long *size_cascade_events, individual ***hiv_pos_progression, 
    long *n_hiv_pos_progression, long *size_hiv_pos_progression, parameters *param, 
    individual ***vmmc_events, long *n_vmmc_events, long *size_vmmc_events, patch_struct *patch,
    int p, int chips_round, debug_struct *debug, output_struct *output, int g, int ac){
    /* 
    Because of the way we draw CHiPs visits at the beginning of the year, it is possible some people
    die before they are visited. If this is the case then do nothing more. 
    They are deleted from age_list so won't be in next year's sample. 
    
    
    Arguments
    ---------
    individual *indiv
    cumulative_outputs_struct *cumulative_outputs
    double tindividual ***cascade_events
    long *n_cascade_events
    long *size_cascade_events
    individual ***hiv_pos_progression
    long *n_hiv_pos_progression
    long *size_hiv_pos_progression
    parameters *param
    individual ***vmmc_events
    long *n_vmmc_events
    long *size_vmmc_events
    patch_struct *patch
    int p
    int chips_round
    debug_struct *debug
    output_struct *output
    int g
    int ac
    
    
    Returns
    -------
    Nothing;
    
    */
    
    /* We need a different variable as chips_round_including_end_trial is used as an array index. */
    int chips_round_including_end_trial;
    int year_idx = (int) floor(t) - param->start_time_simul;
    
    if(chips_round >= 0 && chips_round < NCHIPSROUNDS){
        chips_round_including_end_trial = chips_round;
    }else if(chips_round == CHIPSROUNDPOSTTRIAL){
        /* VMMC parameters should be like last round. */
        chips_round_including_end_trial = NCHIPSROUNDS - 1;
    }else{
        printf("ERROR: Unknown chips_round value =%d. Exiting\n", chips_round);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    if(indiv->cd4 == DUMMYVALUE){
        printf("Trying to CHiPS visit a non-existent person %d %ld !!! Exiting\n", p, indiv->id);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    if(indiv->cd4 == DEAD){
        indiv->VISITED_BY_CHIPS_THISROUND = DIEDBEFORECHIPSVISIT;
        return;
    }
    /* Save what was the old scheduled cascade event type in case needed: */
    int old_cascade_event = indiv->next_cascade_event;
    
    /* Update counters for whether visited this round and number of lifetime visits: */
    indiv->VISITED_BY_CHIPS_THISROUND = TRUE;
    
    /* We only record this during the trial. */
    if(chips_round > -1){
        output->NCHIPS_VISITED[p][g][ac][chips_round]++;
        
        if(indiv->HIV_status > UNINFECTED){
            output->NCHIPS_HIVPOS[p][g][ac][chips_round]++;
            if(
            (indiv->ART_status >= ARTNAIVE) && 
            (indiv->ART_status < ARTDEATH)
            ){
                output->NCHIPS_HIVAWARE[p][g][ac][chips_round]++;
                
                if(
                (indiv->ART_status == EARLYART) || 
                (indiv->ART_status == LTART_VS) || 
                (indiv->ART_status == LTART_VU)
                ){
                    output->NCHIPS_ONART[p][g][ac][chips_round]++;
                    
                    if(indiv->ART_status == LTART_VS){
                        output->NCHIPS_VS[p][g][ac][chips_round]++;
                    }
                }
            }
        }
    }
    indiv->NCHIPSVISITS++;
    
    // Record that there was a chips visit this year
    calendar_outputs->N_calendar_CHIPS_visits[year_idx]++;
    
    /* Are we following specific individuals or patches? */
    if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
        printf("CHiPs visit for adult %ld from patch %d at time %lf with old_cascade_event %d\n",
            indiv->id, indiv->patch_no, t, old_cascade_event);
        fflush(stdout);
    }
    
    /* If their previous event was an HIV test, then at this step they are HIV tested by CHiPs. */
    if( (old_cascade_event == CASCADEEVENT_HIV_TEST_NONPOPART) 
            || (old_cascade_event == CASCADEEVENT_HIV_TEST_POPART) || (old_cascade_event == CASCADEEVENT_HIV_TEST_PrEP_NONPOPART)){
	if(old_cascade_event == CASCADEEVENT_HIV_TEST_PrEP_NONPOPART){
	    printf("Unexpected behaviour in chips_visit_person() - CHIPS visit when PrEP is available. Probably this is fine but please check\n");
	    exit(1);
	}

        /* Unschedule the current event from care cascade. */
        remove_from_cascade_events(indiv, cascade_events, n_cascade_events, 
                size_cascade_events, t, param);
        
        indiv->next_cascade_event = CASCADEEVENT_HIV_TEST_POPART;
        
        hiv_test_process(indiv, param, t, cascade_events, n_cascade_events, size_cascade_events, 
            hiv_pos_progression, n_hiv_pos_progression, size_hiv_pos_progression, 
            cumulative_outputs, calendar_outputs, vmmc_events, n_vmmc_events, size_vmmc_events,
            patch, p, debug);
        
        return;
    }else if(
        (old_cascade_event == CASCADEEVENT_CD4_TEST_NONPOPART) || 
        (old_cascade_event == CASCADEEVENT_CD4_TEST_POPART)
    ){
        /* Unschedule the current event from care cascade. */
        remove_from_cascade_events(indiv, cascade_events, n_cascade_events, 
            size_cascade_events, t, param);
        
        /* Eligibility for ART is determined by calendar time and trial arm.
        * If in arm A and has not dropped out then schedule start of ART. */
        if (patch[p].trial_arm == ARM_A){
            cumulative_outputs->N_total_CD4_tests_popart++;
            calendar_outputs->N_calendar_CD4_tests_popart[year_idx]++;

	    /* Add diagnosis if needed: */
	    if(MIHPSA_MODULE==1 || EXTENDED_OUTPUTS_NNEWDIAGNOSES15PLUS==1){
		if(indiv->ART_status==ARTNEG){
		    printf("Error - POpART test???\n");
		    int age = floor(t - indiv->DoB);
		    //if(age>=15 && age <=49)
		    if(age>=15){
			patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus[indiv->gender]++;
			if(age<=24 && (indiv->gender)==FEMALE)
			    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15to24F++;
		    }
			    
		}
	    }

	    update_ART_state_population_counters_ARTcascade_change(t, patch[p].n_infected_by_all_strata, indiv->ART_status, ARTNAIVE, indiv, FALSE);

	    indiv->ART_status = ARTNAIVE;

            indiv->next_cascade_event = CASCADEEVENT_START_ART_POPART;
            indiv->VISITEDBYCHIPS_TO_INIT_ART = 1;
            schedule_start_of_art(indiv, param, t, cascade_events, 
                n_cascade_events, size_cascade_events);


	    
        /* In arm B but eligible for ART: */
        }else if (is_eligible_for_art(indiv, param, t, patch, p) > 0){
            
            if (patch[p].trial_arm != ARM_B){
                printf("ERROR: Not in arm B 1??? Exiting\n");
                printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                fflush(stdout);
                exit(1);
            }

	    update_ART_state_population_counters_ARTcascade_change(t, patch[p].n_infected_by_all_strata, indiv->ART_status, ARTNAIVE, indiv, FALSE);

	    if(MIHPSA_MODULE==1 || EXTENDED_OUTPUTS_NNEWDIAGNOSES15PLUS==1){
		if(indiv->ART_status==ARTNEG){
		    printf("Error - PopART testing???\n");
		    int age = floor(t - indiv->DoB);
		    //if(age>=15 && age <=49)
		    if(age>=15){
			patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus[indiv->gender]++;
			if(age<=24 && (indiv->gender)==FEMALE)
			    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15to24F++;
		    }
		}
	    }

	    
            indiv->ART_status = ARTNAIVE;
            cumulative_outputs->N_total_CD4_tests_popart++;
            calendar_outputs->N_calendar_CD4_tests_popart[year_idx]++;
            indiv->next_cascade_event = CASCADEEVENT_START_ART_POPART;
            indiv->VISITEDBYCHIPS_TO_INIT_ART = 1;
            schedule_start_of_art(indiv, param, t, cascade_events, 
                n_cascade_events, size_cascade_events);
        
        /* In arm B and not yet eligible for ART: */
        }else{
            if (patch[p].trial_arm != ARM_B){
                printf("ERROR: Not in arm B 2??? Exiting\n");
                printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                fflush(stdout);
                exit(1);
            }
            
            /* Time to next CD4 test is again the sum of the time between 
            getting the HIV test and having the first CD4 test, and the time between consecutive
            CD4 tests. */
            cumulative_outputs->N_total_CD4_tests_popart++;
            calendar_outputs->N_calendar_CD4_tests_popart[year_idx]++;


	    update_ART_state_population_counters_ARTcascade_change(t, patch[p].n_infected_by_all_strata, indiv->ART_status, ARTNAIVE, indiv, FALSE);

	    if(MIHPSA_MODULE==1 || EXTENDED_OUTPUTS_NNEWDIAGNOSES15PLUS==1){
		if(indiv->ART_status==ARTNEG){
		    int age = floor(t - indiv->DoB);
		    printf("Error - PopART testing\n");
		    //if(age>=15 && age <=49)
		    if(age>=15){
			patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15plus[indiv->gender]++;
			if(age<=24 && (indiv->gender)==FEMALE)
			    patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_newHIVdiagnoses_15to24F++;
		    }
		}
	    }


	    indiv->ART_status = ARTNAIVE;
            
            /* Note that we have two events happening here - time to get the CD4 test (to determine
            eligibility) and then time to retest CD4 again - we are scheduling the future CD4 test
             here. So I think this is correct. */
            
            double time_new_cd4 = t + param->t_delay_hivtest_to_cd4test_min[POPART] +
                param->t_delay_hivtest_to_cd4test_range[POPART] * gsl_rng_uniform (rng);
            
            indiv->next_cascade_event = CASCADEEVENT_CD4_TEST_POPART;
            schedule_generic_cascade_event(indiv, param, time_new_cd4, cascade_events,
                n_cascade_events, size_cascade_events,t);
        }
    }else if(old_cascade_event == NOEVENT){
        
        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("Adult %ld at time %lf is in old_cascade_event==NOEVENT if statement\n",
                indiv->id, t);
            fflush(stdout);
        }
        
        /* if already on ART (and has NOEVENT because of this - ie early ART or VS) then we don't
        need to do anything else. */
        if(
            (indiv->ART_status == EARLYART) || 
            (indiv->ART_status == LTART_VS)
        ){
            if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
                printf("Adult %ld at time %lf is already on ART so this is OK.\n", indiv->id, t);
                fflush(stdout);
            }
        }else{
            
            /* If individual has never tested positive this person needs to get an HIV test next.
             (note that this is tested, not serostatus). */
            if(indiv->ART_status == ARTNEG){
                
                // Assign next cascade event as PopART HIV test
                indiv->next_cascade_event = CASCADEEVENT_HIV_TEST_POPART;
                
                hiv_test_process(indiv, param, t, cascade_events, n_cascade_events,
                    size_cascade_events, hiv_pos_progression, n_hiv_pos_progression,
                    size_hiv_pos_progression, cumulative_outputs, calendar_outputs, 
                    vmmc_events, n_vmmc_events, size_vmmc_events, patch, p, debug);
            
            }else{
                
                /* Check that individual can only get here if previously dropped out. */
                if(indiv->ART_status != CASCADEDROPOUT){
                    
                    printf("ERROR: Incorrect cascade in chips_visit_person for ");
                    printf("ART status =%d for person %ld in patch %d. ",
                        indiv->ART_status, indiv->id, indiv->patch_no);
                    
                    printf("Exiting\n");
                    printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                    fflush(stdout);
                    exit(1);
                }
                /* Allow back into cascade if you previously dropped out at some given probability
                (note that this is currently 1): */
                if(
                gsl_ran_bernoulli(rng, 
                    param->p_popart_to_cascade[chips_round_including_end_trial]) == 1
                ){
                    /* If already know HIV+ then can go to clinic and get CD4 test etc. */
                    if(is_eligible_for_art(indiv, param, t, patch, p) > 0){
                        
                        cumulative_outputs->N_total_CD4_tests_popart++;
                        calendar_outputs->N_calendar_CD4_tests_popart[year_idx]++;
                        indiv->next_cascade_event = CASCADEEVENT_START_ART_POPART;

			update_ART_state_population_counters_ARTcascade_change(t, patch[p].n_infected_by_all_strata, indiv->ART_status, ARTNAIVE, indiv, FALSE);

			indiv->ART_status = ARTNAIVE;
                        indiv->VISITEDBYCHIPS_TO_INIT_ART = 1;
                        schedule_start_of_art(indiv, param, t, cascade_events, 
                            n_cascade_events, size_cascade_events);
                    }else{
                        /* 
                        Time to next CD4 test is again the sum of the time between
                        getting the HIV test and having the first CD4 test, and the time between
                        consecutive CD4 tests.
                        */
                        cumulative_outputs->N_total_CD4_tests_popart++;
                        calendar_outputs->N_calendar_CD4_tests_popart[year_idx]++;

			update_ART_state_population_counters_ARTcascade_change(t, patch[p].n_infected_by_all_strata, indiv->ART_status, ARTNAIVE, indiv, FALSE);

			indiv->ART_status = ARTNAIVE;
                        /*
                        Note that we have two events happening here - time to get the CD4 test 
                        (to determine eligibility) and then time to retest CD4 again - we are 
                        scheduling the future CD4 test here. So I think this is correct. 
                        */
                        double time_new_cd4 = t + param->t_delay_hivtest_to_cd4test_min[POPART] + 
                            param->t_delay_hivtest_to_cd4test_range[POPART] * gsl_rng_uniform (rng);
                        
                        indiv->next_cascade_event = CASCADEEVENT_CD4_TEST_POPART;
                        
                        schedule_generic_cascade_event(indiv, param, time_new_cd4, cascade_events, 
                            n_cascade_events, size_cascade_events, t);
                    }
                }
            }
        }
    }
}


/******************************************************************************************
 * These are VMMC intervention events - VMMC can either be through PopART or national 
 * policy/campaigns.
 ******************************************************************************************/
/* Determines if a man gets VMMC, and if so schedules the process: 
 * ASSUMPTION!!! - time is drawn with no data!!! */
void draw_if_VMMC(individual *indiv, parameters *param, individual ***vmmc_events, long *n_vmmc_events, long *size_vmmc_events, double t, int is_popart){
    double p_circ;
    int year, t_step, chips_round;
    printf("Calling draw_if_vmmc at t=%lf\n",t);
    /* For DEBUGGING: */
    if (indiv->gender==FEMALE||(indiv->circ!=UNCIRC)) 
    {
        printf("ERROR: This person %ld is gender=%d with circ=%d is in draw_if_VMMC. Exiting\n",
            indiv->id, indiv->gender, indiv->circ);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    /* Need to see if there is an HIV retest prior to VMMC. */
    if (t <= (param->COUNTRY_VMMC_START)){
        return;                       /* No VMMC so exit function. */
    }
    else{
        if (is_popart==POPART){
            year = (int) floor(t);
            t_step = (int) round((t - year)*N_TIME_STEP_PER_YEAR);
            chips_round = get_chips_round(param, year, t_step);

            /* Note that get_chips_round() returns -1 if after trial. We need to use chips_round as an array index so fix this: */
            if (chips_round==CHIPSROUNDPOSTTRIAL)
                chips_round = NCHIPSROUNDS-1; /* VMMC parameters should be like last round. */
            else if (chips_round<0 || chips_round>=NCHIPSROUNDS){
                printf("ERROR: Unknown chips_round value =%d in draw_if_VMMC() at t=%lf. Exiting\n",chips_round,t);
                printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
                fflush(stdout);
                exit(1);
            }

            //printf("Calling chips_sampling_frame() year=%d t_step=%d. chips_round=%d p=%lf\n",year,t_step,chips_round,param->p_circ_popart[chips_round]);
            p_circ= param->p_circ_popart[chips_round];

        }
        else
            p_circ= param->p_circ_nonpopart;
        /* Assume that probability of VMMC is higher with PopART (hence the index for p_circ): */

        if (gsl_ran_bernoulli(rng,p_circ)==1){
            //printf("Decided VMMC t=%lf is_popart=%d p=%lf\n",t,is_popart,p_circ);
            /* Schedule the person to get VMMC some time in the near future.
             * Note: we allow VMMC to happen quicker during PopART - hence pass is_popart to schedule_vmmc(): */
            schedule_vmmc(indiv, param, vmmc_events, n_vmmc_events, size_vmmc_events, t, is_popart);
        }
    }
}

/* Function is called when a person has just had a -ve HIV test, and decides to get VMMC at some time in the future.
 * The function determines when in the future the person will get VMMC and schedules this in vmmc_events[]. */
void schedule_vmmc(individual *indiv, parameters *param, individual ***vmmc_events, 
        long *n_vmmc_events, long *size_vmmc_events, double t, int is_popart){

    /* For DEBUGGING: */
    if (indiv->gender==FEMALE||(indiv->circ!=UNCIRC)) 
    {
        printf("ERROR: not sure why this person %ld gender=%d with circ=%d is in schedule_VMMC. Exiting\n",indiv->id,indiv->gender,indiv->circ);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    //printf("Individual %ld had been scheduled for VMMC at time %f, is_popart=%d\n",indiv->id,t,is_popart);
    double time_vmmc = t + param->t_get_vmmc_min[is_popart] + param->t_get_vmmc_range[is_popart]*gsl_rng_uniform (rng);
    //printf("Individual %ld had been scheduled for VMMC at t=%f for future time %f, is_popart=%d\n",indiv->id,t,time_vmmc,is_popart);
    /* Set status to waiting for VMMC: */
    indiv->circ = UNCIRC_WAITING_VMMC;
    schedule_generic_vmmc_event(indiv,param,vmmc_events,n_vmmc_events,size_vmmc_events,t,time_vmmc);
    /* Do we need to model people deciding more than once if they get VMMC? */
    return;
}


void schedule_vmmc_healing(individual *indiv, parameters *param, individual ***vmmc_events, 
    long *n_vmmc_events, long *size_vmmc_events, double t){
    /* Determine time between VMMC operation and healing, and schedules a healing event.
    
    This function is called when the VMMC operation is performed.   The healing event for the person
    in question is added to vmmc_events[], a time to healing is generated, and the individual's
    circ status is set to VMMC_HEALING.
    
    Arguments
    ---------
    indiv : pointer to an individual struct
    param : pointer to a parameter struct
    vmmc_events : multidimensional array of pointers to individual struct
    n_vmmc_events : array of long
        Array (of length N_TIME_STEP_PER_YEAR; see constants.h for def) of the number of VMMC events
        in a given time step for the current year.  
    size_vmmc_events : array of long
    t : double
        Current time in years.  
    
    Returns
    -------
    Nothing; a time to healing is drawn and schedule_generic_vmmc_event() is called.  
    */
    
    /* If the individual is female or they are not waiting for VMMC, throw and error */
    if(indiv->gender == FEMALE || (indiv->circ != UNCIRC_WAITING_VMMC)){
        printf("ERROR: not sure why this person %ld ", indiv->id);
        printf("gender=%d with circ=%d is in schedule_vmmc_healing.  ", indiv->gender, indiv->circ);
        printf("Exiting\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    double time_heal = t + param->t_vmmc_healing;
    
    // Change the individuals circumcision status to VMMC_HEALING
    indiv->circ = VMMC_HEALING;
    indiv->t_vmmc = t;
    
    //printf("Scheduling healing for %ld at time %lf for future time %lf\n",indiv->id,t,time_heal);
    schedule_generic_vmmc_event(indiv, param, vmmc_events, n_vmmc_events, size_vmmc_events, 
        t, time_heal);
    return;
}


/* Once someone has reached the end of the VMMC healing period, this function is called.
 * Function sets the individual so they no longer have any VMMC event, and their circ status is "VMMC". */
void finish_vmmc_healing(individual *indiv){
    
    /* For DEBUGGING: */
        if (indiv->gender==FEMALE||(indiv->circ!=VMMC_HEALING)) 
        {
            printf("ERROR: not sure why this person %ld gender=%d with circ=%d is in finish_vmmc_healing. Exiting\n",indiv->id,indiv->gender,indiv->circ);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
    indiv->circ = VMMC;
    /* Do not need to remove from vmmc_events[] array as this event is now in the past. */
    indiv->idx_vmmc_event[0] = -1;
    indiv->idx_vmmc_event[1] = -1;
    return;
}


void schedule_generic_vmmc_event(individual *indiv, parameters *param, individual ***vmmc_events,
    long *n_vmmc_events, long *size_vmmc_events, double t, double t_event){
    /*
    Add a VMMC event to the array vmmc_event[][] for an individual `indiv` at time `t_event`.  
    
    This function adds a VMMC event to the array vmmc_event for the time step at which it occurs in 
    the future, `t_step_vmmc_event`.  This function is called by schedule_vmmc() and
    schedule_vmmc_healing().
    
    Arguments
    ---------
    indiv : pointer to individual struct
        Individual for which the VMMC event is to be scheduled.  
    param : pointer to a parameters struct
    vmmc_events : 
    n_vmmc_events : array of long
    size_vmmc_events : array of long
    t : double
        Current time in years
    t_event : double
        Time in years at which the VMMC event is to take place.  
    
    Returns
    -------
    Nothing.  
    */
    
    /* Check the VMMC event doesn't happen before the end of the simulation */
    if (t_event <= param->end_time_simul){

        /* Note that if indiv->idx_vmmc_event[0] < 0 then the event is either "no event scheduled"
        (-1) or "an event was scheduled but only for after the end of the simulation" (-2).  
        Probably no way that -2 can ever happen but allow it as a possibility for now.  
         */
        if(
        (indiv->debug_last_vmmc_event_index == indiv->idx_vmmc_event[0]) &&
        (indiv->idx_vmmc_event[0] >= 0)
        ){
            printf("ERROR - trying to schedule a new vmmc event ");
            printf("(circumcision status=%d) in schedule_generic_vmmc_event() ", indiv->circ);
            printf("that occurs at the same time as the previous event ");
            printf("for person %ld in patch %d at time = %6.4f. ", indiv->id, indiv->patch_no, t);
            printf("Exiting\n");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
        /* vmmc_events is an array of events occurring in the next 12 months only.  
        So the index at time t is calculated as follows:
        * Suppose VMMC starts in 2008.0. Then for the rest of 2008 we schedule as 
            (int) trunc((t-2008)*N_TIME_STEP_PER_YEAR).
        * However, after 2008 we want to reuse the same array. So in e.g. 2010.25 we take the
        decimal part (0.25) and then
        * (int) trunc(0.25*N_TIMESTEPS_PER_YEAR) gives the new array index. */  
        int t_step_vmmc_event = (int) (floor((t_event - floor(t_event)) * N_TIME_STEP_PER_YEAR));
        int t_step_current_time = (int) (floor((t - floor(t)) * N_TIME_STEP_PER_YEAR));
        
        /* Ensure that we never schedule a cascade event during the current timestep: */
        if (t_step_vmmc_event == t_step_current_time){
            if (t_step_vmmc_event < N_TIME_STEP_PER_YEAR){
                t_step_vmmc_event += 1;
            }else if (t_step_vmmc_event == N_TIME_STEP_PER_YEAR){
                t_step_vmmc_event = 0;
            }
        }
        
        if (t_step_vmmc_event < 0 || t_step_vmmc_event >= N_TIME_STEP_PER_YEAR){
            printf("Error - trying to schedule VMMC outside array indices %d\n",
                t_step_vmmc_event);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }

        if (indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("Individual %ld is in schedule_generic_vmmc_event\n", indiv->id);
        }
        
        indiv->idx_vmmc_event[0] = t_step_vmmc_event;
        indiv->idx_vmmc_event[1] = n_vmmc_events[t_step_vmmc_event];
        
        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("New generic VMMC event for adult %ld generated with array indices  %ld %ld\n",
                indiv->id, indiv->idx_vmmc_event[0], indiv->idx_vmmc_event[1]);
            fflush(stdout);
        }

        /* Check if we've run out of memory: */
        if (n_vmmc_events[t_step_vmmc_event] >= (size_vmmc_events[t_step_vmmc_event])){

            /* Note that realloc does not work (we need to pass a pointer to the pointer, which is
            really complicated as it propagates through several functions (so maybe make
            planned_breakups[time_breakup] **), so ditch this code for now and use the following
            lines: */
            printf("Unable to re-allocate vmmc_events[i]. Execution aborted.");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
        /* Add a pointer to this individual to the vmmc_events array in the correct location */
        vmmc_events[t_step_vmmc_event][n_vmmc_events[t_step_vmmc_event]] = indiv;
        n_vmmc_events[t_step_vmmc_event]++;
    
    }else{ // If VMMC event lies after end of the simulation.  
        
        /* If next event scheduled for after the end of the simulation set to be dummy entries. */
        indiv->idx_vmmc_event[0] = EVENTAFTERENDSIMUL;
        indiv->idx_vmmc_event[1] = -1;
        if (indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("No VMMC event scheduled for %ld as event lies after end of the simulation.\n",
                indiv->id);
        }
    }
}


void carry_out_VMMC_events_per_timestep(int t_step, double t, patch_struct *patch, int p){
    /*Carry out any event associated with VMMC in the current time step
    
    
    Arguments
    ---------
    t_step : int
        Current time step (used to index the patch[p].vmmc_events and patch[p].n_vmmc_events)
    t : double
        Current time in years.  
    patch : pointer to an array of patch_struct structures
        The array of patch_struct objects that house information on patches.  See structures.h for 
        a list of attributes that these objects have.  
    p : int
        Patch identifier (generally 0 or 1).  
    
    Returns
    -------
    Nothing; carries out VMMC events on individuals for which they are scheduled.  
    */
    
    /* For debugging: */
    if(t_step < 0 || t_step >= N_TIME_STEP_PER_YEAR){
        printf("ERROR: array index %d for vmmc event out of bounds", t_step);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    int n_events = patch[p].n_vmmc_events[t_step];
    individual *indiv;
    int n;
    //printf("Carrying out %d VMMC events at time t=%f\n",n_events,t);
    
    for(n = 0; n < n_events; n++){
        indiv = patch[p].vmmc_events[t_step][n];
        //printf("Person %ld with circ=%d is in vmmc_events.\n",indiv->id,indiv->circ);
        
        /* Throw an error if this individual is female */
        if (indiv->gender == FEMALE){
            printf("ERROR: There is a woman %ld in vmmc_events. Exiting\n",indiv->id);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
        /* If this individual is dead, move on to the next person.  
        Note - we can set up a similar procedure to other lists to remove this person from this
        list but it is not necessary. As things stand, no VMMC event happens to the dead person and
        no new event is scheduled for them. */
        if(indiv->cd4 == DEAD){
            continue;
        }
        /* If uncircumcised but waiting for VMMC then at this timestep they get circumcised. */
        if (indiv->circ == UNCIRC_WAITING_VMMC){
            //printf("Person %ld with circ=%d is being scheduled for VMMC healing.\n",
            //      indiv->id,indiv->circ);

	    /* Add to VMMC count to extended outputs: */
	    int age = floor(t - indiv->DoB);
	    if(age>=15 && age <=49)
		patch[p].cumulative_outputs->cumulative_outputs_MIHPSA->N_VMMC_15to49++;

            schedule_vmmc_healing(indiv, patch[p].param, patch[p].vmmc_events,
                patch[p].n_vmmc_events, patch[p].size_vmmc_events, t);
            
            // Count the number of VMMC procedures in the current year by counting the 
            // time at which the VMMC procedure was performed.  
            int year_idx = (int) floor(t) - patch[p].param->start_time_simul;
            patch[p].calendar_outputs->N_calendar_VMMC[year_idx]++;
            
        }else if (indiv->circ == VMMC_HEALING){
            /* If current status is healing, then finish healing. Note that this is the last event
            in the VMMC process for this individual. */
            
            //printf("Person %ld with circ=%d is being scheduled to move to VMMC .\n",
            //    indiv->id,indiv->circ);
            finish_vmmc_healing(indiv);
            //printf("Person %ld with circ=%d now VMMC .\n",indiv->id,indiv->circ);
        }else{
            printf("ERROR: not sure why this person %ld with circ=%d is in vmmc_events. Exiting\n",
                indiv->id,indiv->circ);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
    }
    
    /* At this point we have carried out all the events stored in vmmc_events[t_step].
    
    We reuse the same array next year, so need to set n_vmmc_events[] to be zero.  Note that we do
    not need to set the elements in vmmc_events[t_step] to be blank
    as we overwrite any elements we use, and n_vmmc_events[] prevents us from accessing elements
    from previous years which have not been overwritten already. */
    patch[p].n_vmmc_events[t_step] = 0;
}




/******************** Manicaland related functions *******************/

/* Function takes age_list and uses it to generate a sample of women in a given age range (18-24) who will receive the PrEP intervention. 
   Function then creates a schedule for receiving the intervention.
   Note that this is NOT starting PrEP - starting PrEP can occur independently (and some time after the intervention?). */



void schedule_PrEP_background(age_list_struct *age_list, PrEP_background_sample_struct *PrEP_background_sample, PrEP_background_params_struct *PrEP_background_params, patch_struct *patch, int p, double t){
    
    /* We generate a list of ids of women in a single year age group ap who are eligible for the PrEP background (by running through age_list) and then draw from this list randomly to create the people who will receive PrEP through background means annually. 
       We then split up each list by timestep (which we do by specifying how many women from the list will be visited in each timestep).
       Note that we could potentially lose some women if they die between being scheduled and the time of the visit - but incidence + mortality aren't too high (and the 'round' shouldn't be too long).
    
    Arguments
    ----------
    age_list : pointer to age_list_struct structure
    PrEP_background_sample: pointer to PrEP_background_sample_struct structure
    PrEP_background_params: PrEP_background_params_struct
    -------    
    Returns: Nothing
    */

    int aa, ai, ap;
    int i;
   
    /* counter for the number of people in each list_eligible element. */
    int n_eligible[MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1];

    /* This is a temporary store of id numbers of people in a single age year - they are the people who are eligible for the background - we sample N of them. */
    long *temp_list_of_ids_for_sampling;
    temp_list_of_ids_for_sampling = malloc(sizeof(long)*MAX_POP_SIZE/40);

    /* Temporary stores used in scheduling people into each timestep. */
    long temp_cumulative_number_visited_this_timestep, temp_cumulative_number_visited_previous_timestep;

    individual *indiv;
    int t_i, n;
    
    if(temp_list_of_ids_for_sampling == NULL){ /* Check memory allocated successfully. */
        printf("Error: Unable to allocate temp_list_of_ids_for_sampling in schedule_PrEP_background().");
        printf(" Execution aborted.");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }


    /* Set counters to zero: */
    for (ap=0; ap<(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1); ap++){
	n_eligible[ap] = 0;
    }
    
    /* Use age_list to find all women aged MIN_AGE_PREP_BACKGROUND to MAX_AGE_PREP_BACKGROUND. 
       MAX_AGE_PREP_BACKGROUND must be below MAX_AGE_ADULT (assuming no very old people get PrEP...). */
    for (aa=(MIN_AGE_PREP_BACKGROUND-AGE_ADULT); aa<(MAX_AGE_PREP_BACKGROUND-AGE_ADULT+1); aa++){
	//printf("Running aa=%i\n",aa);
	ai = age_list->age_list_by_gender[FEMALE]->youngest_age_group_index + aa; /* a is the index of the two arrays age_list->number_per_age_group and age_list->age_group */
	while (ai>(MAX_AGE-AGE_ADULT-1))
	    ai = ai - (MAX_AGE-AGE_ADULT);
	ap = aa-(MIN_AGE_PREP_BACKGROUND-AGE_ADULT);

	/* Now loop over women in each year age group: */
	for (i=0; i<age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai]; i++){
	    //r = age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->sex_risk;
	    if ((age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->HIV_status==UNINFECTED) && (age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->PrEP_cascade_status==NOTONPREP)){
		/* Store their id: */
		temp_list_of_ids_for_sampling[n_eligible[ap]] = age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->id;
		//if (temp_list_of_ids_for_sampling[n_eligible[ap]]==26812)
		//   printf("Storing id in sampling frame ap=%i i=%i id= %li t=%lf\n",ap,i,temp_list_of_ids_for_sampling[n_eligible[ap]],t);
		

		n_eligible[ap]++;
	    }


	    
	    /* Once we have been through all women in this age group, draw sample: */
	    if (i==age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai]-1){
		//printf("Drawing background PrEP sample for age group %i\n",aa+AGE_ADULT);
		/* Calculate how many people to see in this timestep (use integer division): */
		PrEP_background_sample->number_getting_prep_per_year[ap] = PrEP_background_params->proportion_seen_by_age[ap] * n_eligible[ap];
		/* Now add some reserves in case original people are ineligible. Add the extra '1' to make sure it is larger than the original sample. */
		

		PrEP_background_sample->number_in_prep_sample_including_reserves[ap] = ceill(PrEP_background_sample->number_getting_prep_per_year[ap]*SAMPLE_INCLUDING_RESERVES+2);
		
		/* Make sure that this is not more than the total number of people: */
		if (PrEP_background_sample->number_in_prep_sample_including_reserves[ap]>n_eligible[ap])
		    PrEP_background_sample->number_in_prep_sample_including_reserves[ap] = n_eligible[ap];
		/* Make sure that this isn't more than the memory allocated: */
		if (PrEP_background_sample->number_in_prep_sample_including_reserves[ap]>MAX_PREP_ONE_YEAR_AGE_SAMPLE){
		    printf("***WARNING***: PrEP_background_sample->number_in_prep_sample_including_reserves[ap]=%li > MAX_PREP_ONE_YEAR_AGE_SAMPLE=%i\n",PrEP_background_sample->number_in_prep_sample_including_reserves[ap],MAX_PREP_ONE_YEAR_AGE_SAMPLE);
		    PrEP_background_sample->number_in_prep_sample_including_reserves[ap]=MAX_PREP_ONE_YEAR_AGE_SAMPLE;
		}	
		//printf("Number of people getting PrEP via background in this year = %li\n",PrEP_background_sample->number_getting_prep_per_year[ap]);
		//printf("Age ap=%i Need %li people, including reserves we get %li people. n_eligible=%i\n",ap,PrEP_background_sample->number_getting_prep_per_year[ap],PrEP_background_sample->number_in_prep_sample_including_reserves[ap],n_eligible[ap]);
		
		if (PrEP_background_sample->number_getting_prep_per_year[ap]>0){
		    gsl_ran_choose(rng, PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap], PrEP_background_sample->number_in_prep_sample_including_reserves[ap], temp_list_of_ids_for_sampling, n_eligible[ap], sizeof (long));
		    /* Randomise the order (as gsl_ran_choose maintains the order of 
		       the original list). */
		    gsl_ran_shuffle(rng, PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap], PrEP_background_sample->number_in_prep_sample_including_reserves[ap], sizeof (long));
		}
	    }
	    
	}
    }


    /* for (ap=0; ap <(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1); ap++){ */
    /* 	//printf("ap=%i i=%li\n",ap,PrEP_background_sample->number_in_prep_sample_including_reserves[ap]); */
    /* 	for(i=0; i<PrEP_background_sample->number_in_prep_sample_including_reserves[ap]; i++){ */
    /* 	    //printf("i=%li id=%li\n",i,PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][i]); */
    /* 	    if (PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][i]==26812) */
    /* 		printf("Storing id in sampling frame ap=%i i=%i id= %li t=%lf\n",ap,i,PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][i],t); */
    /* 	} */
    /* } */

    /* Initialise values in prep_background_sample->next_person_to_see[] so begin at the start of the list. */
    for(ap=0; ap <(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1); ap++)
	PrEP_background_sample->next_person_to_see[ap] = 0;

    /* Now specify what timestep people will be visited in: */
    for(ap=0; ap <(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1); ap++){
	//printf("Scheduling background PrEP for people in age group ap=%i\n",ap);
	
	temp_cumulative_number_visited_previous_timestep = 0;
	/* Unlike interventions, the background testing is continuous (and restarts annually): */
	for(i=0; i<N_TIME_STEP_PER_YEAR; i++){
	    temp_cumulative_number_visited_this_timestep = (int) round(((i+1)* PrEP_background_sample->number_getting_prep_per_year[ap])/(N_TIME_STEP_PER_YEAR));
	    PrEP_background_sample->number_to_see_per_timestep[ap][i] = temp_cumulative_number_visited_this_timestep - temp_cumulative_number_visited_previous_timestep;
	    temp_cumulative_number_visited_previous_timestep = temp_cumulative_number_visited_this_timestep;
	    //if (ap==1)
	    //printf("temp_cumulative_number_visited_this_timestep in background PrEP=%li for timestep i=%i out of %li seeing %li this timestep\n",temp_cumulative_number_visited_this_timestep,i,PrEP_background_sample->number_getting_prep_per_year[ap],PrEP_background_sample->number_to_see_per_timestep[ap][i]);
	}

	/* Normally the total number of people visited in total should match PrEP_background_sample->number_getting_prep_per_year[ap]. It is possibel that there could be a mismatch by +/-1 due to rounding errors. Check that here and adjust if needed: */
	if (PrEP_background_sample->number_getting_prep_per_year[ap]!=temp_cumulative_number_visited_this_timestep){
	    printf("Issue to be aware of in PrEP background scheduling - may be due to rounding? %li %li\n",PrEP_background_sample->number_getting_prep_per_year[ap],temp_cumulative_number_visited_this_timestep);

	    /* If missing one, arbitrarily add an extra person to last timestep. */
	    if (PrEP_background_sample->number_getting_prep_per_year[ap]==temp_cumulative_number_visited_this_timestep-1)
		PrEP_background_sample->number_to_see_per_timestep[ap][N_TIME_STEP_PER_YEAR-1] += 1;

	    /* If one too many then remove from the last timestep where there is >=1 person. */
	    else if (PrEP_background_sample->number_getting_prep_per_year[ap]==temp_cumulative_number_visited_this_timestep+1){
		i=N_TIME_STEP_PER_YEAR-1;
		while ((i>0) && (PrEP_background_sample->number_to_see_per_timestep[ap][i]==0))
		    i=i-1;
		if (i>-1)
		    PrEP_background_sample->number_to_see_per_timestep[ap][i] -= 1;
	    }
	    /* Otherwise print error report and exit. */
	    else{
		printf("Error: cannot schedule individuals for PrEP background age group %i in schedule_PrEP_background(). Mismatch = %li",ap,PrEP_background_sample->number_getting_prep_per_year[ap]-temp_cumulative_number_visited_this_timestep);
		printf(" Execution aborted.");
		printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
		fflush(stdout);
		exit(1);
	    }
	}
    }

    //int ntemp;
    //printf("*******HEY*** %i\n",(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1));

    //    }

    //for(i=0; i<PrEP_background_sample->number_in_prep_sample_including_reserves[ap]; i++)
    //printf("Id to visit=%li\n",patch[p].PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][i]);


        /* Here we double-check the sample and set their PrEP_cascade_status to be WAITINGTOSTARTPREP: */
    for(ap=0; ap <(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1); ap++){
	//printf("PrEP background for people in age group ap=%i\n",ap);
	n = 0;
	for (t_i=0; t_i<N_TIME_STEP_PER_YEAR; t_i++){
	    for(i=n; (i<(n+ PrEP_background_sample->number_to_see_per_timestep[ap][t_i])); i++){
		indiv = &(patch[p].individual_population[patch[p].PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][i]]);
		//if (indiv->id==26812)
		//    printf("Scheduling backgroup ap=%i id=%li\n",ap,indiv->id);
		if (indiv->PrEP_cascade_status!=NOTONPREP){
		    printf("Error: PrEP status impossible for indiv id=%li in schedule_PrEP_background(). Exiting\n",indiv->id);
		    fflush(stdout);
		    exit(1);
		}

		
		/* Set this so we don't schedule the same person to start PrEP by both background and intervention: */
		indiv->PrEP_cascade_status = WAITINGTOSTARTPREP;
		
		
		//printf("Background PrEP id=%li at t=%i\n",PrEP_background_sample->list_ids_to_visit_per_year[ap][i],t_i);
	    }
	    n += PrEP_background_sample->number_to_see_per_timestep[ap][t_i];
	}
    }

    free(temp_list_of_ids_for_sampling);
}




/******************************************************************************
 *** Not used for Manicaland cascades project - keep for possible future use.**
 ******************************************************************************/

void schedule_PrEP_intervention(age_list_struct *age_list, PrEP_intervention_sample_struct *PrEP_intervention_sample, PrEP_intervention_params_struct *PrEP_intervention_params, patch_struct *patch, int p){
    
    /* We generate a list of ids of women in a single year age group ap who are eligible for the PrEP intervention (by running through age_list) and then draw from this list randomly to create the people who will receive the PrEP intervention (in this round if there is >1 round). 
       We then split up each list by timestep (which we do by specifying how many women from the list will be visited in each timestep) - so we don't have any memory issues if we put all the women in one timestep.
       Note that we could potentially lose some women if they die between being scheduled and the time of the visit - but incidence + mortality aren't too high (and the 'round' shouldn't be too long).
    
    Arguments
    ----------
    age_list : pointer to age_list_struct structure
    PrEP_intervention_sample: pointer to PrEP_intervention_sample_struct structure
    PrEP_intervention_params: PrEP_intervention_params_struct
    -------    
    Returns: Nothing
    */

    int aa, ai, ap;
    int i;
   
    /* counter for the number of people in each list_eligible element. */
    int n_eligible[MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION+1];

    /* This is a temporary store of id numbers of people in a single age year - they are the people who are eligible for the intervention - we sample N of them. */
    long *temp_list_of_ids_for_sampling;
    temp_list_of_ids_for_sampling = malloc(sizeof(long)*MAX_POP_SIZE/40);

    /* Temporary stores used in scheduling people into each timestep. */
    long temp_cumulative_number_visited_this_timestep, temp_cumulative_number_visited_previous_timestep;


    individual *indiv;
    int t_i, n;

    
    if(temp_list_of_ids_for_sampling == NULL){ /* Check memory allocated successfully. */
        printf("Error: Unable to allocate temp_list_of_ids_for_sampling in schedule_PrEP_intervention().");
        printf(" Execution aborted.");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }


    /* Set counters to zero: */
    for (ap=0; ap<(MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION+1); ap++){
	n_eligible[ap] = 0;
    }
    
    /* Use age_list to find all women aged MIN_AGE_PREP_INTERVENTION to MAX_AGE_PREP_INTERVENTION. 
       MAX_AGE_PREP_INTERVENTION must be below MAX_AGE_ADULT (assuming no very old people get PrEP...). */
    for (aa=(MIN_AGE_PREP_INTERVENTION-AGE_ADULT); aa<(MAX_AGE_PREP_INTERVENTION-AGE_ADULT+1); aa++){
	ai = age_list->age_list_by_gender[FEMALE]->youngest_age_group_index + aa; /* a is the index of the two arrays age_list->number_per_age_group and age_list->age_group */
	ap = aa-(MIN_AGE_PREP_INTERVENTION-AGE_ADULT);
	while (ai>(MAX_AGE-AGE_ADULT-1))
	    ai = ai - (MAX_AGE-AGE_ADULT);

	/* Now loop over women in each year age group: */
	for (i=0; i<age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai]; i++){
	    //r = age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->sex_risk;
	    if ((age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->HIV_status==UNINFECTED) && (age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->PrEP_cascade_status==NOTONPREP)){
		/* Store their id: */
		temp_list_of_ids_for_sampling[n_eligible[ap]] = age_list->age_list_by_gender[FEMALE]->age_group[ai][i]->id;
		n_eligible[ap]++;
	    }


	    
	    /* Once we have been through all women in this age group, draw sample: */
	    if (i==age_list->age_list_by_gender[FEMALE]->number_per_age_group[ai]-1){
		//printf("Drawing intervention PrEP sample for age group %i\n",aa+AGE_ADULT);
		/* Calculate how many people to see in this timestep (use integer division): */
		PrEP_intervention_sample->number_getting_prep[ap] = PrEP_intervention_params->proportion_seen_by_age[ap] * n_eligible[ap];

		/* Now add some reserves in case original people are ineligible. Add the extra '1' to make sure it is larger than the original sample. */
		PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap] = ceill(PrEP_intervention_sample->number_getting_prep[ap]*SAMPLE_INCLUDING_RESERVES+2);
		/* Make sure that this is not more than the total number of people: */
		if (PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap]>n_eligible[ap])
		    PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap] = n_eligible[ap];
		/* Make sure that this isn't more than the memory allocated: */
		if (PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap]>MAX_PREP_ONE_YEAR_AGE_SAMPLE){
		    printf("***WARNING***: PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap]=%li > MAX_PREP_ONE_YEAR_AGE_SAMPLE=%i\n",PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap],MAX_PREP_ONE_YEAR_AGE_SAMPLE);
		    PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap]=MAX_PREP_ONE_YEAR_AGE_SAMPLE;
		}
		//printf("Number of people getting intervention PrEP in this round = %li\n",PrEP_intervention_sample->number_getting_prep[ap]);
		if (PrEP_intervention_sample->number_getting_prep[ap]>0){
		    gsl_ran_choose(rng, PrEP_intervention_sample->list_ids_to_visit_including_reserves[ap], PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap], temp_list_of_ids_for_sampling, n_eligible[ap], sizeof (long));
		    /* Randomise the order (as gsl_ran_choose maintains the order of 
		       the original list). */
		    gsl_ran_shuffle(rng, PrEP_intervention_sample->list_ids_to_visit_including_reserves[ap], PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap], sizeof (long));
		}
	    }
	    
	}
    }

    


    /* Initialise values in prep_intervention_sample->next_person_to_see[] so begin at the start of the list. */
    for(ap=0; ap <(MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION+1); ap++)
	PrEP_intervention_sample->next_person_to_see[ap] = 0;

    /* Now specify what timestep people will be visited in: */
    for(ap=0; ap <(MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION+1); ap++){
	//printf("Scheduling intervention PrEP for %li people in age group ap=%i\n",PrEP_intervention_sample->number_getting_prep[ap],ap);
	
	temp_cumulative_number_visited_previous_timestep = 0;
	for(i=0; i<PrEP_intervention_params->n_timesteps_in_round; i++){
	    temp_cumulative_number_visited_this_timestep = (int) round(((i+1)* PrEP_intervention_sample->number_getting_prep[ap])/(PrEP_intervention_params->n_timesteps_in_round));
	    PrEP_intervention_sample->number_to_see_per_timestep[ap][i] = temp_cumulative_number_visited_this_timestep - temp_cumulative_number_visited_previous_timestep;
	    temp_cumulative_number_visited_previous_timestep = temp_cumulative_number_visited_this_timestep;
	    //printf("Intervention temp_cumulative_number_visited_this_timestep=%li for timestep i=% out of %i seeing %i this timestep\n",temp_cumulative_number_visited_this_timestep,i,PrEP_intervention_sample->number_getting_prep[ap],PrEP_intervention_sample->number_to_see_per_timestep[ap][i]);
	}

	/* Normally the total number of people visited in total should match PrEP_intervention_sample->number_getting_prep[ap]. It is possibel that there could be a mismatch by +/-1 due to rounding errors. Check that here and adjust if needed: */
	if (PrEP_intervention_sample->number_getting_prep[ap]!=temp_cumulative_number_visited_this_timestep){
	    printf("Issue to be aware of in PrEP intervention scheduling - may be due to rounding? %li %li\n",PrEP_intervention_sample->number_getting_prep[ap],temp_cumulative_number_visited_this_timestep);

	    /* If missing one, arbitrarily add an extra person to last timestep. */
	    if (PrEP_intervention_sample->number_getting_prep[ap]==temp_cumulative_number_visited_this_timestep-1)
		PrEP_intervention_sample->number_to_see_per_timestep[ap][PrEP_intervention_params->n_timesteps_in_round-1] += 1;

	    /* If one too many then remove from the last timestep where there is >=1 person. */
	    else if (PrEP_intervention_sample->number_getting_prep[ap]==temp_cumulative_number_visited_this_timestep+1){
		i=PrEP_intervention_params->n_timesteps_in_round-1;
		while ((i>0) && (PrEP_intervention_sample->number_to_see_per_timestep[ap][i]==0))
		    i=i-1;
		if (i>-1)
		    PrEP_intervention_sample->number_to_see_per_timestep[ap][i] -= 1;
	    }
	    /* Otherwise print error report and exit. */
	    else{
		printf("Error: cannot schedule individuals for PrEP intervention age group %i in schedule_PrEP_intervention(). Mismatch = %li",ap,PrEP_intervention_sample->number_getting_prep[ap]-temp_cumulative_number_visited_this_timestep);
		printf(" Execution aborted.");
		printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
		fflush(stdout);
		exit(1);
	    }
	}
    }


    /* Here we double-check the sample and set their PrEP_cascade_status to be WAITINGTOSTARTPREP: */
    for(ap=0; ap <(MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION+1); ap++){
	//printf("PrEP intervention for people in age group ap=%i\n",ap);
	n = 0;
	for (t_i=0; t_i<PrEP_intervention_params->n_timesteps_in_round; t_i++){
	    for(i=n; (i<(n+ PrEP_intervention_sample->number_to_see_per_timestep[ap][t_i])); i++){
		indiv = &(patch[p].individual_population[patch[p].PrEP_intervention_sample->list_ids_to_visit_including_reserves[ap][i]]);
		//printf("Scheduling intervention ap=%i id=%li\n",ap,indiv->id);

		if (indiv->PrEP_cascade_status!=NOTONPREP){
		    printf("Error: PrEP status impossible for indiv id=%li in schedule_PrEP_intervention(). Exiting\n",indiv->id);
		    fflush(stdout);
		    exit(1);
		}
		
		/* Set this so we don't schedule the same person to start PrEP by both background and intervention: */
		indiv->PrEP_cascade_status = WAITINGTOSTARTPREP;
		
		
		//printf("Intervention id=%li at t=%i\n",PrEP_intervention_sample->list_ids_to_visit_including_reserves[ap][i],t_i);
	    }
	    n += PrEP_intervention_sample->number_to_see_per_timestep[ap][t_i];
	}
    }
    free(temp_list_of_ids_for_sampling);
}

/* Check if the individual indiv is eligible to start PrEP or not: */
int get_prep_eligibility(individual *indiv){
    if ((indiv->HIV_status==UNINFECTED) && (indiv->PrEP_cascade_status==NOTONPREP || indiv->PrEP_cascade_status==WAITINGTOSTARTPREP)  && (indiv->cd4!=DEAD))
	return 1;
    else
	return 0;
}

//********************************************************
/* Carry out any event associated with the PrEP background in the current time step. */
void carry_out_PrEP_background_events_per_timestep(int t_step, int year, patch_struct *patch, int p, debug_struct *debug){
    
    /* 
    Arguments
    ---------
    t_step : int - Current time step since the beginning of the year (used to index the patch[p].vmmc_events and patch[p].n_vmmc_events) 
    year: int - Current year.  
    patch : pointer to an array of patch_struct structures
        The array of patch_struct objects that house information on patches.  See structures.h for a list of attributes that these objects have.  
    p : int - Patch identifier (generally 0 or 1).  

    ----------
    Returns:    Nothing; carries out scheduled PrEP background events.  
    */

    

    /* t_i is number of timesteps since the beginning of the PrEP background.
       In the main code we use t_i to index the number of people to visit in timestep t_i.
       Note that PrEP background rounds MUST last exactly 1 year.  */
    //printf("Running background for time=%i+N_TIMESTEP_PER_YEAR*%i\n",year,t_step);
    long t_i = t_step - patch[p].param->PrEP_background_params->timestep_start_background;
    /* if backgreound starts mid-year then add so that it is not negative: */
    if (t_i<0)
	if (year>(patch[p].param->PrEP_background_params->year_start_background))
	    t_i = t_i + N_TIME_STEP_PER_YEAR;
	

    /* Check timestep is OK: */
    if ((t_i<0) || (t_i>=N_TIME_STEP_PER_YEAR)){
	printf("Error in carry_out_PrEP_background_events_per_timestep() - t_i=%li is outside allowed bounds. Exiting\n",t_i);
	fflush(stdout);
	exit(1);
    }

    int ap;
    int i,j;
    double t = year + t_step*TIME_STEP;

    individual *indiv;
    int prep_eligible;

    /* Now PrEP background reaches each sub-population (women by year age group ap) in turn: */
    /* Go through the list of id's of people to visit, and visit them: */
    for(ap=0; ap <(MAX_AGE_PREP_BACKGROUND-MIN_AGE_PREP_BACKGROUND+1); ap++){
	//printf("Next person background PrEP = %li\n",patch[p].PrEP_background_sample->next_person_to_see[ap]);
	//printf("number per timestep background PrEP = %li\n",patch[p].PrEP_background_sample->number_to_see_per_timestep[ap][t_i]);
	j = 0;
	for(i=0; i<patch[p].PrEP_background_sample->number_to_see_per_timestep[ap][t_i]; i++){
	    /* This is the person potentially being visited. */
	    indiv = &(patch[p].individual_population[patch[p].PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][j+patch[p].PrEP_background_sample->next_person_to_see[ap]]]);

	    /* If  they are not eligible, keep going until find someone who is (or run out of reserves): */
	    prep_eligible = get_prep_eligibility(indiv);
	    while ((prep_eligible==0) && j<(patch[p].PrEP_background_sample->number_in_prep_sample_including_reserves[ap]-patch[p].PrEP_background_sample->next_person_to_see[ap]-1)){
		j++;
		indiv = &(patch[p].individual_population[patch[p].PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][j+patch[p].PrEP_background_sample->next_person_to_see[ap]]]);

		prep_eligible = get_prep_eligibility(indiv);
	    }
	    if (prep_eligible==1){
		//printf("Bg prep: ID=%li. Supposed to be %li ap=%i i=%i\n",indiv->id,patch[p].PrEP_background_sample->list_ids_to_visit_per_year_including_reserves[ap][i],ap,i);
		/* They start PrEP due to background: */
		//if (indiv->id==26812){
		//   printf("Starting PrEP for 26812 ap=%i\n",ap);
		//}
		start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PREPTYPE_DAILYORALPREP, REASON_START_PREP_BACKGROUND);
		//printf("BStartijng PrEP for id=%li\n",indiv->id);

		j+=1;
	    }
	    else{
		/* This really shouldn't happen. If you think it's an error (e.g. putting PrEP into  a subgroup that has high incidence/mortality >=10%) then increase SAMPLE_INCLUDING_RESERVES to be bigger (i.e. get more reserves). */ 
		printf("***Warning: run out of reserves in PrEP background sample in carry_out_PrEP_background_events_per_timestep() ap=%i timestep=%li Number to start on PrEP=%li Number including reserves=%li. Code still running!\n",ap,t_i,patch[p].PrEP_background_sample->number_getting_prep_per_year[ap],patch[p].PrEP_background_sample->number_in_prep_sample_including_reserves[ap]);
		fflush(stdout);
	    }
	}

	//printf("Number of background reserves used[ap=%i] = %li out of %li to see. Total reserves = %li\n",ap,j-patch[p].PrEP_background_sample->number_to_see_per_timestep[ap][t_i],patch[p].PrEP_background_sample->number_to_see_per_timestep[ap][t_i],patch[p].PrEP_background_sample->number_in_prep_sample_including_reserves[ap]);
	/* Update this index ready for the next timestep: */
	patch[p].PrEP_background_sample->next_person_to_see[ap] += j;
    }
}



//********************************************************
/* Carry out any event associated with the PrEP intervention in the current time step. */
void carry_out_PrEP_intervention_events_per_timestep(int t_step, int year, patch_struct *patch, int p, debug_struct *debug){
    
    /* 
    Arguments
    ---------
    t_step : int - Current time step since the beginning of the year (used to index the patch[p].vmmc_events and patch[p].n_vmmc_events) 
    year: int - Current year.  
    patch : pointer to an array of patch_struct structures
        The array of patch_struct objects that house information on patches.  See structures.h for a list of attributes that these objects have.  
    p : int - Patch identifier (generally 0 or 1).  

    ----------
    Returns:    Nothing; carries out scheduled PrEP intervention events.  
    */

    

    /* t_i is number of timesteps since the beginning of the PrEP intervention.
       When it is <0 then the intervention has not started; when it is >n_timestpes_in_intervention then the intervention has finished.
       In the main code we use t_i to index the number of people to visit in timestep t_i.
       Note that PrEP intervention rounds MUST last <=1 year (as this is how much memory is allocated to the PrEP intervention schedule. So t_i<=N_TIME_STEP_PER_YEAR.  */
    long t_i = t_step - patch[p].param->PrEP_intervention_params->timestep_start_intervention;

    if (t_i<0)
	t_i = t_i + N_TIME_STEP_PER_YEAR;

    /* Don't do anything if the intervention isn't currently running: */
    if ((t_i<0) || (t_i>=patch[p].param->PrEP_intervention_params->n_timesteps_in_round))
	return;
    //printf("Running intervention for time=%i+N_TIMESTEP_PER_YEAR*%i\n",year,t_step);
    

    int ap;
    int i,j;  

    double t = year + t_step*TIME_STEP;

    individual *indiv;
    int prep_eligible;


    /* Now PrEP intervention reaches each sub-population (women by year age group ap) in turn: */
    /* Go through the list of id's of people to visit, and visit them: */
    for(ap=0; ap <(MAX_AGE_PREP_INTERVENTION-MIN_AGE_PREP_INTERVENTION+1); ap++){
	//printf("Next person intervention PrEP = %li\n",patch[p].PrEP_intervention_sample->next_person_to_see[ap]);
	//printf("number per timestep intervention PrEP = %li\n",patch[p].PrEP_intervention_sample->number_to_see_per_timestep[ap][t_i]);


	////


	j = 0;

	for(i=0; i<patch[p].PrEP_intervention_sample->number_to_see_per_timestep[ap][t_i]; i++){
	    /* This is the person potentially being visited. */
	    indiv = &(patch[p].individual_population[patch[p].PrEP_intervention_sample->list_ids_to_visit_including_reserves[ap][j+patch[p].PrEP_intervention_sample->next_person_to_see[ap]]]);

	    /* If  they are not eligible, keep going until find someone who is (or run out of reserves): */
	    prep_eligible = get_prep_eligibility(indiv);
	    while ((prep_eligible==0) && j<(patch[p].PrEP_intervention_sample->number_in_prep_sample_including_reserves[ap]-patch[p].PrEP_intervention_sample->next_person_to_see[ap]-1)){
		j++;
		indiv = &(patch[p].individual_population[patch[p].PrEP_intervention_sample->list_ids_to_visit_including_reserves[ap][j+patch[p].PrEP_intervention_sample->next_person_to_see[ap]]]);
		prep_eligible = get_prep_eligibility(indiv);
	    }
	    if (prep_eligible==1){

		/* They start PrEP due to intervention: */
		start_PrEP_for_person(indiv, patch, p, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, patch[p].cumulative_outputs, t, debug, PREPTYPE_DAILYORALPREP, REASON_START_PREP_INTERVENTION);
		j+=1;
	    }
	    else{
		/* This really shouldn't happen. If you think it's an error (e.g. putting PrEP into  a subgroup that has high incidence/mortality >=10%) then increase SAMPLE_INCLUDING_RESERVES to be bigger (i.e. get more reserves). */ 
		printf("***Warning: run out of reserves in PrEP intervention sample in carry_out_PrEP_intervention_events_per_timestep(). Code still running!\n");
		fflush(stdout);
	    }
	}

	if (j-patch[p].PrEP_intervention_sample->number_to_see_per_timestep[ap][t_i]>0)
	    printf("Number of intervention reserves used = %li\n",j-patch[p].PrEP_intervention_sample->number_to_see_per_timestep[ap][t_i]);
	/* Update this index ready for the next timestep: */
	patch[p].PrEP_intervention_sample->next_person_to_see[ap] += j;

    }
}



/* Function 
   PrEP is allowed for both men and women. */
void start_PrEP_for_person(individual *indiv, patch_struct *patch, int p, parameters *param, individual ***PrEP_events, long *n_PrEP_events, long *size_PrEP_events, cumulative_outputs_struct *cumulative_outputs, double t, debug_struct *debug, int PrEP_type, int reason_starting_PrEP){


    double t_next_PrEP_event;   /* Time of next PrEP event. */
    //printf("Starting PrEP for person %li at t=%lf\n",indiv->id, t);
    /* FOr debugging: */
    if(indiv->cd4 == DUMMYVALUE){
        printf("Trying to start PrEP for a non-existent person id=%ld !!! Exitin//g\n",indiv->id);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }

    if(indiv->id == FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH){
	printf("Potentially starting PrEP in function start_PrEP_for_person() id=%li current PrEP status=%i, starting PrEP type %i at time t=%lf\n",indiv->id,indiv->PrEP_cascade_status,PrEP_type, t);
	fflush(stdout);
    }

    if(indiv->PrEP_cascade_status!=NOTONPREP){
	printf("Error - in function start_PrEP_for_person id=%li is already on PrEP: current PrEP status=%i at time t=%lf\n",indiv->id,indiv->PrEP_cascade_status,t);
	fflush(stdout);
	exit(1);
    }
    
    /* double age = t-indiv->DoB; */
    /* /\* Add 1 to make sure we didn't schedule when they were eligible: *\/ */
    /* if((age>(MAX_AGE_PREP_INTERVENTION+1) && age>(MAX_AGE_PREP_BACKGROUND+1)) || (age<MIN_AGE_PREP_INTERVENTION && age<MIN_AGE_PREP_BACKGROUND)){ */
    /*     printf("Trying to start PrEP for a woman aged %lf id=%ld !!! Exiting\n", age,indiv->id); */
    /*     printf("LINE %d; FILE %s\n", __LINE__, __FILE__); */
    /*     fflush(stdout); */
    /*     exit(1); */
    /* } */

    if(indiv->cd4 == DEAD || indiv->HIV_status>UNINFECTED){
	//if (VERBOSE_OUTPUT==1){
	/*  Because of the way we draw PrEP intervention visits (for non-Manicaland) at the beginning of the year, it is possible some people die or become HIV+ before they are visited. If this is the case then do nothing more. */
	if (MANICALAND_CASCADE==0){
	    if(indiv->cd4 == DEAD)
		printf("individual %li died before receiving PrEP intervention.\n",indiv->id);
	    else
		cumulative_outputs->N_total_seroconvert_before_starting_PrEP++;

	    return;
	}
	/* In the Manicaland cascade PrEP is done on a timestep basis so this shouldn't happen. */
	else if (MANICALAND_CASCADE==1){
	    if(indiv->cd4 == DEAD){
		printf("Error: individual %li died before receiving PrEP intervention. Exiting\n",indiv->id);
		exit(1);
	    }
	    else if(HIV_TEST_WHEN_ON_PrEP==0){
		printf("Error: individual %li seroconverted before receiving PrEP intervention. Exiting\n",indiv->id);
		exit(1);
	    }

	}
    }

    /************************************ HERE WE INCLUDE HIV TESTING *************************************/
    /* In the other HIV_TEST_WHEN_ON_PrEP scenarios we assume that we only consider HIV-negative people (because otherwise when PrEP levels are high, the PrEP-related HIV test is a super-effective way to mop up all HIV+ individuals in primary pop - in reality we probably won't find all the primary pop people). */
    if(HIV_TEST_WHEN_ON_PrEP==1){
	if(indiv->id == FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH){
	    printf("In function start_PrEP_for_person() id=%li we are removing this person from any scheduled future HIV test (as they will get HIV tested as part of being on PrEP (previous index was %li). They should be getting an HIV test now.\n",indiv->id,indiv->idx_cascade_event[0]);
	    fflush(stdout);
	}
	/* Conduct an HIV tests, so remove this person from HIV testing this year if they've got one scheduled: */
	remove_from_cascade_events(indiv, patch[p].cascade_events, patch[p].n_cascade_events, patch[p].size_cascade_events, t, patch[p].param);
	indiv->next_cascade_event=CASCADEEVENT_HIV_TEST_PrEP_NONPOPART;

	/* Carry out HIV test for this person: */
	hiv_test_process(indiv, patch[p].param, t, patch[p].cascade_events, 
			 patch[p].n_cascade_events, patch[p].size_cascade_events, patch[p].hiv_pos_progression, 
			 patch[p].n_hiv_pos_progression, patch[p].size_hiv_pos_progression, 
			 patch[p].cumulative_outputs, patch[p].calendar_outputs, 
			 patch[p].vmmc_events, patch[p].n_vmmc_events, patch[p].size_vmmc_events, 
			 patch, p, debug);
	if(indiv->id == FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH){
	    if(indiv->ART_status==ARTNAIVE)
		printf("Individual id=%li tested HIV+ when trying to initate PrEP at time t=%lf\n",indiv->id,t);
	    fflush(stdout);
	}

	
	
	/* If they test positive, then the ART initiation is dealt with by HIV_test_process(), so we can just move to the next person. */
	if(indiv->ART_status==ARTNAIVE){
	    //cumulative_outputs->N_total_seroconvert_before_starting_PrEP++;
	    return;
	}
    }
    /************************************ END OF PRE-PREP HIV TEST  *************************************/


    
    /* There is a probability that they will start PrEP in this timestep (which is a function of their PrEP cascade immediately start PrEP, and we schedule future PrEP events
       (stopping PrEP, becoming less adherent etc). : */

    if(PrEP_type==PREPTYPE_DAILYORALPREP){
	double x = gsl_rng_uniform(rng);

	/* Here we allow for different PrEP adherence profiles if start due to intervention or not: */
	double p_becomes_adherent;
	p_becomes_adherent = param->PrEP_background_params->p_becomes_PrEP_adherent_background;

	/* Individual initiates PrEP and is fully adherent: */
	if (x<=p_becomes_adherent){
	    indiv->PrEP_cascade_status = ONPREP_ADHERENT;
	    //printf("Indiv %li is now on PrEP at t=%lf\n",indiv->id,t);
	    /* Decide what they will do next (if they will become less adherent, or eventually stop PrEP). */
	    t_next_PrEP_event = draw_next_PrEP_event_from_adherent(indiv,t);
	    schedule_generic_PrEP_event(indiv, param, PrEP_events, n_PrEP_events, size_PrEP_events, t, t_next_PrEP_event);

	}
	/* Individual initiates PrEP but only semi-adherent: */
	else{
	    indiv->PrEP_cascade_status = ONPREP_SEMIADHERENT;
	    printf("Indiv %li is now semi-adherent on PrEP at t=%lf\n",indiv->id,t);
	    /* Decide what they will do next (if they will become more adherent, or eventually stop PrEP). */
	    t_next_PrEP_event = draw_next_PrEP_event_from_semiadherent(indiv,t);
	    schedule_generic_PrEP_event(indiv, param, PrEP_events, n_PrEP_events, size_PrEP_events, t, t_next_PrEP_event);
	
	}
	/* If this person has no previous oral PrEP initiation time, then this is a first-time initiation: */
	if(indiv->date_most_recent_oralPrEP_initiation==PREP_DUMMY_DATEMOSTRECENTPREPINIT){
	    if(reason_starting_PrEP==REASON_START_PREP_AGYWINTERVENTION)
		cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15to24F++;
	    else if(reason_starting_PrEP==REASON_START_PREP_SDPARTNERINTERVENTION)
		cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15plus_sdpartner++;
	    else if(reason_starting_PrEP!=REASON_START_PREP_BACKGROUND && reason_starting_PrEP!=REASON_START_PREP_INTERVENTION){
		printf("Error: Unknown reason for starting PrEP. Exiting\n");
		exit(1);
	    }
	}
	
	indiv->date_most_recent_oralPrEP_initiation = t;
    }
    else if(PrEP_type==PREPTYPE_DAPIVIRINERINGPREP){
	indiv->PrEP_cascade_status = ONDAPIVIRINERING_PREP;
	//printf("Indiv %li is now on dapivirine ring PrEP at t=%lf\n",indiv->id,t);
	/* Decide what they will do next: */
	t_next_PrEP_event = draw_next_dapivirineringPrEP_event_from_initiation(indiv,t);
	schedule_generic_PrEP_event(indiv, param, PrEP_events, n_PrEP_events, size_PrEP_events, t, t_next_PrEP_event);

	/* If this person has no previous dapivirine ring PrEP initiation time, then this is a first-time initiation: */
	if(indiv->date_most_recent_dapivirineringPrEP_initiation==PREP_DUMMY_DATEMOSTRECENTPREPINIT){
	    if(reason_starting_PrEP==REASON_START_PREP_AGYWINTERVENTION)
		cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_dapivirineringPrEPinitiations_15to24F++;
	    else if(reason_starting_PrEP==REASON_START_PREP_SDPARTNERINTERVENTION)
		cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_dapivirineringPrEPinitiations_15plus_sdpartner++;
	    else{
		printf("Error: Unknown reason for starting PrEP. Exiting\n");
		exit(1);
	    }
	}
	indiv->date_most_recent_dapivirineringPrEP_initiation = t;
    }
    else if(PrEP_type==PREPTYPE_CABLAPREP){
	indiv->PrEP_cascade_status = ONCABLA_PREP;
	//printf("Indiv %li is now on long-acting injectable Cabotegravir PrEP at t=%lf\n",indiv->id,t);
	/* Decide what they will do next: */
	t_next_PrEP_event = draw_next_CABLAPrEP_event_from_initiation(indiv,t);
	schedule_generic_PrEP_event(indiv, param, PrEP_events, n_PrEP_events, size_PrEP_events, t, t_next_PrEP_event);

	/* If this person has no previous CABLA PrEP initiation time, then this is a first-time initiation: */
	if(indiv->date_most_recent_CABLAPrEP_initiation==PREP_DUMMY_DATEMOSTRECENTPREPINIT){
	    if(reason_starting_PrEP==REASON_START_PREP_AGYWINTERVENTION)
		cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_CABLAPrEPinitiations_15to24F++;
	    else if(reason_starting_PrEP==REASON_START_PREP_SDPARTNERINTERVENTION)
		cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_CABLAPrEPinitiations_15plus_sdpartner++;
	    else{
		printf("Error: Unknown reason for starting PrEP. Exiting\n");
		exit(1);
	    }
	}
	indiv->date_most_recent_CABLAPrEP_initiation = t;
    }
    else{
	printf("Unknown PrEP type in function start_PrEP_for_person(). Exiting\n");
	fflush(stdout);
	exit(1);
    }

    /* Set the reason for starting PrEP: */
    indiv->reason_for_starting_PrEP = reason_starting_PrEP;

    if(HIV_TEST_WHEN_ON_PrEP==1 || HIV_TEST_WHEN_ON_PrEP==2){
	/* Note that t_next_PrEP_event is the calendar time of the next PrEP event. */
	double THIS_PREPTYPE_TIME_TO_NEXT_HIV_TEST;
	if(PrEP_type==PREPTYPE_DAILYORALPREP)
	    THIS_PREPTYPE_TIME_TO_NEXT_HIV_TEST = ORALPREP_TIME_TO_NEXT_HIV_TEST;
	else if(PrEP_type==PREPTYPE_DAPIVIRINERINGPREP)
	    THIS_PREPTYPE_TIME_TO_NEXT_HIV_TEST = DAPIVIRINERING_TIME_TO_NEXT_HIV_TEST;
	else if(PrEP_type==PREPTYPE_CABLAPREP)
	    THIS_PREPTYPE_TIME_TO_NEXT_HIV_TEST = CABLA_TIME_TO_NEXT_HIV_TEST;
	else{
	    printf("Unknown PrEP type in function start_PrEP_for_person(). Exiting\n");
	    fflush(stdout);
	    exit(1);
	}
	if((t_next_PrEP_event-t)>=THIS_PREPTYPE_TIME_TO_NEXT_HIV_TEST){
	    if(indiv->id == FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH){
		printf("In function start_PrEP_for_person() id=%li we are scheduling a future HIV test as part of being on PrEP\n",indiv->id);
		fflush(stdout);
	    }
	    indiv->next_cascade_event=CASCADEEVENT_HIV_TEST_PrEP_NONPOPART;
	    schedule_new_PrEPrelated_hiv_test(indiv, param, t, 
					      patch[p].cascade_events, patch[p].n_cascade_events, patch[p].size_cascade_events, PrEP_type);
	    /* could also use existing schedule_new_hiv_test??? 
	    schedule_new_hiv_test(indiv, param, t, 
				  individual ***cascade_events, long *n_cascade_events, long *size_cascade_events)
	    */
	}
    }
}



/* Decide what the next (daily oral) PrEP event will be for indiv who is currently adherent.
   Modifies indiv->next_PrEP_event and returns the time at which this will happen. */
double draw_next_PrEP_event_from_adherent(individual *indiv, double t){
    indiv->next_PrEP_event = PREP_STOP;
    /* Uniform random number between 0.4 and 0.6. */
    double x = 0.4 + gsl_rng_uniform(rng) * 0.2;
    return t + x;
    //return t + 1.0;
    //return t + 0.5;
}



/* Decide what the next PrEP event will be for indiv who is currently semi-adherent.
   Modifies indiv->next_PrEP_event and returns the time at which this will happen. */
double draw_next_PrEP_event_from_semiadherent(individual *indiv, double t){
    indiv->next_PrEP_event = PREP_STOP;
    printf("Person %li was semiadherent on PrEP at t=%lf\n",indiv->id,t);
    //return t + 1.0;
    return t + 0.5;
}

/* Decide when person stops using dapiviring ring PrEP.
   Modifies indiv->next_PrEP_event and returns the time at which this will happen. */
double draw_next_dapivirineringPrEP_event_from_initiation(individual *indiv, double t){
    indiv->next_PrEP_event = PREP_STOP;
    /* Uniform random number between 0.4 and 0.6. */
    double x = 0.4 + gsl_rng_uniform(rng) * 0.2;
    return t + x;
    //return t + 1.0;
}


/* Decide when person stops using long-acting injectable cabotegravir PrEP.
   Modifies indiv->next_PrEP_event and returns the time at which this will happen. */
double draw_next_CABLAPrEP_event_from_initiation(individual *indiv, double t){
    indiv->next_PrEP_event = PREP_STOP;
    /* Uniform random number between 0.4 and 0.6. */
    double x = 0.4 + gsl_rng_uniform(rng) * 0.2;
    return t + x;
    //return t + 1.0;
}



/* Function adds a PrEP event to the array PrEP_events[][] for an individual `indiv` at time `t_next_PrEP_event`. 
   Function is called by prep_intervention_for_person() and prep_background_for_person() */
void schedule_generic_PrEP_event(individual *indiv, parameters *param, individual ***PrEP_events, long *n_PrEP_events, long *size_PrEP_events, double t_now, double t_next_PrEP_event){

    /*
    Arguments
    ---------
    indiv : pointer to individual struct
        Individual for which the PrEP event is to be scheduled.  
    param : pointer to a parameters struct
    PrEP_events : calendar of who gets a PrEP event - consists of a 2d matrix where each row is a timestep, within each row (timestep t_i) is a list of pointers to n_PrEP_events[t_i] individuals. 
    n_PrEP_events : array of long
    size_PrEP_events : array of long
    t : double
        Current time in years
    t_event : double
        Time in years at which the VMMC event is to take place.  
    
    -------
    Returns:  Nothing.  
    */


    // This is the index for PrEP_events (and n_PrEP_events and size_PrEP_events) arrays
    int idx_this_PrEP_event = (int) (round((t_next_PrEP_event - param->COUNTRY_T_PrEP_START) * N_TIME_STEP_PER_YEAR));
    
    // Ensure that we never schedule a PrEP event during the current timestep:
    int idx_current_time = (int) (round((t_now - param->COUNTRY_T_PrEP_START) * N_TIME_STEP_PER_YEAR));
    
    // Make sure event is not scheduled for the current time
    if(idx_this_PrEP_event==idx_current_time){
        idx_this_PrEP_event += 1;
    }
    else if(idx_this_PrEP_event<idx_current_time){
        printf("Error. Scheduled PrEP event in the past.");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }


    /* Only schedule if event occurs before the end of the simulation. */    
    if(idx_this_PrEP_event<=(param->end_time_simul-param->COUNTRY_T_PrEP_START)*N_TIME_STEP_PER_YEAR){
	
	if (indiv->id==FOLLOW_INDIVIDUAL && indiv->patch_no==FOLLOW_PATCH)
	    printf("+++++Individual %ld is in schedule_generic_PrEP_event. Current events: %li %li\n", indiv->id, indiv->idx_PrEP_event[0], indiv->idx_PrEP_event[1]);

	/* Put calendar entry into the individual's struct. */	
	indiv->idx_PrEP_event[0] = idx_this_PrEP_event;
	indiv->idx_PrEP_event[1] = n_PrEP_events[idx_this_PrEP_event];
        
        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("+++++New generic PrEP event for adult %ld generated with array indices  %ld %ld\n",indiv->id, indiv->idx_PrEP_event[0], indiv->idx_PrEP_event[1]);
            fflush(stdout);
        }

        /* Check if we've run out of memory: */
        if (n_PrEP_events[idx_this_PrEP_event]>=(size_PrEP_events[idx_this_PrEP_event])){

            /* Note that I haven't got realloc to work, but in principle we could use realloc() here to increase storage. */
            printf("Unable to re-allocate PrEP_events[i]. Execution aborted.");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
        /* Add a pointer to this individual to the PrEP_events array in the correct location */
        PrEP_events[idx_this_PrEP_event][n_PrEP_events[idx_this_PrEP_event]] = indiv;
        n_PrEP_events[idx_this_PrEP_event]++;
    
    }
    else{ // If PrEP event lies after end of the simulation.  
        
        /* If next event scheduled for after the end of the simulation set to be dummy entries. */
        indiv->idx_PrEP_event[0] = EVENTAFTERENDSIMUL;
        indiv->idx_PrEP_event[1] = -1;
	indiv->next_PrEP_event = PREP_NOEVENT;
        if (indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("+++++No PrEP event scheduled for %ld as event lies after end of the simulation.\n", indiv->id);
        }
    }
}


/* Only called if MANICALAND_CASCADE==1. */
void carry_out_PrEP_events_per_timestep(double t, patch_struct *patch, int p, cumulative_outputs_struct *cumulative_outputs){
    /*Carry out any event associated with PrEP in the current time step
    
    
    Arguments
    ---------
    t : double - Current time in years.
    patch : pointer to an array of patch_struct structures
        The array of patch_struct objects that house information on patches.  See structures.h for a list of attributes that these objects have.
    p : int - Patch identifier (generally 0 or 1).
    
    Returns
    -------
    Nothing; carries out PrEP events on individuals for which they are scheduled.
    */

    int array_index_for_PrEP_event = (int) (round((t - patch[p].param->COUNTRY_T_PrEP_START) * N_TIME_STEP_PER_YEAR));

    
    /* For debugging: */
    if((array_index_for_PrEP_event<0) || (array_index_for_PrEP_event>(N_TIME_STEP_PER_YEAR*patch[p].param->end_time_simul-patch[p].param->COUNTRY_T_PrEP_START))){
        printf("ERROR: array index %d for PrEP event out of bounds", array_index_for_PrEP_event);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    int n_events = patch[p].n_PrEP_events[array_index_for_PrEP_event];
    individual *indiv;
    int n;
    /* Once we have carried out the current PrEP event, we schedule a new one at time t_next_PrEP_event. */
    double t_next_PrEP_event;

    //printf("Carrying out %d PrEP events at time t=%f\n",n_events,t);
    
    for(n=0; n<n_events; n++){
        indiv = patch[p].PrEP_events[array_index_for_PrEP_event][n];

	if(indiv->id == FOLLOW_INDIVIDUAL && p==FOLLOW_PATCH){
	    printf("In function carry_out_PrEP_events_per_timestep() id=%li current PrEP status=%i at time t=%lf with array index %i %li %li. In function, the time index is %i\n",indiv->id,indiv->PrEP_cascade_status,t,n, indiv->idx_PrEP_event[0],indiv->idx_PrEP_event[1],array_index_for_PrEP_event);
	    fflush(stdout);
	}
	
        //printf("Person %ld with PrEP status=%d is in carry_out_PrEP_events_per_timestep.\n",indiv->id,indiv->PrEP_cascade_status);
        
        /* If this individual is dead or seroconverted to HIV+, move on to the next person.
        Note - we can set up a similar procedure to other lists to remove this person from this list. */
	if(indiv->cd4 == DEAD){
	    /* For dead people, we don't need to do any new PrEP events (so use 'continue' to go to next person in the event list). */
	    //if (VERBOSE_OUTPUT==1)
		printf("individual %li died2 before receiving PrEP intervention.\n",indiv->id);
	    continue;
	}
	    
	/* For people who've seroconverted, we still carry on as normal assigning them a new PrEP event: */
	//if (VERBOSE_OUTPUT==1)

	
	if(indiv->HIV_status>UNINFECTED){
		    
	    patch[p].cumulative_outputs->N_total_seroconvert_before_starting_PrEP++;
	    if(PRINT_HIV_PREVENTION_CASCADE_INFO==1)
		printf("individual %li PrEP status %i seroconverted2 before PrEP event %i at t=%lf.\n",indiv->id,indiv->PrEP_cascade_status,indiv->next_PrEP_event,t);
			
	}
    

	/* If uncircumcised but waiting for VMMC then at this timestep they get circumcised. */
        if (indiv->next_PrEP_event==BECOME_PREP_FULLYADHERENT){
	    /* Only counts as initiation if not switching: */
	    if(indiv->PrEP_cascade_status==NOTONPREP || indiv->PrEP_cascade_status==WAITINGTOSTARTPREP){
		/* If this person has no previous oral PrEP initiation time, then this is a first-time initiation: */
		if(indiv->date_most_recent_oralPrEP_initiation==PREP_DUMMY_DATEMOSTRECENTPREPINIT){
		    if(indiv->reason_for_starting_PrEP==REASON_START_PREP_AGYWINTERVENTION)
			cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15to24F++;
		    else if(indiv->reason_for_starting_PrEP==REASON_START_PREP_SDPARTNERINTERVENTION)
			cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15plus_sdpartner++;
		    else if(indiv->reason_for_starting_PrEP!=REASON_START_PREP_BACKGROUND && indiv->reason_for_starting_PrEP!=REASON_START_PREP_INTERVENTION){
			printf("Error: Unknown reason for starting PrEP. Exiting\n");
			exit(1);
		    }
		}
		indiv->date_most_recent_oralPrEP_initiation = t;
	    }
	    indiv->PrEP_cascade_status=ONPREP_ADHERENT;
	    
	    /* Decide what they will do next (if they will become less adherent, or eventually stop PrEP). */
	    t_next_PrEP_event = draw_next_PrEP_event_from_adherent(indiv,t);
	    schedule_generic_PrEP_event(indiv, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, t, t_next_PrEP_event);
        }
	else if (indiv->next_PrEP_event==BECOME_PREP_SEMIADHERENT){
	    if(indiv->PrEP_cascade_status==NOTONPREP || indiv->PrEP_cascade_status==WAITINGTOSTARTPREP){
		/* If this person has no previous oral PrEP initiation time, then this is a first-time initiation: */
		if(indiv->date_most_recent_oralPrEP_initiation==PREP_DUMMY_DATEMOSTRECENTPREPINIT){
		    if(indiv->reason_for_starting_PrEP==REASON_START_PREP_AGYWINTERVENTION)
			cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15to24F++;
		    else if(indiv->reason_for_starting_PrEP==REASON_START_PREP_SDPARTNERINTERVENTION)
			cumulative_outputs->cumulative_outputs_MIHPSA->N_firsttime_oralPrEPinitiations_15plus_sdpartner++;
		    else if(indiv->reason_for_starting_PrEP!=REASON_START_PREP_BACKGROUND && indiv->reason_for_starting_PrEP!=REASON_START_PREP_INTERVENTION){
			printf("Error: Unknown reason for starting PrEP. Exiting\n");
			exit(1);
		    }
		}
		
		indiv->date_most_recent_oralPrEP_initiation = t;
	    }
	    indiv->PrEP_cascade_status=ONPREP_SEMIADHERENT;
	    /* Decide what they will do next (if they will become more adherent, or eventually stop PrEP). */
	    t_next_PrEP_event = draw_next_PrEP_event_from_semiadherent(indiv,t);
	    schedule_generic_PrEP_event(indiv, patch[p].param, patch[p].PrEP_events, patch[p].n_PrEP_events, patch[p].size_PrEP_events, t, t_next_PrEP_event);
        }

	/* No future need for PrEP (or no longer eligible due to age?). */
	else if (indiv->next_PrEP_event==PREP_STOP){
	    /* Set the correct PrEP stop time variable (e.g. indiv->date_most_recent_oralPrEP_stoppage) for the PrEP modality they are stopping. Note - this needs to be done before we set their PrEP status to nothing. */
	    set_PrEP_stop_time(indiv, t);
	    
	    indiv->PrEP_cascade_status=NOTONPREP;
	    if (indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
		printf("+++++In carry_out_PrEP_events_per_timestep() at t=%6.4lf, indiv %li had PrEP eevnts %ld %ld, and is now stopping PrEP.\n", t, indiv->id,indiv->idx_PrEP_event[0],indiv->idx_PrEP_event[1]);
	    }
	    indiv->idx_PrEP_event[0] = -1;
	    indiv->idx_PrEP_event[1] = -1;
	    indiv->next_PrEP_event = PREP_NOEVENT;
	    //printf("Stopped PrEP for individual %li at time=%lf\n",indiv->id,t);
	}
	else{
            printf("ERROR: not sure why this person %ld with PrEP status=%d is in carry_out_PrEP_events_per_timestep(), array index=%i %li %li. Exiting\n",indiv->id,indiv->PrEP_cascade_status,n,indiv->idx_PrEP_event[0],indiv->idx_PrEP_event[1]);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
    }
    
}



/* Function deals with what happens when someone finds out they are HIV+ in hiv_test_process() function in hiv.c. 
   Stops any type of PrEP (oral, ring, injectable).
*/
void cancel_PrEP(individual *indiv, individual ***PrEP_events, long *n_PrEP_events, long *size_PrEP_events, double t, parameters *param, cumulative_outputs_struct *cumulative_outputs){

    /* /\* FOR DEBUGGING: *\/ */
    /* if (cascade_events[i][indiv->idx_cascade_event[1]]->id!=indiv->id){ */
    /* 	printf("ERROR: trying to swap out the wrong person in remove_from_cascade_events(). Trying to swap %li but in cascade_events[] the person is %li. Exiting\n",indiv->id,cascade_events[i][indiv->idx_cascade_event[1]]->id); */
    /* 	printf("LINE %d; FILE %s\n", __LINE__, __FILE__); */
    /* 	fflush(stdout); */
    /* 	exit(1); */
    /* } */
    /* if (n_cascade_events[i]>0){ */
    /* 	individual *person_to_move; */
	
    /* 	person_to_move = cascade_events[i][n_cascade_events[i]-1]; */
	
    /* 	/\* Now replace the indiv with the person_to_move in cascade_events: *\/ */
	
    /* 	cascade_events[i][indiv->idx_cascade_event[1]] = person_to_move; */
    /* 	/\* Update the details of person_to_move (note idx_cascade_event[0] remains the same): *\/ */
    /* 	person_to_move->idx_cascade_event[1] = indiv->idx_cascade_event[1]; */
    /* 	/\* We have removed one person: *\/ */
    /* 	n_cascade_events[i]--; */
    /* } */
    //printf("individual %li is diagnosed HIV+ while on PrEP status=%i\n",indiv->id,indiv->PrEP_cascade_status);
    cumulative_outputs->N_total_seroconvert_while_on_PrEP++;
    remove_from_PrEP_events(indiv, PrEP_events, n_PrEP_events, size_PrEP_events, t, param);
	//indiv->PrEP_cascade_status=NOTONPREP;
    //if (VERBOSE_OUTPUT==1)
    
    //PrEP_events[indiv->idx_PrEP_event[0]][indiv->idx_PrEP_event[1]]
    //indiv->idx_PrEP_event[0] = -1;
    //indiv->idx_PrEP_event[1] = -1;
    //indiv->next_PrEP_event = PREP_NOEVENT;

}

