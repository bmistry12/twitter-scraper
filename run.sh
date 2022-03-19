#!/bin/bash
set -eu

KEYWORDS=$1
NUM_OF_TWEETS=${2-1000}
OUTPUT_FILE=${3-tweets}
OUTPUT_CSV=${4-analysis}

echo '=========================== Check OS & Python Version ==========================='
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     OS="Linux" PYTHON_CMD="python3" LOG_PATH="/tmp/twitter-scraper/logs";;
    Darwin*)    OS="Mac" PYTHON_CMD="python" LOG_PATH="./logs";;
    CYGWIN*)    OS="Windows" PYTHON_CMD="python" LOG_PATH="./logs";;
    MINGW*)     OS="Windows" PYTHON_CMD="py" LOG_PATH="./logs";;
    *)          OS"UNKNOWN:${unameOut}" PYTHON_CMD="python" LOG_PATH="./logs";;
esac

export LOG_PATH

${PYTHON_CMD} --version
pip --version

echo '=========================== Install Requirements ==========================='
pip install -r requirements.txt

echo '=========================== Make Log Files ==========================='
mkdir -p ${LOG_PATH}
touch "$LOG_PATH/hist_twitter_data.log" "${LOG_PATH}/json_analysis.log" "${LOG_PATH}/credentials.log"

echo '=========================== Run Credentials.Py ==========================='
${PYTHON_CMD} credentials.py 2>&1 | tee "${LOG_PATH}/credentials.log"

echo '=========================== Run Historic Data Analysis ==========================='
${PYTHON_CMD} historic_twitter_data.py "${KEYWORDS}" "${NUM_OF_TWEETS}" "${OUTPUT_FILE}" 2>&1 | tee "$LOG_PATH/hist_twitter_data.log"
JSON_FILE="${OUTPUT_FILE}.json"
if [ -f ${JSON_FILE} ]; then
    echo "Output File ${JSON_FILE} Exists"
    ${PYTHON_CMD} json_analysis.py ${JSON_FILE} "${OUTPUT_CSV}.csv" "${LOG_PATH}/json_analysis.log"
fi

echo '=========================== Map It Out ==========================='
if [ -f "${OUTPUT_CSV}.csv" ]; then
    echo "Running Mapper..."
    echo "This might take a while...go make yourself a tea..."
    ${PYTHON_CMD} mapper.py "${OUTPUT_CSV}.csv"
fi

echo "My job here is done."
