#!/bin/bash
cd base
docker build -t deivac/base -f Dockerfile.base .
cd ../paraview
 docker build -t deivac/paraview:5.6 -f Dockerfile.paraview --build-arg PV_VERSION=5.6.0 . 
 cd ../vpic
docker build -t deivac/vpic -f Dockerfile.vpic .
cd ../vpic_catalyst
docker build -t deivac/vpic_catalyst -f Dockerfile.vpic_catalyst .
docker run -it -p 11111:11111 deivac/vpic_catalyst
# connect via Paraview localhost:11111, start the catalyst connection and execute one of the start scripts in the container