#!/bin/bash
#文件名:sleep.sh
count=0
while true;
do
if [ ${count} -lt 40 ];
	then
		count=$((${count}+1));
		sleep 1;
		echo ${count};
else exit 0;
fi
done
