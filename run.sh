#!/bin/bash

if [ "$1" = "--ingest" ]; then
    cd ./ingestion
    if [ ! -d "raw_data" ]; then
        mkdir raw_data
    fi
    if [ ! -d "stripped_data" ]; then
        mkdir stripped_data
    fi
    if [ ! -d "combined_data" ]; then
        mkdir combined_data
    fi
    python get_data.py
    echo "Data downloaded"
    python strip_data.py
    echo "Data stripped"
    python combine_data.py
    echo "Data combined"
    cd ..
elif [ "$1" = "--install" ]; then
    pip install -r requirements.txt
elif [ "$1" = "--reqs" ]; then
    pip install pipreqs
	pipreqs . --force
fi
