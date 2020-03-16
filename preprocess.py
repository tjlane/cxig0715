

import argparse
import numpy as np
import h5py
from scipy.signal import medfilt

import psana
from xtcav2.LasingOnCharacterization import LasingOnCharacterization
from psgeom.radavg import Averager

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', type=int, required=True,
                    help='the run number to preprocess')
args = parser.parse_args()


dsource   = psana.MPIDataSource('exp=cxig0715:run=%d:smd' % args.run)
smldata   = dsource.small_data('/reg/d/psdm/cxi/cxig0715/scratch/smalldata/run%d.h5' % args.run)

# --- spectrometer
feespec   = psana.Detector('FEE-SPEC0')


# --- cspad
cspad_det = psana.Detector('CxiDs2.0:Cspad.0')

f = h5py.File('geometry/thor_format.h5', 'r')
q_xyz = np.array(f['q_xyz_reshaped'])
q_mag = np.sqrt( np.sum( np.power(q_xyz, 2), axis=-1 ) )
f.close()

ds2_mask = np.load('geometry/minimal_mask_psanashp.npy')
radavg = Averager(q_mag, ds2_mask, n_bins=500)


# --- xtcav
XTCAV = LasingOnCharacterization(num_bunches=2)



# >>> event loop
for nevt, evt in enumerate(dsource.events()):

    # we'll only save events with a full set of interesting data
    save_evt = True

    # use for debugging on a small number of events
    #if nevt > 200:
    #    print('event #', nevt)
    #    break

    # ---------------------------------------------------------------
    # get the CSPAD, radially integrate it

    calib = cspad_det.calib(evt) # .image = 2d corrected image
    if calib is None:
        save_evt = False
    else:
        Iq = radavg(calib)
        Iq[342:] = Iq[342:] / 2.8 # gain map TODO fix this

        # hitfind (gets both xtals and soln)
        if Iq.mean(0) < 2.0:
            save_evt = False


    # ---------------------------------------------------------------
    # get the XTCAV data and compute the inter-pulse separation
    XTCAV.processEvent(evt)
    xray_delays = XTCAV.pulseDelay()
    if xray_delays is None:
        save_evt = False

    # ---------------------------------------------------------------
    # FEE spectrometer
    spc = feespec.get(evt)

    if spc is None:
        save_evt = False
    else:

        trace = np.copy(spc.hproj())

        trace = trace - np.median(trace)
        trace[trace < 0.0] = 0.0

        pump_position = np.average(np.arange(1000), weights=trace[:1000])
        pump_mag = np.sum(trace[:1000])

        probe_position = np.average(np.arange(1000)+1000, weights=trace[1000:2000])
        probe_mag = np.sum(trace[1000:2000])

        # if we have bad overlap, simply reject the shot
        if pump_position > 750:
            print 'Pump position too close to Fe edge (%f)' % pump_position
            save_evt = False
        if probe_position < 1250:
            print 'Probe position too close to Fe edge (%f)' % probe_position
            save_evt = False

    if save_evt == True:
        smldata.event(radial_profile=Iq,
                      pulse_time=xray_delays,
                      pump_energy=pump_position,
                      pump_mag=pump_mag,
                      probe_energy=probe_position,
                      probe_mag=probe_mag)


# save HDF5 file
smldata.save(radial_profile_qvalues=radavg.bin_centers)



