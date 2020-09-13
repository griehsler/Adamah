# How to set up adamah watcher as scheduled job on a QNAP NAS #
## Prerequisites ##
QPKG [Python3](https://download.qnap.com/QPKG/Python3_3.5.0.2b_arm-x19.zip) must be installed
## Installation ##
1. Have adaham watcher copied and configured as documented
2. Create a fake qpkg to have a persistent place for scheduled scripts, e.g.:
```bash
mkdir /share/MD0_Data/.qpkg/custom
```
*This is necessary because all folders on the system drive except for `.qpkg` will be reset upon system reboot.* 

3. Copy the script `send_adamah_notifications.sh` into there, adjust the location of adamha watcher in line #4.
4. Make the script executable
``` bash
chmod +x /share/MD0_DATA/.qpkg/custom/send_adamah_notifications.sh
```
5. add a cron job *(in this example for every day 7:00)*
``` bash
echo "0 7 * * * /share/MD0_DATA/.qpkg/custom/send_adamah_notifications.sh" >> /etc/config/crontab
```
6. restart cron.d
``` bash
crontab /etc/config/crontab && /etc/init.d/crond.sh restart
```