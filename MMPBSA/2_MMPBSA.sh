#!/bin/bash 
#SBATCH --mem-per-cpu=10G 
#SBATCH --time=48:00:00
#SBATCH --ntasks=32
#SBATCH --ntasks-per-node=16
module --force purge
module load StdEnv/2023
module load gcc/12.3
module load openmpi/4.1.5
module load amber/22
module load scipy-stack  # Si nécessaire
module load python/3.7.9

mpirun -np 16 MMPBSA.py.MPI -O -eo ene.csv -deo dec.csv -i mmpbsa.in -o mmpbsa.dat -sp bilayer_MSMP_CCR2G_2out_lipid.prmtop -cp complex.prmtop -rp rec.prmtop -lp lig.prmtop -y ../../../md_all.nc

jobinfo ${SLURM_JOBID}
infoincidentjob
exit
