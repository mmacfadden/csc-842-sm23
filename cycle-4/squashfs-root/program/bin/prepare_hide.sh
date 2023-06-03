#kill mware relevant process
killall -9 daemon 1>/dev/null 2>&1
#send 20 to exit hisi mpp
killall -20 mwareserver 1>/dev/null 2>&1
sleep 1
killall -9 mwareserver 1>/dev/null 2>&1
killall -9 maintain 1>/dev/null 2>&1
killall -9 iwareserver 1>/dev/null 2>&1
killall -9 udhcpc_mware 1>/dev/null 2>&1
killall -9 mw_udhcpc_4G 1>/dev/null 2>&1
killall -9 mw_udhcpc_wired 1>/dev/null 2>&1
killall -9 mw_wpas_WiFi 1>/dev/null 2>&1
killall -9 mw_udhcpc_WiFi 1>/dev/null 2>&1
killall -9 mw_wpas_8021x 1>/dev/null 2>&1
killall -9 hostapd 1>/dev/null 2>&1
