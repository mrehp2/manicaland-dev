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


#ifndef HSV_H_
#define HSV_H_


#include "constants.h"
#include "structures.h"
#include "utilities.h"
#include "output.h"
#include "debug.h"


double hsv2_transmission_probability(individual* , individual* , parameters * );

void hsv2_acquisition(individual* , double , patch_struct *, int , all_partnerships *, output_struct *, debug_struct *, file_struct *, int , int );

void inform_partners_of_hsv2seroconversion_and_update_list_hsv2serodiscordant_partnerships(individual* , individual** , long *);

void new_hsv2_infection(double , int , individual* , population_size_one_year_age *, population_size_one_year_age *, age_list_struct *, parameters *, individual ***, long *, long *, file_struct *);

void draw_initial_hsv2_infection(double , individual* , patch_struct *, int , all_partnerships *, output_struct *, file_struct *);

void next_hsv2_event(individual* , individual ***, long *, long *, parameters *, double );

void carry_out_HSV2_events_per_timestep(double , patch_struct *, int , all_partnerships *, debug_struct *, file_struct *);

#endif /* HSV_H_ */
