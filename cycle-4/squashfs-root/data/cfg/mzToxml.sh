#! /ext/bin/
[ "$#" -lt 1 ] && echo "Plz enter sensor name." && exit 0
echo "Sensor name : ${1}"
armMZ -l8 d ${1}".bin.mz" ${1}".bin"
armMZ -l8 d isp_dbg_buf.xml.mz isp_dbg_buf.xml
makeBINxml_NewXML -x isp_dbg_buf.xml -b ${1}".bin"
