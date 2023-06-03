#!/bin/sh

result="fail"

echo "@"

while [ 1 ]
do 
    mw_state=`cat /tmp/stateofmware |grep state|awk -F '[][]' '{print $2}'`
    if [ $mw_state != 1 ]; then
        echo "mware not ready"
        break
    else
        echo "mware ready"
    fi
    
	if [ -x /program/bin/check_isp_int.sh ];then
        isp_state=`sh /program/bin/check_isp_int.sh |grep status|awk -F '[][]' '{print $2}'`
        if [ $isp_state != 1 ]; then
            echo "isp interrupts not ready"
            break
        else
            echo "isp interrupts ready"
        fi
    else
        break
	fi
    
    result="pass"
    break
done

echo ""
echo "test result:"$result
echo "\$\$"