#!/bin/bash

function run_all {
    run_service && \
    sleep 10 && \
    run_scrap && \
    run_check && \
    run_ui
}

function run_service {
    docker compose up -d
}

function run_scrap {
    python indeed-scrapper/app.py
}

function run_check {
    python qualification-check/app.py
}

function run_ui {
    cd ui
    npm start
}

if [ -z "$1" ]
then
    run_all
else
    case $1 in
        service)
            run_service
            ;;
        scrap)
            run_scrap
            ;;
        check)
            run_check
            ;;
        ui)
            run_ui
            ;;
        *)
            echo "Invalid argument. Please use one of the following: service, scrap, check, ui"
            ;;
    esac
fi