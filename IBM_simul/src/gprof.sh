outputdirectory="/home/mike/MANICALAND/manicaland-dev/IBM_simul/data/SAMPLED_PARAMETERS/PARAMS_COMMUNITY5/"
nruns=3

./popart-simul.exe $outputdirectory $nruns

gprof popart-simul.exe gmon.out > gprof.txt
