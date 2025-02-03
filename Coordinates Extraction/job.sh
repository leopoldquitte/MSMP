#!/bin/bash
#SBATCH -J "extract_Mnew"
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=8G
#SBATCH --time=10:00:00
ml --force purge
ml StdEnv/2020 gcc/9.3.0 cuda/11.4 openmpi/4.0.3 amber/20.12-20.15
cpptraj -p ../../md_wrap.prmtop -y ../../md_wrap_all1.nc -i frames.in
