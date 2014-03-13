#!/bin/sh

#This script sets permissions in a few directories 
#that have been giving us trouble.

DIR=`dirname $0`
source ${DIR}/project_env.sh
chmod 774 -R "$USER_DIR"

for a in "$ASSETS_DIR"/*
do
    chmod 774 -R "$a"/geo/abcFiles
done
echo "FINISHED"