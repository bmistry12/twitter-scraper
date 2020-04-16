#!/bin/bash
# export LOG_PATH=~/opt/twitter/log
export LOG_PATH=./logs
KEYWORDS=$1
OUTPUT_FILE=$2
OUTPUT_CSV=$3

echo '=========================== Check Python Version ==========================='
python --version
pip --version

echo '=========================== Make Log Files ==========================='
mkdir ${LOG_PATH}
touch "$LOG_PATH/hist_twitter_data.log"
touch "${LOG_PATH}/json_analysis.log"
touch "${LOG_PATH}/credentials.log"

echo '=========================== Run Credentials.Py ==========================='
python credentials.py 2>&1 | tee "${LOG_PATH}/credentials.log"

echo '=========================== Run Historic Data Analysis ==========================='
python historic_twitter_data.py "${KEYWORDS}" "${OUTPUT_FILE}" 2>&1 | tee "$LOG_PATH/hist_twitter_data.log"
echo ${KEYWORDS}
echo ${OUTPUT_FILE}
JSON_FILE="${OUTPUT_FILE}.json"
echo $JSON_FILE
if [ -f ${JSON_FILE} ]; then
    echo "File exists"
    echo ${OUTPUT_FILE}
    python json_analysis.py ${JSON_FILE} ${OUTPUT_CSV} 2>&1 "${LOG_PATH}/json_analysis.log"
fi

set -e