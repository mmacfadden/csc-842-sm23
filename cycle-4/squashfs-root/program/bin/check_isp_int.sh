#!/bin/sh

isp_int_info=`cat /proc/interrupts|grep isp`
if [ -z "$isp_int_info" ];then
    isp_int_info=`cat /proc/interrupts|grep ISP`
fi

cpu_num=`cat /proc/interrupts | awk '(NR == 1){print NF}'` 
echo -e $cpu_num"\n${isp_int_info}" | awk '                     
BEGIN {ok=0}
{
    if (1 == NR)
    {
        num=$1
    }
    else
    {
        #print "num:"num
        for(i=0;i<num;i++)
        {
            n=i+2;
            #print "i:"i
            if ($n>0)
            {
                print "sensor["i"] int ok"
			    # Ŀǰֻ��һ��sensor������ֻҪ��һ��sensor���жϾ���Ϊok����Ŀ�豸������Ҫ�޸�
				ok=1
            }
        }
    }
}
END {print "isp int status: ["ok"]"}
'
