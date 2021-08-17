#!/bin/bash
. /etc/profile.d/z10_spack_environment.sh
. /opt/spack/share/spack/setup-env.sh
spack load mpi fenics
PATH=/opt/software/paraview_build/bin:$PATH
pushd /home/docker/catalyst/Examples/build/PythonDolfinExample
./run-catalyst-step6.sh