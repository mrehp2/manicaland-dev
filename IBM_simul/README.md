IBM for the PopART trial
========================
Repository for the C and Python code (and public data) used to run the individual-based model for the PopART trial.  There is also a [data dictionary](./doc/data_dict_output.md) for output from the model.  


Compilation
----------------
In order to run the model, the C code needs to first be compiled, linked, and an executable (`popart-simul.exe`) created.  

```
cd src
make clean
make all
cd ..
```


Running the model
-------------------------

There are a couple of steps needed to have the IBM running on your local machine as the IBM (and Python scripts that process the data) assumes that CHiPs and population cohort (PC) data are in a specific location.  

1. **Data prerequisites**

    a. *Trial schedule*
    * The file `community_dictionary_withtrialarm.csv` needs to be copied to the folder [data/RAW_PRIORS](data/RAW_PRIORS).  

    b. *Fertility and mortality data*
    * Within `~/Dropbox/PoPART/IBM Model Background/Demographic data/` there needs to be the following files: `ZambiaFertility.csv`, `SouthAfricaFertility.csv`,`SouthAfricaMortalityMen.csv`, `SouthAfricaMortalityWomen.csv`, `ZambiaMortalityMen.csv`, `ZambiaMortalityWomen.csv` (**Note**: these are all publicly available data so could be housed on github).  
    
    c. *CHiPs data*
    * Within the folder `~/Dropbox/PoPART/Data:Stats/CHiPs data/` there should be a range of folders called `Round1`, `Round2` etc, within which there should be two folders (`TimeToARTInitiation` and  `TimeOfChipsVisits`)/  Within each folder called `TimeToARTInitiation` there needs to be a file called `TwoExpFitsByQuarter_Zambia.txt`.  Within each folder called `TimeOfChipsVisits` there needs to be files called  `Chips_schedule_by_age_and_gender_round1_community1.txt`, 
            `Chips_schedule_by_age_and_gender_round1_community2.txt` and so on.  
    * Within the folders for rounds 3 and 4 there is simply a folder called `TimeOfChipsVisits`with three further folders within it called `Central_Chips`, `Optim_Chips`, `Pessim_Chips`, which then have files called (for instance) `Chips_schedule_by_age_and_gender_round3_community1.txt` for each community of interest.  

    d. *Population cohort data*
    * Within the folder `~/Dropbox/PoPART/Data:Stats/PC Data Downloads/15-12-2016_PC0_NEWFINAL/` there needs to be two files called `param_partnerships_fromPC0_SA.txt` and `param_partnerships_fromPC0_Za.txt` in the subfolder called `R/partnerships`.  Then within the subfolder `R/PC0schedules` there needs to be a range of csv files called `PC0_schedule_by_age_and_gender_community1.csv` and `PC0_schedule_by_HIV_status_age_and_gender_community1.csv`.  

    * The following files are also checked for within the PC folder: `R/DataCleaning/Read_PC0_final_data.R`, `R/DataCleaning/PC0.yml`, `R/DataCleaning/PC0_partner.yml`, `"R/DataCleaning/RenameColMergedPC0.yml`, `R/DataCleaning/recipes.yml`, `RawData/PC0.csv`, `RawData/PC0_partner.csv`, `MergedAndCleanData/Recoded_PC0_merged_dat.rds`, `MergedAndCleanData/Recoded_PC0_merged_dat.rds`, `R/partnerships/ExtractPartnershipParamFromPC0.Rnw`.  


A template for all these files (`Dropbox_template.zip`) can be provided by the repo maintainers.  


2. **Running the simulation**

Provided that the private data are on your local machine (PC0 and CHiPs data), after compilation (see above), the model can be run using [run.sh](run.sh) by simply running:

```
./run.sh
```


Output from the simulation
-----------------------------------

Output will be stored in `data/SAMPLED_PARAMETERS/PARAMS_COMMUNITY5/Output`.  Several files will be output depending upon which macros are switched 'on' (set to 1) within the file [constants.h](src/constants.h).  

