#!/bin/bash

#!/bin/bash

#SBATCH -A p2011084
#SBATCH -p core
#SBATCH -n 1
#SBATCH -t 10:00:00
#SBATCH -J rdist_profile_analysis

SAMPLES_DIR="/home/muneeb/sdist_pref/mem_stride_samples/"
ANALYSIS_TOOL_DIR="/home/muneeb/workspace/uart/analysis_orig/"

WORKING_DIR=$(pwd)

cd ${ANALYSIS_TOOL_DIR}

export PYTHONPATH=/home/muneeb/workspace/uart/python/

benchmark=${1}-${2}
    
count=0

OUTFILE=${WORKING_DIR}/${benchmark}.mem-sdist.data

rm -rf ${OUTFILE}

BENCH_SAMPLE_DIR=${SAMPLES_DIR}${1}-cwrapp-bin-${2}"/"

#BENCH_SAMPLE_DIR=${SAMPLES_DIR}${1}-mem-stride-bin-${2}"/"

echo ${BENCH_SAMPLE_DIR}

SAMPLE_FILES=$(ls ${BENCH_SAMPLE_DIR}sample*)
    
total_L1_bound=0
total_L2_bound=0
total_L3_bound=0
total_mem_bound=0

for file in ${SAMPLE_FILES}
do
    
    ./sdistprint.py ${file} > .tmp.${benchmark}
    L1_bound=$(cat .tmp.${benchmark} | grep 'L1' | awk '{print $2}')
    
    if [[ ${L1_bound} == "" ]]
    then
	echo "error processing this file - will be ignored!"$'\n'${file}
	continue
    fi
    
    total_L1_bound=$(echo ${total_L1_bound}"+"${L1_bound} | bc -l)
    
    L2_bound=$(cat .tmp.${benchmark} | grep 'L2' | awk '{print $2}')
    total_L2_bound=$(echo ${total_L2_bound}"+"${L2_bound} | bc -l)

    L3_bound=$(cat .tmp.${benchmark} | grep 'L3' | awk '{print $2}')
    total_L3_bound=$(echo ${total_L3_bound}"+"${L3_bound} | bc -l)
    
    mem_bound=$(cat .tmp.${benchmark} | grep 'Memory' | awk '{print $2}')
    total_mem_bound=$(echo ${total_mem_bound}"+"${mem_bound} | bc -l)
    
    count=$((${count}+1))
    
done

avg_L1_bound=$(echo ${total_L1_bound}"/"${count} | bc -l)
avg_L2_bound=$(echo ${total_L2_bound}"/"${count} | bc -l)
avg_L3_bound=$(echo ${total_L3_bound}"/"${count} | bc -l)
avg_mem_bound=$(echo ${total_mem_bound}"/"${count} | bc -l)

avg_non_L1_bound=$(echo "100.0-"${avg_L1_bound} | bc -l)

norm_L2_bound=$(echo ${avg_L2_bound}"*"${avg_non_L1_bound}"/100" | bc -l)
norm_L3_bound=$(echo ${avg_L3_bound}"*"${avg_non_L1_bound}"/100" | bc -l)
norm_mem_bound=$(echo ${avg_mem_bound}"*"${avg_non_L1_bound}"/100" | bc -l)

printf "%s %.2f %.2f %.2f %.2f \n" "${benchmark}" "${avg_L1_bound}" "${norm_L2_bound}" "${norm_L3_bound}" "${norm_mem_bound}" >> ${OUTFILE}

rm -rf .tmp.${benchmark}

#printf "L1 bound memory accesses %.2f %% of total \n" "${avg_L1_bound}"  >> ${OUTFILE}
#printf "L2 bound memory accesses %.2f %% of %.2f %% \n" "${avg_L2_bound}" "${avg_non_L1_bound}"  >> ${OUTFILE}
#printf "L3 bound memory accesses %.2f %% of %.2f %% \n" "${avg_L3_bound}" "${avg_non_L1_bound}"  >> ${OUTFILE}
#printf "Memory bound memory accesses %.2f %% of %.2f %% \n" "${avg_mem_bound}" "${avg_non_L1_bound}"  >> ${OUTFILE}

