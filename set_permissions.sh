#!/bin/bash

#This script sets permissions in a few directories 
#that have been giving us trouble.

source project_env.sh
chmod 774 -R "$USER_DIR"

for a in "$ASSETS_DIR"/*
do
    chmod 774 -R "$a"/geo/abcFiles
done