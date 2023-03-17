#!/bin/bash

main_dir=`pwd`
num_events=100000
num_events_short="100k"

list_mass="0.5 0.7 1. 3. 5. 7. 10. 15. 20. 25. 30."
list_cYY="0.1 0.3 0.5 0.7 0.9"

# list_mass="1."
# list_cYY="0.5"

mkdir results
bg_dir=$main_dir/results/background/

###################_________BACKGROUND______##########################
#LETS GENERATE BACKGROUND PROCESSES ee->2gamma AND ee->Z->ee

mkdir $bg_dir
cd $bg_dir
cp $main_dir/Scripts/analysis_stage1_batch.py analysis_stage1_batch.py
cp $main_dir/Scripts/analysis_stage1_bg.py analysis_stage1_bg.py
sed -i "s@mydir@$bg_dir@" analysis_stage1_batch.py
sed -i "s@mydir@$bg_dir@" analysis_stage1_bg.py

#BATCH
# echo "stage1_batch"
# fccanalysis run analysis_stage1_batch.py

#LOCAL
# START_TIME=$(date +%s)
# echo "stage1_bg"
# fccanalysis run analysis_stage1_bg.py
# END_TIME=$(date +%s)
# difference=$(( $END_TIME - $START_TIME ))
# echo "Runtime stage1_bg: $difference seconds"

cp $main_dir/Scripts/analysis_final_bg.py analysis_final_bg.py
sed -i "s@mydir@$bg_dir/@" analysis_final_bg.py

echo "stage final_bg"
fccanalysis final analysis_final_bg.py


cd ../..

#RUNNING THE LOOP OVER MASS AND CYY FOR ee->Z->gamma a -> 3 gamma
#echo "mass        cYY        cross section" > $main_dir/output_file.txt
for ALP_mass in $list_mass; do
    for ALP_cYY in $list_cYY; do
        echo "RUN FOR mass=$ALP_mass cYY=$ALP_cYY"
        process_name="ALP_Z_aa_${ALP_mass}GeV_cYY_${ALP_cYY}"
        mad_graph_dir=$process_name
        run_dir="/results/ALPs_ne_${num_events_short}_mass_${ALP_mass}GeV_cYY_${ALP_cYY}"
        mkdir $main_dir/$run_dir
        cd $main_dir/$run_dir

        # ####################___MC_SIMULATION_STAGE____######################
        # echo "MC SIMULATION STAGE"

        # mad_graph_script_name="mg5_proc_card_ALP_aa_${ALP_mass}GeV_${ALP_cYY}CYY.dat"
        # cp $main_dir/Scripts/mg5_proc_card_ALP_aa_mGeV_cCYY.dat $mad_graph_script_name

        # sed -i "s@ALP_mass@$ALP_mass@" $mad_graph_script_name
        # sed -i "s@num_events@$num_events@" $mad_graph_script_name
        # sed -i "s@ALP_cYY@$ALP_cYY@" $mad_graph_script_name
        # sed -i "s@mad_graph_dir@$mad_graph_dir@" $mad_graph_script_name

        # cp $main_dir/Scripts/ALP_pythia.cmnd ALP_pythia.cmnd
        # sed -i "s@num_events@$num_events@" ALP_pythia.cmnd
        # sed -i "s@process_name.lhe@${process_name}.lhe@" ALP_pythia.cmnd

        # python $main_dir/MG5_aMC_v3_4_2/bin/mg5_aMC $mad_graph_script_name

        # cd $mad_graph_dir/Events/run_01/
        # gunzip unweighted_events.lhe.gz
        # cp unweighted_events.lhe $main_dir/$run_dir/${process_name}.lhe

        # cd $main_dir/$run_dir
        # mkdir output_MadgraphPythiaDelphes
        # DelphesPythia8_EDM4HEP $main_dir/FCC-config/FCCee/Delphes/card_IDEA.tcl $main_dir/FCC-config/FCCee/Delphes/edm4hep_IDEA.tcl ALP_pythia.cmnd output_MadgraphPythiaDelphes/$process_name.root

        ####################___ANALYSIS_STAGE____######################

        echo "ANALYSIS STAGE"

        #RUNNING FCCAnalysis

        dir_name="$main_dir/$run_dir/"
        #extracting the cross section value from "run_01_tag_1_banner.txt"
        line=`grep "Integrated weight"  $main_dir/$run_dir/$process_name/Events/run_01/run_01_tag_1_banner.txt`
        prefix="# Integrated weight (pb) :"
        cross_section=`echo "$line" | cut -c 36-`

        cp $main_dir/Scripts/analysis_stage1.py analysis_stage1.py
        sed -i "s@mydir@$dir_name@" analysis_stage1.py
        sed -i "s@process_name@$process_name@" analysis_stage1.py

        # echo "stage1"
        # fccanalysis run analysis_stage1.py

        background_bool=false
        if [ "$background_bool" = false ]
        then #if you consider only main process
            cp $main_dir/Scripts/analysis_final.py analysis_final.py
            sed -i "s@mydir@$dir_name@" analysis_final.py
            sed -i "s@process_name@$process_name@" analysis_final.py
            sed -i "s@ALPs_mass@$ALP_mass@" analysis_final.py
            sed -i "s@ALPs_cYY@$ALP_cYY@" analysis_final.py
            sed -i "s@num_events@$num_events@" analysis_final.py
            sed -i "s@cross_section_value@$cross_section@" analysis_final.py

            echo "stage final"
            fccanalysis final analysis_final.py

            # cp $main_dir/Scripts/analysis_plots.py analysis_plots.py
            # sed -i "s@mydir@$dir_name@" analysis_plots.py
            # sed -i "s@process_name@$process_name@" analysis_plots.py
            # sed -i "s@ALPs_mass@$ALP_mass@" analysis_plots.py
            # sed -i "s@ALPs_cYY@$ALP_cYY@" analysis_plots.py

            # echo "plotting stage"
            # fccanalysis plots analysis_plots.py
        else #if you need to show background on plots
            mkdir $main_dir/$run_dir/output_stage1/p8_ee_Zee_ecm91 $main_dir/$run_dir/output_stage1/wzp6_ee_gammagamma_ecm91
            ln -sf $bg_dir/output_stage1/p8_ee_Zee_ecm91/*.root $main_dir/$run_dir/output_stage1/p8_ee_Zee_ecm91/
            ln -sf $bg_dir/output_stage1/wzp6_ee_gammagamma_ecm91/*.root $main_dir/$run_dir/output_stage1/wzp6_ee_gammagamma_ecm91/

            cp $main_dir/Scripts/analysis_final_bg_sig.py analysis_final_bg_sig.py
            sed -i "s@mydir@$dir_name@" analysis_final_bg_sig.py
            sed -i "s@process_name@$process_name@" analysis_final_bg_sig.py
            sed -i "s@ALPs_mass@$ALP_mass@" analysis_final_bg_sig.py
            sed -i "s@ALPs_cYY@$ALP_cYY@" analysis_final_bg_sig.py
            sed -i "s@num_events@$num_events@" analysis_final_bg_sig.py
            sed -i "s@cross_section_value@$cross_section@" analysis_final_bg_sig.py

            echo "stage final_bg"
            fccanalysis final analysis_final_bg_sig.py

            cp $main_dir/Scripts/analysis_plots_bg.py analysis_plots_bg.py
            sed -i "s@mydir@$dir_name@" analysis_plots_bg.py
            sed -i "s@process_name@$process_name@" analysis_plots_bg.py
            sed -i "s@ALPs_mass@$ALP_mass@" analysis_plots_bg.py
            sed -i "s@ALPs_cYY@$ALP_cYY@" analysis_plots_bg.py

            echo "plotting stage"
            fccanalysis plots analysis_plots_bg.py
        fi

        # saving data to a file
        # echo "$ALP_mass         $ALP_cYY        $cross_section" >> $main_dir/output_file.txt

        cd ..
    done
done


