#!/usr/bin/env bash

GREEN="\033[0;32m"
RED="\033[0;31m"
NO_COLOR="\033[0m"

colored_print(){
    echo -e "$1 $2 $NO_COLOR"
}

colored_print ${GREEN} "STEP 1: Pull changes from origin [default master]"

eval $(ssh-agent -s)
colored_print ${GREEN} "STEP 1.1: Check if repository exists"
if [ -d "7_trinhvt" ]; then
    colored_print ${GREEN} "STEP 1.1.1: Repository found in $(pwd)/7_trinhvt"
    cd 7_trinhvt
    git pull origin origin/danghh_6
    git checkout danghh_6
else
    colored_print ${RED} "STEP 1.1.1: Not found"
    git clone git@gitlab.com:is_soict/it4434_20192/7_trinhvt.git
    cd 7_trinhvt
fi

source ~/7_trinhvt/script/aio.sh
