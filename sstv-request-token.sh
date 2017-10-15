#!/bin/sh
#enter your sstv login site here
SITE=viewstvn
USERNAME=johnsmith
PASSWORD=mypassword
curl --silent -X "GET" "http://auth.smoothstreams.tv/hash_api.php?username="$USERNAME"&password="$PASSWORD"&site="$SITE"" | jq -r .hash
