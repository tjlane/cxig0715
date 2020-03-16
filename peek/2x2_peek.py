

import psana
import sys
from matplotlib import pyplot as plt


RUN = int(sys.argv[-1])

ds = psana.DataSource('exp=cxig0715:run=%d:smd' % RUN)
cspad_det = psana.Detector('Sc2spec140k')

for n_evt, evt in enumerate(ds.events()):

    if n_evt < 1000: continue

    img = cspad_det.image(evt)
    #img = cspad_det.raw(evt).reshape(-1, 388)
    if img is None:
        continue

    plt.figure()
    plt.imshow(img, vmin=-1, vmax=30)
    plt.show()

