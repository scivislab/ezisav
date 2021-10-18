#!/bin/bash
cd base
# needs spack version 0.16.1 for vtk-m@ascent_ver
docker build -t ezisav/base:ascent -f Dockerfile.base --build-arg SPACK_VERSION=0.16.1 .
cd ../ascent
docker build -t ezisav/ascent -f Dockerfile.ascent .
cd ../clover
docker build -t ezisav/clover -f Dockerfile.clover .
docker run -p 80:80 ezisav/clover
# connect to localhost:80 in your browser to see the viewer
