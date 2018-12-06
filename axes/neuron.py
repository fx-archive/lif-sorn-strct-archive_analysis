
import pickle
import numpy as np
from brian2.units import mV, ms, second


def raster_plot(ax, bpath, nsp, tmin, tmax):
    '''
    '''

    with open(bpath+'/raw/gexc_spks.p', 'rb') as pfile:
        GExc_spks = pickle.load(pfile)
    with open(bpath+'/raw/ginh_spks.p', 'rb') as pfile:
        GInh_spks = pickle.load(pfile)

    try:
        indx = np.logical_and(GExc_spks['t']/ms>tmin/ms, GExc_spks['t']/ms<tmax/ms)
        ax.plot(GExc_spks['t'][indx]/second, GExc_spks['i'][indx],
                marker='.', color='blue', markersize=.5,
                linestyle='None')
    except AttributeError:
        print(bpath[-4:], "reports: AttributeError. Guess: no exc. spikes from",
              "{:d}s to {:d}s".format(int(tmin/second),int(tmax/second)))

    try:
        indx = np.logical_and(GInh_spks['t']/ms>tmin/ms, GInh_spks['t']/ms<tmax/ms)
        ax.plot(GInh_spks['t'][indx]/second,
                GInh_spks['i'][indx]+nsp['N_e'], marker='.',
                color='red', markersize=.5, linestyle='None')
    except AttributeError:
        print(bpath[-4:], "reports: AttributeError. Guess: no inh. spikes from",
              "{:d}s to {:d}s".format(int(tmin/second),int(tmax/second)))


    ax.set_xlim(tmin/second, tmax/second)
    ax.set_xlabel('time [s]')
    ax.set_ylim(0, nsp['N_e'] + nsp['N_i'])
    
    # ax.set_title('T='+str(T/second)+' s')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')





def raster_plot_poisson(ax, bpath, nsp, tmin, tmax):
    '''
    '''

    with open(bpath+'/raw/pinp_spks.p', 'rb') as pfile:
        PInp_spks = pickle.load(pfile)

    try:
        indx = np.logical_and(PInp_spks['t']/ms>tmin/ms, PInp_spks['t']/ms<tmax/ms)
        ax.plot(PInp_spks['t'][indx]/second, PInp_spks['i'][indx], marker='.',
                color='blue', markersize=.5, linestyle='None')
    except AttributeError:
        print(bpath[-4:], "reports: AttributeError. Guess: no PInp. spikes from",
              "{:d}s to {:d}s".format(int(tmin/second),int(tmax/second)))


    ax.set_xlim(tmin/second, tmax/second)
    ax.set_xlabel('time [s]')
    ax.set_ylim(0, nsp['NPInp'])
    
    # ax.set_title('T='+str(T/second)+' s')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    

    
def ge_plot(ax, bpath, nsp, tmin, tmax):

    with open(bpath+'/raw/gexc_stat.p', 'rb') as pfile:
        GExc_stat = pickle.load(pfile)

    ge_data=GExc_stat['ge']

    indx = np.logical_and(GExc_stat['t']>tmin, GExc_stat['t']<tmax)

    for i in range(np.shape(ge_data)[1]):
        ax.plot(GExc_stat['t'][indx]/second, ge_data[:,i][indx])
        
    #ax.set_xlim(tmin/second, tmax/second)
    ax.set_xlabel('time [s]')

    #ax.set_ylim(0, nsp['N_e'] + nsp['N_i'])
    # ax.set_title('T='+str(T/second)+' s')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')    


def voltage_traces(ax, bpath, nsp, tmin, tmax):
    
    with open(bpath+'/raw/gexc_stat.p', 'rb') as pfile:
        GExc_stat = pickle.load(pfile)

    if len(GExc_stat['V']) == 0:
        pass
    
    else:

        indx = np.logical_and(GExc_stat['t']>tmin, GExc_stat['t']<tmax)

        for i in range(len(GExc_stat['V'].T)):
            ax.plot(GExc_stat['t'][indx]/second, GExc_stat['V'][:,i][indx]/mV)

        ax.set_ylim(nsp['Vr_e']/mV-1.5, nsp['Vt_e']/mV+1.5)
        ax.set_title('Membrane Voltage Traces')
        ax.set_xlabel('time [s]')
        ax.set_ylabel('voltage [mV]')

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        
    
