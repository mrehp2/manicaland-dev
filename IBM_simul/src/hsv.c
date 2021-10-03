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


/* HSV-2 processes for the PopART model: */

#include "hsv.h"
#include "constants.h"
#include "output.h"
#include "utilities.h"
#include "partnership.h"
#include "interventions.h"
#include "debug.h"


/* Function allows HSV-2 transmission probability to be a function of HIV status of each partner, HSV-2 stage etc. */
double hsv2_transmission_probability(individual* susceptible, individual* positive_partner, parameters *param){
    
    double hazard;
    
    // Assign hazard as baseline HSV-2 hazard
    hazard = param->average_annual_hazard_hsv2;



    // Add a multiplying factor for assortative risk mixing: high-high is twice as risky and low-low half as risky as other combinations. We use the same values as for HIV (assuming that they modify coital frequency and condom use).
    if(CHANGE_RR_BY_RISK_GROUP == 1){
	if(positive_partner->sex_risk == LOW && susceptible->sex_risk == LOW)
	    hazard *= 0.5;
	else if(positive_partner->sex_risk == HIGH && susceptible->sex_risk == HIGH)
	    hazard *= 2.0;
    }
    

    // Add a multiplying factor for assortative community mixing: within community is more risky than between community, reflecting higher frequency of sex act and lower condom use. Same values as HIV. 
    if(positive_partner->patch_no != susceptible->patch_no){
	hazard *= param->rr_hiv_between_vs_within_patch;
    }


    return hazard;
}

/* For a given individual, determines if HSV-2 acquisition occurs through sexual contact with any infected partner (ie in partner_pairs_HSV2pos[]) at a given timestep - using hsv2_transmission_probability() to get per-individual transmission probabilities and assuming they sum up to total transmission probability.
*/
void hsv2_acquisition(individual* susceptible, double time_infect, patch_struct *patch, int p,
    all_partnerships *overall_partnerships, output_struct *output, debug_struct *debug, 
    file_struct *file_data_store, int t0, int t_step){

    
    /* if(susceptible->id == FOLLOW_INDIVIDUAL && susceptible->patch_no == FOLLOW_PATCH){ */
    /*     printf("checking HSV-2 acquisition for adult %ld from patch %d at time %6.4f\n", */
    /*         susceptible->id, susceptible->patch_no, time_infect); */
    /*     fflush(stdout); */
    /* } */
    if(susceptible->HSV2_status!=HSV2_UNINFECTED){
        printf("ERROR: Trying to infect an HSV-2+ person %li in patch %i\n",
            susceptible->id, susceptible->patch_no);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }

    /* Characteristics of the seropositive partner which may influence transmission. Assumed to be heterosexual partners always: */
    int partner_gender = 1 - susceptible->gender;

    int i; /* Index for summing over partners. */


    /* The number of HSV2+ partners of this susceptible. */
    int npos = susceptible->n_HSV2pos_partners;

    /* FOR DEBUGGING */
    if(npos < 1){
        printf("Problem: trying to HSV-2 infect someone who is in no serodiscordant partnership\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }

    /* This will create an alias for each seropositive partner to save typing. */
    individual* temp_HSV2pos_partner;

    /* Store for the total probability of getting infected (given the susceptible's partners) at this timestep: */
    double total_hazard_per_timestep = 0.0;
    
    /* Now sum hazard over each HSV2+ partner: */
    for(i = 0; i < npos; i++){
        /* This is a pointer to the ith HSV2+ partner of the susceptible: */
        temp_HSV2pos_partner = susceptible->partner_pairs_HSV2pos[i]->ptr[partner_gender];

	total_hazard_per_timestep += hsv2_transmission_probability(susceptible, temp_HSV2pos_partner, patch[p].param) * TIME_STEP;
    }


    if (susceptible->PrEP_cascade_status>WAITINGTOSTARTPREP){
	if (susceptible->PrEP_cascade_status==ONPREP_ADHERENT)
	    total_hazard_per_timestep = total_hazard_per_timestep * (1.0-patch[p].param->eff_prep_adherent_hsv2);
	else if (susceptible->PrEP_cascade_status==ONPREP_SEMIADHERENT)
	    total_hazard_per_timestep = total_hazard_per_timestep * (1.0-patch[p].param->eff_prep_semiadherent_hsv2);
    }

    /* Reduced susceptibility if VMMC or TMC respectively: */
    if (susceptible->gender==MALE){
	if (susceptible->circ==VMMC)
	    total_hazard_per_timestep = total_hazard_per_timestep * (1.0-patch[p].param->eff_circ_hsv2_vmmc);
	if (susceptible->circ==TRADITIONAL_MC)
	    total_hazard_per_timestep = total_hazard_per_timestep * (1.0-patch[p].param->eff_circ_hsv2_tmc);
    }
    
    double x = gsl_rng_uniform (rng);
    if(x <= total_hazard_per_timestep){

        
        /* Transmit HSV-2 to this individual. */
        if(susceptible->id == FOLLOW_INDIVIDUAL && susceptible->patch_no == FOLLOW_PATCH){
            printf("Transmitting HSV-2 infection to adult %ld in patch %d at time %6.4f\n",
                susceptible->id, susceptible->patch_no, time_infect);
            fflush(stdout);
        }

        new_hsv2_infection(time_infect, FALSE, susceptible,  patch[p].n_infected_hsv2, 
            patch[p].n_newly_infected_hsv2, patch[p].age_list, patch[p].param, 
            patch[p].hsv2_pos_progression, patch[p].n_hsv2_pos_progression, 
	    patch[p].size_hsv2_pos_progression, file_data_store);
        

        /* Update each of their HSV2- partners so that they know that they have a serodiscordant partner and update list of serodiscrodant partnerships */
        inform_partners_of_hsv2seroconversion_and_update_list_hsv2serodiscordant_partnerships(susceptible, 
            overall_partnerships->susceptible_in_hsv2serodiscordant_partnership, 
            overall_partnerships->n_susceptible_in_hsv2serodiscordant_partnership);



    }
}


/* Function: inform_partners_of_hsv2seroconversion_and_update_list_hsv2serodiscordant_partnerships()
Update lists of HSV-2 serodiscorant partnerships following an HSV-2 seroconversion.  

Function firstly sets the n_HSV2pos_partners attribute of the seroconverter to zero (note:
this variable is only >0 if the individual is HSV2-, as well as has HSV2+ partners, and it is -1
for someone who is HSV2+).  Then the function goes through each partner of the seroconverter in
turn to see which are HSV2-.
For each HSV2- partner they are informed that they now have a seropositive partner (ie the
seroconverter), and if this HSV2- partner did not have any seropositive partners before they
were not in the susceptible_in_serodiscordant_partnership list, and hence are now added to this
list. 

Note: n_partners can be zero for imported cases (i.e. those in which we seed the infection).  
This should be accounted for in this function.  

Arguments
---------
seroconverter : pointer to an individual
    The individual who has just seroconverted
susceptible_in_serodiscordant_partnership : pointer to an array of individuals
    
n_susceptible_in_serodiscordant_partnership : int

Returns
-------
Nothing; adjusts the partnerships attributes of the seroconverter and each of the 
seroconverter's partners, and 
*/

void inform_partners_of_hsv2seroconversion_and_update_list_hsv2serodiscordant_partnerships(
    individual* seroconverter, individual** susceptible_in_hsv2serodiscordant_partnership, 
    long *n_susceptible_in_hsv2serodiscordant_partnership){
    
    int i;
    //printf("Informing partners of HSV-2 for id=%li n_partners=%i\n",seroconverter->id, seroconverter->n_partners);
    
    // The gender of (all) partners of this seroconverter (since the model only has heterosexuals)
    int partner_gender = 1 - seroconverter->gender;
    
    // Set up a pointer to each partner in turn; an alias to save on code
    individual* temp_partner;
    
    // Update the list of HSV-2 serodiscordant and HSV-2 seropositive partners.
    // This person has just HSV-2 seroconverted, so set the count of HSV2+ and serodiscordant partners to
    // zero as we no longer care about them. The list of indices does not need changing as this
    // counter tells us everything we need to know.  
    seroconverter->n_HSV2pos_partners = 0;

    // Loop through the partners of the seroconverter
    for(i = 0; i < seroconverter->n_partners; i++){

        // Find pointer to the ith partner of the seroconverter
        // (it points to an already allocated person so no malloc needed)
        temp_partner = seroconverter->partner_pairs[i]->ptr[partner_gender]; 
        
        // Check if the partner is currently seronegative (do nothing if they're HSV2+)
        if(temp_partner->HSV2_status == UNINFECTED){

            // Note: temp_partner->n_HSV2pos_partners is the number of HSV2+ partners
            // of this partner (prior to the current seroconversion).

            // Add the current seroconverter to the array of HSV2pos partners of temp_partner
            temp_partner->partner_pairs_HSV2pos[temp_partner->n_HSV2pos_partners] =
                seroconverter->partner_pairs[i];
            
            // Increment this partner's number of HSV2+ partners (n_HSV2pos_partners)
            temp_partner->n_HSV2pos_partners++;

	    
            /* This partnership has become HSV-2 serodiscordant so, unless the HSV2- temp_partner was already in the list of susceptible_in_hsv2serodiscordant_partnership, they have to be added there.
	       idx_hsv2_serodiscordant == -1 means before HSV-2 seroconversion of seroconverter, this individual was in no HSV-2 serodiscordant partnerships. */
            if(temp_partner->idx_hsv2_serodiscordant == -1 ){
                add_susceptible_to_list_hsv2serodiscordant_partnership(temp_partner,
                    susceptible_in_hsv2serodiscordant_partnership,
                    n_susceptible_in_hsv2serodiscordant_partnership);
            }
        } // We do nothing if the partner is currently seropositive
    }
    // Remove seroconverter from list of suscepts in serodiscordant partnerships, if appropriate
    remove_susceptible_from_list_hsv2serodiscordant_partnership(seroconverter,
        susceptible_in_hsv2serodiscordant_partnership, n_susceptible_in_hsv2serodiscordant_partnership);
}


/* Function: new_infection()
Set variables related to HSV-2 in the individual structure for a newly infected individual. 
 - Allocates what the next hsv2-related event to happen.
 - Also updates the counts of incident and prevalent cases. 
*/
void new_hsv2_infection(double time_infect, int SEEDEDHSV2INFECTION, individual* seroconverter, population_size_one_year_age *n_infected_hsv2, 
    population_size_one_year_age *n_newly_infected_hsv2, age_list_struct *age_list, 
    parameters *param, individual ***hsv2_pos_progression, long *n_hsv2_pos_progression, 
    long *size_hsv2_pos_progression, file_struct *file_data_store){

    /* SEEDEDHSV2INFECTION tells us whether this is one of the initial infections seeded at time start_time_hsv2, or an infection acquired since then.
     * For seeded infections we start them in asymptomatic infection (to avoid a wave of initial acutes). */

    int g = seroconverter->gender;
    long ncheck; 
    int aa;

    double time_to_next_event;
    int idx_next_event, idx_current_time;

    if(seroconverter->id==FOLLOW_INDIVIDUAL && seroconverter->patch_no==FOLLOW_PATCH){
        printf("New HSV-2 infection of adult %ld from patch %d and gender %d at time %6.4f\n",seroconverter->id,seroconverter->patch_no,g,time_infect);
        print_specific_IDs_by_age(FOLLOW_INDIVIDUAL,age_list,FOLLOW_PATCH);

        fflush(stdout);
    }

    
    // For non-seed cases
    if(SEEDEDHSV2INFECTION == FALSE){

        // Person is now in acute stage.
        seroconverter->HSV2_status = HSV2_ACUTE;
        seroconverter->next_HSV2_event = HSV2EVENT_BECOMEASYMPTOMATIC_FROMACUTE;
        
        // Draw time to end of acute phase
        time_to_next_event = gsl_ran_exponential(rng, param->mean_dur_hsv2event[HSV2EVENT_BECOMEASYMPTOMATIC_FROMACUTE]);
        
        if(seroconverter->id == FOLLOW_INDIVIDUAL && seroconverter->patch_no == FOLLOW_PATCH){
            printf("Individual %ld from patch %d", seroconverter->id, seroconverter->patch_no);
            printf(" is scheduled to progress from acute HSV-2 to asymptomatic HSV-2 at ");
            printf("t=%6.4f. Currently t=%6.4f\n", time_to_next_event + time_infect, time_infect);
            fflush(stdout);
        }

    }else{
        // For seeded infections assume person is in asymptomatic stage:
        seroconverter->HSV2_status = HSV2_ASYMPTOMATIC;
	seroconverter->next_HSV2_event = HSV2EVENT_RECURRENCE_FROMASYMPTOMATIC;

        // Draw time to next HSV-2 stage
        time_to_next_event = gsl_ran_exponential(rng, param->mean_dur_hsv2event[HSV2EVENT_RECURRENCE_FROMASYMPTOMATIC]);
        
        if(seroconverter->id == FOLLOW_INDIVIDUAL && seroconverter->patch_no == FOLLOW_PATCH){
            printf("Individual %ld from patch %d", seroconverter->id, seroconverter->patch_no);
            printf(" is seeded HSV2+ at time %6.4f. Scheduled to progress to next HSV-2 event %i at time %6.4lf\n", time_infect, seroconverter->next_HSV2_event, time_to_next_event + time_infect);
            fflush(stdout);
        }
    }

    idx_next_event = (int) round(((time_infect-param->start_time_hsv2) +
            time_to_next_event) * N_TIME_STEP_PER_YEAR);
    
    idx_current_time = (int) round(((time_infect-param->start_time_hsv2)) *
        N_TIME_STEP_PER_YEAR);

    // Make sure that an event is not scheduled to occur in the current time-step
    if(idx_next_event == idx_current_time){
        idx_next_event++;
    }
    
    if(time_infect+time_to_next_event < param->end_time_simul){
        seroconverter->idx_hsv2_pos_progression[0] = idx_next_event;
        seroconverter->idx_hsv2_pos_progression[1] =
            n_hsv2_pos_progression[idx_next_event];

        // Check if we've run out of memory:
        if(n_hsv2_pos_progression[idx_next_event] >=(size_hsv2_pos_progression[idx_next_event])){
            printf("Unable to re-allocate hsv2_pos_progression[i]. Execution aborted.");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
	
        hsv2_pos_progression[idx_next_event][n_hsv2_pos_progression[idx_next_event]] = seroconverter;
        n_hsv2_pos_progression[idx_next_event]++;
    }else{
        seroconverter->idx_hsv2_pos_progression[0] = EVENTAFTERENDSIMUL;
        seroconverter->idx_hsv2_pos_progression[1] = -1;

        if(seroconverter->id==FOLLOW_INDIVIDUAL && seroconverter->patch_no == FOLLOW_PATCH){
            printf("Not scheduling first HSV2 progression event after seroconversion ");
            printf("for individual %ld from patch %d as after end of simulation at t=%6.4f\n", 
                seroconverter->id, seroconverter->patch_no, time_infect + time_to_next_event);
            fflush(stdout);
        }
    }

    // Add seroconverter to lists of infected individuals, in the correct age category
    aa = (int) floor(floor(time_infect) - seroconverter->DoB) - AGE_ADULT;
    
    /* DEBUGGING - CAN REMOVE ALL THE DIFFERENT AI HERE */
    if(aa < (MAX_AGE - AGE_ADULT)){

        /* ai is the age index of the array n_infected_hsv2->pop_size_per_gender_age1_risk[g][ai][r] for the person with DoB as above at t_infect. */

        // Indices for the HSV-2 prevalence, incidence counters:
        int ai_prev = n_infected_hsv2->youngest_age_group_index + aa;
        while (ai_prev>(MAX_AGE-AGE_ADULT-1))
            ai_prev = ai_prev - (MAX_AGE-AGE_ADULT);

        int ai_inc = n_newly_infected_hsv2->youngest_age_group_index + aa;
        while (ai_inc>(MAX_AGE-AGE_ADULT-1))
            ai_inc = ai_inc - (MAX_AGE-AGE_ADULT);

        int ai_age = age_list->age_list_by_gender[g]->youngest_age_group_index + aa;
        while (ai_age>(MAX_AGE-AGE_ADULT-1))
            ai_age = ai_age - (MAX_AGE-AGE_ADULT);

        /* looking for the seroconverter in the age_list --> presumably only for debugging, could get rid of this in final code to speed up. */
        ncheck = 0;
        while ((ncheck<age_list->age_list_by_gender[g]->number_per_age_group[ai_age]) && (age_list->age_list_by_gender[g]->age_group[ai_age][ncheck]->id!=seroconverter->id)){
            ncheck++;
        }

        if((ncheck>=age_list->age_list_by_gender[g]->number_per_age_group[ai_age])){
            printf("PROBLEM in new_hsv2_infection() at time %f: Person not found %li from patch %d: should be in age group %i\n",time_infect,seroconverter->id,seroconverter->patch_no,ai_age);
            printf("time = %6.4f, DoB= %6.4f, aa = %i\n",time_infect,seroconverter->DoB,aa);

            /* For debugging: */
            find_in_age_list(time_infect,seroconverter,age_list,param);
            printf("Patch %d: ",seroconverter->patch_no);
            fflush(stdout);
            print_specific_IDs_by_age(FOLLOW_INDIVIDUAL,age_list,FOLLOW_PATCH);

            print_individual(seroconverter);
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
        // Add the seroconverter to n_infected_hsv2 in the correct age group
        (n_infected_hsv2->pop_size_per_gender_age1_risk[seroconverter->gender][ai_prev][seroconverter->sex_risk])++;


        /* adding the seroconverter to n_newly_infected_hsv2 in the right age group */
        (n_newly_infected_hsv2->pop_size_per_gender_age1_risk[seroconverter->gender][ai_inc][seroconverter->sex_risk])++;



    }else{

        /* looking for the seroconverter in the age_list --> presumably only for debugging, could get rid of this? */
        ncheck = 0;
        while ((ncheck<age_list->age_list_by_gender[g]->number_oldest_age_group) && (age_list->age_list_by_gender[g]->oldest_age_group[ncheck]->id!=seroconverter->id)){
            ncheck++;
        }
        if ((ncheck>=age_list->age_list_by_gender[g]->number_oldest_age_group))
            printf("PROBLEM: Person not found in oldest age group: %li in patch %d gender %d\n",seroconverter->id,seroconverter->patch_no,g);

        /* adding the seroconverter to n_infected_hsv2 in the right age group */
        (n_infected_hsv2->pop_size_oldest_age_group_gender_risk[seroconverter->gender][seroconverter->sex_risk])++;

        /* adding the seroconverter to n_newly_infected_hsv2 in the right age group */
        (n_newly_infected_hsv2->pop_size_oldest_age_group_gender_risk[seroconverter->gender][seroconverter->sex_risk])++;

    }
}


/* Function: draw_initial_hsv2_infection()
Seed initial HSV2 infection - determines if an individual from the population will be a seeding HSV-2 infection. 
 This function is called within simul.c when HSV2 seeding is started.  For each individual in the population, the test of whether or not they are a seed cases is a Bernoulli trial, infecting individual indiv with probability param->initial_prop_hsv2infected. 

Arguments
---------
t : double
    Year
indiv : pointer to an individual structure
    An individual in the population, a potential seed case
patch : pointer to a patch structure
p : int
    Patch number
overall_partnerships : pointer to an all_partnerships structure
output : pointer to a output_struct structure
    Used for the called functions that might write something to file
file_data_store : pointer to a file_struct structure
    Used for the called functions that might write something to file

Returns
-------
Nothing; sets an input individual (indiv) as a seeding case according to a Bernoulli trial.  If the
individual is a seeding case this function calls new_hsv2_infection(), increments the number of infected
cases, sets the individual's SPVL to -1, and updates lists of serodiscorant partnerships following
a seroconversion.  
*/

void draw_initial_hsv2_infection(double t, individual* indiv, patch_struct *patch, int p,
    all_partnerships *overall_partnerships, output_struct *output, file_struct *file_data_store){
    
    // Run a couple of checks to begin with
    if(indiv->cd4 == DUMMYVALUE){
        printf("Error: using an uninitialised person in draw_initial_hsv2_infection().\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    if(indiv->cd4 == DEAD){
        printf("Error: trying to make a dead person acquire HSV2 at HSV2 introduction.\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    

    if(indiv->HSV2_status > UNINFECTED){
        printf("Error: trying to seed HSV-2 in an HSV-2 positive person.\n");
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }

    
    // Draw a random uniform number and determine if this individual is a seed case or not
    double random = gsl_rng_uniform(rng);
    if(random < patch[p].param->initial_prop_hsv2infected){

        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("Seeding HSV-2 infection of adult %ld in patch %d at time %6.4f\n", indiv->id, indiv->patch_no,t);
            fflush(stdout);
        }
	
        // Generate a new HSV-2 infection
        new_hsv2_infection(t, TRUE, indiv, patch[p].n_infected_hsv2, patch[p].n_newly_infected_hsv2,
            patch[p].age_list, patch[p].param, patch[p].hsv2_pos_progression,
            patch[p].n_hsv2_pos_progression, patch[p].size_hsv2_pos_progression,
	    file_data_store);

        inform_partners_of_hsv2seroconversion_and_update_list_hsv2serodiscordant_partnerships(indiv,
            overall_partnerships->susceptible_in_hsv2serodiscordant_partnership,
            overall_partnerships->n_susceptible_in_hsv2serodiscordant_partnership);
        
    }
}


/* Function: next_hsv2_event()
Determine the next HSV2-related event for an individual given their current HSV-2 state. 

Arguments
---------
indiv : pointer to an individual structure
    The individual in question (for whom these events are to be scheduled).  
hsv2_pos_progression : pointer to a multi-dimensional array of individuals
n_hsv2_pos_progression : pointer to long
size_hsv2_pos_progression : pointer to long
param : pointer to a parameters structure
    Parameters structure of the simulation
t : double
    Current time in years


Returns
-------
Nothing;
*/

void next_hsv2_event(individual* indiv, individual ***hsv2_pos_progression, long *n_hsv2_pos_progression, long *size_hsv2_pos_progression, parameters *param, double t){
    
    double time_to_next_event;
    int t_step_event;
    
    if((indiv->cd4 < 0) || (indiv->cd4 > 3)){
        printf("ERROR: Unrecognised cd4  %i %li\n",indiv->cd4,indiv->id);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }


    if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
        printf("Individual %ld in patch %d time = %6.4f in next_hsv2_event()\n",
            indiv->id, indiv->patch_no, t);
        fflush(stdout);
    }
    
    /* Draw time to next HSV-2 event: */
    time_to_next_event = gsl_ran_exponential(rng, param->mean_dur_hsv2event[indiv->next_HSV2_event]);
    
    /* Ensure we never have an event in the current timestep. */
    if(time_to_next_event < TIME_STEP){
        time_to_next_event = TIME_STEP;
    }
    
    if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
        printf("Individual %ld in patch %d ", indiv->id, indiv->patch_no);
        printf("time = %6.4f. Time to next HSV-2 event = %6.4f in function next_hsv2_event() drawn from exp(%lf)\n",t,time_to_next_event,param->mean_dur_hsv2event[indiv->next_HSV2_event]);
        fflush(stdout);
    }

    
    
    /* This gets the index for hsv2_pos_progression
    (and n_hsv2_pos_progression and size_hsv2_pos_progression) arrays. */
    t_step_event = (int) round(((t - param->start_time_hsv2) + time_to_next_event) * N_TIME_STEP_PER_YEAR); 
    
    /* For debugging: */
    if(t_step_event == indiv->idx_hsv2_pos_progression[0]){
        printf("ERROR - trying to schedule a new HSV-2 event in next_hsv2_event() that occurs ");
        printf("at the same time as the current event for person %ld ", indiv->id);
        printf("in patch %d at time = %6.4f. Exiting\n",indiv->patch_no, t);
        printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
        fflush(stdout);
        exit(1);
    }
    
    /* Only add an event if this happens before the end of the simulation: */
    if(t_step_event <= (param->end_time_simul - param->start_time_hsv2) * N_TIME_STEP_PER_YEAR){
        
        //indiv->debug_last_hsv2_event_index = indiv->idx_hsv2_pos_progression[0];
        indiv->idx_hsv2_pos_progression[0] = t_step_event;
        indiv->idx_hsv2_pos_progression[1] = n_hsv2_pos_progression[t_step_event];
        
        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("Adding HSV-2 progression event for %ld in patch %d ", indiv->id, indiv->patch_no);
            printf("at time = %6.4f i=%i. Indiv indices %ld %ld\n",
                t + time_to_next_event, t_step_event,
                indiv->idx_hsv2_pos_progression[0], indiv->idx_hsv2_pos_progression[1]);
            
            fflush(stdout);
        }

        /* Check if we've run out of memory: */
        if(n_hsv2_pos_progression[t_step_event] >= (size_hsv2_pos_progression[t_step_event])){
            
            /* Note that realloc does not work (we need to pass a pointer to the pointer, which is
            really complicated as it propagates through several functions (so maybe make
            planned_breakups[time_breakup] **), so ditch this code for now and use the following
            lines: */
            printf("Unable to re-allocate hsv2_pos_progression[i]. Execution aborted.");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        hsv2_pos_progression[t_step_event][n_hsv2_pos_progression[t_step_event]] = indiv;
        n_hsv2_pos_progression[t_step_event]++;

    }else{
        /* Next event happens after end of simulation so set to no event. */
        indiv->idx_hsv2_pos_progression[0] = EVENTAFTERENDSIMUL;
        indiv->idx_hsv2_pos_progression[1] = -1;

        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("Not scheduling HSV-2 progression event for %ld ", indiv->id);
            printf("in patch %d as after end of simulation at t=%6.4f\n",
                indiv->patch_no, t + time_to_next_event);
            fflush(stdout);
        }
    }
    if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
        printf("Next HSV-2 progression event for %ld in patch %d ", indiv->id, indiv->patch_no);
        printf("is scheduled to be %i at t=%6.4f. Indiv indices are %li %li\n",
            indiv->next_HSV2_event, t + time_to_next_event, 
            indiv->idx_hsv2_pos_progression[0], indiv->idx_hsv2_pos_progression[1]);
        
        fflush(stdout);
    }
}




/* Function: carry_out_HSV2_events_per_timestep()
Go through the list of scheduled HSV-2 events for HSV-2+ people for this timestep

For each person to whom some HSV-2 event happens, draw their next HSV2-based event (via 
indiv->next_HSV2_event).  The list of scheduled HSV-2 events are stored in the array patch[p].hsv2_pos_progression and the list of possible events are
defined in constants.h.  This function checks the individual's attribute next_HSV2_event and determines the following HSV-2 event.
Finally, next_HSV2_event() is called to determine the next event for an individual.  

Arguments
---------

t : double
    Year in question
patch : pointer to a patch_struct structure
p : int
    Patch number
overall_partnerships : pointer to an all_partnerships structure
debug : pointer to a debug_struct structure
file_data_store : pointer to a file_struct structure

Returns
-------
Nothing; carries out HSV-2 events for a particular timestep for individuals with a scheduled event and schedules new events for those individuals.  Various lists and individual attributes are updated.  
*/

void carry_out_HSV2_events_per_timestep(double t, patch_struct *patch, int p, 
    all_partnerships *overall_partnerships, debug_struct *debug, file_struct *file_data_store){

    int array_index_for_hsv2_event = 
        (int) round((t - patch[p].param->start_time_hsv2) * N_TIME_STEP_PER_YEAR);
    
    int n;
    int n_events = patch[p].n_hsv2_pos_progression[array_index_for_hsv2_event];
    individual *indiv;
    
    // Loop through all HSV-2 events this timestep
    for(n = 0; n < n_events; n++){
        // Assign pointer to the individual in question
        indiv = patch[p].hsv2_pos_progression[array_index_for_hsv2_event][n];
        
        if(indiv->cd4 == DUMMYVALUE){
            printf("Error. Using uninitialised person.\n");
            printf("LINE %d; FILE %s\n", __LINE__, __FILE__);
            fflush(stdout);
            exit(1);
        }
        
        if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
            printf("Calling carry_out_HSV2_events_per_timestep() for ");
            printf("%ld in patch %d at t=%6.4f, index = %i %i. Indiv indices are %li %li\n",
                indiv->id, indiv->patch_no, t, array_index_for_hsv2_event, n,
                indiv->idx_hsv2_pos_progression[0], indiv->idx_hsv2_pos_progression[1]);
            fflush(stdout);
        }
        
        if(indiv->cd4 == DEAD){  // Note that cd4 is ALWAYS an indicator that the person is dead!
            if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
                printf("Individual %ld from patch %d is dead, ", indiv->id, indiv->patch_no);
                printf("so not carrying out further HSV-2 events for this person at t=%6.4f\n",t);
                fflush(stdout);
            }
            // Move to the next person. Note - we can set up a similar procedure to other lists to
            // remove this person from this list but it is not necessary. As things stand, no hsv-2
            // event happens to the dead person and no new event is scheduled for them.
            continue;
        }




	/* Decide next HSV2 event following this one: */
	if (indiv->next_HSV2_event==HSV2EVENT_BECOMEASYMPTOMATIC_FROMACUTE){
	    indiv->HSV2_status = HSV2_ASYMPTOMATIC;
	    indiv->next_HSV2_event = HSV2EVENT_RECURRENCE_FROMASYMPTOMATIC;
	
	}
	else if (indiv->next_HSV2_event==HSV2EVENT_RECURRENCE_FROMASYMPTOMATIC){
	    indiv->HSV2_status = HSV2_RECURRENCE;
	    indiv->next_HSV2_event = HSV2EVENT_BECOMEASYMPTOMATIC_FROMRECURRENCE;
	}
	else if (indiv->next_HSV2_event==HSV2EVENT_BECOMEASYMPTOMATIC_FROMRECURRENCE){
	    indiv->HSV2_status = HSV2_ASYMPTOMATIC;
	    indiv->next_HSV2_event = HSV2EVENT_RECURRENCE_FROMASYMPTOMATIC;
	}
	else{
	    printf("Unknown HSV-2 event in next_hsv2_event(). Exiting\n");
	    fflush(stdout);
	    exit(1);
	}



                
	if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
	    printf("Individual %ld from patch %d is ", indiv->id, indiv->patch_no);
	    printf("progressing to HSV-2 stage %i at t=%6.4f, with next HSV-2 event to be %i\n",indiv->HSV2_status,t,indiv->next_HSV2_event);
	    fflush(stdout);
	}


	// Schedule next HSV-2 event. 
	if(indiv->next_HSV2_event != NOEVENT){
	    if(indiv->id == FOLLOW_INDIVIDUAL && indiv->patch_no == FOLLOW_PATCH){
		printf("Individual %ld in patch %d ", indiv->id, indiv->patch_no);
		printf("time = %6.4f going from carry_out_HSV2_events_per_timestep()", t);
		printf(" to next_hsv2_event()\n");
		fflush(stdout);
	    }


	    next_hsv2_event(indiv, patch[p].hsv2_pos_progression, 
		patch[p].n_hsv2_pos_progression, patch[p].size_hsv2_pos_progression,
	        patch[p].param, t);
	}
    }
}



/* Function is a prototype for Weibull distribution RV.
   Orroth et al (STDSIM) assume that HSV-2 ulcers last 1 week on average
   with Weibull distribution with shape parameter=2. */
double get_ulcer_duration(){
    double t_ulcer_duration;
    //gsl_ran_weibull(const gsl_rng * r, double a, double b);
    /* where:
       b = k = shape parameter
       a = lambda = scale parameter
       
       So b =2
       Mean of Weibull is lambda * Gamma(1+1/k) = a*Gamma(3/2)
       So a = 1 week / (Gamma(3/2))
 */


    /* lgamma(x) in C is the natural log of the Gamma function. */
    /* Gamma(3/2) = 0.5*sqrt(pi) = 0.8862269254527580137. */
    
    double g = exp(lgamma(1.5));
    double a = (7/365.0) /g;



    /* Unit test I ran to check this works - checking mean was roughly 1 week, and distribution was Weibull-like. */
    /* int i; */
    /* for(i=0;i<1000;i++){ */
    /* 	x = gsl_ran_weibull(rng, a, 2); */
    /* 	printf("%12.10lf\n",x); */
    /* } */

    t_ulcer_duration = gsl_ran_weibull(rng, a, 2);
    return t_ulcer_duration;
}
