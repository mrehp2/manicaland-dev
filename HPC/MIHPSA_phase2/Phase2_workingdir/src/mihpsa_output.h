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


#ifndef MIHPSA_OUTPUT_H_
#define MIHPSA_OUTPUT_H_


#include "constants.h"
#include "structures.h"
#include "utilities.h"

int get_MIHPSA_condom_use_last_act(individual *);
void store_annual_outputs_MIHPSA(patch_struct *, int , output_struct *, double );
void write_MIHPSA_outputs(file_struct *, output_struct *, int );


#endif /* MIHPSA_OUTPUT_H_ */
