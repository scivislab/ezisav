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
&&   echo "      variants: '@4.1.1 +legacylaunchers+pmi+thread_multiple fabrics=ucx schedulers=slurm'" \
&&   echo "    mesa:" \
&&   echo "      variants: ~glx" \
&&   echo "    ascent:" \
&&   echo "      variants: +mpi+vtk-h+fortran+test+python+serial ~openmp~adios~mfem" \
&&   echo "    conduit:" \
&&   echo "      variants: ~test" \
&&   echo "    vtk-m:" \
&&   echo "      variants: ~openmp" \
&&   echo "    vtk-h:" \
&&   echo "      variants: +mpi" \
&&   echo "  specs:" \
&&   echo "  - ascent" \
&&   echo "  - cloverleaf3d" \
&&   echo "  concretization: together" \
&&   echo "  config:" \
&&   echo "    install_tree: /opt/software" \
&&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

# Install the software, remove unnecessary deps
RUN cd /opt/spack-environment && \
    spack env activate . && \
    spack install --fail-fast && \
    spack gc -y

# Strip all the binaries
RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
    xargs file -i | \
    grep 'charset=binary' | \
    grep 'x-executable\|x-archive\|x-sharedlib' | \
    awk -F: '{print $1}' | xargs strip -s

# Modifications to the environment that are necessary to run
RUN cd /opt/spack-environment && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

# make sure that the cloverleaf binary with ascent support is accessible in PATH
RUN spack env activate -d /opt/spack-environment \
 && ln -s $(spack location -i ascent)/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par /opt/view/bin


# Bare OS image to run the installed executables
FROM ubuntu:18.04

COPY --from=builder /opt/spack-environment /opt/spack-environment
COPY --from=builder /opt/software /opt/software
COPY --from=builder /opt/view /opt/view
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

RUN apt-get -yqq update && apt-get -yqq upgrade \
 && apt-get -yqq install vim less libgfortran4 \
 && rm -rf /var/lib/apt/lists/*


ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
