 #!/bin/bash
 #SBATCH --mem-per-cpu=2000M
 #SBATCH --time=3:00:00
 
 module purge
 module load StdEnv/2023 ambertools/23
 packmol-memgen \
    --pdb *.pdb \
    --lipids DOPE:DOPG \
    --ratio 3:1 \
    --preoriented \
    --parametrize 
