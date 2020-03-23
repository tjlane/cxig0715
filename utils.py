
import numpy as np
import h5py
import os

def is_crystal(radial_profile, tv_threshold=75.0):    
    tv = np.abs(np.gradient(radial_profile[:,40:120], axis=1)).sum(1)
    return (tv > tv_threshold)


def load_runs(runs_to_analyze, one_color=False, 
              file_loc='/reg/d/psdm/cxi/cxig0715/scratch/smalldata/',
              verbose=True):
    """
    ugly but useful
    """
    
    probe_energy   = []
    probe_mag      = []
    pp_delay       = []
    pump_energy    = []
    pump_mag       = []
    radial_profile = []
    

    for run in runs_to_analyze:

        fn = file_loc + 'run%d.h5' % run

        if os.path.exists(fn):

            f = h5py.File(fn, 'r')

            try:
                probe_energy.append( np.array(f['probe_energy']) )
                probe_mag.append( np.array(f['probe_mag']) )
                pump_energy.append( np.array(f['pump_energy']) )
                pump_mag.append( np.array(f['pump_mag']) )
                radial_profile.append( np.array(f['radial_profile']) )

                if one_color:
                    pp_delay.append( -1 * np.ones(f['pulse_time'].shape[0]) )
                else:
                    pulse_times = np.array(f['pulse_time'])
                    pp_delay.append( np.abs(pulse_times[:,0] - pulse_times[:,1]) )

                radial_profile_qvalues = np.array(f['radial_profile_qvalues'])
            except KeyError as e:
                print('WARNING! Issue loading run: %d' % run)
                print(e)
                print('Attempting to continue...')
                continue
                
            f.close()
        else:
            print('run %d not on disk...' % run)
            
    datadict = { 'probe_energy'   : np.concatenate(probe_energy),
                 'probe_mag'      : np.concatenate(probe_mag),
                 'pp_delay'       : np.concatenate(pp_delay),
                 'pump_energy'    : np.concatenate(pump_energy),
                 'pump_mag'       : np.concatenate(pump_mag),
                 'radial_profile' : np.concatenate(radial_profile),
                 'radial_profile_qvalues' : radial_profile_qvalues}

    if verbose == True:
        print('\n')
        print('--- LOADED %d RUNS --' % len(runs_to_analyze))
        for k,v in datadict.items():
            print('%s : %s' % (k.ljust(25), str(v.shape)))
            
    return datadict


