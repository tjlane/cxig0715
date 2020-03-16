
for run in `seq 107 265`; do
  echo ${run}
  bsub -q psanaq -n 8 mpirun python preprocess.py -r ${run}
done

