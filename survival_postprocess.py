
import argparse, sys, os, itertools, pickle, time
import numpy as np
from brian2.units import mV, ms, second

from .methods.process_survival import extract_survival


def add_survival(ax, bin_w, bpath, nsp, t_split, t_cut):

    label = str(int(nsp['T2']/second)) + ' s'

    survival_probabilities_linear(ax, bpath, nsp,
                                  bin_w=bin_w,
                                  t_split=t_split,
                                  t_cut=t_cut,
                                  density=True,
                                  label=label)
    

    
if __name__ == "__main__":

    
    # return a list of each build (simulations run)
    # e.g. build_dirs = ['builds/0003', 'builds/0007', ...]
    # sorted to ensure expected order
    build_dirs = sorted(['builds/'+pth for pth in next(os.walk("builds/"))[1]])

    bin_w = 1*second
    fit = False


    for bpath in build_dirs:

        try:
            
            print('Found ', bpath)
            # if bpath=='builds/0000':
                
            #     with open(bpath+'/raw/namespace.p', 'rb') as pfile:
            #         nsp=pickle.load(pfile)

            #     t_split = 49500*second
            #     t_cut = 1005*second

            #     print('started loading data')
            #     a = time.time()
            #     with open(bpath+'/raw/turnover.p', 'rb') as pfile:
            #         turnover = pickle.load(pfile)
            #     b=time.time()
            #     print('finished loading data, took %.2f seconds' %(b-a))

            #     a=time.time()
            #     print('\n started survival extractation')
            #     s_times, s_counts = extract_survival(turnover, bin_w,
            #                                          nsp['N_e'],
            #                                          t_split,
            #                                          t_cut = t_cut)
            #     b = time.time()
            #     print('finished survival extraction, took %.2f seconds' %(b-a))

            #     with open(bpath+'/raw/survival.p', 'wb') as pfile:
            #         out = {'t_split': t_split, 't_cut': t_cut,
            #                's_times': s_times, 's_counts': s_counts}
            #         pickle.dump(out, pfile)
                    

            if bpath=='builds/0009':
                
                with open(bpath+'/raw/namespace.p', 'rb') as pfile:
                    nsp=pickle.load(pfile)

                t_split = 49500*second
                t_cut = 1005*second

                print('started loading data')
                a = time.time()
                with open(bpath+'/raw/turnover.p', 'rb') as pfile:
                    turnover = pickle.load(pfile)
                b=time.time()
                print('finished loading data, took %.2f seconds' %(b-a))

                a=time.time()
                print('\n started survival extractation')
                s_times, s_counts = extract_survival(turnover, bin_w,
                                                     nsp['N_e'],
                                                     t_split,
                                                     t_cut = t_cut)
                b = time.time()
                print('finished survival extraction, took %.2f seconds' %(b-a))

                with open(bpath+'/raw/survival.p', 'wb') as pfile:
                    out = {'t_split': t_split, 't_cut': t_cut,
                           's_times': s_times, 's_counts': s_counts}
                    pickle.dump(out, pfile)
                    


        except FileNotFoundError:
            print(bpath[-4:], "reports: No namespace data. Skipping.")



