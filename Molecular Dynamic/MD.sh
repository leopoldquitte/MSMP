#!/bin/sh
#SBATCH -J "mdCCRL2G2"
#SBATCH -t 167:00:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --ntasks-per-core=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:p100:1
#SBATCH --mem=90G

ml --force purge
ml StdEnv/2020 gcc/9.3.0 cuda/11.0 openmpi/4.0.3 amber/20.9-20.15
ulimit -s 86400

top=${1##*.}

if [ -z $top ]; then
    echo "eq_amber.sh : Aucun fichier indique."
    echo "usage : ./job_amber_gpu_onejob.sh [file.prmtop]"
    exit 1
fi
if [ "$top" != "prmtop" ] || [ ! -e "$1" ]; then
    echo "eq_amber.sh : le premier argument doit etre un fichier prmtop"
    echo "usage : ./job_amber_gpu_onejob.sh [file.inpcrd] [file.prmtop]"
    exit 1
fi

srun pmemd.cuda.MPI -O -i md_mem.in -o md7.out -p $1 -c md6.rst -ref md6.rst -r md7.rst -x md7.nc

grep -E "TEMP\(K\)|Etot" md1.out | sed 's/=/ = /g'  | awk -v OFS="," 'NR==1 {print "NSTEP,TIME(PS),TEMP(K),PRESS,Etot,EKtot,EPtot"} /NSTEP/{ORS="" ;print $3,$6,$9,$12;getline;print "," ;print $3,$6,$9; print "\n" }' > results_md7.csv

jobinfo ${SLURM_JOBID}
infoincidentjob
exit
