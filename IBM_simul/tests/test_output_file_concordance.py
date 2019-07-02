"""
Test internal validity of the annual outputs file using pytest. 

Several checks are performed to make sure incidence, prevalence, and other measures have internal
validity within the `Annual_outputs*.csv` files.  A single file is checked.  
"""
import subprocess, shutil, os
from os.path import join
import numpy as np, pandas as pd

# Directories
INPUTDIR = join("data", "SAMPLED_PARAMETERS", "PARAMS_COMMUNITY5")
NRUNS = 1
IBM_DIR = "src"
IBM_DIR_TMP = IBM_DIR + "_tmp"
EXE = "popart-simul.exe"

# Filenames
f_timestep = "Timestep_outputs_CL05_Za_A_V1.2_patch0_Rand10_Run1_PCseed0_0.csv"
f_annual = "Annual_outputs_CL05_Za_A_V1.2_patch0_Rand10_Run1_PCseed0_0.csv"
f_cost_effectiveness = "Cost_effectiveness_CL05_Za_A_V1.2_patch0_Rand10_Run1_PCseed0_0.csv"

# Range of years over which we want to ensure consistency across files (arbitrary)
years = range(1981, 2010)


def adjust_macros(input_file, macro_name, macro_value, output_file):
    """
    Adjust macros within the constants.h file of the IBM to produce different output.  
    """
    f = open(input_file, 'r')
    data = f.readlines()
    f.close()
    
    # Split on white space
    d = [[i, line] for i, line in enumerate(data) if line.startswith('#define ' + macro_name)]
    print("Found", macro_name, "at line", d[0][0])
    line = d[0][1]
    line = line.split()
    new_line = " ".join([line[0], line[1], macro_value, "\n"])
    
    # Add the line into the output data ... 
    for i, line in enumerate(data):
        if i == d[0][0]:
            data[i] = new_line
            print(data[i])
    
    # Write to file ... 
    f = open(output_file, 'w')
    f.writelines(data)
    f.close()


class TestClass(object):
    """
    Test class for checking 
    """
    @classmethod
    def setup_class(self):
        """
        Set up function: call the IBM so as to generate test output of 
        Annual_outputs, Timestep_output, and Cost_effectiveness_output files
        """
        # Remove "Output" directory and create a new dir
        shutil.rmtree(join(INPUTDIR, "Output"), ignore_errors = True)
        os.mkdir(join(INPUTDIR, "Output"))
        
        # Make a temporary copy of the code (remove this temporary directory if it already exists)
        shutil.rmtree(IBM_DIR_TMP, ignore_errors = True)
        shutil.copytree(IBM_DIR, IBM_DIR_TMP)
        
        # Turn on the macros for the output files above
        macros = [
            "WRITE_CALIBRATION", 
            "WRITE_COST_EFFECTIVENESS_OUTPUT", 
            "PRINT_EACH_RUN_OUTPUT", 
            "PRINT_ALL_RUNS", 
            "WRITE_EVERYTIMESTEP"]
        macro_file = join(IBM_DIR_TMP, "constants.h")
        [adjust_macros(macro_file, macro, "1", macro_file) for macro in macros]
        
        # Construct the compilation command and compile
        compile_command = "make clean; make all"
        completed_compilation = subprocess.run([compile_command], 
            shell = True, cwd = IBM_DIR_TMP, capture_output = True)
        
        # Construct the executable command
        command = join(IBM_DIR_TMP, EXE)
        
        # Call the model
        completed_run = subprocess.run([command, INPUTDIR, str(NRUNS)], capture_output = True)
        
        # Read the Annual_output* and Timestep_outputs* dataframes
        self.df_annual = pd.read_csv(join(INPUTDIR, "Output", f_annual))
        self.df_timestep = pd.read_csv(join(INPUTDIR, "Output", f_timestep))
        self.df_cost_effectiveness = pd.read_csv(join(INPUTDIR, "Output", f_cost_effectiveness))
        
    @classmethod
    def teardown_class(self):
        """
        Remove the temporary code directory
        """
        shutil.rmtree(IBM_DIR_TMP, ignore_errors = True)
    
    ####################################################################################
    ###################### Internal consistency of Annual_outputs ######################
    ####################################################################################
    
    def test_incidence(self):
        # Check that incidence is calculated correctly
        incidence = self.df_annual['NAnnual']/(self.df_annual['TotalPopulation'] - \
            self.df_annual['NumberPositive'])
        
        np.testing.assert_allclose(incidence.values, \
            self.df_annual['Incidence'].values, atol = 1e-5)
    
    def test_hiv_positive_population_by_sex(self):
        
        # Check that total positive population size is sum of male and female parts
        population = self.df_annual['NumberPositiveM'] + self.df_annual['NumberPositiveF']
        np.testing.assert_array_equal(population.values, \
            self.df_annual['NumberPositive'].values)
    
    def test_number_positive_by_new_cases(self):
        # Check that number positive is sum of incident cases
        numberpositive = (self.df_annual['NewCasesThisYear'].cumsum() - \
            self.df_annual['NHIV_pos_dead'])
        
        np.testing.assert_array_equal(numberpositive.values, 
            self.df_annual['NumberPositive'].values)
    
    def test_total_population_by_sex(self):
        # Check that total population size is sum of male and female populations
        population = self.df_annual['PopulationM'] + self.df_annual['PopulationF']
        np.testing.assert_array_equal(population.values, self.df_annual['TotalPopulation'].values)
    
    def test_prevalence(self):
        # Check that prevalance is calculated correctly
        prevalence = self.df_annual['NumberPositive']/self.df_annual['TotalPopulation']
        np.testing.assert_allclose(prevalence.values, self.df_annual['Prevalence'].values, 
            atol = 1e-5)
    
    def test_new_cases_by_age(self):
        # Check that new cases this year is sum across all age groups
        inc_cols = [c for c in self.df_annual.columns if ("Inc" in c) & ("age" in c)]
        newcases = self.df_annual[inc_cols].sum(axis = 1)
        np.testing.assert_array_equal(newcases.values, self.df_annual['NewCasesThisYear'].values)
    
    def test_number_positive_by_age(self):
        # Check that number positive is sum across all age groups
        npos_cols = [c for c in self.df_annual.columns if ("NPos" in c) & ("age" in c)]
        numberpos = self.df_annual[npos_cols].sum(axis = 1)
        np.testing.assert_array_equal(numberpos.values, self.df_annual['NumberPositive'].values)
    
    def test_number_positive_men_by_age(self):
        # Check number positive men is same across all age groups
        ntotm_cols = [c for c in self.df_annual.columns if ("NMage" in c)]
        ntotm = self.df_annual[ntotm_cols].sum(axis = 1)
        np.testing.assert_array_equal(ntotm.values, self.df_annual['PopulationM'].values)
    
    def test_number_positive_women_by_age(self):
        # Check number positive women is same across all age groups
        ntotf_cols = [c for c in self.df_annual.columns if ("NFage" in c)]
        ntotf = self.df_annual[ntotf_cols].sum(axis = 1)
        np.testing.assert_array_equal(ntotf.values, self.df_annual['PopulationF'].values)
    
    def test_proportion_on_art(self):
        # Check that proportion on ART is correct when looking across all genders
        pronart = (self.df_annual['NOnARTM'] + \
            self.df_annual['NOnARTF'])/self.df_annual['NumberPositive']
        pronart.replace(np.nan, 0, inplace = True)
        
        np.testing.assert_allclose(pronart.values, self.df_annual['PropHIVPosONART'].values, 
            atol = 1e-5)
    
    ####################################################################################
    ############### Consistency of Annual_ and Timestep_ outputs #######################
    ####################################################################################
    
    def test_number_women(self):
        # Check that the number of women is the same in the listed years in both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['N_f']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['PopulationF']
    
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_number_men(self):
        # Check that the number of men is the same in the listed years in both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['N_m']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['PopulationM']
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_number_positive_women(self):
        # Check that the number of HIV positive women is the same in the listed years in both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['NPos_f']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['NumberPositiveF']
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_number_positive_men(self):
        # Check that the number of HIV positive men is the same in the listed years in both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['NPos_m']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['NumberPositiveM']
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_number_art_women(self):
        # Check that the number of women on ART between both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['NART_f']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['NOnARTF']
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_number_art_men(self):
        # Check that the number of men on ART between both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['NART_m']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['NOnARTM']
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_prop_men_circ(self):
        # Check that the number of men on ART between both files
        timestep = self.df_timestep[self.df_timestep.Time.isin(years)]['PropMenCirc']
        annual = self.df_annual[self.df_annual.Year.isin(years)]['PropMenCirc']
        np.testing.assert_array_equal(timestep.values, annual.values)
    
    def test_incident_cases(self):
        # Check incident cases are calculated correctly between the two files
        
        # Isolate cumulative cases in timestep outputs
        timestepf = self.df_timestep[self.df_timestep.Time.isin(years)]['Cumulative_Infected_f']
        timestepm = self.df_timestep[self.df_timestep.Time.isin(years)]['Cumulative_Infected_m']
        
        # Find total new cases from cumulative cases by sex
        timestep = timestepf.diff() + timestepm.diff()
        annual = self.df_annual[self.df_annual.Year.isin(years)]['NewCasesThisYear']
        
        # Remove the first value (the diff command means the first value is an NaN).
        np.testing.assert_array_equal(timestep[1:].values, annual[1:].values)
    
    ####################################################################################
    ######### Consistency of Annual_ and Cost_effectiveness outputs ####################
    ####################################################################################
    def test_ce_Incidence(self):
        annual = self.df_annual['Incidence']
        ce = self.df_cost_effectiveness['Incidence']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_Prevalence(self):
        annual = self.df_annual['Prevalence']
        ce = self.df_cost_effectiveness['Prevalence']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_NumberPositive(self):
        annual = self.df_annual['NumberPositive']
        ce = self.df_cost_effectiveness['NumberPositive']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_NAnnual(self):
        annual = self.df_annual['NAnnual']
        ce = self.df_cost_effectiveness['NAnnual']
        np.testing.assert_array_equal(annual.values, ce.values)

    def test_ce_TotalPopulation(self):
        annual = self.df_annual['TotalPopulation']
        ce = self.df_cost_effectiveness['TotalPopulation']
        np.testing.assert_array_equal(annual.values, ce.values)
        
    def test_ce_NumberPositiveM(self):
        annual = self.df_annual['NumberPositiveM']
        ce = self.df_cost_effectiveness['NumberPositiveM']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_PopulationM(self):
        annual = self.df_annual['PopulationM']
        ce = self.df_cost_effectiveness['PopulationM']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_NumberPositiveF(self):
        annual = self.df_annual['NumberPositiveF']
        ce = self.df_cost_effectiveness['NumberPositiveF']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_PopulationF(self):
        annual = self.df_annual['PopulationF']
        ce = self.df_cost_effectiveness['PopulationF']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_AnnualNonPopartHIVtests(self):
        annual = np.diff(self.df_annual['CumulativeNonPopartHIVtests'])
        ce = self.df_cost_effectiveness['AnnualNonPopartHIVtests']
        np.testing.assert_array_equal(annual, ce.values[1:])
    
    def test_ce_AnnualPopartHIVtests(self):
        annual = np.diff(self.df_annual['CumulativePopartHIVtests'])
        ce = self.df_cost_effectiveness['AnnualPopartHIVtests']
        np.testing.assert_array_equal(annual, ce.values[1:])
    
    def test_ce_AnnualPopartHIVtests_split(self):
        ce_total = self.df_cost_effectiveness['AnnualPopartHIVtests']
        ce_positive = self.df_cost_effectiveness['AnnualPopartHIVtests_positive']
        ce_negative = self.df_cost_effectiveness['AnnualPopartHIVtests_negative']
        np.testing.assert_array_equal(ce_total.values, ce_positive.values + ce_negative.values)
    
    def test_ce_AnnualNonPopartCD4tests(self):
        annual = np.diff(self.df_annual['CumulativeNonPopartCD4tests'])
        ce = self.df_cost_effectiveness['AnnualNonPopartCD4tests']
        np.testing.assert_array_equal(annual, ce.values[1:])
    
    def test_ce_AnnualPopartCD4tests(self):
        annual = np.diff(self.df_annual['CumulativePopartCD4tests'])
        ce = self.df_cost_effectiveness['AnnualPopartCD4tests']
        np.testing.assert_array_equal(annual, ce.values[1:])
    
    def test_ce_NOnARTM(self):
        annual = self.df_annual['NOnARTM']
        ce = self.df_cost_effectiveness['NOnARTM']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_NOnARTF(self):
        annual = self.df_annual['NOnARTF']
        ce = self.df_cost_effectiveness['NOnARTF']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_NDied_from_HIV(self):
        annual = self.df_annual['NDied_from_HIV']
        ce = self.df_cost_effectiveness['NDied_from_HIV']
        np.testing.assert_array_equal(annual.values, ce.values)
    
    def test_ce_NumberPositiveM_CD4(self):
        cols = ['NumberPositiveM_CD4_1', 'NumberPositiveM_CD4_2', 
            'NumberPositiveM_CD4_3', 'NumberPositiveM_CD4_4']
        
        ce_cd4 = self.df_cost_effectiveness[cols].sum(axis = 1)
        ce = self.df_cost_effectiveness['NumberPositiveM']
        np.testing.assert_array_equal(ce_cd4.values, ce.values)
    
    def test_ce_NumberPositiveF_CD4(self):
        cols = ['NumberPositiveF_CD4_1', 'NumberPositiveF_CD4_2', 
            'NumberPositiveF_CD4_3', 'NumberPositiveF_CD4_4']
        
        ce_cd4 = self.df_cost_effectiveness[cols].sum(axis = 1)
        ce = self.df_cost_effectiveness['NumberPositiveF']
        np.testing.assert_array_equal(ce_cd4.values, ce.values)
    
    def test_ce_NumberPositiveOnARTM_CD4(self):
        cols = ['NumberPositiveOnARTM_CD4_1', 'NumberPositiveOnARTM_CD4_2',
            'NumberPositiveOnARTM_CD4_3', 'NumberPositiveOnARTM_CD4_4']
        
        ce_cd4 = self.df_cost_effectiveness[cols].sum(axis = 1)
        ce = self.df_cost_effectiveness['NOnARTM']
        np.testing.assert_array_equal(ce_cd4.values, ce.values)
    
    def test_ce_NumberPositiveOnARTF_CD4(self):
        cols = ['NumberPositiveOnARTF_CD4_1', 'NumberPositiveOnARTF_CD4_2',
            'NumberPositiveOnARTF_CD4_3', 'NumberPositiveOnARTF_CD4_4']
        
        ce_cd4 = self.df_cost_effectiveness[cols].sum(axis = 1)
        ce = self.df_cost_effectiveness['NOnARTF']
        np.testing.assert_array_equal(ce_cd4.values, ce.values)
    
    def test_ce_NumberPositiveNotOnARTM_CD4(self):
        cols = ['NumberPositiveNotOnARTM_CD4_1', 'NumberPositiveNotOnARTM_CD4_2',
            'NumberPositiveNotOnARTM_CD4_3', 'NumberPositiveNotOnARTM_CD4_4']
        
        ce_cd4 = self.df_cost_effectiveness[cols].sum(axis = 1)
        ce = self.df_cost_effectiveness['NumberPositiveM'] - self.df_cost_effectiveness['NOnARTM']
        np.testing.assert_array_equal(ce_cd4.values[-20:], ce.values[-20:])
    
    def test_ce_NumberPositiveNotOnARTF_CD4(self):
        cols = ['NumberPositiveNotOnARTF_CD4_1', 'NumberPositiveNotOnARTF_CD4_2',
            'NumberPositiveNotOnARTF_CD4_3', 'NumberPositiveNotOnARTF_CD4_4']
        
        ce_cd4 = self.df_cost_effectiveness[cols].sum(axis = 1)
        ce = self.df_cost_effectiveness['NumberPositiveF'] - self.df_cost_effectiveness['NOnARTF']
        np.testing.assert_array_equal(ce_cd4.values[-20:], ce.values[-20:])

