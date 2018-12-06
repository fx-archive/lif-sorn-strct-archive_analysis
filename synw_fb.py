
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
from matplotlib import rc

rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',   
    r'\usepackage{sansmath}',  
    r'\sansmath'               
    r'\usepackage{siunitx}',   
    r'\sisetup{detect-all}',   
]  

import argparse, sys, os, itertools, pickle
import numpy as np
from brian2.units import mV, ms, second

from .axes.synapse import *
from .axes.parameter_display import *



def synw_figure(bpath, nsp):


    fig = pl.figure()
    ax_lines, ax_cols = 6,4
    axs = {}
    for x,y in itertools.product(range(ax_lines),range(ax_cols)):
        axs['%d,%d'%(x+1,y+1)] = pl.subplot2grid((ax_lines, ax_cols), (x, y))

    fig.set_size_inches(1920/150*5/4,1080/150*7/3)


    ##########################################################################


    synapse_weights_linear(axs['1,1'], bpath, nsp, tstep=0, bins=50,
                           cutoff=0.)
    synapse_weights_linear(axs['2,1'], bpath, nsp, tstep=3, bins=50,
                           cutoff=0.)
    synapse_weights_linear(axs['3,1'], bpath, nsp, tstep=6, bins=50,
                           cutoff=0.)
    synapse_weights_linear(axs['4,1'], bpath, nsp, tstep=10, bins=50,
                           cutoff=0.)
    synapse_weights_linear(axs['5,1'], bpath, nsp, tstep=15, bins=50,
                           cutoff=0.)
    synapse_weights_linear(axs['6,1'], bpath, nsp, tstep=19, bins=50,
                           cutoff=0.)
    
    synapse_weights_linear(axs['1,2'], bpath, nsp, tstep=0, bins=50,
                           cutoff=10.**(-20))
    synapse_weights_linear(axs['2,2'], bpath, nsp, tstep=3, bins=50,
                           cutoff=10**(-20))
    synapse_weights_linear(axs['3,2'], bpath, nsp, tstep=6, bins=50,
                           cutoff=10.**(-20))
    synapse_weights_linear(axs['4,2'], bpath, nsp, tstep=10, bins=50,
                           cutoff=10.**(-20))
    synapse_weights_linear(axs['5,2'], bpath, nsp, tstep=15, bins=50,
                           cutoff=10.**(-20))
    synapse_weights_linear(axs['6,2'], bpath, nsp, tstep=19, bins=50,
                           cutoff=0.0001)

    synapse_weights_linear(axs['1,3'], bpath, nsp, tstep=0, bins=50,
                           cutoff=10**(-10))
    synapse_weights_linear(axs['2,3'], bpath, nsp, tstep=3, bins=50,
                           cutoff=10**(-10))
    synapse_weights_linear(axs['3,3'], bpath, nsp, tstep=6, bins=50,
                           cutoff=10**(-10))
    synapse_weights_linear(axs['4,3'], bpath, nsp, tstep=10, bins=50,
                           cutoff=10**(-10))
    synapse_weights_linear(axs['5,3'], bpath, nsp, tstep=15, bins=50,
                           cutoff=10**(-10))
    synapse_weights_linear(axs['6,3'], bpath, nsp, tstep=19, bins=50,
                           cutoff=10**(-10))
        

    netw_params_display(axs['1,4'], bpath, nsp)
    neuron_params_display(axs['2,4'], bpath, nsp)
    synapse_params_display(axs['3,4'], bpath, nsp)
    stdp_params_display(axs['4,4'], bpath, nsp)
    sn_params_display(axs['5,4'], bpath, nsp)
    strct_params_display(axs['6,4'], bpath, nsp)


    
    ##########################################################################
    

    pl.tight_layout()

    directory = "figures/synw/linear"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    pl.savefig(directory+"/{:s}.png".format(bpath[-4:]),
               dpi=100, bbox_inches='tight')

    



    
if __name__ == "__main__":

    
    # return a list of each build (simulations run)
    # e.g. build_dirs = ['builds/0003', 'builds/0007', ...]
    # sorted to ensure expected order
    build_dirs = sorted(['builds/'+pth for pth in next(os.walk("builds/"))[1]])



    for bpath in build_dirs:

        try:
            with open(bpath+'/raw/namespace.p', 'rb') as pfile:
                nsp=pickle.load(pfile)

            synw_figure(bpath, nsp)

        except FileNotFoundError:
            print(bpath[-4:], "reports: No namespace data. Skipping.")


