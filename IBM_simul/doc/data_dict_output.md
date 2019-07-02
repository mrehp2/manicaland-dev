Data dictionary for files output by the IBM
===============================

The following files may be output by the IBM:

* [Age_distribution_check](#age_distribution_check)
* [Annual_outputs](#annual_outputs)
* [ART_distribution](#art_distribution)
* [ART_transition_dist](#art_transition_dist)
* [Calibration_output](#calibration_output)
* [CHIPS_outputs_annual](#chips_outputs_annual)
* [CHIPS_outputs_visit](#CHIPS_outputs_visit)
* [DEBUG_ART_population](#debug_art_population)
* [DEBUG_HIV_CD4_after_seroconversion](#debug_hiv_cd4_after_seroconversion)
* [DEBUG_HIV_initialSPVLdistribution](#debug_hiv_initialspvldistribution)
* [DEBUG_HIVduration](#debug_hivduration)
* [DEBUG_HIVduration_KM](#debug_hivduration_km)
* [DEBUG_HIVstates_population](#debug_hivstates_population)
* [Distr_n_lifetime_partners](#distr_n_lifetime_partners)
* [Distr_n_partners_lastyear](#distr_n_partners_lastyear)
* [Hazards](#hazards)
* [HIVsurvival_individualdata](#hivsurvival_individualdata)
* [NBirthsNNewAdultsNdeaths_Run](#nbirthsnnewadultsndeaths_run)
* [OneYearAgeGp](#oneyearagegp)
* [PC_outputs](#pc_outputs)
* [phylogenetic_individualdata](#phylogenetic_individualdata)
* [phylogenetic_transmission](#phylogenetic_transmission)
* [Timestep_outputs](#timestep_outputs)
* [Timestep_outputs_PConly](#timestep_outputs_pconly)


Questions to be answered when adding data to this data dictionary:

0. What is the purpose of this file?  Why is it output?  
1. What is the output in the file?  Is this file output for a complete simulation or a bunch of simulations?  
2. What are the rows of the output file?  
3. How is this output file 'turned on' in the IBM?  For instance, which macro in `constants.h` needs to be set so that this file is output?  
4. What are the columns of this file?  What do they mean?  
5. How many columns does this file have?  
6. Are the files output for each patch or just a single patch?  


# Age_distribution_check

This file outputs data for a single simulation run with each row specifying the output for a complete calendar year for a single simulation.  62 columns.  

#### Time: int
Calendar year

#### M:13-14 - M80+: int

#### F:13-14 - F:80+: int

#### DeadM:13-14 - DeadM80+ : int

#### DeadF:13-14 - DeadF:80+: int

#### CumulativeDead : int

# Annual_partnerships

313 columns

#### Year
MeanNcurrentpart_riskLow
MeanNcurrentpart_riskMed
MeanNcurrentpart_riskHigh
MeanNcurrentpart_risk_outsideLow
MeanNcurrentpart_risk_outsideMed
MeanNcurrentpart_risk_outsideHigh
MeanNcurrentsdpart_riskLow
MeanNcurrentsdpart_riskMed
MeanNcurrentsdpart_riskHigh
MeanNcurrentsdpart_risk_outsideLow
MeanNcurrentsdpart_risk_outsideMed
MeanNcurrentsdpart_risk_outsideHigh
MeanNewPartnersthisyear_riskLow
MeanNewPartnersthisyear_riskMed
MeanNewPartnersthisyear_riskHigh
MeanNewPartnersthisyear_risk_outsideLow
MeanNewPartnersthisyear_risk_outsideMed
MeanNewPartnersthisyear_risk_outsideHigh
MeanNlifetimepart_riskLow
MeanNlifetimepart_riskMed
MeanNlifetimepart_riskHigh
MeanNlifetimepart_risk_outsideLow
MeanNlifetimepart_risk_outsideMed
MeanNlifetimepart_risk_outsideHigh
MeanNcurrentpart_gend_risk_age_M_risk0_age0
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age0
MeanNcurrentpart_gend_risk_age_F_risk0_age0
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age0
MeanNcurrentpart_gend_risk_age_M_risk0_age1
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age1
MeanNcurrentpart_gend_risk_age_F_risk0_age1
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age1
MeanNcurrentpart_gend_risk_age_M_risk0_age2
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age2
MeanNcurrentpart_gend_risk_age_F_risk0_age2
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age2
MeanNcurrentpart_gend_risk_age_M_risk0_age3
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age3
MeanNcurrentpart_gend_risk_age_F_risk0_age3
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age3
MeanNcurrentpart_gend_risk_age_M_risk0_age4
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age4
MeanNcurrentpart_gend_risk_age_F_risk0_age4
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age4
MeanNcurrentpart_gend_risk_age_M_risk0_age5
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age5
MeanNcurrentpart_gend_risk_age_F_risk0_age5
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age5
MeanNcurrentpart_gend_risk_age_M_risk0_age6
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age6
MeanNcurrentpart_gend_risk_age_F_risk0_age6
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age6
MeanNcurrentpart_gend_risk_age_M_risk0_age7
MeanNcurrentpart_gend_risk_age_M_outside_risk0_age7
MeanNcurrentpart_gend_risk_age_F_risk0_age7
MeanNcurrentpart_gend_risk_age_F_outside_risk0_age7
MeanNcurrentpart_gend_risk_age_M_risk1_age0
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age0
MeanNcurrentpart_gend_risk_age_F_risk1_age0
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age0
MeanNcurrentpart_gend_risk_age_M_risk1_age1
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age1
MeanNcurrentpart_gend_risk_age_F_risk1_age1
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age1
MeanNcurrentpart_gend_risk_age_M_risk1_age2
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age2
MeanNcurrentpart_gend_risk_age_F_risk1_age2
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age2
MeanNcurrentpart_gend_risk_age_M_risk1_age3
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age3
MeanNcurrentpart_gend_risk_age_F_risk1_age3
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age3
MeanNcurrentpart_gend_risk_age_M_risk1_age4
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age4
MeanNcurrentpart_gend_risk_age_F_risk1_age4
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age4
MeanNcurrentpart_gend_risk_age_M_risk1_age5
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age5
MeanNcurrentpart_gend_risk_age_F_risk1_age5
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age5
MeanNcurrentpart_gend_risk_age_M_risk1_age6
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age6
MeanNcurrentpart_gend_risk_age_F_risk1_age6
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age6
MeanNcurrentpart_gend_risk_age_M_risk1_age7
MeanNcurrentpart_gend_risk_age_M_outside_risk1_age7
MeanNcurrentpart_gend_risk_age_F_risk1_age7
MeanNcurrentpart_gend_risk_age_F_outside_risk1_age7
MeanNcurrentpart_gend_risk_age_M_risk2_age0
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age0
MeanNcurrentpart_gend_risk_age_F_risk2_age0
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age0
MeanNcurrentpart_gend_risk_age_M_risk2_age1
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age1
MeanNcurrentpart_gend_risk_age_F_risk2_age1
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age1
MeanNcurrentpart_gend_risk_age_M_risk2_age2
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age2
MeanNcurrentpart_gend_risk_age_F_risk2_age2
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age2
MeanNcurrentpart_gend_risk_age_M_risk2_age3
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age3
MeanNcurrentpart_gend_risk_age_F_risk2_age3
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age3
MeanNcurrentpart_gend_risk_age_M_risk2_age4
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age4
MeanNcurrentpart_gend_risk_age_F_risk2_age4
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age4
MeanNcurrentpart_gend_risk_age_M_risk2_age5
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age5
MeanNcurrentpart_gend_risk_age_F_risk2_age5
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age5
MeanNcurrentpart_gend_risk_age_M_risk2_age6
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age6
MeanNcurrentpart_gend_risk_age_F_risk2_age6
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age6
MeanNcurrentpart_gend_risk_age_M_risk2_age7
MeanNcurrentpart_gend_risk_age_M_outside_risk2_age7
MeanNcurrentpart_gend_risk_age_F_risk2_age7
MeanNcurrentpart_gend_risk_age_F_outside_risk2_age7
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age0
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age0
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age0
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age0
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age1
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age1
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age1
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age1
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age2
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age2
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age2
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age2
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age3
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age3
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age3
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age3
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age4
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age4
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age4
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age4
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age5
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age5
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age5
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age5
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age6
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age6
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age6
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age6
MeanNewPartnersthisyear_gend_risk_age_M_risk0_age7
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk0_age7
MeanNewPartnersthisyear_gend_risk_age_F_risk0_age7
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk0_age7
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age0
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age0
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age0
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age0
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age1
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age1
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age1
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age1
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age2
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age2
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age2
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age2
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age3
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age3
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age3
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age3
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age4
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age4
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age4
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age4
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age5
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age5
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age5
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age5
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age6
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age6
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age6
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age6
MeanNewPartnersthisyear_gend_risk_age_M_risk1_age7
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk1_age7
MeanNewPartnersthisyear_gend_risk_age_F_risk1_age7
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk1_age7
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age0
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age0
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age0
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age0
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age1
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age1
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age1
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age1
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age2
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age2
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age2
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age2
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age3
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age3
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age3
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age3
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age4
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age4
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age4
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age4
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age5
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age5
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age5
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age5
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age6
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age6
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age6
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age6
MeanNewPartnersthisyear_gend_risk_age_M_risk2_age7
MeanNewPartnersthisyear_gend_risk_age_M_outside_risk2_age7
MeanNewPartnersthisyear_gend_risk_age_F_risk2_age7
MeanNewPartnersthisyear_gend_risk_age_F_outside_risk2_age7
MeanNlifetimepart_gend_risk_age_M_risk0_age0
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age0
MeanNlifetimepart_gend_risk_age_F_risk0_age0
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age0
MeanNlifetimepart_gend_risk_age_M_risk0_age1
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age1
MeanNlifetimepart_gend_risk_age_F_risk0_age1
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age1
MeanNlifetimepart_gend_risk_age_M_risk0_age2
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age2
MeanNlifetimepart_gend_risk_age_F_risk0_age2
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age2
MeanNlifetimepart_gend_risk_age_M_risk0_age3
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age3
MeanNlifetimepart_gend_risk_age_F_risk0_age3
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age3
MeanNlifetimepart_gend_risk_age_M_risk0_age4
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age4
MeanNlifetimepart_gend_risk_age_F_risk0_age4
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age4
MeanNlifetimepart_gend_risk_age_M_risk0_age5
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age5
MeanNlifetimepart_gend_risk_age_F_risk0_age5
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age5
MeanNlifetimepart_gend_risk_age_M_risk0_age6
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age6
MeanNlifetimepart_gend_risk_age_F_risk0_age6
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age6
MeanNlifetimepart_gend_risk_age_M_risk0_age7
MeanNlifetimepart_gend_risk_age_M_outside_risk0_age7
MeanNlifetimepart_gend_risk_age_F_risk0_age7
MeanNlifetimepart_gend_risk_age_F_outside_risk0_age7
MeanNlifetimepart_gend_risk_age_M_risk1_age0
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age0
MeanNlifetimepart_gend_risk_age_F_risk1_age0
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age0
MeanNlifetimepart_gend_risk_age_M_risk1_age1
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age1
MeanNlifetimepart_gend_risk_age_F_risk1_age1
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age1
MeanNlifetimepart_gend_risk_age_M_risk1_age2
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age2
MeanNlifetimepart_gend_risk_age_F_risk1_age2
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age2
MeanNlifetimepart_gend_risk_age_M_risk1_age3
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age3
MeanNlifetimepart_gend_risk_age_F_risk1_age3
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age3
MeanNlifetimepart_gend_risk_age_M_risk1_age4
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age4
MeanNlifetimepart_gend_risk_age_F_risk1_age4
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age4
MeanNlifetimepart_gend_risk_age_M_risk1_age5
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age5
MeanNlifetimepart_gend_risk_age_F_risk1_age5
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age5
MeanNlifetimepart_gend_risk_age_M_risk1_age6
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age6
MeanNlifetimepart_gend_risk_age_F_risk1_age6
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age6
MeanNlifetimepart_gend_risk_age_M_risk1_age7
MeanNlifetimepart_gend_risk_age_M_outside_risk1_age7
MeanNlifetimepart_gend_risk_age_F_risk1_age7
MeanNlifetimepart_gend_risk_age_F_outside_risk1_age7
MeanNlifetimepart_gend_risk_age_M_risk2_age0
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age0
MeanNlifetimepart_gend_risk_age_F_risk2_age0
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age0
MeanNlifetimepart_gend_risk_age_M_risk2_age1
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age1
MeanNlifetimepart_gend_risk_age_F_risk2_age1
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age1
MeanNlifetimepart_gend_risk_age_M_risk2_age2
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age2
MeanNlifetimepart_gend_risk_age_F_risk2_age2
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age2
MeanNlifetimepart_gend_risk_age_M_risk2_age3
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age3
MeanNlifetimepart_gend_risk_age_F_risk2_age3
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age3
MeanNlifetimepart_gend_risk_age_M_risk2_age4
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age4
MeanNlifetimepart_gend_risk_age_F_risk2_age4
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age4
MeanNlifetimepart_gend_risk_age_M_risk2_age5
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age5
MeanNlifetimepart_gend_risk_age_F_risk2_age5
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age5
MeanNlifetimepart_gend_risk_age_M_risk2_age6
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age6
MeanNlifetimepart_gend_risk_age_F_risk2_age6
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age6
MeanNlifetimepart_gend_risk_age_M_risk2_age7
MeanNlifetimepart_gend_risk_age_M_outside_risk2_age7
MeanNlifetimepart_gend_risk_age_F_risk2_age7
MeanNlifetimepart_gend_risk_age_F_outside_risk2_age7

# Annual_outputs

This file outputs data for a single simulation run with each row specifying the output for a complete calendar year for a single simulation.  Approximately 76 columns, depending on the different number of age and risk groups.  

#### Year : int
#### Prevalence : float
#### Incidence : float
#### NumberPositive : int
#### NewCasesThisYear : int
The number of incident cases occurring in the year in question, including seeding infections.  

#### NewCasesThisYearFromOutside : int
#### NewCasesThisYearFromAcute : int
#### PropHIVPosONART : float
#### NAnnual : int
The number of incident cases occurring in the year in question, excluding seeding infections (the same as NewCasesThisYear after the first years in which HIV seeding is occurring).  
#### TotalPopulation : int
#### NumberPositiveM : int
#### PopulationM : int
#### NumberPositiveF : int
#### PopulationF : int
#### CumulativeNonPopartHIVtests : int
#### CumulativePopartHIVtests : int
#### CumulativeNonPopartCD4tests : int
#### CumulativePopartCD4tests : int
#### NHIVTestedThisYear : int
#### NOnARTM : int
#### NNeedARTM : int
#### NOnARTF : int
#### NNeedARTF : int
#### PropMenCirc : float
#### NindInSdPart : int
#### NDied_from_HIV : int
#### NHIV_pos_dead : int
#### N_dead : int
#### Prop_riskLow : float
#### Prop_riskMed : float
#### Prop_riskHigh : float
#### Prevalence_riskLow : float
#### Prevalence_riskMed : float
#### Prevalence_riskHigh : float
#### NMage13-18  : int
#### NMage60-80 : int
#### NFage13-18 : int
#### NFage60-80 : int
#### IncMage13-18 : float
#### IncMage60-80 : float
#### IncFage13-18: float
#### IncFage60-80 : float
#### NPosMage13-18 : int
#### NPosMage60-80 : int
#### NPosFage13-18 : int
#### NPosFage60-80 : int

# ART_distribution

* What are these values?  Their column names sound like integers but they are floats upon output.  

9 columns

#### t
Calendar year.  

#### n_hivpos_dontknowstatus
#### n_hivpos_knowposneverart
#### n_hivpos_earlyart
#### n_hivpos_artvs
#### n_hivpos_artvu
#### n_hivpos_dropout
#### n_hivpos_cascadedropout
#### n_artdeath

# ART_transition_dist

14 columns

#### t
#### annual_change_n_start_emergency_art_fromartnaive
#### annual_change_n_start_emergency_art_fromcascadedropout
#### annual_change_n_learnhivpos_fromuntested
#### annual_change_n_startART_fromartnaive
#### annual_change_n_becomeVS_fromearlyart
#### annual_change_n_becomeVS_fromartvu
#### annual_change_n_becomeVU_fromearlyart
#### annual_change_n_becomeVU_fromartvs
#### annual_change_n_ARTdropout_fromearlyart
#### annual_change_n_ARTdropout_fromartvs
#### annual_change_n_ARTdropout_fromartvu
#### n_cascadedropout_fromARTneg
#### annual_change_n_aidsdeaths_fromearlyart


# Calibration_output

This file outputs data across multiple simulations.  Each row summarises information for a simulation run that is used to calibrate the model.  

* How are the number of DHS rounds in the output determined?  
* How are the number of age groups in the DHS columns determined?  
* How are the number of CHiPs rounds in the output determined?  
* How are the number of age groups in the CHiPs columns determined?  
* What is the window of timing for DHS Round 1 and CHiPs Round 1?  
* What are the final age groups in CHiPs?  Is this 80+ or is it just 80yos?  
* What are `CHIPSRound1NonARTM18` and `CHIPSRound1NvsM18`?  How is not on ART defined and how is VS defined?  

#### SampleNumber : int
An identifier for the parameter set being used (e.g. the same parameter set may be run several times using a different random seed for the random number generator in in the IBM).  

#### RepNumber : int
An identifier for the stochastic realisation being run (for the same parameter set).  

#### RunNumber : int
An identifier for the overall simulation number (across both parameter sets and stochastic realisations of those parameter sets).  

#### RandomSeed : int
The random seed used within the IBM (`RANDOMSEED` as input in the `init` parameter file).  

#### DHSRound1NtotM15 - DHSRound1NtotM59 : int
Total number of males in a particular age group (ages 15 to 59) at the timing of DHS round 1.  

#### DHSRound1NtotF15 - DHSRound1NtotF59 : int
Total number of females in a particular age group (ages 15 to 59) at the timing of DHS round 1.  

#### DHSRound1NposM15 - DHSRound1NposM59 : int
Total number of HIV+ males in a particular age group (ages 15 to 59) at the timing of DHS round 1.  

#### DHSRound1NposF15 - DHSRound1NposF59 : int
Total number of HIV+ females in a particular age group (ages 15 to 59) at the timing of DHS round 1.  

#### Same as above but for all DHS rounds (1-3 for Zambia; 1-4 for South Africa)

#### CHIPSRound1NtotM18 - CHIPSRound1NtotM80 : int
Total number of males in a particular age group (ages 18 to 80) at the timing of CHiPs round 1.  

#### CHIPSRound1NtotF18 - CHIPSRound1NtotF80 : int
Total number of females in a particular age group (ages 18 to 80) at the timing of CHiPs round 1.  

#### CHIPSRound1NposM18 - CHIPSRound1NposM80 : int
Total number of HIV+ males in a particular age group (ages 18 to 80) at the timing of CHiPs round 1.  

#### CHIPSRound1NposF18 - CHIPSRound1NposF8 : int
Total number of HIV+ females in a particular age group (ages 18 to 80) at the timing of CHiPs round 1.  

#### CHIPSRound1NawareM18 - CHIPSRound1NawareM80 : int
Total number of HIV+ males aware of status in a particular age group (ages 18 to 80) at the timing of CHiPs round 1.  

#### CHIPSRound1NawareF18 - CHIPSRound1NawareF80 : int
Total number of HIV+ females aware of status in a particular age group (ages 18 to 80) at the timing of CHiPs round 1.  

#### CHIPSRound1NonARTM18 - CHIPSRound1NonARTM80 : int

#### CHIPSRound1NonARTF18 - CHIPSRound1NonARTF80 : int
#### CHIPSRound1NvsM18 - CHIPSRound1NvsM80 : int
#### CHIPSRound1NvsF18 - CHIPSRound1NvsF80 : int
#### Same as above but for all CHiPs rounds


# distr_n_lifetime_partners

Output from the IBM when the macro `WRITE_PARTNERSHIPS_AT_PC0` is set to 1 (within `constants.h`).  This macro outputs two files: `Distr_n_lifetime_partners*.csv` and `Distr_n_lastyear_partners*.csv` which give distributions of partnerships at time `TIME_PC0` (as set in `constants.h`).  

* `Distr_n_lastyear_partners*.csv`: 


| Name  | Type  | Description | In code |
|---|---|---|---|
| `n_lifetime_partners` | int | Number of lifetime partners (this is just the tally |  |
| `Ma0r0` | int | Tally...  of partners last year of males in age group 1, risk group 1 |  |
...
| `Ma6r2 ` | int | Number of partners last year of males in age group 7, risk group 3 |  |
| `Fa0r0` | int | Number of partners last year of females in age group 1, risk group 1 |  |
...
| `Fa6r2 ` | int | Number of partners last year of females in age group 7, risk group 3 |  |


* `Distr_n_lastyear_partners*.csv`: 

# distr_n_partners_lastyear

Output from the IBM when the macro `WRITE_PARTNERSHIPS_AT_PC0` is set to 1 (within `constants.h`).  






# phylogenetic_individualdata


Output from the IBM when the macro `PRINT_PHYLOGENETICS_OUTPUT` is set to 1 (within `constants.h`) is two files for the inside patch: 1) individual level data and 2) transmission data.  


The following column names are given in the output of individual-level data.  The writing of these files is documented in the function `write_phylo_individual_data()` within [`output.c`](../src/output.c).  


There is one row for each individual ever created in the community.  In order to get analogous data for the outside patch (patch 1) it is required to change the macro `PHYLO_PATCH` within [`constants.h`](../src/constants.h) to 1.  

| Name  | Type  | Description | In code |
|---|---|---|---|
| `Id` | int | unique ID for each person, one number for each row (starting from 0) | recoded from `individual.id` |
| `Sex`  | str M,F | sex of the individual | recoded from `individual.gender` |
| `DoB`  | double | date of birth in decimal years | `individual.DoB` |
| `DoD`  | double | date of death in decimal years (-1 if the individual hasn't died at the end of the simulation). | `individual.DoD` |
| `HIV_pos`  | int 0,1  | HIV status of the individual. | `individual.HIV_status > 0` |
| `RiskGp`  | str L,M,H | Risk group of the individual  | `individual.sex_risk` |
| `t_diagnosed`  | str or double  | Time diagnosed in decimal years (or "ND" for not diagnosed). When the file is being printed this is set to "ND" if the attribute is still -1. | `individual.PANGEA_t_diag` (defaults to -1 when indiv. is created; see [`structures.h`](../src/structures.h)) |
| `cd4_diagnosis`  | double | CD4 count at time of diagnosis; -1 if HIV neg. | `individual.PANGEA_cd4atdiagnosis` |
| `cd4atfirstART`  | double | CD4 at the time of first ART; -1 if HIV neg | `individual.PANGEA_cd4atfirstART` |
| `t_1stARTstart`  | double | time at which individual started ART in decimal years.  -1 if HIV neg | `individual.PANGEA_date_firstARTstart` |
| `t_1stVLsupp_start`  | double | First date of viral suppression | `individual.PANGEA_date_startfirstVLsuppression`, set within `carry_out_cascade_events_per_timestep()` in [`hiv.c`](../src/hiv.c)|
| `t_1stVLsupp_stop` | double | End date of viral suppression |`individual.PANGEA_date_endfirstVLsuppression` |


# phylogenetic_transmission

Output from the IBM when the macro `PRINT_PHYLOGENETICS_OUTPUT` is set to 1 (within `constants.h`) is two files for the inside patch: 1) individual level data and 2) transmission data.  


The following column names are given in the output of transmission data files.  The writing of these files is documented in the function `store_phylogenetic_transmission_output()` within [`output.c`](../src/output.c).  

There is one row for each HIV positive individual in the inside patch.  In order to get analogous data for the outside patch (patch 1) it is required to change the macro `PHYLO_PATCH` within [`constants.h`](../src/constants.h) to 1.  


| Name  | Type  | Description | In code |
|---|---|---|---|
| `IdInfector` | int | ID for the infector (-1 if this person was a seed case).  |  |
| `IdInfected` | int | ID for each infected person (unique identifier, one row for each `IdInfected`) |  |
|`TimeOfInfection` | double | Date of infection in decimal years. |  |
|`IsInfectorAcute` | int, -1, 0, 1 | Whether the infector was in the actute stage of HIV (`2 - individual.HIV_status`)).  -1 for seed cases.  |  |
| `PartnerARTStatus` | int | This is the ART status of the infector.  From [structures.h](../src/structures.h) (**NEEDS UPDATING**): -1 if never tested positive, 0 if positive but not yet on ART (or dropped out), 1 if on ART for <6 months, 2 if on ART for >=6 months and virally suppressed, 3 if on ART for >=6 months and not virally suppressed.  See [`constants.h`](../src/constants.h): -1 = if never tested HIV positive (note that this is tested, not serostatus); 0 = Never been on ART; 1 = first few weeks/months before achieve viral suppression. Higher mortality and drop-out rate; 2 = longer-term ART and Virally Suppressed (so low transmission, no CD4 progression or drug resistance); 3 = longer-term ART and Virally Unsuppressed (so higher transmission, could have (but not currently) CD4 progression and drug resistance); 4 = has been on ART before but not currently; 5 = dropped out of HIV care cascade prior to ever starting ART; 6 = Signals that the person needs to be removed as they die while on ART. | `individual.ART_status` |
| `IsInfectorOutsidePatch` | int, -1, 0, 1 | Is the infector in the outside patch as the infected person (transmission data is only followed for those in the inside patch).  -1 for seed cases.  |  |
| `InfectorCD4` | int, -1, 0, 1, 2, 3 | CD4 category of the infector.  -1 for seed cases.  See [`structures.h`](../src/structures.h) for the categories: -2: dead ; -1: uninfected ; 0: CD4>500, 1: CD4 350-500, 2: CD4 200-350, 3: CD4<200.  | `infector.cd4` |
| `InfectorSPVL` | double | SPVL of the infector.  Missing for seed cases.  |  |
| `InfecteeSPVL` | double | SPVL of the infected.  Missing for seed cases.  |  |
| `Infector_NPartners` | int | Number of partners of the infector.  Range from 1-10.  Missing for seed cases.  |  `individual.n_partners` | 
|`InfectorGender` | str M,F | Gender of the infector.  Missing for seed cases. | recoded from `individual.gender` | 






# Timestep_outputs

**Columns**

#### Time : float
Time step in decimal years

#### N_m : int
Number of males

#### N_f : int
Number of females

#### NPos_m : int
Number of positive men

#### NPos_f : int
Number of positive females

#### N_knowpos_m : int
Number of positive males who know their status

#### N_knowpos_f : int
Number of positive females who know their status

#### NART_m : int
Number of males on ART

#### NART_f : int
Number of females on ART

#### NVS_m : int
Number of males on ART who are virally suppressed

#### NVS_f : int
Number of females on ART who are virally suppressed

#### NNotKnowStatus_m : int
Number of positive males who do not know their status

#### NNotKnowStatus_f : int
Number of HIV positive females who do not know their status

#### PropMenCirc : float
Proportion of men who are circumcised (VMMC, VMMC_HEALING, or TMC) within the whole pop.
See output.c::store_impact_prev_art_timestep().  

#### Cumulative_Infected_m : int
Cumulative number of infected males

#### Cumulative_Infected_f : int
Cumulative number of infected females


# Timestep_outputs_PConly


These files write the same information as the `Timestep_outputs_` files ... 
(`filename_timestep_output_PConly` within the code)


**Columns**

#### Time : float
Time step in decimal years

#### N_m : int
Number of males (of PC-eligible age; age > 18 & age < 45)

#### N_f : int
Number of females (of PC-eligible age; age > 18 & age < 45)

#### NPos_m : int
Number of positive men

#### NPos_f : int
Number of positive females

#### N_knowpos_m : int
Number of positive males who know their status

#### N_knowpos_f : int
Number of positive females who know their status

#### NART_m : int
Number of males on ART

#### NART_f : int
Number of females on ART

#### NVS_m : int
Number of males on ART who are virally suppressed

#### NVS_f : int
Number of females on ART who are virally suppressed

#### NNotKnowStatus_m : int
Number of positive males who do not know their status

#### NNotKnowStatus_f : int
Number of HIV positive females who do not know their status

#### PropMenCirc : float
Proportion of men who are circumcised (VMMC, VMMC_HEALING, or TMC) within the PC-eligible pop.
See output.c::store_impact_prev_art_timestep().  This is different to the PropMenCirc in the 
timesteps output (above) because there is a different denominator and numerator.  

#### Cumulative_Infected_m : int
Cumulative number of infected males

#### Cumulative_Infected_f : int
Cumulative number of infected females
