#!/bin/sh

PartitionName="program"
VolumeName="program"
DeviceName="ubi0"
FolderName="/program"
#PRODUCT_TYPE=`zcat /proc/config.gz | grep "CONFIG_UNIVIEW_" | grep "=y" | sed 's/=y//'`
PRODUCT_ID=255
BUILD_INFO="NULL"


#FLASH���ڻ���ʱ��ʹ��manuinfotool���ӡbad block���ֶε��½������󡣹��ڴ��ȵ���
#һ��manuinfotool������/tmp/Ŀ¼������manuinfo�ļ�������manuinfotool���ȷ��ʸ��ļ�
/program/bin/manuinfotool get LENS >/dev/null


kernel_ver=$(uname -r)


#�޵��ӱ�ǩ������ֹ���Զ�����dhcp�ȴ�д����ӱ�ǩ
#check manuinfo
DEVICENAME=`/program/bin/manuinfotool | grep PROTOTYPE_NAME|cut -d : -f 2`
if [ -z "$DEVICENAME" ]; then
      #restart udhcpc & exit
	  echo "-----------------------------------------------------------"
	  echo "----------------begin to start udhcpc----------------------"
	  echo "-----------------------------------------------------------"
	  #�޵��ӱ�ǩʱ ����update ������/tmp/bin ֧�ְ汾����
	  cd /
      mkdir -p /tmp/bin   
      cp -rf /program/bin/update_move /tmp/bin/update
      chmod a+x /tmp/bin/update 
	  
      if [ -r /usr/sbin/nandwrite_move ]; then
          cp -rf /usr/sbin/nandwrite_move /tmp/bin/nandwrite
          chmod a+x /tmp/bin/nandwrite 
      fi
      
      if [ -r /usr/sbin/flashwrite_move ]; then
          cp -rf /usr/sbin/flashwrite_move /tmp/bin/flashwrite
          chmod a+x /tmp/bin/flashwrite 
      fi
	  
      cp -rf /program/bin/reboot.sh  /tmp/bin/reboot.sh
      chmod a+x /tmp/bin/reboot.sh

      cp /program/bin/mwarecmd.sh /tmp/bin/mwarecmd.sh -f
      chmod a+x /tmp/bin/mwarecmd.sh     	
 
      killall -9 udhcpc
      
      udhcpc -s /usr/share/udhcpc/udhcpc.script > /dev/null &
      #exit 1
fi

#����������Ҫ�õ��ӱ�ǩ���
BUILD_INFO=`/program/bin/manuinfotool | grep BUILD_INFO|cut -d : -f 2`
PROTOTYPE_NAME=`/program/bin/manuinfotool | grep PROTOTYPE_NAME|cut -d : -f 2`

if [ -r /lib/modules/$kernel_ver/extra/kmanuparse.ko ]; then
	insmod /lib/modules/$kernel_ver/extra/kmanuparse.ko  pszBuildInfo=$BUILD_INFO pszProductTypeName=$PROTOTYPE_NAME
		case "$?" in
		0)
		UV_BOARD_NAE=$(cat /proc/driver/productname)
		UV_SENSOR_TYPE=$(cat /proc/driver/sensortype)
		;;
		*)
		echo "odporbe kgpio failed!"
		;;
	esac
fi	

if [ -r /lib/modules/$kernel_ver/extra/kgpio.ko ]; then
	insmod /lib/modules/$kernel_ver/extra/kgpio.ko
fi	

motor_load()
{
    # ��ȡ����������λ��
    if [ -r /config/motorpos ];then
        zoompos=`cat /config/motorpos | grep ZOOM | awk -F ':' '{print $2}'`
        focuspos=`cat /config/motorpos | grep FOCUS | awk -F ':' '{print $4}'`
        status=`cat /config/motorpos | grep STATUS | awk -F ':' '{print $6}'`
    else
        zoompos=0xffffffff
        focuspos=0xffffffff
        status=0xffffffff
    fi

    if [ "$zoompos" = "" -o "$focuspos" = "" ];then                       
        zoompos=0xffffffff                                            
        focuspos=0xffffffff                                          
    fi

    # ����������״̬Ϊ�˶�״̬��ɾ��motorpos�ļ���������λ�����AF�����۽�
    if [ "$status" = "1" ];then
        if [ -r /config/motorpos ]; then
            rm /config/motorpos
        fi
        zoompos=0xffffffff
        focuspos=0xffffffff
        status=0xffffffff
    fi

    # ��������: ����ģʽ��, ÿ�����������о�ͷ��ʼ��
    if [ -r /calibration/factory.txt ]; then
        if [ -r /config/motorpos ]; then
            rm /config/motorpos
        fi
        zoompos=0xffffffff
        focuspos=0xffffffff
        status=0xffffffff
    fi

    if [ "$status" = "" ];then
    	status=0
    fi

    if [ "$UV_PRODUCT_NAME" = "11000111" ];then # ���ޱ䱶����,ȡһ�������õ���ֵ11000111, �б䱶��������滻����ֵ
    # �䱶�������kmotorcm.ko
        if [ -r /lib/modules/$kernel_ver/extra/kmotorcm.ko ]; then
            insmod  /lib/modules/$kernel_ver/extra/kmotorcm.ko guiZoomPos=$zoompos guiFocusPos=$focuspos g_uiStatus=$status
        fi
    else
    # �������ޱ䱶�������kmotor.ko
        if [ "$zoompos" = "0xffffffff" -o "$focuspos" = "0xffffffff" ];then                       
            zoompos=0xfffffff
            focuspos=0xfffffff
        fi

        if [ -r /lib/modules/$kernel_ver/extra/kmotor.ko ]; then
            insmod /lib/modules/$kernel_ver/extra/kmotor.ko  glZoomPos=$zoompos glFocusPos=$focuspos
        fi
    fi
}

motor_load;

if [ -r /lib/modules/$kernel_ver/extra/kruntime.ko ]; then
     insmod /lib/modules/$kernel_ver/extra/kruntime.ko
fi

insmod /lib/modules/4.9.84/extra/mdrv_crypto.ko
#kernel_mod_list
insmod /lib/modules/4.9.84/extra/mhal.ko
#misc_mod_list
insmod /lib/modules/4.9.84/extra/mi_common.ko
insmod /lib/modules/4.9.84/extra/mi_sys.ko logBufSize=256 default_config_path='/program/lib/configs'
insmod /lib/modules/4.9.84/extra/mi_sensor.ko
insmod /lib/modules/4.9.84/extra/mi_dma.ko
insmod /lib/modules/4.9.84/extra/mi_rgn.ko
insmod /lib/modules/4.9.84/extra/mi_ao.ko
insmod /lib/modules/4.9.84/extra/mi_ai.ko
insmod /lib/modules/4.9.84/extra/mi_vpe.ko
insmod /lib/modules/4.9.84/extra/mi_shadow.ko
insmod /lib/modules/4.9.84/extra/mi_ldc.ko
insmod /lib/modules/4.9.84/extra/mi_vif.ko
insmod /lib/modules/4.9.84/extra/mi_divp.ko
insmod /lib/modules/4.9.84/extra/mi_disp.ko
insmod /lib/modules/4.9.84/extra/mi_sd.ko
#insmod /lib/modules/4.9.84/extra/mi_alsa.ko
insmod /lib/modules/4.9.84/extra/mi_venc.ko UseAntiTamper=0
insmod /lib/modules/4.9.84/extra/mi_panel.ko
insmod /lib/modules/4.9.84/extra/mi_vdisp.ko
#mi
#misc_mod_list_late
#kernel_mod_list_late
if [ "$UV_SENSOR_TYPE" == "imx274" ]; then
     insmod /lib/modules/4.9.84/extra/imx274_MIPI.ko chmap=1
fi

if [ "$UV_SENSOR_TYPE" == "sc4238" ]; then
     /program/bin/riu_w 0xF 0x7 0x0214
     echo 192000000 > /sys/devices/virtual/mstar/isp0/isp_clk
     insmod /lib/modules/4.9.84/extra/SC4238_MIPI.ko chmap=1 lane_num=4
fi

if [ "$UV_SENSOR_TYPE" == "sc500ai" ]; then
     /program/bin/riu_w 0xF 0x7 0x0214
     echo 192000000 > /sys/devices/virtual/mstar/isp0/isp_clk
     insmod /lib/modules/4.9.84/extra/SC500AI_MIPI.ko chmap=1 lane_num=4
fi

if [ "$UV_SENSOR_TYPE" == "sc8238" ]; then
     insmod /lib/modules/4.9.84/extra/sc8238_MIPI.ko chmap=1
fi

if [ "$UV_SENSOR_TYPE" == "sc5238" ]; then
     /program/bin/riu_w 0xF 0x7 0x0214
     echo 192000000 > /sys/devices/virtual/mstar/isp0/isp_clk
     insmod /lib/modules/4.9.84/extra/SC5238_MIPI.ko chmap=1
fi

if [ "$UV_SENSOR_TYPE" == "os05a20" ]; then
     insmod /lib/modules/4.9.84/extra/os05a20_MIPI.ko chmap=1
fi

echo isproot /program/lib/configs/iqfile > /dev/ispmid
ln /program/lib/configs/iqfile /config/iqfile -s
echo 576000000 > /sys/venc/ven_clock
echo 288000000 > /sys/module/mhal/parameters/drv_scl_module.scl_clock

#echo 3 > /proc/mi_modules/mi_venc/debug_level

sysctl -w net.core.wmem_max=655360
sysctl -w net.core.wmem_default=655360

export LD_LIBRARY_PATH=/program/lib
#property_service
mkdir /dev/socket
touch /dev/.coldboot_done

#����/data�ɶ�д
mkdir /tmp/.data
cp -af /data/* /tmp/.data/
mount --bind /tmp/.data/ /data

/program/bin/property_service &

mkdir /dev/graphics
ln -s /dev/fb0 /dev/graphics/fb0
ln -s /dev/fb1 /dev/graphics/fb1
ln -s /dev/fb2 /dev/graphics/fb2

sleep 5
insert_wifi_ko()
{
    insmod cfg80211.ko
    insmod ath.ko
    insmod ath9k_hw.ko
    insmod ath9k_common.ko
    insmod mac80211.ko
    insmod ath9k_htc.ko
    insmod ath9k.ko
    echo "insmod ko for uipc wifi success"
}
remove_wifi_ko()
{
    rmmod ath9k
    rmmod ath9k_htc
    rmmod mac80211
    rmmod ath9k_common
    rmmod ath9k_hw
    rmmod ath
    rmmod cfg80211
    echo "rmmod ko for uipc wifi success"
}
set_wifi_mac()
{
    MACADDR_STRING=`/program/bin/mactool -wifi`
    #include dos chracter
    MAC_ADDR_COPPER_TEMP=${MACADDR_STRING#*is:}
    #delete dos chracter
    MAC_ADDR_COPPER=`echo $MAC_ADDR_COPPER_TEMP |awk '{print $1}'`
    if [ "MAC_ADDR_COPPER" != "invalid" ]; then
        echo $MAC_ADDR_COPPER >/tmp/softmac
		ifconfig wlan0 hw ether $MAC_ADDR_COPPER
    else
        echo "wifi mac addr is invalid,so use random mac addr"
    fi
}
#gpio ģ����سɹ��󣬼��wifi ģ���Ƿ��н��뵽�豸�ϣ����м���wifiģ��
WIFI_ID=`lsusb |grep 9271|cut -d : -f 3`
if [ "$WIFI_ID" == "9271" ];then    
    echo "i detect wireless dev:AR9271,now insmod kernel modules!" >/dev/console
    cd /program/lib
    insert_wifi_ko
    sleep 3
	set_wifi_mac
    ifconfig wlan0 up
fi

#Run mware.sh
/program/bin/mware_init.sh  &



#ֻ�滻root�û����벿�֣����ⵥPCD54901
if [ -e "/config/passwd" ]; then
    CONF_DIR="/config/passwd"                    
    ETC_DIR="/etc/passwd"                        
    conf_var=`cat ${CONF_DIR} | grep ^root:`
    etc_var=`cat ${ETC_DIR} | grep ^root:`
    conf_temp=`echo $conf_var  | cut -f2 -d':'`
    etc_temp=`echo $etc_var  | cut -f2 -d':'`
    if [ "$conf_temp" != "$etc_temp" ]; then 
        echo "passwd has changed"
        sed -i "s:$etc_temp:$conf_temp:g" ${ETC_DIR}
    fi
fi

/bin/sh
