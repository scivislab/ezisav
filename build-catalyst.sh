#!/bin/bash
cd base
docker build -t deivac/base -f Dockerfile.base .
cd ../paraview
docker build -t deivac/paraview -f Dockerfile.paraview .
cd ../dolfin
docker build -t deivac/dolfin -f Dockerfile.dolfin .
cd ../catalyst
docker build -t deivac/catalyst -f Dockerfile.catalyst .
docker run -p 11111:11111 deivac/catalyst
# connect via Paraview localhost:11111, start the catalyst connection and execute one of the start scripts in the container