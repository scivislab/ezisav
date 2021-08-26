# Build stage with Spack pre-installed and ready to be used
FROM spack/ubuntu-bionic:latest as builder


# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir /opt/spack-environment \
&&  (echo "spack:" \
&&   echo "  packages:" \
&&   echo "    all:" \
&&   echo "      target:" \
&&   echo "      - haswell" \
&&   echo "      providers:" \
&&   echo "        mpi:" \
&&   echo "        - openmpi" \
&&   echo "    boost:" \
&&   echo "      version:" \
&&   echo "      - 1.74.0" \
&&   echo "    llvm:" \
&&   echo "      variants: ~compiler-rt~clang~gold~libcxx~lld~lldb~internal_unwind" \
&&   echo "    openmpi:" \
&&   echo "      variants: +legacylaunchers+pmi+thread_multiple fabrics=ucx schedulers=slurm" \
&&   echo "      version:" \
&&   echo "      - 4.1.1" \
&&   echo "    flex:" \
&&   echo "      version:" \
&&   echo "      - 2.6.4" \
&&   echo "    mesa:" \
&&   echo "      variants: ~glx" \
&&   echo "    paraview:" \
&&   echo "      variants: '@5.9.1 +osmesa+python3'" \
&&   echo "      version:" \
&&   echo "      - 5.9.1" \
&&   echo "    doxygen:" \
&&   echo "      version:" \
&&   echo "      - 1.8.17" \
&&   echo "    fenics:" \
&&   echo "      variants: +mpi+scotch+petsc ~hdf5~openmp~parmetisx~petsc4py~slepc~slepc4py~suite-sparse~trilinos" \
&&   echo "  specs:" \
&&   echo "  - fenics" \
&&   echo "  - paraview" \
&&   echo "  concretization: together" \
&&   echo "  config:" \
&&   echo "    install_tree: /opt/software" \
&&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

# Install the software, remove unnecessary deps
RUN  cd /opt/spack-environment && spack env activate . && export SPACKMON_USER=$(cat /run/secrets/su) && export SPACKMON_TOKEN=$(cat /run/secrets/st) && spack install --fail-fast && spack gc -y

# Strip all the binaries
RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
    xargs file -i | \
    grep 'charset=binary' | \
    grep 'x-executable\|x-archive\|x-sharedlib' | \
    awk -F: '{print $1}' | xargs strip -s

# Modifications to the environment that are necessary to run
RUN cd /opt/spack-environment && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh


# Bare OS image to run the installed executables
FROM ubuntu:18.04

COPY --from=builder /opt/spack-environment /opt/spack-environment
COPY --from=builder /opt/software /opt/software
COPY --from=builder /opt/view /opt/view
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

RUN apt-get -yqq update && apt-get -yqq upgrade \
 && apt-get -yqq install libgfortran4 g++ \
 && rm -rf /var/lib/apt/lists/*

# link python interpreter
RUN find /opt/software -path "/opt/software/linux-*/*/python-3.*/bin/python*" -type l -print0 \ 
  | xargs -0i -n 1 ln -fvs '{}' /opt/view/bin
COPY data /exp/data
COPY run.py pipeline.py /exp/
# work in root directory 
WORKDIR /exp


ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
