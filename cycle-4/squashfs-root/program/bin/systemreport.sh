#! /bin/sh
#this shell is used in ALL-device

INFODIR=/tmp/mware/info
LOGDIR=/tmp/mware/log
COMMONLOG=$INFODIR/diagnosesinfo.log
configname="config.tgz"

rm -rf $INFODIR/
rm -rf /tmp/log.tgz
rm -rf /tmp/*config.tgz /tmp/config_a.*
rm -rf /tmp/ipcsystemreport.tgz
rm -rf /tmp/config_all.tgz

#---------- proc core file -------
exec_get_core()
{
	echo "find in $1"
	for corenewfilename in `ls ${1}core-*`
	do			
		if [ -z "$corefilename" ]; then
			corefilename=${corenewfilename}
		else
			if [ "$corenewfilename" -ot "$corefilename" ]; then
				corefilename="$corenewfilename"
			fi
		fi
	done
}

exec_core_proc()
{
	echo "[1]Try to find core file!"
	coredir="/tmp/mmcblk0p1/"
	if [ -e ${coredir} ]; then
		corebakfilename=$(find ${coredir}* -name "corefile-*" -print0)
		
		exec_get_core "/tmp/mmcblk0p1/"
		
		if [ -z "$corefilename" ]; then
			corefilename=${corebakfilename}
		fi
	fi
	
	if [ -z "$corefilename" ]; then 
		coredir="/tmp/"
		exec_get_core "/tmp/"
	fi	

	if [ -n "$corefilename" ]; then
		echo "[2]core file found:$corefilename"
		cd ${coredir}
		corefilename=${corefilename#${coredir}}
		if [ "$2" == "-c" ]; then
			echo "[3]trans from: `pwd` to $1"
			tftp -pl $corefilename $1 -b 8192
			if [ $? -ne 0 ]; then
				echo "trans $corefilename to $1 failed"
				echo "exit systemreport.sh"
				exit 
			fi
		fi
		echo "[4]delete core file"
		rm -rf $corefilename
	else 
	    echo "[2]no core file found!"
	fi
}

exec_cmd()
{
	if [ ! -f $COMMONLOG ]; then
		mkdir -p $INFODIR
		touch $COMMONLOG
	fi

	echo "$1" >> $COMMONLOG
	`$1 >> $COMMONLOG 2>>$COMMONLOG`
	echo >> $COMMONLOG
	echo "=========================================" >> $COMMONLOG
}

qry_proc()
{
	if [ ! -f $COMMONLOG ]; then
		mkdir -p $INFODIR
		touch $COMMONLOG
	fi
	
	echo "[+] collect for process $1" >> $COMMONLOG
 	echo "[-] pidof $1 $(pidof $1)" >> $COMMONLOG
	for pid in $(pidof $1) ; do
  		echo "[-] current stack of ${pid}" >> $COMMONLOG
    	#pstack ${pid} >> $COMMONLOG 2>>$COMMONLOG
    	echo "[-] proc info for ${pid}" >> $COMMONLOG
    	ls -ald /proc/${pid} >> $COMMONLOG 2>>$COMMONLOG
    	cat /proc/${pid}/wchan >> $COMMONLOG
  	done
	echo >> $COMMONLOG
	echo "=========================================" >> $COMMONLOG
}

mkdir -p $INFODIR
mkdir -p $INFODIR/proc
#---------- with param "-c" try to collect core file  -------
if [ -n "$2" -a "$2" == "-c" ] || [ -n "$2" -a "$2" == "-dc" ]; then
	echo "==========proc core file =========="
	exec_core_proc "$1" "$2"
else 
	corefilename=$(find /tmp/* -name "core-*" -print0)
		
	if [ -n "$corefilename" ]; then
		if [ -n "$1" -a "$1" == "-i" ] || [ -n "$1" -a "$1" == "collectkeyinfo" ]; then
			echo find coredumpfile:$corefilename >> $COMMONLOG 2>>$COMMONLOG
			echo "=========================================" >> $COMMONLOG
		else
			echo "find core file:  
		please use  systemreport.sh xxx.xxx.xxx.xxx -c to down core file 
		or     use  systemreport.sh xxx.xxx.xxx.xxx -dc to delete core file "
		exit 1
		fi
	fi	
fi


echo "=======IPC diagnosis info collect========"
#---------- collect time and software version  -------
exec_cmd "date"
exec_cmd "update -v"

#---------- collect interrupts info  -------
exec_cmd "cat /proc/interrupts"
sleep 1
exec_cmd "cat /proc/interrupts"

#---------- collect system info  -------
exec_cmd "uname -a"
exec_cmd "uptime"
exec_cmd "cat /proc/loadavg"
exec_cmd "cat /proc/cmdline"
exec_cmd "cat /proc/cpuinfo"
exec_cmd "ls -l /proc/"
exec_cmd "cat /proc/*/wchan"
exec_cmd "sysctl -a"
exec_cmd "lsmod"
exec_cmd "cat /proc/modules"

#---------- collect driver info  -------
exec_cmd "cat /proc/driver/gpiodev_info"
exec_cmd "manuinfotool"
exec_cmd "cat /proc/driver/jed_motor" 
exec_cmd "cat /proc/devices"
exec_cmd "mpstat"
exec_cmd "cat /proc/driver/runtime"
exec_cmd "cat /sys/class/hwmon/hwmon0/device/temp1_input"

#---------- collect network info -------
exec_cmd "ip link show"
exec_cmd "ifconfig -a"
exec_cmd "mii_tool"
exec_cmd "mii_tool -p 1"
exec_cmd "mii_tool -p 2"
exec_cmd "route -n"
exec_cmd "netstat -an"
exec_cmd "arp -an"
exec_cmd "cat /proc/net/tcp"
exec_cmd "cat /proc/net/udp"
exec_cmd "cat /proc/net/snmp"

#---------- collect ps info ------------
exec_cmd "ps"
exec_cmd "ps -T"
exec_cmd "ls -al /proc/*/fd/*"

#---------- collect syslog info --------
exec_cmd "ls -al /var/log/"
echo lensinfo > /proc/driver/motor
echo "=================dmesg===================" >> $COMMONLOG
date >> $COMMONLOG
uptime >> $COMMONLOG
dmesg | tail -n 500 >>  $COMMONLOG
echo "=========================================" >> $COMMONLOG

#---------- collect disks info ---------
exec_cmd "df -h"
exec_cmd "du -h /config/*"
exec_cmd "fdisk -l"
exec_cmd "cat /proc/partitions"
exec_cmd "cat /proc/scsi/scsi"
exec_cmd "cat /proc/mounts"
exec_cmd "ls /dev/"
exec_cmd "cat /sys/block/mmcblk0/device/cid"
exec_cmd "cat /sys/block/mmcblk1/device/cid"

#---------- collect memory info --------
exec_cmd "cat /proc/meminfo"
exec_cmd "cat /proc/slabinfo"
exec_cmd "cat /proc/buddyinfo"
exec_cmd "cat /proc/media-mem"
exec_cmd "free" 

#---------- collect iscsi info ------
exec_cmd "iscsiadm -m node"
exec_cmd "iscsiadm -m session -P 3"
exec_cmd "iscsiadm -m session --info"

#---------- collect proc info ------
qry_proc "daemon"
qry_proc "img"
qry_proc "updateserver"
qry_proc "mwareserver"
qry_proc "iwareserver"

#---------- collect config info  -------
exec_cmd "ls -al /config/"
exec_cmd "cat /config/localtime"
exec_cmd "cat /config/reboot_cnt"
exec_cmd "cat /config/updatestatus"

#---------- collect IPC CDS version -----
echo "CDS Version Info" >> $COMMONLOG
echo `strings /program/bin/mwareserver | grep "Libcds"` >> $COMMONLOG
echo "=========================================" >> $COMMONLOG

#-----------with pararm "collectkeyinfo" try to collect last keyinfo----
if [ $1 = "collectkeyinfo" ]; then
	echo "Begin collectkeyinfo!"
	cd /var/log/
	rm keyinfo.log 1>/dev/null 2>&1
	echo -ne "#########################MW_MWARE00.log:\n" >> keyinfo.log
	tail /var/log/MW_MWARE00.log -n 400 >> keyinfo.log
	echo -ne "\n\n#########################MW_MWARE00.error:\n" >> keyinfo.log
	tail /var/log/MW_MWARE00.error -n 50 >> keyinfo.log
	echo -ne "\n\n#########################MW_DRV00.log:\n" >> keyinfo.log
	tail /var/log/MW_DRV00.log -n 200 >> keyinfo.log
	echo -ne "\n\n#########################diagnosesinfo.log:\n" >> keyinfo.log
	cat $COMMONLOG >> keyinfo.log
	echo "End collectkeyinfo!"
	exit 0
fi

#-----------ready to pack file--------         
cp `find /var/log/* -type f -size +1c -maxdepth 0 |grep -v ".jpg"` $INFODIR/ -rf
cp /dev/logmpp $INFODIR/ -rf 
cp /proc/umap/* $INFODIR/proc -rf
cp /proc/mi_modules/mi_divp/mi_divp0 $INFODIR/proc -rf
cp /proc/mi_modules/mi_rgn/mi_rgn0 $INFODIR/proc -rf
cp /proc/mi_modules/mi_sensor/mi_sensor0 $INFODIR/proc -rf
cp /proc/mi_modules/mi_sys_mma/mma_heap_name0 $INFODIR/proc -rf
cp /proc/mi_modules/mi_venc/mi_venc0 $INFODIR/proc -rf
cp /proc/mi_modules/mi_venc/mi_venc1 $INFODIR/proc -rf
cp /proc/mi_modules/mi_vif/mi_vif0 $INFODIR/proc -rf
cp /proc/mi_modules/mi_vpe/mi_vpe0 $INFODIR/proc -rf
cp `ls /config/flashlog/* | grep -v log.tgz` $INFODIR/ -rf
cp ~/.ash_history $INFODIR/history_cmd.log 1>/dev/null 2>&1
cp /config/3dcover /config/3DCover /config/PTPreset /config/FPreset /config/ZPreset /config/PresetPosition $INFODIR/ -f 1>/dev/null 2>&1
cp -rf /calibration/lens* /config/lens.dat /calibration/KeyPoint.txt $INFODIR/ 1>/dev/null 2>&1
cp /tmp/*.log /tmp/puma* /tmp/stateofmware /tmp/tempctrl $INFODIR/ -f 1>/dev/null 2>&1

if [ ! -f $LOGDIR ]; then
	mkdir -p $LOGDIR
fi

#================tar===============
#�����Ҫ���Ĵ˴�����ļ������֣������ͬ���޸Ĵ���
#---------------tar log.tgz--------
tar czvf $LOGDIR/log.tgz $INFODIR/* 1>/dev/null 2>&1
rm -rf $INFODIR/

#---------tar config.tgz------
cd $LOGDIR >/dev/null 
cp /config/config_a.xml /config/config_a.chk  ./ -f 
customercode=`cat /config/manuinfo.xml |grep "CustomerCode" | sed "s/[^>]*>\\([0-9 ]*\\)<.*/\\1/g"`
ipaddr=`ifconfig | grep "eth0" -A 2|grep "inet addr"|sed "s/[^:]*:\\([0-9.]*\\).*/\\1/g"`
devicename=`cat /config/manuinfo.xml |grep "DeviceName" | sed "s/[^>]*>\\([^<]*\\)<.*/\\1/g"`
if [ $customercode == "00" -o $customercode == "08" -o $customercode == "09" ];then
	configname=${devicename}"_"${ipaddr}"_config.tgz"
else
	configname="config.tgz"
fi
echo $configname
tar czvf $LOGDIR/$configname config_a.xml config_a.chk   1>/dev/null 2>&1
rm -rf config_a.* 
cd - >/dev/null

#---------tar config_all.tgz------
tar czvf $LOGDIR/config_all.tgz /config 1>/dev/null 2>&1

#--------tar ipcsystemreport.tgz-------
cp $LOGDIR/* /tmp/
rm -f $LOGDIR/$configname $LOGDIR/log.tgz $LOGDIR/config_all.tgz
tar czvf /tmp/ipcsystemreport.tgz /tmp/config_all.tgz /tmp/$configname /tmp/log.tgz 1>/dev/null 2>&1

echo "ipc diagnosis info collect completely"

#============ download tgz file =========
#sh systemreport.sh -i���ֵ������Ϊ����ڲ����ã����������ɾ�����ɵ���ʱ�ļ���
if [ -n "$1" -a $1 != "-i" ]; then
	cd /tmp;echo current dir: `pwd`
	tftp -pl ipcsystemreport.tgz $1 -b 8192
	echo "rm all packlog"
	rm -rf /tmp/log.tgz
	rm -rf /tmp/$configname
	rm -rf /tmp/config_all.tgz
	rm -rf /tmp/ipcsystemreport.tgz
fi
