

import psana
import sys
from matplotlib import pyplot as plt
from psgeom.radavg import Averager
import h5py
import numpy as np

RUN = int(sys.argv[-1])

ds = psana.DataSource('exp=cxig0715:run=%d:smd' % RUN)
cspad_det = psana.Detector('CxiDs2.0:Cspad.0')

f = h5py.File('../geometry/thor_format.h5', 'r')
q_xyz = np.array(f['q_xyz_reshaped'])
q_mag = np.sqrt( np.sum( np.power(q_xyz, 2), axis=-1 ) )
f.close()

#ds2_mask = np.load('../geometry/minimal_mask_psanashp.npy')
evt = ds.events().next()
ds2_mask = cspad_det.mask(evt, calib=False, status=True, edges=True, central=True, unbondnbrs=True)
radavg = Averager(q_mag, ds2_mask, n_bins=500)

gain_map = np.fromfile('../geometry/gain-center.cal', dtype=np.float32).reshape(32,185,388)

for n_evt, evt in enumerate(ds.events()):


    if n_evt < 1000: continue


    #calib = cspad_det.calib(evt)
    raw = (cspad_det.raw(evt) - cspad_det.pedestals(evt)) * gain_map
    Iq = radavg(raw)

    #img = cspad_det.image(evt)
    img = cspad_det.image(evt, raw)
    if img is None:
        continue

    print(n_evt, raw.mean())

    #break
    plt.figure()
    plt.subplot(121)
    plt.imshow(img, vmin=-1, vmax=30)
    plt.subplot(122)
    plt.plot(Iq)
    plt.show()

