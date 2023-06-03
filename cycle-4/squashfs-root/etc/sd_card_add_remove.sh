#!/bin/sh

if [ -z $ACTION ];then
   ACTION=add
fi

if [ $ACTION = "remove" ];then
   sync

   umount /mnt/sdcard
   rm /mnt/sdcard -rf

else   
   MNT=$(/bin/mount | grep "mmcblk0")

   if [ -e /dev/mmcblk0 -a "$MNT" = "" ];then
       
       if [ ! -e "/tmp/fsckrecord0.log" -a -e /dev/mmcblk0p1 ];then
           fsck.fat -p  /dev/mmcblk0p1 60 >> /tmp/fsckrecord0.log
           FSCK_RESULT=$?
           echo "=== mmcblk0p1 $FSCK_RESULT ===" >> /tmp/fsckrecord0.log
       fi
       
       mkdir -p /mnt/sdcard
       /bin/mount -tvfat -o umask=077 /dev/mmcblk0p1 /mnt/sdcard
       if [ $? -ne 0 ];then      
           /bin/mount -tvfat /dev/mmcblk0 /mnt/sdcard
       fi
       
    fi

fi
