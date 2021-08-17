#!/bin/bash
cd base
docker build -t deivac/base -f Dockerfile.base .
cd ../ascent
docker build -t deivac/ascent -f Dockerfile.ascent .
cd ../clover
docker build -t deivac/clover -f Dockerfile.clover .
docker run -p 80:80 deivac/clover
# connect to localhost:80 in your browser to see the viewer
