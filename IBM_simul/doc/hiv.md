HIV parameters
===========


`p_child_circ`
`eff_circ_vmmc`
`eff_circ_tmc`
`rr_circ_unhealed`

* `t0_pmtct`: dates related to when services are offered concerning mother-to-child transmission.  Used within the function `hiv.c::mtct_transmission()` (although this function is not currently used in the IBM).  
* `t50_pmtct` : dates related to when services are offered concerning mother-to-child transmission.  Used within the function `hiv.c::mtct_transmission()` (although this function is not currently used in the IBM).  


* `p_misclassify_cd4` : probability of misclassifying a CD4 category into another CD4 category (all set to classify perfectly).  

* `factor_for_slower_progression_ART_VU`

* `time_200to350_to_200_spvl3` : These define the mean time in years to the next CD4 progression event (i.e. changing in CD4 category from *200-350* to *> 200*) conditional an individual's SPVL (i.e. SPVL category 3).  These parameters are stored within the array attribute `time_hiv_event[cd4][spvl]` as part of the parameters structure within the model.  They are used within the function `hiv.c::get_mean_time_hiv_progression`.  

