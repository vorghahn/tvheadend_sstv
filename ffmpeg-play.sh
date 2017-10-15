#!/bin/bash
URL=$1
ffmpeg -i $URL -codec copy -loglevel error -f mpegts pipe:1
