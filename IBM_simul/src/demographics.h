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

#ifndef DEMOGRAPHICS_H_
#define DEMOGRAPHICS_H_

#include "structures.h"

double per_woman_fertility_rate(int , parameters *, int, double);
void get_mtct_fraction(double , patch_struct *, int , double *, double *);
void get_unpd_time_indices(double , int *, double *);
double childhood_mortality(parameters *, double );
double natural_death_rate(int , int , parameters *, double );
int draw_sex_risk(int, parameters *);
void create_mtct_templates(mtct_hiv_template *, parameters *);
int get_art_status_of_mtct_new_adult(double , parameters *);
void add_hiv_info_for_new_hiv_positive_adult(individual *, int, double , parameters *, patch_struct *, int );
void create_new_individual(individual *, double , int, parameters *, int, 
    patch_struct *, int, all_partnerships *, int );
void update_population_size_new_adult(individual *, population_size *, 
    population_size_one_year_age *, stratified_population_size *);
void update_population_size_death(individual *, population_size *, 
    population_size_one_year_age *, population_size_one_year_age *, population_size_one_year_age *n_infected, 
    stratified_population_size *, int, age_list_struct *,
    population_size_one_year_age_hiv_by_stage_treatment *);
void initialize_first_cascade_event_for_new_individual(individual *, double, 
    parameters *, individual ***, long *, long *, individual ***, long *, long *, population_size_one_year_age_hiv_by_stage_treatment *);
void update_age_list_new_adult(age_list_struct *, individual *);
void update_age_list_death(age_list_struct *, int, int, long, double , int);
int get_age_index(double , double );
int get_age_indexv2(double , double , int);
int get_age_group(double , double , const int [], int);
int get_age_group_unpd(double , double );
void update_n_population_ageing_by_one_year(patch_struct *patch, int p);
void age_population_by_one_year(age_list_struct *);
void update_pop_available_partners_ageing_by_one_year(patch_struct *, int, 
    all_partnerships *, double );
void age_population_size_one_year_age_by_one_year(population_size_one_year_age *);
void update_n_infected_by_all_strata_ageing_by_one_year(population_size_one_year_age_hiv_by_stage_treatment *);
void remove_dead_person_from_susceptible_in_serodiscordant_partnership(individual *, 
    individual **, long *);
void remove_dead_person_from_susceptible_in_hsv2serodiscordant_partnership(individual *dead_person, individual **susceptible_in_hsv2serodiscordant_partnership, long *n_susceptible_in_hsv2serodiscordant_partnership);
void remove_dead_person_from_list_available_partners(double, individual *,population_partners *,
    population_size_all_patches *);
void remove_dead_persons_partners(individual *, population_partners *, 
    population_size_all_patches *, double );
void remove_from_hiv_pos_progression(individual *, individual ***, long *, long *, 
    double, parameters *, population_size_one_year_age_hiv_by_stage_treatment *, int);
void remove_from_cascade_events(individual *, individual ***, long *, long *, double, parameters *);
void remove_from_vmmc_events(individual *, individual ***, long *, long *, double , parameters *);
void remove_from_PrEP_events(individual *, individual ***, long *, long *, double , parameters *);
void remove_from_hsv2_pos_progression(individual *indiv, individual ***hsv2_pos_progression, long *n_hsv2_pos_progression, long *size_hsv2_pos_progression, double t, parameters *param);
void deaths_natural_causes(double, patch_struct *, int , all_partnerships *,  file_struct *);
//void make_new_adults(double, patch_struct *, int , all_partnerships *, individual ***, long *, long *, individual ***, long *, long *, population_size_one_year_age_hiv_by_stage_treatment *);
void make_new_adults(double, int, patch_struct *, int , all_partnerships *, int );
void add_new_kids(double , patch_struct *, int );
void make_pop_from_age_list(population *, age_list_struct *, individual *);
void individual_death_AIDS(age_list_struct *, individual *, population_size *, 
    population_size_one_year_age *, population_size_one_year_age *, population_size_one_year_age *n_infected,
    stratified_population_size *, double , parameters *, individual **, 
    long *, individual **, long *,
    population_partners *, population_size_all_patches *, individual ***, 
    long *, long *, patch_struct *, int , file_struct *);

#endif /* DEMOGRAPHICS_H_ */
