#!/usr/bin/env python

from pypad import cspad
d = cspad.CSPad.load_crystfel('ds2_lysozyme.geom')
dt = d.to_thor(7121.0, 69.0, filename='ds2_lysozyme.dtc')
print dt.q_max

