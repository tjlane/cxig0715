

import psana
import sys
from matplotlib import pyplot as plt

from scipy.signal import medfilt

RUN = int(sys.argv[-1])

ds = psana.DataSource('exp=cxig0715:run=%d' % RUN)
xtcav_cam = psana.Detector('xtcav')

roi_x = psana.Detector('XTCAV_ROI_sizeX')
roi_y = psana.Detector('XTCAV_ROI_sizeY')

ebeam        = psana.Detector('EBeam')
um_per_px    = psana.Detector('OTRS:DMP1:695:RESOLUTION')
rf_amp       = psana.Detector('SIOC:SYS0:ML01:AO214')
str_strength = psana.Detector('OTRS:DMP1:695:TCAL_X')

def fs_per_px(evt):
    fpp = -um_per_px(evt) * rf_amp(evt) / \
           (0.3 * str_strength(evt) * ebeam.get(evt).ebeamXTCAVAmpl())
    return fpp

for evt in ds.events():

    img = xtcav_cam.image(evt)
    if img is None:
        continue

    print(img.min(), img.max(), roi_x(evt), roi_y(evt))

    print(fs_per_px(evt))

    pulse1 = medfilt(img[:470,:].sum(axis=0), 5)
    pulse2 = medfilt(img[470:,:].sum(axis=0), 5)

    plt.figure()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.plot(pulse1)
    plt.plot(pulse2)
    plt.show()

