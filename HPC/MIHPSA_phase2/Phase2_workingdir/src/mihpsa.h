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

#ifndef MIHPSA_H_
#define MIHPSA_H_

#include "structures.h"


double find_population_scale(patch_struct *patch, int p, double real_population);
void count_adult_pop_by_gender(patch_struct *patch, int p, double *N_m, double *N_f);

double count_15plus_scale(patch_struct *patch, int p);

void MIHPSA_determine_PrEP_scenario(double t, patch_struct *patch, int p, debug_struct *);


void mihpsa_minimalscenario_increasemulitplepartners(double , patch_struct *);

void MIHPSA_sweep_through_condomusepartnerships_reduce_forcondomuse_minimalscenario(patch_struct *patch, int p, double t);

void MIHPSA_update_partnership_condom_use_in_response_to_reducedcondomuse(individual *indiv1, individual *indiv2, double duration_partnership, parameters *param, double t);

double MIHPSA_new_condomuse_when_CUPP_switchedoff(double original_condomuse, double decreasein_nonuse_with_CUPPon);

void initialise_MIHPSA_flags(patch_struct *patch, int p);

void fix_MIHPSA_parameters(patch_struct *patch, int p);

void MIHPSA_hack_set_PrEP_parameters(parameters *allrunparameters, int n_runs);

#endif /* MIHPSA_H_ */
