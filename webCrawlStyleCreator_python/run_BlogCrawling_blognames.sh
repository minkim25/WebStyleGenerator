#!/bin/bash
#
# 2019.11.22
# Donggu, Lee
#######################################################################

# Constant
readonly HOME_PATH='.'
readonly PATH_TO_FILES=$HOME_PATH
readonly LOCK_PATH=${HOME_PATH}/lock
SCRIPT_FILE_NAME='BlogCrawling_blognames.py'
PATH_TO_SCRIPT=$PATH_TO_FILES$SCRIPT_FILE_NAME

TUMBLR_SDDES_FILE_NAME='candidates.csv'
TUMBLR_SEEDS_PATH=$HOME_PATH/tumblrBlogList
TUMBLR_SEEDS_FILE_PATH=$TUMBLR_SEEDS_PATH/$TUMBLR_SDDES_FILE_NAME

DEFAULT_COUNT=5
LAYER_COUNT=2

TUMBLR_BLOG='tumblr'
WEBSITE='website'

TARGET_CRAWLING=$TUMBLR_BLOG
THREAD_COUNT=$DEFAULT_COUNT

FILE_NAME=`basename $0`
LOCKFILE=${LOCK_PATH}/lock.${FILE_NAME}.$$

listInput=""

function lock(){
    touch ${LOCKFILE}
    if [ ! -f ${LOCKFILE} ]; then
        echo "Unable to create lockfile ${LOCKFILE}!"
        exit 1
    fi
        echo "Created lockfile ${LOCKFILE}"
}

function unlock(){
    # Check for an existing lock file
    while [ -f ${LOCK_PATH}/lock.${FILE_NAME}* ]
    do
        # A lock file is present
        if [[ `find ${LOCK_PATH}/.* > "0"` ]]; then
            echo "WARNING: found and removing old lock file...`ls ${LOCK_PATH}/lock.${FILE_NAME}*`"
            rm -f ${LOCK_PATH}/lock.${FILE_NAME}*
        else
            echo "A recent lock file already exists : `ls ${LOCK_PATH}/lock.${FILE_NAME}*`"
        fi
            sleep 5
    done
}

function cleanup_lock(){
    echo "Cleaning up... "
    rm -f ${LOCKFILE}
    if [ -f ${LOCKFILE} ]; then
        echo "Unable to delete lockfile ${LOCKFILE}!"
        exit 1
    fi
        echo "Lock file ${LOCKFILE} removed."
}

# Tumblr blog seed(name)
function make_parameter()
{
    temp=""
    PID_TEST=$$

    # Get a tumblr blog name(seed) 
    while IFS='' read -r blognames
    do
        if [ "$temp" == "" ]; then
            temp="$blognames;$LAYER_COUNT"
        else
            temp="$temp $blognames;$LAYER_COUNT"
        fi
    done < "$TUMBLR_SEEDS_FILE_PATH"
    
    listInput=$temp
    echo $listInput
}



#################################################################################
# Main
#################################################################################

# Check if command line argument is empty or not present
if [ "$1" == "" ]; then
        echo "[Error] Please check inputs"
        echo "Ex) ./run_blog_crawling.sh [Thread Count] [Layer Count]"
        echo "Ex) ./run_blog_crawling.sh 5 2"
        exit 0        
elif [ "$2" = "" ]; then
        echo "[Error]"
else
        echo "THIS IS THE VALID BLOCK"
        THREAD_COUNT=$1
        LAYER_COUNT=$2
        echo "The number of Threads: $THREAD_COUNT, The number of layers: $LAYER_COUNT"
fi


start=`date +%s`

# Create a lock
lock

echo "$THREAD_COUNT"
echo "$LOCKFILE"

# Get a tumblr blog name(seed) 
make_parameter 

# # Release a lock
cleanup_lock

# Release a lock
unlock

# Run
parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $listInput

# export IFS=" "
# for word in $listInput; do
#     echo $word
#   parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $word
# done

end=`date +%s`
runtime=$((end-start))

echo "***************************"
echo "Start Time : $start"
echo "End Time : $end"
echo "Run time : $runtime"
echo "***************************"

if [ $? -eq 0 ]
then
  echo "Successfully executed script"
else
  echo "Script exited with error."
fi

exit