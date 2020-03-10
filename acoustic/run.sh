#!/bin/sh
SPECFEM_DIR=~/src/specfem2d_devel

rm -rf OUTPUT_FILES*
mkdir OUTPUT_FILES

# Forward run
sed -i "/^SIMULATION_TYPE/s|=.*$|= 1|" DATA/Par_file
sed -i "/^SAVE_FORWARD/s|=.*$|= .true.|" DATA/Par_file

echo "Running mesher"
${SPECFEM_DIR}/bin/xmeshfem2D > OUTPUT_FILES/mesher_output
echo "Running forward simulation"
${SPECFEM_DIR}/bin/xspecfem2D > OUTPUT_FILES/specfem_forward_output

rm -rf SEM
mkdir SEM

../bin/create_adj.py BXX

# Adjoint run
sed -i "/^SIMULATION_TYPE/s|=.*$|= 3|" DATA/Par_file
sed -i "/^SAVE_FORWARD/s|=.*$|= .false.|" DATA/Par_file


echo "Running adjoint simulation"
${SPECFEM_DIR}/bin/xspecfem2D > OUTPUT_FILES/specfem_adjoint_output

cp ./DATA/proc000000_{x,z}.bin OUTPUT_FILES
../bin/plot_kernel.py OUTPUT_FILES c_acoustic_kernel -m 1e-23 -o OUTPUT_FILES/acoustic_kernel.png
mv OUTPUT_FILES{,_BXX}

mkdir OUTPUT_FILES

# Forward run
sed -i "/^SIMULATION_TYPE/s|=.*$|= 1|" DATA/Par_file
sed -i "/^SAVE_FORWARD/s|=.*$|= .true.|" DATA/Par_file

echo "Running mesher"
${SPECFEM_DIR}/bin/xmeshfem2D > OUTPUT_FILES/mesher_output
echo "Running forward simulation"
${SPECFEM_DIR}/bin/xspecfem2D > OUTPUT_FILES/specfem_forward_output


rm -rf SEM
mkdir SEM

../bin/create_adj.py BXZ

# Adjoint run
sed -i "/^SIMULATION_TYPE/s|=.*$|= 3|" DATA/Par_file
sed -i "/^SAVE_FORWARD/s|=.*$|= .false.|" DATA/Par_file


echo "Running adjoint simulation"
${SPECFEM_DIR}/bin/xspecfem2D > OUTPUT_FILES/specfem_adjoint_output

cp ./DATA/proc000000_{x,z}.bin OUTPUT_FILES
../bin/plot_kernel.py OUTPUT_FILES c_acoustic_kernel -m 1e-23 -o OUTPUT_FILES/acoustic_kernel.png
mv OUTPUT_FILES{,_BXZ}

