# Repair problems with rtl8187 and rfkill in BT5 / BT5r1

prepare-kernel-sources
cd /usr/src/linux/drivers/net/wireless/rtl818x/rtl8187/
wget http://backtrack-linux.org/silly-rfkill-patch.patch
patch -p0 < silly-rfkill-patch.patch
rm silly-rfkill-patch.patch
cd /usr/src/linux
make drivers/net/wireless/rtl818x/rtl8187/rtl8187.ko
cp drivers/net/wireless/rtl818x/rtl8187/rtl8187.ko /lib/modules/$(uname -r)/kernel/drivers/net/wireless/rtl818x/rtl8187/rtl8187.ko
reboot
