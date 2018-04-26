#!/bin/bash
### the script's use to run rsync with retrying when raise errors and up to a maximum number of tries.

trap ctrl_c INT
# trap "echo Exited!; exit;" SIGINT SIGTERM SIGHUP
function ctrl_c() {
    echo "** Trapped CTRL-C"
}


MAX_RETRIES=3
i=0
TIMEOUT=120

# Set the initial return value to failure
false

while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]
do
    i=$(($i+1))
    rsync -vazCog --chown=$1:$2 --exclude=".*" $3 $4
    if [ "$?" = "0" ] ; then
        echo "rsync completed normally"
        exit
    else
        echo "rsync failure. Retrying after $TIMEOUT"
        sleep $TIMEOUT
    fi
done

if [ $i -eq $MAX_RETRIES ]
then
  echo "Hit maximum number of retries, giving up."
fi