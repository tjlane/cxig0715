

import psana
import sys
import numpy as np
from matplotlib import pyplot as plt

from scipy.signal import medfilt

RUN = int(sys.argv[-1])

ds = psana.DataSource('exp=cxig0715:run=%d' % RUN)
feespec   = psana.Detector('FEE-SPEC0')

for evt in ds.events():

    # FEE spectrometer
    spc = feespec.get(evt)

    if spc is None:
        pass
    else:

        trace = np.copy(spc.hproj())

        trace = trace - np.median(trace)
        trace[trace < 0.0] = 0.0

        plt.figure()
        plt.plot(trace)
        plt.vlines(0.0, 1.0, [750, 1250])
        plt.show()


