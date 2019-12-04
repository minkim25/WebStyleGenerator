#!/bin/bash
#
# 2019.11.22
# Donggu, Lee
#######################################################################

# Constant
readonly HOME_PATH='.'
readonly PATH_TO_FILES=$HOME_PATH
readonly LOCK_PATH=${HOME_PATH}/lock
SCRIPT_FILE_NAME='BlogCrawling_bloginfo.py'
PATH_TO_SCRIPT=$PATH_TO_FILES$SCRIPT_FILE_NAME

TUMBLR_SDDES_FILE_NAME='blognames.csv'
TUMBLR_SEEDS_PATH=$HOME_PATH/tumblrdata
TUMBLR_SEEDS_FILE_PATH=$TUMBLR_SEEDS_PATH/$TUMBLR_SDDES_FILE_NAME

DEFAULT_COUNT=5
LAYER_COUNT=2
LIMITS_OF_FILE_COUNTS=100

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
    listInput=""
    index=0
    count=0
    file_path=""
    
    yourfilenames=`ls ./tumblrBlogList/output/*.csv`
    for eachfile in $yourfilenames
    do         
        # Get a tumblr blog name(seed) 
        while IFS='' read -r blognames
        do 
            blogname=$(echo $blognames | sed -e "s/ \/ //g")
          
            file_name=$blogname
            
            if [ "$temp" == "" ]; then
                temp="$blognames"
            else
                temp="$temp;$blogname"
            fi
            count=$((count+1))     

        if [ $count -ge $LIMITS_OF_FILE_COUNTS ]; then
            if [ "$listInput" == "" ]; then
                listInput="$temp&$index&$file_name"
                count=0
                temp=""
            else
                listInput="$listInput $temp&$index&$file_name"
                count=0
                temp=""
            fi
        fi             
        index=$((index+1))
        done < "$eachfile"
    done
    
    if [ -z "$temp" ]; then
        echo "temp is empty"
    else
        echo "temp is NOT empty"
        if [ "$listInput" == "" ]; then
            listInput="$temp&$index&$file_name"
            temp=""
            count=0
        else
            listInput="$listInput $temp&$index&$file_name"
            temp=""
            count=0
        fi
    fi         
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
#     parallel --j $THREAD_COUNT python $SCRIPT_FILE_NAME ::: $word
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