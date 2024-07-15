
# goconda
# conda activate ana-409-tj

for run in 127 144 148 150 152 154 166 168 171 174 179 184 189 192 194 205 207 209 212 215 232 234 236 248 257 261 263 222 223 224 225 231 233 235 256 258 259 260 262 264; do
  echo ${run}
  sbatch -p psanaq --nodes 1 --ntasks-per-node 16 --wrap="mpirun python preprocess.py -r ${run}"
done

