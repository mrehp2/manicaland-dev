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


void set_VMMC_prevention_cascade(individual *indiv, int age, double p_use_VMMC[N_PREVENTIONBARRIER_GROUPS][2], int i_VMMC_intervention_running_flag);
void set_PrEP_prevention_cascade(individual *indiv, int age, int g, double p_use_PrEP[N_PREVENTIONBARRIER_GROUPS*N_GENDER][2], int i_PrEP_intervention_running_flag);
void set_condom_prevention_cascade(individual *indiv, int age, int g, double p_use_cond_LT[N_PREVENTIONBARRIER_GROUPS*N_GENDER][2], double p_use_cond_casual[N_PREVENTIONBARRIER_GROUPS*N_GENDER][2], int i_condom_intervention_running_flag);

void set_prevention_cascade_barriers(individual *indiv, double t, cascade_barrier_params barrier_params, int scenario_flag);
void draw_VMMC_through_barriers(double t, patch_struct *patch, int p);
void draw_PrEP_through_barriers(double t, patch_struct *patch, int p);

double get_partner_cascade_probability_condom(individual *indiv1, individual *indiv2, double t, double t_partnership);
void get_partnership_condom_use(individual *indiv1, individual *indiv2, double t, double duration_partnership);

void prevention_cascade_intervention_VMMC(double t, patch_struct *patch, int p);
void prevention_cascade_intervention_PrEP(double t, patch_struct *patch, int p);

void intervention_condom_cascade(patch_struct *patch, int p, double t, int is_counterfactual);

#endif /* CASCADES_H_ */
