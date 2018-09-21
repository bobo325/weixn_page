#!/bin/bash

to_nginx="tmp2nginx"
data_folder="${WORKSPACE}/project_root"
to_mysql="tmp2mysql"

cp ./config $data_folder/$to_nginx -rf
cp ./const $data_folder/$to_nginx -rf
cp ./db $data_folder/$to_nginx -rf
cp ./flask_app $data_folder/$to_nginx -rf
cp ./intercept $data_folder/$to_nginx -rf
cp ./logs $data_folder/$to_nginx -rf
cp ./model $data_folder/$to_nginx -rf
cp ./route $data_folder/$to_nginx -rf
cp ./service $data_folder/$to_nginx -rf
cp ./sql $data_folder/$to_nginx -rf
cp ./static_file $data_folder/$to_nginx  -rf
cp ./test $data_folder/$to_nginx -rf
cp ./util $data_folder/$to_nginx -rf
cp ./requirements.txt $data_folder/$to_nginx -rf
cp ./run.py $data_folder/$to_nginx -rf
cp ./table.py $data_folder/$to_nginx -rf

mkdir -p $data_folder"/$to_nginx/www/"
cp ./sql/* $data_folder/$to_mysql/docker-entrypoint-initdb.d/ -rf

rm -f $data_folder/$to_nginx"/make.sh"
