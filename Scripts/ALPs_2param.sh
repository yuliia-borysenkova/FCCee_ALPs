#!/bin/bash

####################___MAIN____VARIABLES____######################

main_dir=`pwd`
num_events=100000
ALP_mass=5.
ALP_cYY=0.7
mad_graph_dir="ALP_Z_aa_${ALP_mass}GeV_cYY_${ALP_cYY}"
process_name="ALP_Z_aa_${ALP_mass}GeV_cYY_${ALP_cYY}"
run_dir="ALPs_NE_100k_mass_${ALP_mass}GeV_cYY_${ALP_cYY}"

mkdir $run_dir
cd $run_dir

####################___MC_SIMULATION_STAGE____######################

mad_graph_script_name="mg5_proc_card_ALP_aa_${ALP_mass}GeV_${ALP_cYY}CYY.dat"
cp $main_dir/Scripts/mg5_proc_card_ALP_aa_mGeV_cCYY.dat $mad_graph_script_name

sed -i "s@ALP_mass@$ALP_mass@" $mad_graph_script_name
sed -i "s@num_events@$num_events@" $mad_graph_script_name
sed -i "s@ALP_cYY@$ALP_cYY@" $mad_graph_script_name
sed -i "s@mad_graph_dir@$mad_graph_dir@" $mad_graph_script_name

cp $main_dir/Scripts/ALP_pythia.cmnd ALP_pythia.cmnd
sed -i "s@num_events@$num_events@" ALP_pythia.cmnd
sed -i "s@process_name.lhe@${process_name}.lhe@" ALP_pythia.cmnd


python $main_dir/MG5_aMC_v3_4_2/bin/mg5_aMC $mad_graph_script_name

cd $mad_graph_dir/Events/run_01/

gunzip unweighted_events.lhe.gz

cp unweighted_events.lhe $main_dir/$run_dir/${process_name}.lhe

cd $main_dir/$run_dir

mkdir output_MadgraphPythiaDelphes

DelphesPythia8_EDM4HEP $main_dir/FCC-config/FCCee/Delphes/card_IDEA.tcl $main_dir/FCC-config/FCCee/Delphes/edm4hep_IDEA.tcl ALP_pythia.cmnd output_MadgraphPythiaDelphes/$process_name.root

####################___ANALYSIS_STAGE____######################

cp $main_dir/Scripts/analysis_stage1.py analysis_stage1.py
cp $main_dir/Scripts/analysis_final.py analysis_final.py
cp $main_dir/Scripts/analysis_plots.py analysis_plots.py

dir_name="$main_dir/$run_dir/"

sed -i "s@mydir@$dir_name@" analysis_stage1.py
sed -i "s@process_name@$process_name@" analysis_stage1.py

sed -i "s@mydir@$dir_name@" analysis_final.py
sed -i "s@process_name@$process_name@" analysis_final.py
sed -i "s@ALPs_mass@$ALP_mass@" analysis_final.py
sed -i "s@ALPs_cYY@$ALP_cYY@" analysis_final.py
sed -i "s@num_events@$num_events@" analysis_final.py

sed -i "s@mydir@$dir_name@" analysis_plots.py
sed -i "s@process_name@$process_name@" analysis_plots.py
sed -i "s@ALPs_mass@$ALP_mass@" analysis_plots.py
sed -i "s@ALPs_cYY@$ALP_cYY@" analysis_plots.py

echo "stage1"
fccanalysis run analysis_stage1.py
echo "stage final"
fccanalysis final analysis_final.py
#echo "plotting"
#fccanalysis plots analysis_plots.py



######################________COMMENTS_______###########################
#source $main_dir/venv/bin/activate
#deactivate

#source $main_dir/FCCAnalyses/setup.sh
#source ../FCCAnalyses/setup.sh