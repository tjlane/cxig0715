# cxig0715
analysis scripts and notebooks for soln damage study

* `preprocess.py` is the script to make HDF5 files. NOTE that it will overwrite the currently processed data so modify it in a smart way :). You can run this in parallel with something like: `mpirun -n 8 python preprocess.py -r 151`.

* `preliminary_look.ipynb` shows a quick scan through the contents of one of the "preprocessed" HDF5 files


