#!/bin/bash

GREEN="\033[0;32m"
RED="\033[0;31m"
NO_COLOR="\033[0m"

colored_print(){
    echo -e "$1 $2 $NO_COLOR"
}

colored_print ${GREEN} "STEP 2: Deploy backend"
colored_print ${GREEN} "STEP 2.1: Backup log"
CURRENT_TIME=$(date +%Y-%m-%d__%H_%M_%S)
LOG_FILE=/tmp/project/project.uwsgi.log
[ -f ${LOG_FILE} ] && mv ${LOG_FILE} /tmp/project/project.uwsgi.${CURRENT_TIME}.log

colored_print ${GREEN} "STEP 2.2: Kill uwsgi master process"
MASTER_PROCESS=$(ps aux | grep uwsgi | grep -v grep | awk '{print $2}' | head -n 1)
[ ${MASTER_PROCESS} ] && kill -9 ${MASTER_PROCESS}

colored_print ${GREEN} "STEP 2.3: Install dependencies"
cd backend
/home/deploy/anaconda3/envs/project/bin/pip install -r requirements.txt

colored_print ${GREEN} "STEP 2.4: Create backend server [default 8000]"
/home/deploy/anaconda3/envs/project/bin/python manage.py migrate
/home/deploy/anaconda3/envs/project/bin/uwsgi project.ini
colored_print ${GREEN} "STEP 2.5: Deploy backend successfully"
source ~/.bashrc
source ~/.env
which node
colored_print ${GREEN} "STEP 3: Deploy frontend"
cd ~/7_trinhvt/frontend
colored_print ${GREEN} "STEP 3.1: Install dependencies"
/home/deploy/.nvm/versions/node/v12.16.1/bin/npm install
colored_print ${GREEN} "STEP 3.2: Build resources"
/home/deploy/.nvm/versions/node/v12.16.1/bin/npm run build
rm -rf /var/www/html/project/dist
cp -r dist /var/www/html/project
colored_print ${GREEN} "STEP 3.3: Deploy frontend successfully"
