#!/bin/bash
TOKEN=$(sh ./sstv-request-token.sh)
#enter SSTV Server here
SERVER=dap
#enter your sstv login site here
SITE=viewstvn

#normal operation is top line enabled, enable the lower line to overwrite the top
#purpose of lower line is to make all channels appear to TVH as running to enable services to be created for normally silent channels
CHANNEL=$1
#CHANNEL=01

#Check if a quality value was sent, else default to 1
if [ -z "$2" ]
then
    VARQUALITY=1
else
    VARQUALITY=$2
fi

#Assign that value to channels 1-60 only, rest receive 1
if [ "$CHANNEL" -le 60 ]
then
	QUALITY="$VARQUALITY"
	echo "$QUALITY"
else
	QUALITY=1
fi

URL=https://"$SERVER".smoothstreams.tv:443/"$SITE"/ch"$CHANNEL"q"$QUALITY".stream/playlist.m3u8?wmsAuthSign="$TOKEN"==

ffmpeg -i $URL -codec copy -loglevel error -f mpegts pipe:1
