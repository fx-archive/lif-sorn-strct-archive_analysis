#!/bin/sh

rm -rf analysis/
mkdir analysis

cp -r ../../analysis/file_based analysis/file_based

# python analysis/file_based/overview_fb.py
# #srun -p x-men --mem 32GB python analysis/file_based/synapse_dynamics_fb.py
# python analysis/file_based/synapse_dynamics_fb.py
# python analysis/file_based/synapse_weight_snapshots_log_fb.py
# python analysis/file_based/synapse_weight_snapshots_fb.py
# python analysis/file_based/network_activity_fb.py
python analysis/file_based/turnover_fb.py
# python analysis/file_based/turnover_x_Aminus_fb.py
# python analysis/file_based/turnover_x_Aminus_fitonly_fb.py
# python analysis/file_based/active_synapses_x_Aminus_fb.py
