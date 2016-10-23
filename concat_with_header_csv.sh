#!/bin/bash

input_dir=./output
files="${input_dir}/monthly_weather_沖縄県_那覇*.csv"
cat_file="${input_dir}/monthly_weather_沖縄県_那覇_2000-2016.csv"
 
for filepath in ${files}
 
do
  if [ -s ${cat_file} ]; then
    sed -e "1d" ${filepath} >> ${cat_file}
  else
    cat ${filepath} > ${cat_file}
  fi
  rm ${filepath}
done
