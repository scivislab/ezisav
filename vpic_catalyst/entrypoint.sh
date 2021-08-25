#!/bin/bash
. /etc/profile.d/z10_spack_environment.sh
. /opt/spack/share/spack/setup-env.sh
spack load mpi
/opt/software/paraview_build/bin/pvserver