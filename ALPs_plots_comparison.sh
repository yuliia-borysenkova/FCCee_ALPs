#!/bin/bash

main_dir=`pwd`
num_events=100000
num_events_short="100k"

list_mass="5."
list_cYY="0.5"

plots_dir="$main_dir/results/general_plots"
mkdir $plots_dir
cd $plots_dir

cp $main_dir/Scripts/analysis_plots_comparison.py $plots_dir/analysis_plots_comparison.py

mkdir root_files

list_processes=()
for ALP_mass in $list_mass; do
    for ALP_cYY in $list_cYY; do
        process_name="ALP_Z_aa_${ALP_mass}GeV_cYY_${ALP_cYY}"
        list_processes+=("$process_name")
        run_dir="$main_dir/results/ALPs_ne_${num_events_short}_mass_${ALP_mass}GeV_cYY_${ALP_cYY}"
        cp $run_dir/output_finalSel/${process_name}_selNone_histo.root $plots_dir/root_files/${process_name}_selNone_histo.root
    done
done

for value in "${list_processes[@]}"; do
     echo $value
done

cd $plots_dir
sed -i "s@my_input_dir@${plots_dir}/root_files/@" analysis_plots_comparison.py
sed -i "s@my_output_dir@${plots_dir}/plots@" analysis_plots_comparison.py


str_processes=""
str_signals=""
for value in "${list_processes[@]}";do
    str_processes+="'$value', "
    str_signals+="'$value': ['$value'], "
done
str_processes=${str_processes::-2}
#str_signals=${str_signals::-2}

#processes
sed -i "s@list_processes@$str_processes@" analysis_plots_comparison.py
#signals
sed -i "s@list_signals@$str_signals@" analysis_plots_comparison.py


fccanalysis plots analysis_plots_comparison.py