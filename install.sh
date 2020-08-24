sudo apt update
sudo apt upgrade -y
sudo apt install -y bluetooth pi-bluetooth bluez python3-bluez python-bluez expect libbluetooth-dev python-dev python3-qrcode

# enable modules/drivers
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules

# create a fake gadget
sudo touch /usr/bin/rpikeyboard
sudo chmod +x /usr/bin/rpikeyboard

sudo sed -i '/^ExecStart=\/usr\/lib\/bluetooth\/bluetoothd/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd -C' /lib/systemd/system/bluetooth.service

sudo sed -i '/^exit\s0/i \/usr\/bin\/rpikeyboard' /etc/rc.local
wget -qO- https://raw.githubusercontent.com/electrocuted-slug/rpizw-bthid-pi-lite/master/rpikeyboard
cat rpikeyboard | sudo tee /usr/bin/rpikeyboard

sudo hciconfig hci0 name 'rpi-bthid'

while true; do
   echo "Please get your phone's mac address from your phone via settings > about phone > status > bluetooth address"
   read -p "Please enter you phone's mac address: " address
   address=$(echo ${address^^})
   read -p "$address is correct (y/n)? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) continue;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "PLEASE GET YOUR PHONE READ BY SELECTING 'PAIR NEW DEVICE' IN YOUR BLUETOOTH SETTINGS"

# setup bluetooth pairing
expect <(wget -qO- https://raw.githubusercontent.com/electrocuted-slug/rpizw-bthid-pi-lite/master/bluetooth.sh) $address

sudo mkdir /opt/rpi-bthid-pi-lite
sudo chown -R $USER:$USER /opt/rpi-bthid-pi-lite
wget -qO- https://raw.githubusercontent.com/electrocuted-slug/rpizw-bthid-pi-lite/master/rfcomm-server.py /opt/rpi-bthid-pi-lite/rfcomm-server.py
wget -qO- https://raw.githubusercontent.com/electrocuted-slug/rpizw-bthid-pi-lite/master/bluetooth_adv.sh /opt/rpi-bthid-pi-lite/bluetooth_adv.sh
sudo chmod +x /opt/rpi-bthid-pi-lite/bluetooth_adv.sh
wget -qO- https://raw.githubusercontent.com/electrocuted-slug/rpizw-bthid-pi-lite/master/my-bluetooth.service
sudo mv my-bluetooth.service /etc/systemd/system/my-bluetooth.service
sudo systemctl enable my-bluetooth
sudo systemctl start my-bluetooth
