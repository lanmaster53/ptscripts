ifconfig wlan0 down
rmmod rtl8187
rfkill block all
rfkill unblock all
modprobe rtl8187
rfkill unblock all
ifconfig wlan0 up
