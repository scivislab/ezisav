#give the container id as a second argument to this script
pushd /home/docker/threshold/
time mpiexec --allow-run-as-root -n 8 ./turbulence_master.Linux