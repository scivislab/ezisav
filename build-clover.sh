#!/bin/bash
cd base
# needs spack version 0.16.1 for vtk-m@ascent_ver
docker build -t deivac/base:ascent -f Dockerfile.base --build-arg TAG=0.16.1 .
cd ../ascent
docker build -t deivac/ascent -f Dockerfile.ascent .
cd ../clover
docker build -t deivac/clover -f Dockerfile.clover .
docker run -p 80:80 deivac/clover
# connect to localhost:80 in your browser to see the viewer
