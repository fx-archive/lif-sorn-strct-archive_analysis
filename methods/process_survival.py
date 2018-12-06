
from brian2.units import second
import time
import numpy as np

def extract_survival(turnover_data, bin_w, N_neuron, t_split,
                      t_cut = 0.*second):
    '''
    turnover data is assumed to be a numpy.array with 
    lines consisting of the four entries
    
      gen/prune, t, i, j     

    where 
      -- gen/prune :: 1 if synapse became active, 
                      0 if synapse became inactive
      -- t         :: simulation time point in seconds(!)
      -- i         :: pre-synaptic neuron index
      -- j         :: post-synaptic neuron index

    -----------

    parameters:
     
     -- turnover_data  :: 
     -- N_neuron       ::
     -- initial        :: determines handling of initially at 
                          t_cut present synapsese

                          - "only" :: returns lifetimes only 
                              for synapses present at t_cut
                          - "with" :: return lifetimes of 
                              synapses present at t_cut and 
                              those generated after t_cut
                          - "without" :: return lifetimes of
                              synapses generated after t_cut      
      
    returns: 

     -- lifetimes  :: duration from generation (or initial presence) 
                      until pruning. Synapses generated (initally 
                      present) but not yet pruned at simulation end 
                      are NOT INCLUDED
     -- deathtimes :: like lifetimes, but from death to generation,
                      i.e. time from begining of simulation until 
                      first generation is not included 
    '''

    # lexsort by pre- and post-synaptic indices
    # Example:
    #
    # array([[  1.,   0.,   2., 347.],
    #        [  1.,   0.,   3., 248.],
    #        [  1.,   0.,   4., 145.],
    #        [  1.,   0.,  14., 210.],
    #        [  1.,   0.,  20., 318.]])
    #
    # becomes
    #
    # array([[1.  , 7.19, 0.  , 1.  ],
    #        [1.  , 1.81, 0.  , 2.  ],
    #        [0.  , 1.86, 0.  , 2.  ],
    #        [1.  , 9.28, 0.  , 2.  ],
    #        [1.  , 1.89, 0.  , 3.  ]])

    survival_times = np.arange(0, t_split/second+bin_w/second,
                              bin_w/second)
    survival_counts = np.zeros_like(survival_times)
    survival_times = survival_times*second

    a = time.time()
    turnover_data = turnover_data[turnover_data[:,1]>= t_cut/second]
    turnover_data[:,1] = turnover_data[:,1]-t_cut/second
    b = time.time()
    print('cutting took %.2f seconds' %(b-a))

    # turnover_data = turnover_data[turnover_data[:,1]<= t_split/second]
    
    a = time.time()
    ind = np.lexsort((turnover_data[:,3],turnover_data[:,2]))
    df_sorted = turnover_data[ind]
    b = time.time()
    print('lexsort took %.2f seconds' %(b-a))
    
    current_synapse = []
    prev_s_id = 0.
    empty_array_count = 0

    a = time.time()
    for syn_rec in df_sorted:
        
        s_id = syn_rec[2] * N_neuron + syn_rec[3]
        
        if not prev_s_id==s_id:
            print('current s_id: %d' %s_id)

            if current_synapse==[]:
                # this can happen only when synapse 0,0 has no event
                empty_array_count += 1
                assert(empty_array_count < 2)

            else:
                c_array = np.array(current_synapse)
                ind = np.argsort(c_array[:,1])
                c_sort = c_array[ind]

                if len(c_sort) == 0:
                    pass
                elif len(c_sort) == 1:
                    if c_sort[0,0]==1 and c_sort[0,1]<=t_split/second:
                        # synapses started but did not die with sim tim
                        # add maximal survival
                        survival_counts += np.ones_like(survival_counts)
                        
                elif len(c_sort) > 1:
                    
                    if c_sort[0,0] == 0:
                        # dies first get rid of first event
                        c_sort = c_sort[1:,:]

                    if len(c_sort)==1 and c_sort[0,1]<=t_split/second:
                        # synapses started but did not die with sim tim
                        # add maximal survival
                        survival_counts += np.ones_like(survival_counts)


                    elif len(c_sort) > 1:


                        # normalizes the times to the growth event
                        c_sort[:,1] = c_sort[:,1]-c_sort[0,1]

                        # filter out events after window t_split
                        c_sort_cut = c_sort[c_sort[:,1]<=t_split/second]

                        if len(c_sort_cut) % 2 == 0:
                            # ends on pruning event
                            lts = np.diff(c_sort_cut[:,1])
                            assert np.max(lts)<=t_split/second
                            
                            for lt in lts:
                                # look up lt in survival_bins
                                # and add survival counts
                                added_counts = np.zeros_like(survival_counts)
                                # print(added_counts)
                                # print(added_counts[survival_times/second<lt])
                                added_counts[survival_times/second<lt]=1

                                survival_counts += added_counts

                        elif len(c_sort_cut) % 2 == 1:
                            # ends on growth event find next death event
                            if len(c_sort_cut) == len(c_sort):
                                # can't find any, add maximal survival
                                survival_counts += np.ones_like(survival_counts)
                            else:
                                c_sort_appendix = c_sort[len(c_sort_cut),:]
                                assert c_sort_appendix[0]==0
                                c_sort_cut = np.vstack((c_sort_cut,
                                                        c_sort_appendix))

                                assert len(c_sort_cut) % 2 ==0

                                lts = np.diff(c_sort_cut[:,1])
                            
                                for lt in lts:
                                    # look up lt in survival_bins
                                    # and add survival counts
                                    added_counts = np.zeros_like(survival_counts)
                                    added_counts[survival_times/second<lt]=1

                                    survival_counts += added_counts

                                    
                            
                current_synapse = []
                
        current_synapse.append(list(syn_rec))
        prev_s_id = s_id


    b = time.time()
    print('main loop took %.2f seconds' %(b-a))
    return survival_times, survival_counts


