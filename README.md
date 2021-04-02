## Raspberry Pi Bluetooth Keyboard From Phone (Currently Android only) Lite Encryption Version (AES)

 * install raspberry pi lite (headless) on your Raspberry Pi Zero W (currently only supported rpi variant)

 * Using terminal simply login
 * Using SSH? Follow this guide for advice https://yunohost.org/#/security but use flag '-t ed25519' during ssh-keygen for security (if your system supports)
 * (ssh optional) change 'AllowUsers' ssh user to have a new user name and create longer passwords for all users or replace the default pi user
 * (optional firewall) WARNING: if you changed your ssh port it should be opened below
 * (optional firewall) sudo apt install -y ufw && echo "IPV6=no" | sudo tee /etc/ufw/ufw.conf && sudo ufw enable && sudo ufw allow ssh && sudo ufw allow https && sudo ufw allow http && sudo ufw enable
 * WARNING: avoid running the install script twice unless you know what you're doing. If the commands get stuck try manually adding each of the next lines of code until the task is completed.

```shell
bash <(wget -qO- https://raw.githubusercontent.com/a93h/rpizw-bthid-pi-lite/master/install.sh)
````

##### after the install completes please reboot

#### notice if you don't use the correct USB micro to USB cable and plug into the USB port to power and transmit keyboard keys the device may not work properly.
