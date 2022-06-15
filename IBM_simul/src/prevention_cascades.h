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


#ifndef CASCADES_H_
#define CASCADES_H_


#include "constants.h"
#include "structures.h"
#include "interventions.h"
//#include "utilities.h"
//#include "output.h"
//#include "debug.h"


int index_HIV_prevention_cascade_PrEP(int age, individual *indiv);
int index_HIV_prevention_cascade_VMMC(int age, int ever_had_sex);
int index_HIV_prevention_cascade_condom(int age, int g);

void assign_individual_PrEP_prevention_cascade(double t, individual *indiv, cascade_barrier_params *barrier_params);
void assign_individual_VMMC_prevention_cascade(double t, individual *indiv, cascade_barrier_params *barrier_params);
void assign_individual_condom_prevention_cascade(double t, individual *indiv, cascade_barrier_params *barrier_params);

void set_prevention_cascade_barriers(individual *indiv, double t, cascade_barrier_params *barrier_params, int scenario_flag);

void sweep_pop_for_VMMC_per_timestep_given_barriers(double t, patch_struct *patch, int p);
void sweep_pop_for_PrEP_per_timestep_given_barriers(double t, patch_struct *patch, int p);

double calculate_partnership_condom_cascade_probability(individual *indiv1, individual *indiv2, double t, int ptype);
void get_partnership_condom_use(individual *indiv1, individual *indiv2, double t, int ptype);

void prevention_cascade_intervention_VMMC(double t, patch_struct *patch, int p);
void prevention_cascade_intervention_PrEP(double t, patch_struct *patch, int p);

void generate_intervention_increase_in_partnership_condom_use_lookuptable(cascade_barrier_params *barrier_params);
void update_partnership_condom_use_in_response_to_intervention(individual *indiv1, individual *indiv2, cascade_barrier_params barrier_params, double t, int ptype);
void prevention_cascade_intervention_condom(double t, patch_struct *patch, int p);

void update_specific_age_VMMCbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p, int age_to_update);
void update_VMMCbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p);
void update_specific_age_PrEPbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p, int age_to_update, int g);
void update_PrEPbarriers_from_ageing(double t, int t_step, patch_struct *patch, int p);
void update_specific_age_condombarriers_from_ageing(double t, int t_step, patch_struct *patch, int p, int age_to_update, int g);
void update_condombarriers_from_ageing(double t, int t_step, patch_struct *patch, int p);
void update_PrEPrates(double t, parameters *param);
void update_VMMCrates(int t, parameters *param, double *adjustment_to_rate);
void get_VMMC_rate_adjustment_foralreadycirc_hivpos(double t, patch_struct *patch, int p, double adjustment_to_rate[2]);
void update_VMMCrates_Manicaland(int t, parameters *param, double *adjustment_to_rate);
void update_VMMCrates_MIHPSA(int t, parameters *param, double *adjustment_to_rate);
    
void update_condomrates(double t, parameters *param);
void update_condomrates_MIHPSA(double t, parameters *param);
void update_condomrates_Manicaland(double t, parameters *param);



#endif /* CASCADES_H_ */
