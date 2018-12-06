
import pickle
import numpy as np
from brian2.units import mV, ms, second, Hz


def inst_rates(ax, bpath, nsp, tmin, tmax):
    
    with open(bpath+'/raw/gexc_rate.p', 'rb') as pfile:
        GExc_rate = pickle.load(pfile)
        GExc_smr = pickle.load(pfile)
    with open(bpath+'/raw/ginh_rate.p', 'rb') as pfile:
        GInh_rate = pickle.load(pfile)
        GInh_smr = pickle.load(pfile)
    # with open(bpath+'/raw/pinp_rate.p', 'rb') as pfile:
    #     PInp_rate = pickle.load(pfile)

        
    if len(GExc_rate['rate']) == 0:
        pass
    
    else:
        indx = np.logical_and(GExc_rate['t']>tmin, GExc_rate['t']<tmax)
        ax.plot(GExc_rate['t'][indx]/second, GExc_smr[indx]/Hz)


    if len(GInh_rate['rate']) == 0:
        pass
    
    else:
        indx = np.logical_and(GInh_rate['t']>tmin, GInh_rate['t']<tmax)
        ax.plot(GInh_rate['t'][indx]/second, GInh_smr[indx]/Hz,
                color='red')
       

    # ax.set_ylim(nsp['Vr_e']/mV-1.5, nsp['Vt_e']/mV+1.5)
    ax.set_title('Rates')
    ax.set_xlabel('time [s]')
    ax.set_ylabel('rate [Hz]')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
        
    
