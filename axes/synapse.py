
import pickle

import numpy as np
from scipy.stats import norm, lognorm
from brian2.units import mV, ms, second
from decimal import Decimal


def n_active_synapses(ax, bpath, nsp):

    try: 
        with open(bpath+'/raw/synee_a.p', 'rb') as pfile:
            synee_a = pickle.load(pfile)


        # trace 1: data from synEE_a (~11 data points)
        active_at_t = np.sum(synee_a['syn_active'], axis=1)

        print(active_at_t)
        print(synee_a['t'])

        all_at_t = np.shape(synee_a['syn_active'])[1]
        assert all_at_t == nsp['N_e']*(nsp['N_e']-1)

        ax.plot(synee_a['t'], active_at_t/all_at_t, lw=2)

        
    except FileNotFoundError:
        print(bpath[-4:], "reports: No n_active data!")
        ax.set_title("No data found")
    
    ax.set_xlabel('time [s]')
    ax.set_ylabel('fraction of synapses active')
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')


    
def synapse_weights_linear(ax, bpath, nsp, tstep, bins, cutoff):

    with open(bpath+'/raw/synee_a.p', 'rb') as pfile:
        synee_a = pickle.load(pfile)

    weight_at_t = synee_a['a'][tstep,:]
    states_at_t = synee_a['syn_active'][tstep,:]

    active_weight_at_t = weight_at_t[states_at_t==1]

    active_weight_at_t_cutoff = active_weight_at_t[active_weight_at_t>cutoff]

    fraction_of_cutoff = len(active_weight_at_t_cutoff)/len(active_weight_at_t)

    print(fraction_of_cutoff)

    ax.hist(active_weight_at_t_cutoff, bins=bins)
    
    ax.set_title('E'+r'$\to$'+'E weights at t=\SI{'+ \
                 str(synee_a['t'][tstep]/second)+'}{s}')

    ax.set_xlabel('synaptic weight')
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')



def synapse_weights_log(ax, bpath, nsp, tstep, bins, cutoff, fit=True):

    with open(bpath+'/raw/synee_a.p', 'rb') as pfile:
        synee_a = pickle.load(pfile)

    weight_at_t = synee_a['a'][tstep,:]
    states_at_t = synee_a['syn_active'][tstep,:]

    active_weight_at_t = weight_at_t[states_at_t==1]

    active_weight_at_t_cutoff = active_weight_at_t[active_weight_at_t>cutoff]

    fraction_of_cutoff = len(active_weight_at_t_cutoff)/len(active_weight_at_t)    

    log_weights = np.log(active_weight_at_t_cutoff)

    if len(log_weights)>0:

        ax.hist(log_weights, bins=bins, density=True)

        if fit:
            floc, fscale = norm.fit(log_weights)
            f_rv = norm(loc=floc, scale=fscale)
            xs = np.linspace(start=np.min(log_weights),
                             stop=np.max(log_weights),
                             num = 1000)
            ax.plot(xs, f_rv.pdf(xs), lw=2, color='red',
                    linestyle='-')


    ax.set_title('E'+r'$\to$'+'E weights at t=\SI{'+ \
                 str(synee_a['t'][tstep]/second)+'}{s}')
        
    ax.set_xlabel('log of synaptic weight')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')




def synapse_weight_traces(ax, bpath, nsp, tmin, tmax, ylim_top=-1,
                          plot_thresholds=False):

    with open(bpath+'/raw/synee_stat.p', 'rb') as pfile:
        synee_stat = pickle.load(pfile)

    for i in range(np.shape(synee_stat['a'])[1]):
        indx = np.logical_and(synee_stat['t'] > tmin,
                              synee_stat['t'] < tmax)
        ax.plot(synee_stat['t'][indx],synee_stat['a'][:,i][indx], color='grey')


    # ax.text(0.47, 0.95,
    # 'ascale='+'%.2E' % Decimal(tr.ascale),
    # horizontalalignment='left',
    # verticalalignment='top',
    # bbox={'boxstyle': 'square, pad=0.3', 'facecolor':'white',
    #       'alpha':1, 'edgecolor':'none'},
    # transform = ax.transAxes)

    # if plot_thresholds:
    #     ax.axhline(tr.a_insert, linestyle='dashed', color='grey')
    #     ax.axhline(tr.prn_thrshld, linestyle='dashed', color='grey')
    #     ax.axhline(tr.amax, color='red')

    if ylim_top>0:
        ax.set_ylim(0,ylim_top)

    ax.set_title('Synaptic Weight Traces')
    ax.set_xlabel('time [s]')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    
