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


#ifndef UTILITIES_H_
#define UTILITIES_H_

#include "structures.h"
#include "constants.h"
#include "utilities.h"
#include <string.h>

void print_here(int );
void print_here_string(char *, int );
void check_if_cannot_read_param(int , char *);
void check_age_group_index(age_list_struct *, int, long, int);
void normalise_four_quantities(double *, double *, double *, double *);
void cumulative_four_quantities(double , double , double , double , double *, double *, 
    double *, double *);
double hill_up(double , double , double , double);
double hill_down(double , double , double , double);
void calcul_population(population_size *, stratified_population_size *);
void calcul_p_risk(int, double [N_RISK][N_RISK], stratified_population_size *, parameters *);
void calcul_n_new_partners_f_to_m(patch_struct *, parameters *, int, int);
void calcul_n_new_partners_m_to_f(patch_struct *, parameters *, int, int);
void balance_contacts_arithmetic(parameters *param);
int are_in_partnership(individual *, individual *);
int has_free_partnership(individual *);
int is_already_selected(long *, long , long );
int get_manicaland_round(double , parameters *, double *);
void calculate_current_c_within_patch(parameters *, double [2], double [2]);
void calculate_c_between_patches(parameters *);
void update_number_new_partners(double , patch_struct *);
void update_time_varying_hazard_onepatch(double , parameters *);
void update_time_varying_hazard_allpatches(double , patch_struct *);    

void copy_array_long(long *, long *, long );
int is_serodiscordant(partnership *);
int is_hsv2_serodiscordant(partnership *);
void calcul_pop_wider_age_groups(population_size *, population_size_one_year_age *);
void calcul_prevalence(proportion_population_size *, population_size *, population_size *, 
    population_size_one_year_age *);
void print_prevalence(population_size *, population_size *, population_size_one_year_age *);
int compare_longs (const void *, const void *);
void get_setting(patch_struct *);
int get_chips_round(parameters *, int , int );
int is_start_of_chips_round(parameters *, int , int , int);
int is_manicaland_cohort_time(int , int , parameters *);
void parse_command_line_arguments(int , char **, int *, int *, int *, int *, int *, int *);
void get_prevention_cascade_scenario(int , parameters *);
void get_IBM_code_version(char *, int );
void add_slash(char *);
void join_strings_with_check(char *, char *, int , char *);
void make_output_filename_labels(char *, parameters *, int , long , int , int, patch_struct *, 
    int , int, int);
void make_output_label_struct(file_label_struct *, long , int , int , int , patch_struct *, 
    int , int );
void make_filenames_for_struct(file_label_struct *, file_struct *,  char *);
void concatenate_filename(char *, char *, char *, char *);
void make_filenames_for_snapshot(char *, char *, file_label_struct *, int , int , char *);
void make_calibration_output_filename(char *, char *, long , patch_struct *, int , int , int, int);
void add_commas_to_calibration_output(char *,int );

void print_demographic_params(parameters *);
void print_hiv_params(parameters *);
void print_hsv2_params(parameters *);
void print_partnership_params(parameters *);
void print_time_params(parameters *);
void print_cascade_params(parameters *);
void print_chips_params(parameters *);
void print_init_params(parameters *);
void print_prep_params(parameters *);
void print_prevention_cascade_params(parameters *);

void print_param_struct(patch_struct *, int);
void check_if_parameters_plausible(parameters *);
void check_if_manicaland_prevention_cascade_parameters_plausible(parameters *);
void check_if_popart_parameters_plausible(parameters *);

void set_PrEP_stop_time(individual *, double );

#endif /* UTILITIES_H_ */
