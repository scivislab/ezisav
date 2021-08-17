#!/bin/bash
. /etc/profile.d/z10_spack_environment.sh
. /opt/spack/share/spack/setup-env.sh
spack load mpi
pushd /home/docker/catalyst/Examples
build/CxxFullExample/CxxFullExample CxxFullExample/SampleScripts/feslicescript.py