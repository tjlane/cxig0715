

import psana
import sys
from matplotlib import pyplot as plt
import h5py
import numpy as np

RUN = int(sys.argv[-1])

ds = psana.DataSource('exp=cxig0715:run=%d' % RUN)
cspad_det = psana.Detector('CxiDs2.0:Cspad.0')
print('data connected')

gain_map = np.fromfile('../geometry/gain-center.cal', dtype=np.float32).reshape(32,185,388)
print('loaded gain map')

for n_evt, evt in enumerate(ds.events()):

    if n_evt < 1000: continue
    print('skipped first 1000 shots')

    #calib = cspad_det.calib(evt)
    raw = (cspad_det.raw(evt) - cspad_det.pedestals(evt)) * gain_map

    #img = cspad_det.image(evt)
    img = cspad_det.image(evt, raw)
    if img is None:
        continue

    print(n_evt, raw.mean())

    #plt.figure()
    #plt.subplot(111)
    #plt.imshow(img, vmin=-1, vmax=30)
    #plt.show()



    #    print('save and quit')
    #    np.save("cspad_image.npy", img)
    #    break

