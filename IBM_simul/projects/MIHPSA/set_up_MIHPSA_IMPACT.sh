# Script that goes in the IMPACT directory, and sets up the basics.

templatedir="../IMPACT_R7_try1/"

cp -r $templatedir/src .
ln -s src/popart-simul.exe .
cp $templatedir/fix_param_times.py .
cp $templatedir/run_baseline.sh .

python fix_param_times.py .
