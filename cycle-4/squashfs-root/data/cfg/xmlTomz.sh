#! /ext/bin/
[ "$#" -lt 1 ] && echo "Plz enter sensor name." && exit 0
echo "Sensor name : ${1}"
makeNewXml_Bin -x ${1}".xml"
armMZ -l8 c ${1}".bin" ${1}".bin.mz"