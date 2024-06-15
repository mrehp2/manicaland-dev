outputdirectory="/home/mike/MANICALAND/manicaland-dev/HPC/MIHPSA_phase2/Phase2_workingdir/params/"
mkdir -p $outputdirectory/Output
nruns=2

./popart-simul.exe $outputdirectory $nruns
