#!/bin/bash
cd base
docker build -t ezisav/base -f Dockerfile.base .
cd ../paraview
docker build -t ezisav/paraview -f Dockerfile.paraview .
cd ../dolfin
docker build -t ezisav/dolfin -f Dockerfile.dolfin .
cd ../catalyst
docker build -t ezisav/catalyst -f Dockerfile.catalyst .
docker run -it -p 11111:11111 ezisav/catalyst
# connect via Paraview localhost:11111, start the catalyst connection and execute one of the start scripts in the container