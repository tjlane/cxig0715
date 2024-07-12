
#for run in 129 131 133 136 252 253 254; do
for run in 252 253 254; do
  echo ${run}
  bsub -q psanaq -n 8 mpirun python preprocess.py -r ${run} -o
done

