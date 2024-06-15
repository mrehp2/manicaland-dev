outputdirectory="/home/mike/MANICALAND/manicaland-dev/HPC/MIHPSA_phase2/Phase2_workingdir/params/"
mkdir -p $outputdirectory/Output
nruns=2

#valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file=valgrind-out.txt ./popart-simul.exe $outputdirectory $nruns
G_SLICE=always-malloc G_DEBUG=gc-friendly  valgrind -v --tool=memcheck --leak-check=full --num-callers=40 --log-file=valgrind-out.txt ./popart-simul.exe $outputdirectory $nruns
