
for run in 129 131 133 136 252 253 254; do
#for run in 252 253 254; do
  echo ${run}
  sbatch -p psanaq --nodes 1 --ntasks-per-node 8 --wrap="mpirun python preprocess.py -r ${run} --onecolor"
done

