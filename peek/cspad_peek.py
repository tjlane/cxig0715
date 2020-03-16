

import psana
import sys
from matplotlib import pyplot as plt


RUN = int(sys.argv[-1])

ds = psana.DataSource('exp=cxig0715:run=%d:smd' % RUN)
cspad_det = psana.Detector('CxiDs2.0:Cspad.0')

for n_evt, evt in enumerate(ds.events()):

    if n_evt < 1000: continue
    print(n_evt)

    #img = cspad_det.image(evt)
    img = cspad_det.calib(evt).reshape(-1, 388)
    if img is None:
        continue

    plt.figure()
    plt.imshow(img, vmin=-1, vmax=30)
    plt.show()

